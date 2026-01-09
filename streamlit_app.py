import streamlit as st
import os
from supabase import create_client, Client
from PIL import Image
from utils.supabase_client import get_supabase_client, get_current_user

# ===============================
# INICIALIZAR SESSION STATE
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "current_page" not in st.session_state:
    st.session_state.current_page = None

supabase = get_supabase_client()

if supabase and not st.session_state.logged_in:
    user = get_current_user(supabase)

    if user:
        st.session_state.logged_in = True
        st.session_state.role = user.user_metadata.get("rol")
        st.session_state.display_id = user.user_metadata.get("display_id")
        st.session_state.nombre = user.user_metadata.get("nombre")
        st.session_state.filial = user.user_metadata.get("filial")
        st.session_state.costos = user.user_metadata.get("costos")




# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Control normativo",
    page_icon="🛡️️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# CSS GLOBAL
# ===============================
st.markdown("""
<style>
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

/* Ocultar cosas de Streamlit */
#MainMenu, footer, header {visibility: hidden;}

/* Fondo general */
.stApp {
    background-color: #ffffff;
}

/* Tarjetas de información */
.info-card {
    background: white;
    border: 1px solid #e8e8e8;
    border-left: 5px solid var(--primary);
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    transition: all 0.3s ease;
}

.info-card:hover {
    box-shadow: 0 8px 22px rgba(27,5,179,0.12);
    transform: translateY(-3px);
}

.info-card h3 {
    color: var(--primary);
    margin-bottom: 12px;
}

.info-card ul {
    margin-left: 20px;
    color: #444;
    line-height: 1.8;
}

/* Colores base */
:root {
    --primary: #0F0575;
    --accent: #C2140F;
}

/* ===== HEADER ===== */
.top-bar {
    height: 6px;
    background: var(--primary);
}

/* ===== LOGIN ===== */
.login-scope > div {
    background: white;
    border: 2px solid var(--primary);
    border-radius: 14px;
    padding: 30px;
    max-width: 420px;
    margin: auto;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.login-title {
    color: var(--primary);
    margin-bottom: 20px;
    border-bottom: 3px solid var(--accent);
    padding-bottom: 8px;
    display: inline-block;
}

/* Inputs */
.login-scope input {
    border-radius: 8px !important;
}

/* Botón */
.login-scope button {
    background-color: var(--primary);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
}

.login-scope button:hover {
    background-color: var(--accent);
}

/* Imagen decorativa */
.image-container {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 25px 0;
}

/* ===== SUPPORT BOX ===== */
.support-box {
    background: #f9f9ff;
    border: 2px solid var(--primary);
    border-radius: 12px;
    padding: 22px;
    margin-top: 25px;
}

.support-box h4 {
    color: var(--primary);
    margin-bottom: 12px;
    font-size: 1.25em;
}

.support-box p {
    color: #555;
    line-height: 1.8;
    margin: 4px 0;
}

.support-box .accent {
    color: var(--accent);
    font-weight: 600;
}

/* ===== FOOTER ===== */
.custom-footer {
    margin-top: 80px;
    padding: 40px 20px;
    text-align: center;
    border-top: 1px solid #e0e0e0;
    background: #fafafa;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SUPABASE
# ===============================
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        st.error("⚠️ Configura SUPABASE_URL y SUPABASE_KEY")
        return None
    return create_client(url, key)

def login_user(email, password, supabase: Client):
    """Autentica usuario y obtiene sus datos desde la tabla Usuarios"""
    try:
        # 1. Autenticar en auth.users
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if auth_response and auth_response.user:
            user_email = auth_response.user.email

            # 2. Obtener datos del usuario desde tabla Usuarios
            usuario_data = supabase.table("Usuarios").select(
                "rol, display_id, id_filial, id_costos, nombre"
            ).eq("email", user_email).single().execute()

            if usuario_data.data:
                return {
                    "auth": auth_response,
                    "rol": usuario_data.data.get("rol"),
                    "display_id": usuario_data.data.get("display_id"),
                    "nombre": usuario_data.data.get("nombre"),
                    "filial": usuario_data.data.get("id_filial"),
                    "costos": usuario_data.data.get("id_costos")
                }

        return None

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

# ===============================
# SESSION STATE
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "go_dashboard" not in st.session_state:
    st.session_state.go_dashboard = False


# ===============================
# LANDING PAGE + LOGIN
# ===============================

# Barra superior
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# Imagen decorativa
st.markdown("""
<div class="image-container">
    <div style='background: linear-gradient(135deg, rgba(6,5,71,0.9) 0%, rgba(26,26,122,0.9) 100%),
                url("https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800") center/cover;
                height: 200px; display: flex; border-radius: 12px; align-items: center;'>
        <div style='text-align: left; color: white; padding: 30px;'>
            <h1 style='font-size: 2.6em; margin: 0; color: white;'>
                Regulación 
            </h1>
            <p style="font-size: 2em; color:#BE040F;">
            Cumplimiento Normativo
            </p>
            <p style='font-size: 0.8em; margin-top: 2px; color: #FFF26B; font-weight: 400;'>
                Seguridad · Legalidad · Excelencia Operativa
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Layout principal
col_left, col_right = st.columns([1.7, 0.35])

# =========================
# COLUMNA IZQUIERDA (INFO)
# =========================
with col_left:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=160)
    except:
        pass

    st.markdown("""
    <h2 style='opacity: 0.8; font-size: 1.2em; margin-top: 15px; color: #3B6C97;'>
        Plataforma integral para el control y seguimiento de obligaciones regulatorias
        en el sector hidrocarburos y petrolíferos
    </h2>
    """, unsafe_allow_html=True)

    # -------- TARJETA 1 --------
    st.markdown("""
    <div class="info-card">
        <h3>🚛 Transporte</h3>
        <ul>
            <li><strong>NOM-006-ASEA</strong> – Ductos y transporte</li>
            <li><strong>NOM-002-SCT</strong> – Materiales peligrosos</li>
            <li>Permisos CRE</li>
            <li>Capacitación obligatoria</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # -------- TARJETA 2 --------
    st.markdown("""
    <div class="info-card">
        <h3>🏭 Almacenamiento</h3>
        <ul>
            <li><strong>NOM-005-ASEA</strong></li>
            <li>Impacto ambiental</li>
            <li>Análisis de riesgo</li>
            <li>Mantenimiento periódico</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # -------- TARJETA 3 --------
    st.markdown("""
    <div class="info-card">
        <h3>⛽ Comercialización</h3>
        <ul>
            <li>Permiso CRE</li>
            <li>Control volumétrico</li>
            <li>CFDI hidrocarburos</li>
            <li>NOM-016-CRE</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# COLUMNA DERECHA (LOGIN)
# =========================
with col_right:
    st.markdown('<div class="login-scope">', unsafe_allow_html=True)

    with st.container():
        st.markdown(
            "<h2 class='login-title' style='opacity: 0.3; color:#052547; font-size: 1.9em;'>" \
            "🔐 Inicio de sesión"
            "</h2>",
            unsafe_allow_html=True
        )

        supabase = init_supabase()

        if supabase:
            with st.form("login_form"):
                email = st.text_input(
                    "Correo",
                    placeholder="usuario@empresa.com",
                    label_visibility="collapsed"
                )
                password = st.text_input(
                    "Contraseña",
                    type="password",
                    placeholder="••••••••",
                    label_visibility="collapsed"
                )
                submit = st.form_submit_button("Iniciar Sesión")

                if submit:
                    if email and password:
                        with st.spinner("Verificando credenciales..."):
                            result = login_user(email, password, supabase)

                            if result:
                                # Guardar datos en session_state
                                st.session_state.logged_in = True
                                st.session_state.role = result["rol"]
                                st.session_state.display_id = result["display_id"]
                                st.session_state.nombre = result["nombre"]
                                st.session_state.filial = result["filial"]
                                st.session_state.costos = result["costos"]

                                # Bandera para redirección
                                st.session_state.go_dashboard = True

                                st.success("✅ ¡Acceso concedido!")
                                st.balloons()
    # Forzar rerun limpio
                                # Forzar rerun limpio
                                st.rerun()
                            else:
                                st.error("❌ Credenciales incorrectas o usuario no registrado")
                    else:
                        st.warning("⚠️ Completa todos los campos")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===== SOPORTE =====
    st.markdown("""
    <div class="support-box">
        <h4>📞 Soporte y Asistencia</h4>
        <p><strong>¿Necesitas ayuda?</strong></p>
        <p>📧 <span class="accent">bmejia@gasen.mx</span></p>
        <p>📱 <span class="accent">+52 (442) 561-1606</span></p>
        <p>🕐 Horario: Lun - Vie<br>9:00 AM - 6:00 PM</p>
        <p style="margin-top: 12px; font-size: 0.95em;">
            Atención personalizada para resolver dudas sobre normatividad
            y uso del sistema.
        </p>
    </div>
    """, unsafe_allow_html=True)

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

# ===============================
# FLUJO PRINCIPAL
# ===============================

if st.session_state.logged_in:
    target = st.session_state.current_page or "pages/Dashboard.py"
    st.switch_page(target)
    st.stop()

