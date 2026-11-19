
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing!")


def get_user_client(token: str) -> Client:
    """Create a separate Supabase client for each authenticated user."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(token)
    return client
