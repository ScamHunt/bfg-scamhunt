import os
from supabase import create_client

supa_url = "https://iyaldvefunvxxmlrerte.supabase.co"
supa_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supa_url, supa_key)
