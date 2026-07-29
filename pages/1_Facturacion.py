import streamlit as st
import pandas as pd
from datetime import datetime
from services.api import obtener_clientes, buscar_producto, generar_factura, validar_sesion

if not validar_sesion():
    st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
    st.stop()
st.title("🧾 Generador de Facturas")

# ==========================================
# RECOLECTOR DE NOTIFICACIONES PENDIENTES
# ==========================================
if 'toast_msg' in st.session_state:
    st.toast(st.session_state['toast_msg'], icon=st.session_state.get('toast_icon', "✅"))
    del st.session_state['toast_msg']
    if 'toast_icon' in st.session_state:
        del st.session_state['toast_icon']

# --- ESTADO DE LA SESIÓN ---
if 'cliente_actual' not in st.session_state:
    st.session_state['cliente_actual'] = None
if 'productos_agregados' not in st.session_state:
    st.session_state['productos_agregados'] = []
if 'producto_temp' not in st.session_state:
    st.session_state['producto_temp'] = None

col1, col2 = st.columns([1, 1])

# ==========================================
# COLUMNA 1: ENTRADA DE DATOS
# ==========================================
with col1:
    st.subheader("1. Selección de Cliente")
    
    # Obtenemos la lista completa de clientes desde la base de datos
    lista_clientes = obtener_clientes()
    
    if not lista_clientes:
        st.warning("⚠️ No hay clientes registrados en el sistema.")
    else:
        # Creamos un diccionario para mapear la vista bonita con los datos reales
        # Ejemplo de llave: "1076503318 - CUANTIAS MENORES"
        opciones_clientes = {f"{c['identificacion']} - {c['nombre']}": c for c in lista_clientes}
        
        # El selectbox mágico: index=None obliga a seleccionar, y placeholder da la pista visual
        cliente_seleccionado_str = st.selectbox(
            "Buscar y Seleccionar Cliente:",
            options=list(opciones_clientes.keys()),
            index=None,
            placeholder="Escribe el nombre o NIT para buscar..."
        )
        
        # Si el usuario selecciona algo del dropdown, lo guardamos en memoria
        if cliente_seleccionado_str:
            st.session_state['cliente_actual'] = opciones_clientes[cliente_seleccionado_str]
            st.success(f"✅ Seleccionado: {st.session_state['cliente_actual']['nombre']}")
        else:
            st.session_state['cliente_actual'] = None

    st.divider()

    st.subheader("2. Agregar Productos")
    
    # PASO 1: Buscar el producto (Se mantiene por código por agilidad del vendedor)
    codigo_prod = st.text_input("Código del Producto:")
    
    if st.button("Buscar Producto"):
        if codigo_prod:
            producto = buscar_producto(codigo_prod)
            if producto:
                st.session_state['producto_temp'] = producto
            else:
                st.error("❌ Código de producto inválido o no encontrado.")
        else:
            st.warning("⚠️ Ingresa un código para buscar.")
            
    # PASO 2: Configurar Precio y Cantidad
    if st.session_state['producto_temp']:
        prod_temp = st.session_state['producto_temp']
        st.info(f"📦 **Producto Encontrado:** {prod_temp['descripcion']}")
        
        with st.form("form_ajuste_producto"):
            precio_aplicado = st.number_input(
                "Precio Unitario a Aplicar ($)", 
                min_value=0.0, 
                value=float(prod_temp['precio_base']), 
                step=100.0
            )
            cantidad = st.number_input("Cantidad", min_value=1.0, step=1.0)
            
            col_add, col_cancel = st.columns(2)
            with col_add:
                btn_agregar = st.form_submit_button("➕ Agregar a Factura", type="primary")
            with col_cancel:
                btn_cancelar = st.form_submit_button("❌ Cancelar")
                
            if btn_agregar:
                if len(st.session_state['productos_agregados']) >= 3:
                    st.error("⚠️ Límite de 3 productos alcanzado según la plantilla.")
                else:
                    detalle = {
                        "producto_id": prod_temp["id"],
                        "codigo": prod_temp["codigo"],
                        "descripcion": prod_temp["descripcion"],
                        "cantidad": cantidad,
                        "precio_aplicado": precio_aplicado,
                        "subtotal": cantidad * precio_aplicado
                    }
                    st.session_state['productos_agregados'].append(detalle)
                    st.session_state['producto_temp'] = None
                    st.rerun()
            
            if btn_cancelar:
                st.session_state['producto_temp'] = None
                st.rerun()

