# ruby-worker-bot/database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_and_delete_token(token: str, user_id: int):
    """टोकन को वेरीफाई करता है और सफल होने पर डिलीट कर देता है।"""
    try:
        # टोकन और यूजर ID के आधार पर डेटा ढूंढें
        response = supabase.table('secure_links').select('file_key').eq('token', token).eq('user_id', user_id).single().execute()
        
        if response.data:
            file_key = response.data['file_key']
            # टोकन को डिलीट करें ताकि वह दोबारा इस्तेमाल न हो सके
            supabase.table('secure_links').delete().eq('token', token).execute()
            return file_key
        else:
            return None # टोकन नहीं मिला या गलत यूजर के लिए है
            
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None