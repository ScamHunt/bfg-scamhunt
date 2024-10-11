from .supabase import supabase
from .report import get_report
from postgrest import APIError
import logging
from io import BytesIO
from PIL import Image
import imagehash
from typing import Optional
from datetime import datetime


class ImageHash:
    def __init__(
        self,
        hash: str,
        report_id: int,
        user_id: int,
        created_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.hash = hash
        self.report_id = report_id
        self.user_id = user_id
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "hash": self.hash,
            "report_id": self.report_id,
            "user_id": self.user_id,
            "created_id": self.created_at,
        }


def insert_image_hash(image_hash: ImageHash) -> ImageHash:
    new = image_hash.to_dict()
    del new["id"]
    try:
        data = supabase.table("image_hash").insert(new).execute()
        return ImageHash.from_dict(data.data)
    except APIError as e:
        logging.error(f"Error creating user: {e}")


async def create_image_hash(file, report_id, user_id):
    image_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(image_bytes))
    hash = str(imagehash.crop_resistant_hash(image))
    insert_image_hash(ImageHash(hash=hash, report_id=report_id, user_id=user_id))


def get_similar_images(
    hash: str,
) -> None | str:
    try:
        data = supabase.rpc(
            "get_image_hashes_by_hamming_distance",
            {"target_hash": hash, "distance_threshold": 10},
        ).execute()
        similar_images = [h["image_report_id"] for h in data.data]
        logging.info(f"Found {len(similar_images)} similar images.")
        return similar_images
    except APIError as e:
        logging.error(f"Error getting user: {e}")


async def get_image_report(file):
    image_bytes = await file.download_as_bytearray()
    image = Image.open(BytesIO(image_bytes))
    hash = str(imagehash.crop_resistant_hash(image))
    images = get_similar_images(hash)
    return get_report(images[0]) if images else None
