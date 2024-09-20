import os
import logging
from supabase import create_client, Client

url = "https://iyaldvefunvxxmlrerte.supabase.co"
key = os.getenv("SUPABASE_KEY")
supabase = create_client(supa_url, supa_key)


def upload_to_supabase(img_bytes: bytearray, img_type: str):
    logging.info("Uploading image to Supabase")
    supabase.storage.from_("test").upload(
        file=bytes(img_bytes),
        path="/screenshots/test",
        file_options={"content-type": img_type},
    )
