import streamlit as st
from datetime import datetime
from services.api import buscar_cliente, buscar_producto, generar_factura

st.set_page_config(page_title="Facturación | RHE", page_icon="🧾", layout="wide")
st.title("🧾 Generador de Facturas")

# --- ESTADO DE LA SESIÓN ---
# Memoria temporal para guardar el cliente y los productos de la factura en curso
if 'cliente_actual' not in st.session_state:
    st.session_state['cliente_actual'] = None
if 'productos_agregados' not in st.session_state:
    st.session_state['productos_agregados'] = []

# ⚠️ IMPORTANTE: Pega aquí el UUID de tu usuario administrador de Supabase
USUARIO_ID = "87210022-a4bc-49bb-acd1-dbe8d6680219" 

col1, col2 = st.columns([1, 1])

# ==========================================
# COLUMNA 1: ENTRADA DE DATOS
# ==========================================
with col1:
    st.subheader("1. Selección de Cliente")
    cc_cliente = st.text_input("Buscar Cliente por NIT/CC:")
    
    if st.button("Buscar Cliente"):
        cliente = buscar_cliente(cc_cliente)
        if cliente:
            st.session_state['cliente_actual'] = cliente
            st.success(f"✅ Seleccionado: {cliente['nombre']}")
        else:
            st.error("❌ Cliente no encontrado en la base de datos.")

    st.divider()

    st.subheader("2. Agregar Productos")
    codigo_prod = st.text_input("Código del Producto:")
    cantidad = st.number_input("Cantidad", min_value=1.0, step=1.0)
    
    if st.button("Agregar a la Factura"):
        if len(st.session_state['productos_agregados']) >= 3:
            st.warning("⚠️ Límite de 3 productos alcanzado según la plantilla.")
        elif codigo_prod:
            producto = buscar_producto(codigo_prod)
            if producto:
                detalle = {
                    "producto_id": producto["id"],
                    "codigo": producto["codigo"],
                    "descripcion": producto["descripcion"],
                    "cantidad": cantidad,
                    "precio_aplicado": producto["precio_base"],
                    "subtotal": cantidad * producto["precio_base"]
                }
                st.session_state['productos_agregados'].append(detalle)
                st.success(f"✅ {producto['descripcion']} agregado.")
            else:
                st.error("❌ Código de producto inválido.")

# ==========================================
# COLUMNA 2: RESUMEN Y GENERACIÓN
# ==========================================
with col2:
    st.subheader("3. Resumen de la Transacción")
    
    # Mostrar Cliente
    if st.session_state['cliente_actual']:
        st.info(f"**Cliente a Facturar:** {st.session_state['cliente_actual']['nombre']}")
    
    # Mostrar Productos y Total
    total_factura = 0.0
    if st.session_state['productos_agregados']:
        for p in st.session_state['productos_agregados']:
            st.write(f"▪️ {p['cantidad']}x **{p['descripcion']}** | Subtotal: ${p['subtotal']:,.2f}")
            total_factura += p['subtotal']
        
        st.write(f"### **Total: ${total_factura:,.2f}**")
        
        if st.button("🗑️ Limpiar Productos"):
            st.session_state['productos_agregados'] = []
            st.rerun()

    st.divider()

    # BOTÓN MAESTRO DE GENERACIÓN
    if st.button("🚀 Generar Factura PDF", type="primary"):
        if not st.session_state['cliente_actual']:
            st.error("⚠️ Por favor, selecciona un cliente primero.")
        elif not st.session_state['productos_agregados']:
            st.error("⚠️ Debes agregar al menos un producto a la factura.")
        else:
            ahora = datetime.now()
            # Estructuración del JSON exacto que espera FastAPI
            payload = {
                "cliente_id": st.session_state['cliente_actual']['id'],
                "usuario_id": USUARIO_ID,
                "hora_generacion": ahora.strftime("%H:%M:%S"),
                "hora_expedicion": ahora.strftime("%H:%M:%S"),
                "detalles": [
                    {
                        "producto_id": item["producto_id"],
                        "cantidad": item["cantidad"],
                        "precio_aplicado": item["precio_aplicado"]
                    } for item in st.session_state['productos_agregados']
                ]
            }
            
            with st.spinner("Procesando y generando PDF en el servidor..."):
                respuesta = generar_factura(payload)
                if respuesta:
                    st.success(f"🎉 ¡Éxito! Factura **{respuesta['numero_factura']}** generada y registrada en la base de datos.")
                    
                    # Limpiamos el formulario para la siguiente venta
                    st.session_state['cliente_actual'] = None
                    st.session_state['productos_agregados'] = []