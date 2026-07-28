import streamlit as st
from services.api import crear_producto, buscar_producto

st.set_page_config(page_title="Productos | RHE", page_icon="📦")
if not st.session_state.get("autenticado", False):
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()
st.title("📦 Catálogo de Productos")

tab_registro, tab_busqueda = st.tabs(["Registrar Producto", "Buscar Producto"])

# --- PESTAÑA 1: REGISTRO ---
with tab_registro:
    st.subheader("Registrar Nuevo Producto")
    with st.form("form_crear_producto", clear_on_submit=True):
        codigo = st.text_input("Código del Producto (Ej: 042)")
        descripcion = st.text_input("Descripción")
        precio_base = st.number_input("Precio Base", min_value=0.0, step=100.0)
        
        submit_btn = st.form_submit_button("Guardar Producto")

        if submit_btn:
            if codigo and descripcion and precio_base > 0:
                payload = {
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "precio_base": precio_base
                }
                respuesta = crear_producto(payload)
                if respuesta:
                    st.success(f"✅ Producto '{respuesta['descripcion']}' registrado exitosamente.")
            else:
                st.warning("⚠️ Completa todos los campos correctamente.")

# --- PESTAÑA 2: BÚSQUEDA ---
with tab_busqueda:
    st.subheader("Consultar Producto Existente")
    search_code = st.text_input("Ingrese Código del Producto:")
    
    if st.button("Buscar Producto"):
        if search_code:
            producto = buscar_producto(search_code)
            if producto:
                st.success("✅ Producto encontrado.")
                st.info(f"**Código:** {producto['codigo']}\n\n**Descripción:** {producto['descripcion']}\n\n**Precio Base:** ${producto['precio_base']:,.2f}")
        else:
            st.warning("⚠️ Ingresa un código válido.")