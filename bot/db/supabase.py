import os
import logging
from supabase import create_client, Client

url = "https://iyaldvefunvxxmlrerte.supabase.co"
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


def upload_to_supabase(img_bytes: bytearray, img_type: str, file_name):
    logging.info("Uploading image to Supabase")
    return supabase.storage.from_("screenshots").upload(
        file=bytes(img_bytes),
        path=f"/{file_name}",
        file_options={"content-type": img_type, "upsert": "true"},
    )
