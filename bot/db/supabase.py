import os
from supabase import create_client
from dotenv import load_dotenv


load_dotenv(override=True)

supa_url = "https://iyaldvefunvxxmlrerte.supabase.co"
supa_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supa_url, supa_key)
