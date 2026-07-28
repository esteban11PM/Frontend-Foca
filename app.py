import streamlit as st
import requests
import base64
import json

# Configuración inicial (Debe ser el primer comando)
st.set_page_config(page_title="RHE - Dashboard", page_icon="🧾", layout="centered")

API_URL = "http://127.0.0.1:8000"

def iniciar_sesion():
    st.title("🔐 Sistema de Facturación RHE")
    st.subheader("Inicia sesión para continuar")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit_btn = st.form_submit_button("Entrar")

        if submit_btn and username and password:
            respuesta = requests.post(f"{API_URL}/login", data={"username": username, "password": password})

            if respuesta.status_code == 200:
                datos = respuesta.json()
                token = datos.get("access_token")
                
                # Magia RHE: Decodificamos el JWT para extraer tu USUARIO_ID real
                payload_base64 = token.split(".")[1]
                payload_base64 += "=" * (-len(payload_base64) % 4)
                payload_decodificado = json.loads(base64.b64decode(payload_base64).decode("utf-8"))
                
                st.session_state["access_token"] = token
                st.session_state["usuario_id"] = payload_decodificado["sub"]
                st.session_state["autenticado"] = True
                st.success("¡Acceso concedido!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
        elif submit_btn:
            st.warning("Por favor, ingresa ambos campos.")

def cerrar_sesion():
    st.session_state.clear() # Limpiamos toda la memoria
    st.rerun()

def dashboard():
    st.title("Bienvenido al Panel de Control 🚀")
    st.write("Tu sistema está seguro y operando correctamente. Utiliza el menú lateral para navegar.")
    
    # Botón para cerrar sesión en el menú lateral
    st.sidebar.title("Navegación")
    st.sidebar.button("Cerrar Sesión", on_click=cerrar_sesion)
    st.sidebar.markdown("---")

# ==========================================
# CEREBRO DEL FRONTEND
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    iniciar_sesion()
else:
    dashboard()