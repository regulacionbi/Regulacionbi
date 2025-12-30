import streamlit as st
from supabase import create_client

# Configurar la página
st.set_page_config(page_title="Mi App", page_icon="🚀")

# Conectar a Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Título de la app
st.title("🎉 Mi Primera App con Supabase")

st.write("¡Hola! Esta es mi primera aplicación.")

# Probar la conexión
if st.button("🔌 Probar conexión a Supabase"):
    try:
        # Intentar hacer una query simple
        response = supabase.table('_realtime_schema_migrations').select("*").limit(1).execute()
        st.success("✅ ¡Conexión exitosa con Supabase!")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

# Agregar algo interactivo
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.write(f"¡Hola {nombre}! 👋")
