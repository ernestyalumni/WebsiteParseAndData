import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path

# Get the app directory
app_dir = Path(__file__).parent.parent

# Load environment variables from .env file
env_path = app_dir.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

@st.cache_resource
def get_supabase_client():
    """
    Get a cached Supabase client instance.
    
    Returns:
        Supabase client or None if credentials are not available
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.warning("Supabase credentials not found. Some features may be limited.")
        return None
    
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        return None