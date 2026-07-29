import streamlit as st
import requests
from services.api import decodificar_token  # Importamos la función centralizada

API_URL = "http://127.0.0.1:8000"

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

            # 1. Usamos nuestra función mágica
            payload_decodificado = decodificar_token(token)

            # 2. Asignamos variables de sesión
            st.session_state["access_token"] = token
            st.session_state["usuario_id"] = payload_decodificado.get("sub")
            st.session_state["autenticado"] = True

            # 3. Guardamos en URL
            st.query_params["token"] = token

            st.success("¡Acceso concedido!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    elif submit_btn:
        st.warning("Por favor, ingresa ambos campos.")