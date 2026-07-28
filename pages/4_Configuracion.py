import streamlit as st
from services.api import obtener_consecutivo, actualizar_consecutivo

st.set_page_config(page_title="Configuración | RHE", page_icon="⚙️")

# --- GUARDIA DE SEGURIDAD ---
if not st.session_state.get("autenticado", False):
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()
# ----------------------------

st.title("⚙️ Configuración del Sistema")

st.subheader("Modificación del Consecutivo de Facturación")
st.write("Ajusta el prefijo y el número desde el cual se generará la próxima factura.")

# Consultamos el dato actual a la base de datos
consecutivo_actual = obtener_consecutivo()

if consecutivo_actual:
    with st.form("form_consecutivo"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Mostramos el prefijo actual y permitimos cambiarlo
            prefijo = st.text_input("Prefijo de Factura", value=consecutivo_actual["prefijo"])
        
        with col2:
            # Mostramos el número actual. El step=1 asegura que solo suba de a 1 número entero
            numero = st.number_input("Número Actual", value=consecutivo_actual["numero_actual"], min_value=1, step=1)
            
        submit = st.form_submit_button("Guardar Cambios", type="primary")
        
        if submit:
            payload = {"prefijo": prefijo, "numero_actual": numero}
            respuesta = actualizar_consecutivo(payload)
            if respuesta:
                st.success(f"✅ Consecutivo actualizado correctamente. Próxima factura será: **{respuesta['prefijo']}{respuesta['numero_actual']}**")
                
                # Pequeño truco para que la vista se recargue con los datos nuevos
                import time
                time.sleep(1.5)
                st.rerun()