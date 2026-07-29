import streamlit as st
import pandas as pd
from services.api import crear_cliente, obtener_clientes, validar_sesion

if not validar_sesion():
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()
st.title("👥 Gestión de Clientes")

# Creación de pestañas para organizar la vista
tab_lista, tab_registro = st.tabs(["Listado de Clientes", "Registrar Cliente"])

# --- PESTAÑA 1: LISTADO ---
with tab_lista:
    st.subheader("Directorio de Clientes")
    if st.button("🔄 Actualizar Lista"):
        st.rerun()
        
    clientes = obtener_clientes()
    
    if clientes:
        # Convertimos la lista de diccionarios a un DataFrame para que se vea como tabla
        df_clientes = pd.DataFrame(clientes)
        # Reordenamos y renombramos columnas para la vista
        df_clientes = df_clientes[["identificacion", "nombre"]]
        df_clientes.columns = ["NIT / CC", "Nombre o Razón Social"]
        
        # Mostramos la tabla interactiva (permite ordenar y hacer scroll)
        st.dataframe(df_clientes, use_container_width=True, hide_index=True)
    else:
        st.info("No hay clientes registrados en el sistema.")

# --- PESTAÑA 2: REGISTRO ---
with tab_registro:
    st.subheader("Registrar Nuevo Cliente")
    with st.form("form_crear_cliente", clear_on_submit=True):
        identificacion = st.text_input("NIT o Cédula de Ciudadanía")
        nombre = st.text_input("Nombre o Razón Social")
        
        submit_btn = st.form_submit_button("Guardar Cliente")

        if submit_btn:
            if identificacion and nombre:
                payload = {
                    "identificacion": identificacion,
                    "nombre": nombre
                }
                respuesta = crear_cliente(payload)
                if respuesta:
                    st.success(f"✅ Cliente '{respuesta['nombre']}' registrado exitosamente.")
            else:
                st.warning("⚠️ Por favor, completa todos los campos.")