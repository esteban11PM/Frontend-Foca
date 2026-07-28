import streamlit as st
from services.api import crear_cliente, buscar_cliente

st.set_page_config(page_title="Clientes | RHE", page_icon="👥")
st.title("👥 Gestión de Clientes")

# Creación de pestañas para organizar la vista
tab_registro, tab_busqueda = st.tabs(["Registrar Cliente", "Buscar Cliente"])

# --- PESTAÑA 1: REGISTRO ---
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

# --- PESTAÑA 2: BÚSQUEDA ---
with tab_busqueda:
    st.subheader("Consultar Cliente Existente")
    search_id = st.text_input("Ingrese NIT o CC para buscar:")
    
    if st.button("Buscar Cliente"):
        if search_id:
            cliente = buscar_cliente(search_id)
            if cliente:
                st.success("✅ Cliente encontrado en la base de datos.")
                # Tarjeta de resumen visual
                st.info(f"**Nombre:** {cliente['nombre']}\n\n**Identificación:** {cliente['identificacion']}")
        else:
            st.warning("⚠️ Ingresa un número de identificación válido.")