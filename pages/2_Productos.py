import streamlit as st
import pandas as pd
from services.api import crear_producto, obtener_productos, validar_sesion

st.set_page_config(page_title="Productos | RHE", page_icon="📦")
if not validar_sesion():
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()
st.title("📦 Catálogo de Productos")

tab_lista, tab_registro = st.tabs(["Listado de Productos", "Registrar Producto"])

# --- PESTAÑA 1: LISTADO ---
with tab_lista:
    st.subheader("Inventario Actual")
    if st.button("🔄 Actualizar Catálogo"):
        st.rerun()
        
    productos = obtener_productos()
    
    if productos:
        df_productos = pd.DataFrame(productos)
        df_productos = df_productos[["codigo", "descripcion", "precio_base"]]
        df_productos.columns = ["Código", "Descripción", "Precio Base ($)"]
        
        # Le damos formato moneda a la columna de precio
        st.dataframe(
            df_productos.style.format({"Precio Base ($)": "{:,.2f}"}), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("El catálogo de productos está vacío.")

# --- PESTAÑA 2: REGISTRO ---
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