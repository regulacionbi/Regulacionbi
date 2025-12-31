import streamlit as st
from supabase import create_client

# Configurar la página
st.set_page_config(page_title="Mi App", page_icon="🚀")

# Conexion
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("🎉 Mi Primera App con Supabase")

st.write("¡Hola! Esta es mi primera aplicación.")

# Probar la conexión
if st.button("🔌 Probar conexión a Supabase"):
    try:
        # prueba con tabla
        response = supabase.table('Filial').select("*").limit(1).execute()
        st.success("✅ ¡Conexión exitosa con Supabase!")
        st.write(f"Datos encontrados: {len(response.data)} registros")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

# Agregar algo interactivo
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.write(f"¡Hola {nombre}! 👋")
