import streamlit as st
import requests
from services.api import decodificar_token

API_URL = "http://127.0.0.1:8000"

col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:
    # 2. Agregar el logo. 
    # AJUSTE: Cambiamos de [1, 1, 1] a [1, 1.8, 1] para darle más anchura a la columna central.
    # Si la quieres aún más grande, prueba con [1, 2, 1]. Si la quieres un poco más pequeña, [1, 1.5, 1].
    col_img_izq, col_img_centro, col_img_der = st.columns([1, 1.8, 1])
    
    with col_img_centro:
        try:
            st.image("./assets/img/Logo_Zoom_sinFondo.png", use_container_width=True)
        except Exception:
            st.markdown("<h1 style='text-align: center;'>🏢</h1>", unsafe_allow_html=True)
            
    # 3. Títulos centrados usando un poco de HTML
    # AJUSTE: Se agregó 'margin-top: -25px;' para reducir el espacio con la imagen de arriba.
    # Puedes ajustar ese -25px a -15px o -35px dependiendo de qué tan pegado lo quieras.
    st.markdown("<p style='text-align: center; margin-top: -25px; margin-bottom: 0; font-weight: bold; font-size: 3.2rem; color: white;'>RHE</p>", unsafe_allow_html=True)

    # 4. El formulario ahora vive exclusivamente dentro de esta columna central
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        # Hacemos que el botón ocupe todo el ancho del formulario
        submit_btn = st.form_submit_button("Entrar", type="primary", use_container_width=True)

        if submit_btn and username and password:
            with st.spinner("Autenticando..."):
                respuesta = requests.post(f"{API_URL}/login", data={"username": username, "password": password})

            if respuesta.status_code == 200:
                datos = respuesta.json()
                token = datos.get("access_token")

                payload_decodificado = decodificar_token(token)

                st.session_state["access_token"] = token
                st.session_state["usuario_id"] = payload_decodificado.get("sub")
                st.session_state["autenticado"] = True

                st.query_params["token"] = token
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
        elif submit_btn:
            st.warning("Por favor, ingresa ambos campos.")