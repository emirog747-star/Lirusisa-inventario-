import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", page_icon="🍕", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stNumberInput>div>div>input { font-size: 1.2em; }
    [data-testid="stExpander"] { border: 2px solid #FF4B4B; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍕 Bitácora de Hamlet y Ofelia")
st.write(f"Turno del día: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN DE CAJAS ---
with st.expander("📦 CONTROL DE CAJAS (Suministros)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        c_14 = st.number_input("Cajas 14\" (Clásica)", min_value=0, step=1)
        c_deep = st.number_input("Cajas Deep Dish", min_value=0, step=1)
    with c2:
        c_puff = st.number_input("Cajas de Crazy Puff", min_value=0, step=1)
        c_italiano = st.number_input("Cajas de Pan Italiano", min_value=0, step=1)
    
    total_cajas = c_14 + c_deep + c_puff + c_italiano
    st.write(f"**Total de Cajas en Inventario:** {total_cajas} piezas")

# --- SECCIÓN DE MASAS E INGREDIENTES ---
with st.expander("🍕 MASAS E INGREDIENTES", expanded=True):
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m_reg = st.number_input("Bolas Masa Regular", min_value=0, step=1)
        m_crazy = st.number_input("Bolas Masa Crazy", min_value=0, step=1)
        total_masas = m_reg + m_crazy
        st.write(f"**Total Masas:** {total_masas} bolas")
    with col_m2:
        queso = st.number_input("Queso (kg)", min_value=0.0, step=0.1)
        pep = st.number_input("Pepperoni (paquetes)", min_value=0, step=1)

# --- SECCIÓN DE MERMA ---
with st.expander("🗑️ REGISTRO DE MERMA", expanded=True):
    merma = st.number_input("Peso Merma Masa (kg)", min_value=0.0, step=0.01)

# --- BOTONES DE ACCIÓN ---
st.divider()
datos_finales = {
    "Concepto": ["Caja 14", "Caja Deep Dish", "Caja Puff", "Caja Italiano", "Masa Reg", "Masa Crazy", "Queso", "Pepperoni", "Merma"],
    "Cantidad": [c_14, c_deep, c_puff, c_italiano, m_reg, m_crazy, queso, pep, merma]
}
df = pd.DataFrame(datos_finales)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 GUARDAR Y DESCARGAR REPORTE",
        data=csv,
        file_name=f"inventario_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv",
    )

with col_btn2:
    if st.button("🔄 LIMPIAR DATOS (NUEVO TURNO)"):
        st.rerun()
