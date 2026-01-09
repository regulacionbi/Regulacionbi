"""
Cliente de Supabase compartido para todas las páginas
"""
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Retorna una instancia única de Supabase que se reutiliza
    en todas las páginas de la aplicación.
    
    Returns:
        Client: Instancia del cliente de Supabase
    """
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    
    if not url or not key:
        st.error("⚠️ Configura SUPABASE_URL y SUPABASE_KEY en .streamlit/secrets.toml")
        return None
    
    return create_client(url, key)

def get_current_user(supabase: Client):
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            return session.user
    except Exception:
        return None