
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# --- CONFIGURACIÓN VISUAL (Tu diseño original) ---
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", page_icon="🍕", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    .stNumberInput>div>div>input { font-size: 1.2em; }
    [data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍕 Bitácora de Hamlet y Ofelia")
st.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN DE CAJAS (Actualizada con las que faltaban) ---
with st.expander("📦 CONTROL DE CAJAS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        caja_14 = st.number_input("Cajas 14\" (Clásica)", min_value=0, step=1)
        caja_deep = st.number_input("Cajas Deep Dish", min_value=0, step=1)
    with col2:
        caja_puff = st.number_input("Cajas de Crazy Puff", min_value=0, step=1)
        caja_italiano = st.number_input("Cajas de Pan Italiano", min_value=0, step=1)

# --- SECCIÓN DE MASAS E INGREDIENTES ---
with st.expander("🍕 MASAS E INGREDIENTES", expanded=True):
    c3, c4 = st.columns(2)
    with c3:
        masa_reg = st.number_input("Bolas Masa Regular", min_value=0, step=1)
        masa_crazy = st.number_input("Bolas Masa Crazy", min_value=0, step=1)
    with c4:
        queso = st.number_input("Queso (kg)", min_value=0.0, step=0.1)
        pep = st.number_input("Pepperoni (paquetes)", min_value=0, step=1)

# --- SECCIÓN DE MERMA ---
with st.expander("🗑️ REGISTRO DE MERMA", expanded=True):
    merma_masa = st.number_input("Peso Merma Masa (kg)", min_value=0.0, step=0.01)

# --- CÁLCULOS Y REPORTE ---
st.divider()
datos = {
    "Producto": ["Caja 14", "Caja Deep Dish", "Caja Puff", "Caja Italiano", "Masa Reg", "Masa Crazy", "Queso", "Pepperoni", "Merma"],
    "Cantidad": [caja_14, caja_deep, caja_puff, caja_italiano, masa_reg, masa_crazy, queso, pep, merma_masa]
}
df = pd.DataFrame(datos)

# --- BOTONES DE GUARDADO (Lo nuevo) ---
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Generar CSV para descargar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 GUARDAR Y DESCARGAR EXCEL",
        data=csv,
        file_name=f"inventario_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv",
    )

with col_btn2:
    if st.button("🔄 LIMPIAR PARA NUEVO TURNO"):
        st.rerun()

st.success("Diseño restaurado. Las cajas nuevas y el botón de descarga están listos.")
