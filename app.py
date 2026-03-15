import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", page_icon="🍕")

st.title("🍕 Bitácora de Hamlet y Ofelia")
st.subheader("Control de Inventario - Little Caesars")

# Fecha actual para el reporte
fecha_hoy = datetime.now().strftime("%d-%m-%Y_%H-%M")

# --- SECCIÓN 1: MASAS E INGREDIENTES ---
st.header("📦 Masas e Ingredientes")
col1, col2 = st.columns(2)

with col1:
    masa_regular = st.number_input("Bolas de Masa Regular", min_value=0, step=1)
    masa_crazy = st.number_input("Bolas de Masa Crazy", min_value=0, step=1)

with col2:
    pepperoni = st.number_input("Paquetes de Pepperoni", min_value=0, step=1)
    queso = st.number_input("Bolsas de Queso (kg)", min_value=0.0, step=0.1)

# --- SECCIÓN 2: SUMINISTROS (CAJAS) ---
st.header("📦 Suministros y Cajas")
c1, c2 = st.columns(2)

with c1:
    caja_14 = st.number_input("Cajas 14\" (Clásica)", min_value=0, step=1)
    caja_deep = st.number_input("Cajas Deep Dish", min_value=0, step=1)

with c2:
    caja_puff = st.number_input("Cajas de Crazy Puff", min_value=0, step=1)
    caja_italiano = st.number_input("Cajas de Pan Italiano", min_value=0, step=1)

# --- SECCIÓN 3: MERMA (PESOS) ---
st.header("🗑️ Registro de Merma")
merma_masa = st.number_input("Peso Merma Masa (kg)", min_value=0.0, step=0.01)

# --- PROCESAMIENTO DE DATOS ---
datos_inventario = {
    "Concepto": ["Masa Regular", "Masa Crazy", "Pepperoni", "Queso", "Caja 14", "Caja Deep Dish", "Caja Puff", "Caja Italiano", "Merma Masa"],
    "Cantidad": [masa_regular, masa_crazy, pepperoni, queso, caja_14, caja_deep, caja_puff, caja_italiano, merma_masa],
    "Unidad": ["Bolas", "Bolas", "Paquetes", "Kg", "Piezas", "Piezas", "Piezas", "Piezas", "Kg"]
}

df = pd.DataFrame(datos_inventario)

st.divider()

# --- BOTONES DE ACCIÓN ---
st.write("### Acciones")

# Función para convertir a CSV
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="💾 Descargar Inventario (Excel/CSV)",
    data=csv,
    file_name=f"inventario_{fecha_hoy}.csv",
    mime="text/csv",
    help="Descarga el reporte y guárdalo en tu celular"
)

if st.button("🔄 Limpiar Datos / Nuevo Turno"):
    st.cache_data.clear()
    st.rerun()

st.info("Nota: Una vez descargado el archivo, presiona 'Limpiar Datos' para el siguiente turno.")
