import streamlit as st
from services.api import obtener_consecutivo, actualizar_consecutivo, validar_sesion

if not validar_sesion():
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()

# ==========================================
# RECOLECTOR DE NOTIFICACIONES PENDIENTES
# ==========================================
if 'toast_msg' in st.session_state:
    st.toast(st.session_state['toast_msg'], icon=st.session_state.get('toast_icon', "⚙️"))
    del st.session_state['toast_msg']
    if 'toast_icon' in st.session_state:
        del st.session_state['toast_icon']

# 1. Envolvemos TODO en una columna central para que no ocupe todo el ancho de la pantalla
col_izq, col_centro, col_der = st.columns([1, 6, 1])

with col_centro:
    # ==========================================
    # SECCIÓN: BIENVENIDA
    # ==========================================
    # Usamos HTML para forzar el centrado de los textos
    st.markdown("<h1 style='text-align: center;'>Bienvenido al Panel de Control</h1>", unsafe_allow_html=True)

    # st.divider()

    # ==========================================
    # SECCIÓN: CONFIGURACIÓN
    # ==========================================
    st.markdown("<h4 style='text-align: center; color: #F4F4F5;'>Modificación del Consecutivo</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 25px; color: #a0aec0;'>Ajusta el prefijo y el número desde el cual se generará la próxima factura.</p>", unsafe_allow_html=True)

    # Consultamos el dato actual a la base de datos
    consecutivo_actual = obtener_consecutivo()

    if consecutivo_actual:
        with st.form("form_consecutivo"):
            # 2. Los inputs ahora van uno debajo del otro, sin columnas
            prefijo = st.text_input("Prefijo de Factura", value=consecutivo_actual["prefijo"])
            numero = st.number_input("Número Actual", value=consecutivo_actual["numero_actual"], min_value=1, step=1)
            
            st.write("") # Un pequeño salto de línea visual
            
            # 3. Sub-columnas dentro del formulario para centrar el botón
            c1, c2, c3 = st.columns([1, 1.2, 1])
            with c2:
                submit = st.form_submit_button("Guardar Cambios", type="primary", use_container_width=True)
            
            if submit:
                payload = {"prefijo": prefijo, "numero_actual": numero}
                respuesta = actualizar_consecutivo(payload)
                if respuesta:
                    # Guardamos el mensaje en la memoria antes de recargar
                    st.session_state['toast_msg'] = f"✅ Consecutivo actualizado a: {respuesta['prefijo']}{respuesta['numero_actual']}"
                    st.session_state['toast_icon'] = "🚀"
                    
                    # Recargamos la pantalla
                    st.rerun()