# ==========================================
# COLUMNA 2: RESUMEN Y GENERACIÓN
# ==========================================
with col2:
    st.subheader("3. Resumen de la Transacción")
    
    if st.session_state['productos_agregados']:
        df_resumen = pd.DataFrame(st.session_state['productos_agregados'])
        total_factura = df_resumen['subtotal'].sum()
        
        st.dataframe(
            df_resumen,
            column_order=("cantidad", "descripcion", "precio_aplicado", "subtotal"),
            column_config={
                "cantidad": st.column_config.NumberColumn("Cant.", step=1),
                "descripcion": "Producto",
                "precio_aplicado": st.column_config.NumberColumn("Precio Uni.", format="$ %.2f"),
                "subtotal": st.column_config.NumberColumn("Subtotal", format="$ %.2f"),
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown(f"<h3 style='text-align: right;'>Total: ${total_factura:,.2f}</h3>", unsafe_allow_html=True)
        
        # --- NUEVA SECCIÓN: LIMPIEZA INDIVIDUAL ---
        st.markdown("**Gestión de items:**")
        
        # Iteramos sobre la lista para crear una fila por producto con su propio botón
        for i, prod in enumerate(st.session_state['productos_agregados']):
            c_texto, c_boton = st.columns([3, 1])
            with c_texto:
                # Mostramos qué producto es para que el vendedor esté seguro de qué va a borrar
                st.write(f"▪️ {prod['cantidad']}x {prod['descripcion']}")
            with c_boton:
                # El parámetro 'key' es obligatorio y vital en Streamlit cuando creamos botones en un ciclo (for)
                if st.button("❌ Quitar", key=f"quitar_{i}", use_container_width=True):
                    # pop(i) elimina exactamente ese elemento de la lista en memoria
                    st.session_state['productos_agregados'].pop(i)
                    st.rerun()

        st.write("") # Pequeño espacio visual
        
        # Mantenemos el botón maestro por si quieren descartar toda la factura de un golpe
        if st.button("🗑️ Limpiar Todos los Productos", use_container_width=True):
            st.session_state['productos_agregados'] = []
            st.rerun()

    st.divider()

    # ==========================================
    # BOTÓN MAESTRO DE GENERACIÓN (CENTRADITO)
    # ==========================================
    # Creamos 3 sub-columnas. Ajusta las proporciones [1, 2, 1] si lo quieres más ancho o estrecho.
    col_vacia1, col_btn_generar, col_vacia2 = st.columns([1, 2, 1])
    
    with col_btn_generar:
        # Asignamos el botón a una variable y le ponemos use_container_width=True
        btn_generar = st.button("🚀 Generar Factura PDF", type="primary", use_container_width=True)

    # Ahora evaluamos si se hizo clic en esa variable
    if btn_generar:
        if not st.session_state['cliente_actual']:
            st.error("⚠️ Por favor, selecciona un cliente primero.")
        elif not st.session_state['productos_agregados']:
            st.error("⚠️ Debes agregar al menos un producto a la factura.")
        else:
            ahora = datetime.now()
            payload = {
                "cliente_id": st.session_state['cliente_actual']['id'],
                "usuario_id": st.session_state["usuario_id"], 
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
                    st.session_state['toast_msg'] = f"🎉 ¡Éxito! Factura {respuesta['numero_factura']} generada."
                    st.session_state['toast_icon'] = "✅"
                    
                    st.session_state['cliente_actual'] = None
                    st.session_state['productos_agregados'] = []
                    
                    st.rerun()