import streamlit as st
from services.api import obtener_consecutivo, actualizar_consecutivo, validar_sesion


if not validar_sesion():
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()

st.title("⚙️ Configuración del Sistema")

# ==========================================
# RECOLECTOR DE NOTIFICACIONES PENDIENTES
# ==========================================
if 'toast_msg' in st.session_state:
    st.toast(st.session_state['toast_msg'], icon=st.session_state.get('toast_icon', "⚙️"))
    del st.session_state['toast_msg']
    if 'toast_icon' in st.session_state:
        del st.session_state['toast_icon']

st.subheader("Modificación del Consecutivo de Facturación")
st.write("Ajusta el prefijo y el número desde el cual se generará la próxima factura.")

# Consultamos el dato actual a la base de datos
consecutivo_actual = obtener_consecutivo()

consecutivo_actual = obtener_consecutivo()

if consecutivo_actual:
    with st.form("form_consecutivo"):
        col1, col2 = st.columns(2)
        
        with col1:
            prefijo = st.text_input("Prefijo de Factura", value=consecutivo_actual["prefijo"])
        
        with col2:
            numero = st.number_input("Número Actual", value=consecutivo_actual["numero_actual"], min_value=1, step=1)
            
        submit = st.form_submit_button("Guardar Cambios", type="primary")
        
        if submit:
            payload = {"prefijo": prefijo, "numero_actual": numero}
            respuesta = actualizar_consecutivo(payload)
            if respuesta:
                # 1. Guardamos el mensaje en la memoria antes de recargar
                st.session_state['toast_msg'] = f"✅ Consecutivo actualizado a: {respuesta['prefijo']}{respuesta['numero_actual']}"
                st.session_state['toast_icon'] = "🚀"
                
                # 2. Recargamos la pantalla
                st.rerun()