import streamlit as st
import requests
import base64
import json

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

            payload_base64 = token.split(".")[1]
            payload_base64 += "=" * (-len(payload_base64) % 4)
            payload_decodificado = json.loads(base64.urlsafe_b64decode(payload_base64).decode("utf-8"))

            st.session_state["access_token"] = token
            st.session_state["usuario_id"] = payload_decodificado["sub"]
            st.session_state["autenticado"] = True

            # Guardamos el token en la URL
            st.query_params["token"] = token

            st.success("¡Acceso concedido!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    elif submit_btn:
        st.warning("Por favor, ingresa ambos campos.")