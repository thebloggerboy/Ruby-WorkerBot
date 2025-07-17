# ruby-worker-bot/database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_and_delete_token(token: str, user_id: int):
    try:
        response = supabase.table('secure_links').select('file_key').eq('token', token).eq('user_id', user_id).single().execute()
        if response.data:
            file_key = response.data['file_key']
            supabase.table('secure_links').delete().eq('token', token).execute()
            return file_key
        return None
    except: return None
