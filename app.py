import streamlit as st
import streamlit.components.v1 as components
from services.api import validar_sesion

# 1. ÚNICO set_page_config de toda la aplicación
st.set_page_config(
    page_title="RHE - Facturación",
    page_icon="./assets/img/Logo_Zoom_sinFondo.ico",
    layout="wide"
)

# ==========================================
# CSS PARA OCULTAR NAVBAR Y AJUSTAR ESPACIOS
# ==========================================
st.markdown(
    """
    <style>
    /* 1. Ocultar el encabezado superior (Deploy, menú, etc.) */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 2. Reducir el espacio blanco superior para eliminar el scroll */
    .block-container {
        padding-top: 2rem !important; 
        padding-bottom: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# FUNCIÓN LATIDO (KEEP-ALIVE)
# ==========================================
def mantener_servidor_despierto():
    """Inyecta un script JS invisible que hace ping a Render cada 10 minutos (600,000 ms)"""
    # Usamos tu URL real de Render
    API_URL = "https://backend-rhe.onrender.com"
    
    codigo_js = f"""
    <script>
        console.log("Sistema de latido activado. Protegiendo contra suspensión de Render.");
        setInterval(function() {{
            fetch('{API_URL}/docs', {{ mode: 'no-cors' }})
                .then(() => console.log('Ping enviado al servidor.'))
                .catch(e => console.log('Ping silencioso.'));
        }}, 600000); // 10 minutos
    </script>
    """
    # Lo renderizamos invisiblemente
    components.html(codigo_js, height=0, width=0)

# Pequeña función para el botón global de cerrar sesión
def cerrar_sesion():
    st.session_state.clear()
    st.query_params.clear()

# 2. LÓGICA DE ENRUTAMIENTO DINÁMICO
if not validar_sesion():
    # Si no hay sesión, el menú solo tiene la página de Login
    login_page = st.Page("views/login.py", title="Iniciar Sesión", icon="🔐")
    pg = st.navigation([login_page])
else:
    # Si HAY sesión, armamos el menú completo
    inicio_page = st.Page("views/dashboard.py", title="Panel Principal", icon="🚀", default=True)
    facturacion_page = st.Page("pages/1_Facturacion.py", title="Facturación", icon="🧾")
    clientes_page = st.Page("pages/2_Clientes.py", title="Clientes", icon="👥")
    productos_page = st.Page("pages/3_Productos.py", title="Productos", icon="📦")
    
    pg = st.navigation([inicio_page, facturacion_page, clientes_page, productos_page])
    
    # Colocamos el botón de cerrar sesión en la barra lateral para que salga en TODAS las páginas
    st.sidebar.button("Cerrar Sesión", on_click=cerrar_sesion)
    st.sidebar.markdown("---")

# 3. EJECUTAR LA PÁGINA
pg.run()