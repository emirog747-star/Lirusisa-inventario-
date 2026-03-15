    import streamlit as st
import pandas as pd
from datetime import datetime
import itertools

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
st.write(f"Turno: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- LÓGICA DE DISPONIBILIDAD (El truco del filtro) ---
st.sidebar.header("🚫 ¿Qué se agotó hoy?")
puffs_ok = st.sidebar.toggle("Crazy Puffs Disponibles", value=True)
deep_ok = st.sidebar.toggle("Deep Dish Disponible", value=True)
italiano_ok = st.sidebar.toggle("Pan Italiano Disponible", value=True)

# --- SECCIÓN DE CAJAS ---
with st.expander("📦 CONTROL DE CAJAS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        c_14 = st.number_input("Cajas 14\" (Clásica)", min_value=0, step=1)
        # Solo mostramos entrada si está disponible
        c_deep = st.number_input("Cajas Deep Dish", min_value=0, step=1) if deep_ok else 0
    with col2:
        c_puff = st.number_input("Cajas de Crazy Puff", min_value=0, step=1) if puffs_ok else 0
        c_italiano = st.number_input("Cajas de Pan Italiano", min_value=0, step=1) if italiano_ok else 0

# --- SECCIÓN DE MASAS ---
with st.expander("🍕 MASAS E INGREDIENTES", expanded=True):
    c3, c4 = st.columns(2)
    with c3:
        m_reg = st.number_input("Bolas Masa Regular", min_value=0, step=1)
        m_crazy = st.number_input("Bolas Masa Crazy", min_value=0, step=1)
    with c4:
        queso = st.number_input("Queso (kg)", min_value=0.0, step=0.1)
        pep = st.number_input("Pepperoni (paquetes)", min_value=0, step=1)

# --- SECCIÓN DE MERMA ---
with st.expander("🗑️ REGISTRO DE MERMA", expanded=True):
    merma = st.number_input("Peso Merma Masa (kg)", min_value=0.0, step=0.01)

#
