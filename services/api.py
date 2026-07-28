import requests
import streamlit as st

# La dirección donde vive nuestro Backend (FastAPI)
BASE_URL = "http://127.0.0.1:8000"

# ==========================================
# 1. SERVICIOS DE CLIENTES
# ==========================================

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