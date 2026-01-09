import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from utils.supabase_client import get_supabase_client

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
    /* Sidebar azul */
    section[data-testid="stSidebar"] {
        background-color: #457EB0;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid;
    }
    
    .kpi-card.green { border-left-color: #28a745; }
    .kpi-card.yellow { border-left-color: #ffc107; }
    .kpi-card.red { border-left-color: #dc3545; }
    .kpi-card.blue { border-left-color: #007bff; }
    
    .kpi-number {
        font-size: 3em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 1.1em;
        color: #666;
        font-weight: 600;
    }
    
    /* Bienvenida */
    .welcome-banner {
        background: linear-gradient(135deg, #457EB0 0%, #2c5a8a 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
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
        "🏠 Dashboard": "Dashboard.py",
        "👥 Usuarios": "Usuarios.py",
        "📋 Permisos": "Permisos.py",
        "🚗 Flota": "Flota.py",
        "📅 Calendario": "Calendario.py"
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
    <p style='font-size: 1.2em; margin-top: 10px;'>Panel de Control Ejecutivo - {datetime.now().strftime('%d/%m/%Y')}</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# OBTENER DATOS
# ===============================

try:
    # Query para cumplimientos con filtro opcional de empresa
    query = supabase.table("Cumplimientos").select("""
        *,
        Permisos!inner(subsidiaria, Filial!inner(nombre)),
        Cat_Obl!inner(obligacion)
    """)
    
    if id_empresa:
        query = query.eq("Permisos.subsidiaria", id_empresa)
    
    cumplimientos = query.execute()
    df = pd.DataFrame(cumplimientos.data)
    
    # Calcular KPIs
    total_obligaciones = len(df)
    
    # Calcular estados basados en fechas
    hoy = datetime.now().date()
    
    def clasificar_estado(row):
        if pd.isna(row.get('fecha_fin')):
            return 'sin_fecha'
        
        fecha_fin = pd.to_datetime(row['fecha_fin']).date()
        dias_restantes = (fecha_fin - hoy).days
        
        if dias_restantes < 0:
            return 'vencido'
        elif dias_restantes <= 30:
            return 'por_vencer'
        else:
            return 'cumplido'
    
    df['estado'] = df.apply(clasificar_estado, axis=1)
    
    cumplidas = len(df[df['estado'] == 'cumplido'])
    por_vencer = len(df[df['estado'] == 'por_vencer'])
    vencidas = len(df[df['estado'] == 'vencido'])
    
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    total_obligaciones = cumplidas = por_vencer = vencidas = 0
    df = pd.DataFrame()

# ===============================
# KPIs - SEMÁFORO
# ===============================

st.markdown("## 🚦 Indicadores de Cumplimiento")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-label">Total Obligaciones</div>
        <div class="kpi-number">{total_obligaciones}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">✅ Cumplidas</div>
        <div class="kpi-number">{cumplidas}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card yellow">
        <div class="kpi-label">⚠️ Por Vencer (30d)</div>
        <div class="kpi-number">{por_vencer}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card red">
        <div class="kpi-label">🚨 Vencidas</div>
        <div class="kpi-number">{vencidas}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===============================
# GRÁFICOS Y ANÁLISIS
# ===============================

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### 📊 Distribución de Estados")
    
    if not df.empty:
        # Gráfico de barras
        estados_count = df['estado'].value_counts()
        
        st.bar_chart(estados_count)
        
        # Tabla detallada de próximos vencimientos
        st.markdown("### ⏰ Próximos Vencimientos (30 días)")
        
        proximos = df[df['estado'] == 'por_vencer'].copy()
        
        if not proximos.empty:
            proximos['dias_restantes'] = proximos.apply(
                lambda row: (pd.to_datetime(row['fecha_fin']).date() - hoy).days,
                axis=1
            )
            proximos = proximos.sort_values('dias_restantes')
            
            st.dataframe(
                proximos[['obligacion', 'fecha_fin', 'dias_restantes']].head(10),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No hay vencimientos próximos")
    else:
        st.info("📭 No hay datos para mostrar")

with col_right:
    st.markdown("### 🏢 Cumplimiento por Empresa")
    
    if not df.empty:
        # Agrupar por empresa
        por_empresa = df.groupby('estado').size().to_frame('count')
        st.dataframe(por_empresa, use_container_width=True)
        
        # Porcentaje de cumplimiento
        if total_obligaciones > 0:
            porcentaje_cumplimiento = (cumplidas / total_obligaciones) * 100
            
            st.markdown("### 📈 Índice de Cumplimiento")
            st.progress(porcentaje_cumplimiento / 100)
            st.markdown(f"**{porcentaje_cumplimiento:.1f}%** de obligaciones cumplidas")

# ===============================
# ALERTAS CRÍTICAS
# ===============================

if vencidas > 0:
    st.markdown("---")
    st.markdown("### 🚨 ALERTAS CRÍTICAS - Obligaciones Vencidas")
    
    vencidas_df = df[df['estado'] == 'vencido']
    
    st.error(f"Hay {vencidas} obligaciones vencidas que requieren atención inmediata")
    
    st.dataframe(
        vencidas_df[['obligacion', 'fecha_fin']].head(10),
        use_container_width=True,
        hide_index=True
    )