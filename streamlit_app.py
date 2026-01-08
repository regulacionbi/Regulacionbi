import streamlit as st
from supabase import create_client, Client
import os
from PIL import Image

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Sistema de Cumplimiento",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# CSS GLOBAL
# ===============================
st.markdown("""
<style>
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
    --primary: #1B05B3;
    --accent: #C2140F;
}

/* ===== HEADER ===== */
.top-bar {
    height: 6px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

/* ===== LOGIN ===== */
.login-box {
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
.login-box input {
    border-radius: 8px !important;
}

/* Botones */
.login-box button {
    background-color: var(--primary);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
}

.login-box button:hover {
    background-color: var(--accent);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #f8f8ff;
    border-right: 2px solid var(--primary);
}

.sidebar-title {
    color: var(--primary);
    font-weight: 700;
}

/* ===== CONTENIDO ===== */
.page-title {
    color: var(--primary);
    font-weight: 700;
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

# Barra superior
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# ===============================
# SUPABASE
# ===============================
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        st.error("Configura SUPABASE_URL y SUPABASE_KEY")
        return None
    return create_client(url, key)

def login_user(email, password, supabase: Client):
    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except:
        return None

# ===============================
# SESSION STATE
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# ===============================
# LANDING + LOGIN
# ===============================
def landing_page():
    col_left, col_right = st.columns([1.7, 1])

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
        <h1 class="page-title">
            Sistema de Gestión de <span style="color:#C2140F;">Cumplimiento Normativo</span>
        </h1>
        <p>
            Plataforma integral para el control y seguimiento de obligaciones regulatorias
            en el sector hidrocarburos y petrolíferos.
        </p>
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
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">🔐 Acceso al Sistema</h2>', unsafe_allow_html=True)

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
                                st.session_state.logged_in = True
                                st.session_state.role = result.user.user_metadata.get(
                                    "role", "oficina"
                                )
                                st.rerun()
                            else:
                                st.error("Credenciales incorrectas")
                    else:
                        st.warning("Completa los campos")

        st.markdown('</div>', unsafe_allow_html=True)

                # ===== SOPORTE =====
        st.markdown("""
        <div class="support-box">
            <h4>📞 Soporte y Asistencia</h4>
            <p><strong>¿Necesitas ayuda?</strong></p>
            <p>📧 <span class="accent">soporte@cumplimiento.mx</span></p>
            <p>📱 <span class="accent">+52 (442) 123-4567</span></p>
            <p>🕐 Horario: Lun - Vie<br>9:00 AM - 6:00 PM</p>
            <p style="margin-top: 12px; font-size: 0.95em;">
                Atención personalizada para resolver dudas sobre normatividad
                y uso del sistema.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ===============================
# APP PRINCIPAL
# ===============================
def main_app():
    with st.sidebar:
        st.markdown("<h3 class='sidebar-title'>📂 Menú</h3>", unsafe_allow_html=True)

        role = st.session_state.role

        pages = []

        if role in ["admdr"]:
            pages = ["Dashboard", "Usuarios", "Catálogos", "Reportes"]
        elif role == "filiar":
            pages = ["Dashboard", "Centros de Costo", "Reportes"]
        elif role == "gerencial":
            pages = ["Dashboard", "Mi Centro de Costos"]
        elif role == "oficina":
            pages = ["Vehículos", "Cumplimientos", "Permisos"]

        page = st.radio("Navegación", pages)

        if st.button("🚪 Cerrar sesión"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

    # ===== CONTENIDO =====
    st.markdown(f"<h1 class='page-title'>{page}</h1>", unsafe_allow_html=True)

    st.write(f"Contenido de **{page}** para rol **{role}**")

# ===============================
# FLUJO PRINCIPAL
# ===============================
if not st.session_state.logged_in:
    landing_page()
else:
    main_app()
