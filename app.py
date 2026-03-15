import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", page_icon="🍕", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .stNumberInput>div>div>input { font-size: 1.2em; }
    .metric-box { background-color: #1e3d33; color: #4ade80; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; font-weight: bold; }
    [data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍕 Bitácora de Hamlet y Ofelia")
st.write(f"Fecha de registro: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN DE HARINA (Corregida según tu foto) ---
with st.expander("🍞 CONTROL DE HARINA", expanded=True):
    costales_abiertos = st.number_input("Costales abiertos (Unidad)", min_value=0.0, step=0.01, value=0.45)
    costales_cerrados = st.number_input("Costales cerrados (Unidad)", min_value=0, step=1)
    
    total_harina = costales_abiertos + costales_cerrados
    st.markdown(f'<div class="metric-box">Equivalente a: {total_harina} costales de harina</div>', unsafe_allow_html=True)

# --- SECCIÓN DE CAJAS (Agregadas las que faltaban) ---
with st.expander("📦 CONTROL DE CAJAS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        caja_14 = st.number_input("Cajas 14\" (Clásica)", min_value=0, step=1)
        caja_deep = st.number_input("Cajas Deep Dish", min_value=0, step=1)
    with col2:
        caja_puff = st.number_input("Cajas de Crazy Puff", min_value=0, step=1)
        caja_italiano = st.number_input("Cajas de Pan Italiano", min_value=0, step=1)

# --- MASAS E INGREDIENTES ---
with st.expander("🍕 INVENTARIO DE PRODUCTOS", expanded=True):
    c3, c4 = st.columns(2)
    with c3:
        masa_reg = st.number_input("Bolas Masa Regular", min_value=0, step=1)
        masa_crazy = st.number_input("Bolas Masa Crazy", min_value=0, step=1)
    with c4:
        queso = st.number_input("Queso (kg)", min_value=0.0, step=0.1)
        pep = st.number_input("Pepperoni (paquetes)", min_value=0, step=1)

# --- BOTONES DE ACCIÓN ---
st.divider()
datos = {
    "Producto": ["Harina Total", "Caja 14", "Caja Deep", "Caja Puff", "Caja Italiano", "Masa Reg", "Masa Crazy", "Queso", "Pep"],
    "Cantidad": [total_harina, caja_14, caja_deep, caja_puff, caja_italiano, masa_reg, masa_crazy, queso, pep]
}
df = pd.DataFrame(datos)

b1, b2 = st.columns(2)
with b1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 GUARDAR Y DESCARGAR", data=csv, file_name=f"inventario_{datetime.now().strftime('%d%m%Y')}.csv", mime="text/csv")
with b2:
    if st.button("🔄 LIMPIAR TURNO"):
        st.rerun()
