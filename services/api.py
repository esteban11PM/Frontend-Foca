import requests
import streamlit as st
import base64
import json

# La dirección donde vive nuestro Backend (FastAPI)
BASE_URL = "http://127.0.0.1:8000"

# ==========================================
# 1. SERVICIOS DE CLIENTES
# ==========================================

@st.cache_data(ttl=300)
def obtener_clientes():
    """Envía petición GET para traer todos los clientes."""
    try:
        response = requests.get(f"{BASE_URL}/clientes/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al obtener clientes: {e}")
        return []

def crear_cliente(datos_cliente: dict):
    """Envía la petición POST para registrar un nuevo cliente."""
    try:
        response = requests.post(f"{BASE_URL}/clientes/", json=datos_cliente)
        response.raise_for_status()

        obtener_clientes.clear()

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión al crear cliente: {e}")
        return None

def buscar_cliente(identificacion: str):
    """Envía la petición GET para buscar un cliente por su NIT o CC."""
    try:
        response = requests.get(f"{BASE_URL}/clientes/{identificacion}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión al buscar cliente: {e}")
        return None

# ==========================================
# 2. SERVICIOS DE PRODUCTOS
# ==========================================

@st.cache_data(ttl=300)
def obtener_productos():
    """Envía petición GET para traer todos los productos."""
    try:
        response = requests.get(f"{BASE_URL}/productos/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al obtener productos: {e}")
        return []

def crear_producto(datos_producto: dict):
    """Envía la petición POST para registrar un nuevo producto en el catálogo."""
    try:
        response = requests.post(f"{BASE_URL}/productos/", json=datos_producto)
        response.raise_for_status()

        obtener_productos.clear()

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión al crear producto: {e}")
        return None

def buscar_producto(codigo: str):
    """Envía la petición GET para buscar un producto por su código."""
    try:
        response = requests.get(f"{BASE_URL}/productos/{codigo}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión al buscar producto: {e}")
        return None

# ==========================================
# 3. SERVICIO DE FACTURACIÓN (EL NÚCLEO)
# ==========================================

def generar_factura(payload_factura: dict):
    """Envía la petición POST al endpoint maestro para generar el PDF y guardar en BD."""
    try:
        response = requests.post(f"{BASE_URL}/facturas/generar", json=payload_factura)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"⚠️ Error del servidor: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error crítico de conexión con el motor PDF: {e}")
        return None

# ==========================================
# 4. SERVICIOS DE CONFIGURACIÓN
# ==========================================

def obtener_consecutivo():
    try:
        response = requests.get(f"{BASE_URL}/consecutivo/")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al obtener consecutivo: {e}")
        return None

def actualizar_consecutivo(payload: dict):
    try:
        response = requests.put(f"{BASE_URL}/consecutivo/", json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al actualizar consecutivo: {e}")
        return None

def validar_sesion() -> bool:
    """Revisa si hay un token activo en session_state o recupera la sesión desde la URL si hubo F5."""
    
    # 1. Si ya estamos autenticados en memoria (Navegación normal)
    if st.session_state.get("autenticado", False) and "access_token" in st.session_state:
        # 🛡️ EL TRUCO: Reinyectamos el token a la URL porque Streamlit lo borra al cambiar de menú
        st.query_params["token"] = st.session_state["access_token"]
        return True

    # 2. Si hubo recarga (F5) y se perdió la memoria, buscamos el token guardado en la URL
    token_in_url = st.query_params.get("token")
    if token_in_url:
        try:
            # Decodificamos el JWT usando 'urlsafe' (El estándar correcto para JWT)
            payload_base64 = token_in_url.split(".")[1]
            payload_base64 += "=" * (-len(payload_base64) % 4)
            payload_decodificado = json.loads(base64.urlsafe_b64decode(payload_base64).decode("utf-8"))

            st.session_state["access_token"] = token_in_url
            st.session_state["usuario_id"] = payload_decodificado["sub"]
            st.session_state["autenticado"] = True
            
            # Aseguramos que se mantenga en la URL
            st.query_params["token"] = token_in_url
            return True
        except Exception as e:
            # Si el token es inválido o se corrompe, limpiamos todo
            st.query_params.clear()
            st.session_state.clear()
            return False

    return False

# ==========================================
# 5. SERVICIOS DE AUTENTICACIÓN Y UTILIDADES
# ==========================================

def decodificar_token(token: str) -> dict:
    """Decodifica un token JWT y devuelve su payload de forma segura."""
    try:
        payload_base64 = token.split(".")[1]
        payload_base64 += "=" * (-len(payload_base64) % 4)
        return json.loads(base64.urlsafe_b64decode(payload_base64).decode("utf-8"))
    except Exception as e:
        return {}

def validar_sesion() -> bool:
    """Revisa si hay un token activo en session_state o recupera la sesión desde la URL si hubo F5."""
    
    # 1. Si ya estamos autenticados en memoria (Navegación normal)
    if st.session_state.get("autenticado", False) and "access_token" in st.session_state:
        st.query_params["token"] = st.session_state["access_token"]
        return True

    # 2. Si hubo recarga (F5) y se perdió la memoria, buscamos el token guardado en la URL
    token_in_url = st.query_params.get("token")
    if token_in_url:
        payload_decodificado = decodificar_token(token_in_url)
        
        # Si la decodificación fue exitosa (el diccionario no está vacío)
        if payload_decodificado:
            st.session_state["access_token"] = token_in_url
            st.session_state["usuario_id"] = payload_decodificado.get("sub")
            st.session_state["autenticado"] = True
            
            st.query_params["token"] = token_in_url
            return True
        else:
            # Token inválido o corrupto
            st.query_params.clear()
            st.session_state.clear()
            return False

    return False