import streamlit as st
from supabase import create_client, Client
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión de Cumplimiento",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado con fondo blanco y detalles en azul/rojo
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general blanco */
    .stApp {
        background: #FFFFFF;
    }
    
    /* Header con barra azul */
    .top-bar {
        background: linear-gradient(90deg, #0C0C5C 0%, #1a1a7a 100%);
        height: 8px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
    }
    
    .header-section {
        background: white;
        padding: 30px 60px;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 40px;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 30px;
        margin-bottom: 20px;
    }
    
    .title-section h1 {
        color: #0C0C5C;
        font-size: 2.2em;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .title-section p {
        color: #666;
        font-size: 1.1em;
        margin-top: 8px;
    }
    
    .red-accent {
        color: #C40012;
        font-weight: 600;
    }
    
    /* Contenedor principal */
    .main-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px 60px;
    }
    
    /* Login box con azul */
    .login-container {
        background: white;
        border: 2px solid #0C0C5C;
        border-radius: 12px;
        padding: 35px;
        box-shadow: 0 4px 15px rgba(12,12,92,0.1);
    }
    
    .login-container h2 {
        color: #0C0C5C;
        margin-bottom: 25px;
        font-size: 1.6em;
        border-bottom: 3px solid #C40012;
        padding-bottom: 10px;
        display: inline-block;
    }
    
    /* Botones */
    .stButton > button {
        background-color: #0C0C5C;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-size: 1.05em;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #C40012;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(12,12,92,0.3);
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
        box-shadow: 0 0 0 3px rgba(12,12,92,0.1);
    }
    
    /* Cards de información con borde azul sutil */
    .info-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-left: 4px solid #0C0C5C;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 5px 20px rgba(12,12,92,0.08);
        transform: translateY(-3px);
    }
    
    .info-card h3 {
        color: #0C0C5C;
        font-size: 1.4em;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .info-card .icon {
        margin-right: 12px;
        font-size: 1.4em;
    }
    
    .info-card p {
        color: #444;
        line-height: 1.8;
        font-size: 1.02em;
        margin-bottom: 15px;
    }
    
    .info-card ul {
        margin-left: 20px;
        color: #555;
        line-height: 1.9;
    }
    
    .info-card ul li strong {
        color: #0C0C5C;
    }
    
    /* Alert boxes */
    .alert-info {
        background-color: #f8f9ff;
        border-left: 4px solid #0C0C5C;
        padding: 20px;
        border-radius: 8px;
        margin: 25px 0;
        color: #333;
    }
    
    .alert-warning {
        background-color: #fff8f8;
        border-left: 4px solid #C40012;
        padding: 20px;
        border-radius: 8px;
        margin: 25px 0;
        color: #333;
    }
    
    .alert-info strong, .alert-warning strong {
        color: #0C0C5C;
        font-size: 1.05em;
    }
    
    /* Imagen decorativa */
    .image-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 25px 0;
    }
    
    /* Support box */
    .support-box {
        background: #f8f9ff;
        border: 2px solid #0C0C5C;
        border-radius: 10px;
        padding: 25px;
        margin-top: 25px;
    }
    
    .support-box h4 {
        color: #0C0C5C;
        margin-bottom: 15px;
        font-size: 1.3em;
    }
    
    .support-box p {
        color: #555;
        line-height: 1.8;
        margin: 5px 0;
    }
    
    .support-box .red-text {
        color: #C40012;
        font-weight: 600;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 40px 20px;
        color: #666;
        border-top: 1px solid #e0e0e0;
        margin-top: 60px;
        background: #fafafa;
    }
    
    .custom-footer p {
        margin: 5px 0;
    }
    
    /* Badge de normas */
    .norm-badge {
        display: inline-block;
        background: #0C0C5C;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 3px;
    }
    
    /* Separador decorativo */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, #0C0C5C 0%, #C40012 100%);
        margin: 30px 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Barra superior azul
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

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

# Header con logo
st.markdown('<div class="header-section">', unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 4])

