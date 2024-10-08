from .supabase import supabase
from postgrest import APIError
import logging
from io import BytesIO
from PIL import Image
import imagehash
from typing import Optional



class ImageHash:
    def __init__(
        self,
        hash: str,
        report_id: int,
        user_id: int,
        id: Optional[int] = None,
    ):
        self.id = id
        self.hash = hash
        self.report_id = report_id
        self.user_id = user_id
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            hash=data["hash"],
            report_id=data["report_id"],
            user_id=data["user_id"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "hash": self.hash,
            "report_id": self.report_id,
            "user_id": self.user_id
        }
        
def insert_image_hash(image_hash: ImageHash) -> ImageHash:
    new = image_hash.to_dict()
    del new["id"]
    try:
        data = supabase.table("image_hash").insert(new).execute()
        return data.data[0]
    except APIError as e:
        logging.error(f"Error creating user: {e}")
        
async def create_image_hash(file, report_id, user_id):
    image_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(image_bytes))
    hash = str(imagehash.crop_resistant_hash(image))
    insert_image_hash(ImageHash(hash=hash, report_id=report_id, user_id=user_id))
    
def hash_exists(hash: str, user_id=None) -> bool:
    try:
        if user_id:
            data = supabase.table("image_hash").select("*").eq("user_id", user_id).eq("hash", hash).limit(1).execute()
        else:
            data = supabase.table("image_hash").select("*").eq("hash", hash).limit(1).execute()
        return True if data.data else False
    except APIError as e:
        logging.error(f"Error getting user: {e}")

async def image_exists(file, user_id=None):
    image_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(image_bytes))
    hash = str(imagehash.crop_resistant_hash(image))
    return hash_exists(hash)