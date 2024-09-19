
import os
from dotenv import load_dotenv

from supabase import create_client, Client

load_dotenv()


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
def  upload_to_supabase(image_bytes:bytearray, img_type:str):
    print("uploading to supabase")
    supabase.storage.from_("test").upload(file=bytes(image_bytes),path="/screenshots/test", file_options={"content-type": img_type})



