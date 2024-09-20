
import os
from dotenv import load_dotenv

from supabase import create_client, Client
from  typing import Tuple
load_dotenv()
from .img_utils import generate_image_hashes
from snowflake import SnowflakeGenerator

gen = SnowflakeGenerator(64)

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))



def  upload_to_supabase(image_bytes:bytearray,image_size:Tuple[int,int], img_type:str) ->str:
    print("uploading to supabase")
    snowid = next(gen)
    # phash, avg_hash, color_hash, d_hash, w_hash, crop_hash = generate_image_hashes(image_bytes, image_size)
    supabase.storage.from_("test").upload(file=bytes(image_bytes),path=f'/screenshots/{snowid}', file_options={"content-type": img_type})
    return snowid



def get_image_temp_url(image_name:str):
    print("getting image temp url")
    url = supabase.storage.from_("test").create_signed_url(path=f'/screenshots/{image_name}', expires_in=3600)
    return url["signedURL"]