import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from utils.supabase_client import get_supabase_client

st.session_state.current_page = "pages/Dashboard.py"



#------------FUNCION DE FORMATEO DE NÚMEROS CON COMAS------------
def fmt(num):
    """Formatea número con comas, maneja casos especiales"""
    try:
        if num is None:
            return "0"
        if pd.isna(num):
            return "0"
        # Convertir a entero si es float sin decimales
        if isinstance(num, float) and num.is_integer():
            num = int(num)
        return f"{num:,}"
    except (ValueError, TypeError, AttributeError):
        # Si falla todo, devolver como string
        return str(num)


# ===============================
# PROTECCIÓN DE PÁGINA
# ===============================
if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Debes iniciar sesión primero")
    st.switch_page("streamlit_app.py")
    st.stop()

# Solo admdr puede ver esta página
if st.session_state.get("role") != "admdr":
    st.error("❌ No tienes permisos para ver esta página")
    st.stop()

# ===============================
# CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Dashboard - Control Normativo",
    page_icon="🏠",
    layout="wide"
)
# CSS personalizado
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* OCULTAR MENU AUTOMÁTICO DE STREAMLIT */
div[data-testid="stSidebarNav"] {
    display: none;
}

/* ===============================
TIPOGRAFÍA GLOBAL
=============================== */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ===============================
SIDEBAR
=============================== */
section[data-testid="stSidebar"] {
    background-color: #2E2F70 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===============================
KPI CARDS
=============================== */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: clamp(16px, 2vw, 24px);
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-left: 5px solid;
}

