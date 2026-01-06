import streamlit as st
from supabase import create_client, Client
import os

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión de Cumplimiento",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado con tu paleta de colores
st.markdown("""
<style>
    /* Colores principales */
    :root {
        --primary-blue: #0C0C5C;
        --accent-red: #C40012;
        --light-gray: #F5F5F5;
        --white: #FFFFFF;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #0C0C5C 0%, #1a1a7a 100%);
    }
    
    /* Contenedor principal */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 1400px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 30px 0;
        border-bottom: 3px solid #0C0C5C;
        margin-bottom: 40px;
    }
    
    .header h1 {
        color: #0C0C5C;
        font-size: 2.8em;
        font-weight: 700;
        margin: 0;
    }
    
    .header p {
        color: #666;
        font-size: 1.2em;
        margin-top: 10px;
    }
    
    /* Sección de login */
    .login-box {
        background: linear-gradient(135deg, #0C0C5C 0%, #1a1a7a 100%);
        border-radius: 15px;
        padding: 40px;
        color: white;
        box-shadow: 0 5px 20px rgba(12,12,92,0.3);
    }
    
    .login-box h2 {
        color: white;
        margin-bottom: 25px;
        font-size: 1.8em;
    }
    
    /* Botones */
    .stButton > button {
        background-color: #C40012;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-size: 1.1em;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #a00010;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(196,0,18,0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        font-size: 1em;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0C0C5C;
        box-shadow: 0 0 0 2px rgba(12,12,92,0.1);
    }
    
    /* Cards de información */
    .info-card {
        background: #F5F5F5;
        border-left: 5px solid #0C0C5C;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .info-card h3 {
        color: #0C0C5C;
        font-size: 1.5em;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .info-card p {
        color: #444;
        line-height: 1.8;
        font-size: 1.05em;
    }
    
    .info-card ul {
        margin-left: 20px;
        color: #444;
        line-height: 2;
    }
    
    /* Iconos */
    .icon {
        display: inline-block;
        margin-right: 10px;
        font-size: 1.3em;
    }
    
    /* Alert boxes */
    .alert-info {
        background-color: #e3f2fd;
        border-left: 5px solid #0C0C5C;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    .alert-warning {
        background-color: #fff3e0;
        border-left: 5px solid #C40012;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 30px;
        color: #666;
        border-top: 2px solid #e0e0e0;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar Supabase
@st.cache_resource
def init_supabase():
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")
    
    if not url or not key:
        st.error("⚠️ Configura SUPABASE_URL y SUPABASE_KEY en los secrets de Streamlit")
        return None
    
    return create_client(url, key)

# Función de login
def login(email: str, password: str, supabase: Client):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        return None

# Estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🛢️ Sistema de Gestión de Cumplimiento Normativo</h1>
    <p>Control y seguimiento de obligaciones en transporte, almacenamiento y distribución de combustibles</p>
</div>
""", unsafe_allow_html=True)

# Layout de dos columnas
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("## 📋 Marco Normativo")
    
    st.markdown("""
    <div class="alert-info">
        <strong>🎯 Objetivo:</strong> Este sistema facilita el cumplimiento de las normativas mexicanas aplicables 
        al sector de hidrocarburos, combustibles y petrolíferos.
    </div>
    """, unsafe_allow_html=True)
    
    # Card 1: Transporte
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">🚛</span> Transporte de Combustibles</h3>
        <p>El transporte de hidrocarburos y petrolíferos está regulado por:</p>
        <ul>
            <li><strong>NOM-006-ASEA-2017:</strong> Diseño, construcción, operación y mantenimiento de Ductos de Transporte</li>
            <li><strong>Ley de Hidrocarburos:</strong> Regulación del transporte por ducto, autotanque y otros medios</li>
            <li><strong>SCT:</strong> Normas de transporte terrestre de materiales peligrosos (NOM-002-SCT)</li>
            <li><strong>Permisos CRE:</strong> Autorización para transporte de petrolíferos</li>
            <li><strong>Seguros obligatorios:</strong> Cobertura de responsabilidad civil y daños ambientales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 2: Almacenamiento
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">🏭</span> Almacenamiento y Distribución</h3>
        <p>Las instalaciones de almacenamiento deben cumplir con:</p>
        <ul>
            <li><strong>NOM-005-ASEA-2016:</strong> Diseño, construcción, operación y mantenimiento de Terminales de Almacenamiento</li>
            <li><strong>NOM-016-CRE-2016:</strong> Calidad de petrolíferos en estaciones de servicio</li>
            <li><strong>Permisos ASEA:</strong> Autorización ambiental para almacenamiento</li>
            <li><strong>Análisis de Riesgo:</strong> Estudios técnicos de seguridad industrial</li>
            <li><strong>Programa de Prevención:</strong> Plan de respuesta a emergencias</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 3: Comercialización
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">⛽</span> Venta y Comercialización</h3>
        <p>La comercialización de combustibles requiere:</p>
        <ul>
            <li><strong>Permiso CRE:</strong> Autorización de la Comisión Reguladora de Energía</li>
            <li><strong>Registro de Contratos:</strong> Ante la Dirección de Comercialización</li>
            <li><strong>Control Volumétrico:</strong> Sistema de medición y reporte (Anexo 30-A)</li>
            <li><strong>Precios máximos:</strong> Cumplimiento de disposiciones tarifarias</li>
            <li><strong>Normas de calidad:</strong> Especificaciones técnicas de producto (NOM-016-CRE)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert-warning">
        <strong>⚠️ Importante:</strong> El incumplimiento de estas normativas puede resultar en sanciones 
        administrativas, clausura de instalaciones y responsabilidades penales.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("## 🔐 Acceso al Sistema")
    
    if not st.session_state.logged_in:
        supabase = init_supabase()
        
        if supabase:
            with st.form("login_form"):
                email = st.text_input("📧 Correo electrónico", placeholder="usuario@empresa.com")
                password = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Iniciar Sesión")
                
                if submit:
                    if email and password:
                        with st.spinner("Verificando credenciales..."):
                            result = login(email, password, supabase)
                            if result:
                                st.session_state.logged_in = True
                                st.success("✅ ¡Bienvenido al sistema!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas. Intenta nuevamente.")
                    else:
                        st.warning("⚠️ Por favor completa todos los campos")
            
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: white; font-size: 0.9em;'>
                <p>¿Olvidaste tu contraseña?</p>
                <p>Contacta al administrador del sistema</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Sesión activa")
        st.markdown("""
        <div style='color: white; padding: 20px;'>
            <h3>🎉 ¡Bienvenido!</h3>
            <p>Ya puedes acceder a todas las funcionalidades del sistema:</p>
            <ul>
                <li>📊 Dashboard de cumplimientos</li>
                <li>📝 Gestión de permisos</li>
                <li>🚗 Control de vehículos</li>
                <li>📁 Documentación</li>
                <li>📈 Reportes y análisis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 10px; margin-top: 20px;'>
        <h4 style='color: #0C0C5C;'>📞 Soporte Técnico</h4>
        <p style='color: #666;'>
            ¿Necesitas ayuda?<br>
            📧 soporte@empresa.com<br>
            📱 +52 (442) 123-4567<br>
            🕐 Lun - Vie: 9:00 - 18:00 hrs
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    <p><strong>Sistema de Gestión de Cumplimiento Normativo</strong></p>
    <p>© 2025 - Todos los derechos reservados</p>
    <p style='font-size: 0.9em; color: #999;'>
        Desarrollado para el cumplimiento de normativas mexicanas en el sector de hidrocarburos
    </p>
</div>
""", unsafe_allow_html=True)