with col_logo:
    # Aquí puedes cargar tu logo
    # Descomenta y ajusta la ruta cuando tengas tu logo:
    # try:
    #     logo = Image.open("logo.png")
    #     st.image(logo, width=150)
    # except:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0C0C5C 0%, #1a1a7a 100%); 
                width: 120px; height: 120px; border-radius: 12px; 
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 4px 15px rgba(12,12,92,0.2);'>
        <span style='font-size: 3.5em;'>🛢️</span>
    </div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="title-section">
        <h1>Sistema de Gestión de <span class="red-accent">Cumplimiento Normativo</span></h1>
        <p>Control y seguimiento integral de obligaciones regulatorias en el sector de hidrocarburos</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Contenido principal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Layout principal
col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("## 📋 Marco Normativo y Regulatorio")
    
    st.markdown("""
    <div class="alert-info">
        <strong>🎯 Objetivo del Sistema:</strong> Facilitar el cumplimiento integral de las normativas 
        mexicanas aplicables al transporte, almacenamiento, distribución y comercialización de 
        hidrocarburos, combustibles y petrolíferos, garantizando la operación segura y legal.
    </div>
    """, unsafe_allow_html=True)
    
    # Imagen representativa de normatividad
    # Descomenta cuando tengas tu imagen:
    # try:
    #     norm_image = Image.open("normatividad.jpg")
    #     st.image(norm_image, use_column_width=True, caption="Cumplimiento Normativo en Hidrocarburos")
    # except:
    st.markdown("""
    <div class="image-container">
        <div style='background: linear-gradient(135deg, rgba(12,12,92,0.9) 0%, rgba(26,26,122,0.9) 100%), 
                    url("https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800") center/cover;
                    height: 280px; display: flex; align-items: center; justify-content: center;'>
            <div style='text-align: center; color: white; padding: 30px;'>
                <h2 style='font-size: 2em; margin: 0;'>⚖️ Cumplimiento Normativo</h2>
                <p style='font-size: 1.2em; margin-top: 10px;'>Seguridad · Legalidad · Excelencia Operativa</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Card 1: Transporte
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">🚛</span> Transporte de Combustibles y Petrolíferos</h3>
        <p>El transporte de hidrocarburos requiere cumplimiento estricto de múltiples normativas:</p>
        <ul>
            <li><strong>NOM-006-ASEA-2017:</strong> Diseño, construcción, operación y mantenimiento de Ductos de Transporte</li>
            <li><strong>Ley de Hidrocarburos:</strong> Marco legal para transporte por ducto, autotanque y ferrocarril</li>
            <li><strong>NOM-002-SCT:</strong> Normativa SCT para transporte terrestre de materiales peligrosos</li>
            <li><strong>Permisos CRE:</strong> Autorización de la Comisión Reguladora de Energía</li>
            <li><strong>Seguros obligatorios:</strong> Cobertura de responsabilidad civil y daños ambientales</li>
            <li><strong>Capacitación:</strong> Personal certificado en manejo de materiales peligrosos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 2: Almacenamiento
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">🏭</span> Almacenamiento y Terminales</h3>
        <p>Las instalaciones de almacenamiento deben cumplir requisitos técnicos y ambientales:</p>
        <ul>
            <li><strong>NOM-005-ASEA-2016:</strong> Requisitos para Terminales de Almacenamiento y Reparto</li>
            <li><strong>NOM-016-CRE-2016:</strong> Especificaciones de calidad en instalaciones</li>
            <li><strong>Permisos ASEA:</strong> Autorización de Impacto Ambiental y Riesgo</li>
            <li><strong>Análisis de Riesgo:</strong> Estudios técnicos de seguridad industrial y operativa</li>
            <li><strong>Programa de Prevención:</strong> Plan documentado de respuesta a emergencias</li>
            <li><strong>Mantenimiento:</strong> Inspecciones periódicas y pruebas de integridad</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 3: Comercialización
    st.markdown("""
    <div class="info-card">
        <h3><span class="icon">⛽</span> Venta y Comercialización</h3>
        <p>La comercialización de combustibles implica cumplimiento fiscal y operativo:</p>
        <ul>
            <li><strong>Permiso CRE:</strong> Autorización para comercialización de petrolíferos</li>
            <li><strong>Registro de Contratos:</strong> Ante la Dirección General de Comercialización</li>
            <li><strong>Control Volumétrico:</strong> Sistema de medición dinámica (Anexo 30 del CFF)</li>
            <li><strong>Precios máximos:</strong> Cumplimiento de disposiciones de la CRE</li>
            <li><strong>NOM-016-CRE:</strong> Especificaciones de calidad de gasolinas y diésel</li>
            <li><strong>Facturación electrónica:</strong> CFDI con complemento de hidrocarburos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert-warning">
        <strong>⚠️ Importante:</strong> El incumplimiento de estas normativas puede derivar en sanciones 
        económicas significativas, clausura temporal o definitiva de instalaciones, suspensión de permisos 
        y, en casos graves, responsabilidades de carácter penal conforme al Código Penal Federal.
    </div>
    """, unsafe_allow_html=True)
    
    # Badges de normas principales
    st.markdown("""
    <div style='margin: 30px 0;'>
        <h4 style='color: #0C0C5C; margin-bottom: 15px;'>📜 Principales Normas Aplicables:</h4>
        <span class="norm-badge">NOM-005-ASEA</span>
        <span class="norm-badge">NOM-006-ASEA</span>
        <span class="norm-badge">NOM-016-CRE</span>
        <span class="norm-badge">NOM-002-SCT</span>
        <span class="norm-badge">Ley de Hidrocarburos</span>
        <span class="norm-badge">Anexo 30 CFF</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h2>🔐 Acceso al Sistema</h2>", unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        supabase = init_supabase()
        
        if supabase:
            with st.form("login_form"):
                email = st.text_input("📧 Correo electrónico", placeholder="usuario@empresa.com")
                password = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Iniciar Sesión")
                with col2:
                    st.form_submit_button("Olvidé mi contraseña", disabled=True)
                
                if submit:
                    if email and password:
                        with st.spinner("Verificando credenciales..."):
                            result = login(email, password, supabase)
                            if result:
                                st.session_state.logged_in = True
                                st.success("✅ ¡Acceso concedido!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas")
                    else:
                        st.warning("⚠️ Completa todos los campos")
    else:
        st.success("✅ Sesión activa")
        st.markdown("""
        <div style='padding: 20px 0;'>
            <h3 style='color: #0C0C5C;'>🎉 ¡Bienvenido al Sistema!</h3>
            <p style='color: #555; line-height: 1.8;'>Accede a todas las funcionalidades:</p>
            <ul style='color: #555; line-height: 2;'>
                <li>📊 <strong>Dashboard</strong> de cumplimientos</li>
                <li>📝 <strong>Gestión</strong> de permisos y licencias</li>
                <li>🚗 <strong>Control</strong> de flota vehicular</li>
                <li>📁 <strong>Repositorio</strong> documental</li>
                <li>📈 <strong>Reportes</strong> ejecutivos</li>
                <li>🔔 <strong>Alertas</strong> de vencimientos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Support box
    st.markdown("""
    <div class="support-box">
        <h4>📞 Soporte y Asistencia</h4>
        <p><strong>¿Necesitas ayuda?</strong></p>
        <p>📧 <span class="red-text">soporte@cumplimiento.mx</span></p>
        <p>📱 <span class="red-text">+52 (442) 123-4567</span></p>
        <p>🕐 Horario: Lun - Vie<br>9:00 AM - 6:00 PM</p>
        <p style='margin-top: 15px; font-size: 0.95em;'>
            Atención personalizada para resolver dudas sobre normatividad y uso del sistema
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    <p style='color: #0C0C5C; font-weight: 700; font-size: 1.1em;'>
        Sistema de Gestión de Cumplimiento Normativo
    </p>
    <p style='color: #C40012; font-weight: 600;'>
        Sector Hidrocarburos y Petrolíferos
    </p>
    <p style='margin-top: 15px;'>© 2025 - Todos los derechos reservados</p>
    <p style='font-size: 0.9em; color: #999; margin-top: 10px;'>
        Cumplimiento integral de normativas mexicanas · ASEA · CRE · SCT · SEMARNAT
    </p>
</div>
""", unsafe_allow_html=True)