import streamlit as st
import requests

# Configuración inicial de la pestaña del navegador
st.set_page_config(
    page_title="RHE - Facturación",
    page_icon="./assets/img/Logo_Zoom_sinFondo.ico",
    layout="centered"
)

# Constante con la URL base de tu API (FastAPI)
API_URL = "http://127.0.0.1:8000"

st.title("🧊 Sistema Web RHE")
st.subheader("Módulo de Facturación")

st.info("✅ La interfaz gráfica se ha inicializado correctamente. Lista para consumir la API.")