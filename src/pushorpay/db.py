import os
from supabase import create_client
from dotenv import load_dotenv

"""Handle database connection"""

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test database connection
try:
    result = supabase_client.table("users").select("*").limit(1).execute()
    print("Supabase connection success!")
    print(f"Response: {result}")
except Exception as e:
    print(f"Connection failed: {e}")
