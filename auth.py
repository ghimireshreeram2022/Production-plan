# auth.py
from supabase import create_client
import streamlit as st

SUPABASE_URL = "https://phxybrgcyfcwaclhdmqy.supabase.co"  # Your actual project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBoeHlicmdjeWZjd2FjbGhkbXF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4OTExOTUsImV4cCI6MjA2OTQ2NzE5NX0.PXU8JCN68gcQrZFLJp2omuUUq3QzW3WTDFU1jpM3Qgo"  # Your anon public API key

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def login(email, password):
    supabase = init_connection()
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None