.kpi-card.green  { border-left-color: #28a745; }
.kpi-card.yellow { border-left-color: #ffc107; }
.kpi-card.red    { border-left-color: #dc3545; }
.kpi-card.blue   { border-left-color: #007bff; }

.kpi-number {
    font-size: clamp(1.8rem, 3vw, 3rem);
    font-weight: 700;
    color: #0A0A38;
    margin: 10px 0;
}

.kpi-label {
    font-size: clamp(0.9rem, 1.2vw, 1.1rem);
    color: #666;
    font-weight: 600;
}
            
.kpi-card small {
    color: #4D4D8A;
    font-weight: 500;
    font-size: clamp(0.75rem, 1vw, 0.9rem);
}            

/* ===============================
BIENVENIDA
=============================== */
.welcome-banner {
    background: linear-gradient(135deg, #457EB0 0%, #2c5a8a 100%);
    color: white;
    padding: clamp(18px, 2.5vw, 26px);
    border-radius: 12px;
    margin-bottom: 30px;
}

.welcome-banner h1 {
    font-size: clamp(1.35rem, 2vw, 1.75rem);
    font-weight: 600;
    margin: 0;
    line-height: 1.25;
}

/* Subtítulo */
.welcome-banner .subtitle {
    font-size: clamp(0.95rem, 1.1vw, 1.05rem);
    margin-top: 8px;
    font-weight: 500;
    opacity: 0.95;
}

/* Fecha */
.welcome-banner .date {
    font-size: clamp(0.8rem, 1vw, 0.9rem);
    margin-top: 4px;
    opacity: 0.75;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# SUPABASE
# ===============================
supabase = get_supabase_client()


# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("### 🏢 Filtros")

    # Selector de Empresa
    try:
        filiales = supabase.table("Filial").select("id_cia, nombre").execute()
        empresas = {f["nombre"]: f["id_cia"] for f in filiales.data}

        empresa_seleccionada = st.selectbox(
            "Seleccionar Empresa",
            options=["Todas"] + list(empresas.keys())
        )

        if empresa_seleccionada != "Todas":
            id_empresa = empresas[empresa_seleccionada]
        else:
            id_empresa = None

    except Exception as e:
        st.error(f"Error al cargar empresas: {e}")
        id_empresa = None

    st.markdown("---")

    # Menú de navegación
    st.markdown("### 📊 Menú")

    menu_options = {
        "Dashboard": "Dashboard.py",
        "Usuarios": "Usuarios.py",
        "Permisos": "Permisos.py",
        "Flota": "Flota.py",
        "Calendario": "Calendario.py"
    }

    for label, page in menu_options.items():
        if st.button(label, use_container_width=True):
            st.switch_page(f"pages/{page}")

    st.markdown("---")

    # Botón de Logout
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("streamlit_app.py")

# ===============================
# CONTENIDO PRINCIPAL
# ===============================

# Banner de bienvenida
nombre_usuario = st.session_state.get("nombre", "Usuario")

st.markdown(f"""
<div class="welcome-banner">
    <h1>👋 Bienvenido, {nombre_usuario}</h1>
    <div class="subtitle">Panel de Resumen</div>
    <div class="date">
        {datetime.now().strftime('%A %d de %B de %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# OBTENER DATOS (SIMPLIFICADO)
# ===============================

try:
    # Obtener información del usuario
    rol = st.session_state.get("role")
    id_filial_usuario = st.session_state.get("id_filial")
    id_costos_usuario = st.session_state.get("id_costos")
    
    # 1. OBTENER TOTAL DEL CATÁLOGO DE OBLIGACIONES
    cat_obl = supabase.table("Cat_Obl").select("id_obl").execute()
    total_cat_obl = len(cat_obl.data)
    
    # 2. OBTENER PERMISOS CON FILTROS SEGÚN ROL
    query_permisos = supabase.table("Permisos").select("id_permisos, subsidiaria, ctro_costos")
    
    # Aplicar filtros según el rol del usuario
    if rol == "admdr":
        # ADMDR ve TODOS los permisos
        permisos = query_permisos.execute()
        
    elif rol == "filial":
        # FILIAL ve solo los permisos de SU filial
        if id_filial_usuario and id_filial_usuario != "ALL":
            st.info(f"🏭 **Rol:** FILIAL - Filtrado por filial: {id_filial_usuario}")
            permisos = query_permisos.eq("subsidiaria", id_filial_usuario).execute()
        else:
            st.info("🏭 **Rol:** FILIAL - Sin filtro específico")
            permisos = query_permisos.execute()
            
    elif rol in ("oficina", "gerencial"):
        # OFICINA/GERENCIAL ve solo los permisos de SU centro de costos
        if id_costos_usuario and id_costos_usuario != "ALL":
            st.info(f"💼 **Rol:** {rol.upper()} - Filtrado por centro de costos: {id_costos_usuario}")
            permisos = query_permisos.eq("ctro_costos", id_costos_usuario).execute()
        else:
            st.info(f"💼 **Rol:** {rol.upper()} - Sin filtro específico")
            permisos = query_permisos.execute()
            
    else:
        st.warning(f"❓ Rol no reconocido: {rol}")
        permisos = query_permisos.execute()
    
    df_permisos = pd.DataFrame(permisos.data)
    
    #------------------------ 
    # KPI: TOTAL DE OBLIGACIONES
    #------------------------
    if df_permisos.empty:
        total_obligaciones = 0
        st.warning("⚠️ No se encontraron permisos para este usuario/filtro")
    else:
        # Fórmula: Total Obligaciones = (Total en Cat_Obl) × (Permisos filtrados)
        total_obligaciones = total_cat_obl * len(df_permisos)
        
    
    # 4. INFORMACIÓN ADICIONAL PARA MOSTRAR (opcional)
    cumplidas = por_vencer = vencidas = 0  # Por ahora, solo el total
    df = pd.DataFrame()  # DataFrame vacío por ahora
    
    # 5. OBTENER NOMBRES DE EMPRESAS PARA ADMDR (si hay permisos)
    if rol == "admdr" and not df_permisos.empty:
        try:
            # Agrupar permisos por subsidiaria
            obligaciones_por_empresa = df_permisos.groupby('subsidiaria').size().reset_index(name='num_permisos')
            
            # Obtener nombres de las filiales
            filiales_resp = supabase.table("Filial").select("id_cia, nombre").execute()
            filiales_dict = {f['id_cia']: f['nombre'] for f in filiales_resp.data}
            
            # Mapear IDs a nombres
            obligaciones_por_empresa['nombre_empresa'] = obligaciones_por_empresa['subsidiaria'].map(filiales_dict)
            obligaciones_por_empresa['total_obligaciones'] = obligaciones_por_empresa['num_permisos'] * total_cat_obl
            
            # Guardar en session_state para usar después
            st.session_state['obligaciones_por_empresa'] = obligaciones_por_empresa
            
        except Exception as e:
            st.warning(f"No se pudo obtener información por empresa: {e}")
    
except Exception as e:
    st.error(f"❌ Error al calcular total de obligaciones: {str(e)}")
    import traceback
    with st.expander("📜 Ver detalles del error"):
        st.code(traceback.format_exc())
    
    total_obligaciones = 0
    total_cat_obl = 0
    df_permisos = pd.DataFrame()
    df = pd.DataFrame()


 # ===============================
# KPI: CUMPLIDAS (SEGÚN ROL)
# ===============================

estatus_cumplidas = ["autorizado", "vigente", "excenta"]

# Query base a Cumplimientos con joins
query_cumplimientos = supabase.table("Cumplimientos").select("""
    id_cumpl,
    estatus,
    id_permiso,
    Permisos!inner(
        id_permisos,
        subsidiaria,
        ctro_costos,
        Filial!inner(id_cia, nombre),
        Ctro_Costos!inner(id_costos, nombre)
    )
""").in_("estatus", estatus_cumplidas)

# Aplicar los MISMOS filtros por rol
if rol == "admdr":
    cumplimientos_resp = query_cumplimientos.execute()

elif rol == "filial":
    if id_filial_usuario and id_filial_usuario != "ALL":
        cumplimientos_resp = query_cumplimientos.eq(
            "Permisos.subsidiaria", id_filial_usuario
        ).execute()
    else:
        cumplimientos_resp = query_cumplimientos.execute()

elif rol in ("oficina", "gerencial"):
    if id_costos_usuario and id_costos_usuario != "ALL":
        cumplimientos_resp = query_cumplimientos.eq(
            "Permisos.ctro_costos", id_costos_usuario
        ).execute()
    else:
        cumplimientos_resp = query_cumplimientos.execute()

else:
    cumplimientos_resp = query_cumplimientos.execute()

df_cumplidas = pd.DataFrame(cumplimientos_resp.data)

if df_cumplidas.empty:
    cumplidas = 0
    porcentaje_cumplidas = 0

else:
    cumplidas = len(df_cumplidas)

    if total_obligaciones > 0:
        porcentaje_cumplidas = (cumplidas / total_obligaciones) * 100
    else:
        porcentaje_cumplidas = 0

# ===============================
# KPIs - Cards
# ===============================

st.markdown("## 🚦 Total de Obligaciones")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-label">Total Obligaciones</div>
        <div class="kpi-number">{fmt(total_obligaciones)}</div>
        <small>Catálogo: {fmt(total_cat_obl)} × Permisos: {fmt(len(df_permisos))}</small>
    </div>
    """, unsafe_allow_html=True)



with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">✅ Cumplidas</div>
        <div class="kpi-number">{fmt(cumplidas)}</div>
        <small>{porcentaje_cumplidas:.1f}% del total</small>
    </div>
    """, unsafe_allow_html=True)

# Los otros 2 KPIs los dejamos vacíos por ahora

with col3:
    st.markdown("""
    <div class="kpi-card yellow">
        <div class="kpi-label">⚠️ Por Vencer</div>
        <div class="kpi-number">0</div>
        <small>Por implementar</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card red">
        <div class="kpi-label">🚨 Vencidas</div>
        <div class="kpi-number">0</div>
        <small>Por implementar</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===============================
# INFORMACIÓN DETALLADA
# ===============================

if total_obligaciones > 0:
    st.markdown(f"### ✅ Total calculado correctamente: **{fmt(total_obligaciones)}** obligaciones")
    
    # Para ADMDR: mostrar distribución por empresa
    if rol == "admdr" and 'obligaciones_por_empresa' in st.session_state:
        st.markdown("### 🏢 Distribución por Empresa")
        
        obligaciones_por_empresa = st.session_state['obligaciones_por_empresa']
        
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.dataframe(
                obligaciones_por_empresa[['nombre_empresa', 'total_obligaciones', 'num_permisos']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    'nombre_empresa': 'Empresa',
                    'total_obligaciones': 'Total Obligaciones',
                    'num_permisos': 'N° Permisos'
                }
            )
        
        with col_b:
            st.metric("Total Empresas", len(obligaciones_por_empresa))
            st.metric("Total Permisos", obligaciones_por_empresa['num_permisos'].sum())
    
    # Para otros roles: mostrar su información específica
    elif rol != "admdr":
        st.markdown("### 👤 Información del Usuario")
        col_x, col_y = st.columns(2)
        
        with col_x:
            st.metric("Catálogo de Obligaciones", total_cat_obl)
        
        with col_y:
            st.metric("Permisos Asignados", len(df_permisos) if not df_permisos.empty else 0)
        
        if id_filial_usuario and id_filial_usuario != "ALL":
            try:
                # Intentar obtener nombre de la filial
                filial_resp = supabase.table("Filial")\
                    .select("nombre")\
                    .eq("id_cia", id_filial_usuario)\
                    .execute()
                
                if filial_resp.data:
                    nombre_filial = filial_resp.data[0]['nombre']
                    st.info(f"**Empresa asignada:** {nombre_filial}")
            except:
                pass

else:
    st.warning("⚠️ **No se pudieron calcular las obligaciones**")
    
    # Botón para forzar recálculo
    if st.button("🔄 Intentar nuevamente"):
        st.rerun()

