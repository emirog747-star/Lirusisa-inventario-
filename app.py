import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from fpdf import FPDF

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bitácora", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 18px; font-weight: bold; border-radius: 10px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; margin-bottom: 10px; }
    /* Estilo especial para botones de calculadora */
    .calc-btn > div > button { height: 2.5em !important; font-size: 16px !important; background-color: #f0f2f6 !important; }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "bitacora_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: 
                data = json.load(f)
                if "notas" not in data: data["notas"] = ""
                if "historial" not in data: data["historial"] = []
                return data
        except: return {"historial": [], "notas": ""}
    return {"historial": [], "notas": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()

# --- CALCULADORA DE BOTONES EN SIDEBAR ---
if "calc_val" not in st.session_state:
    st.session_state.calc_val = ""

def click_button(val):
    if val == "=":
        try:
            # Reemplazamos x por * para que Python entienda la multiplicación
            st.session_state.calc_val = str(eval(st.session_state.calc_val.replace('x', '*')))
        except:
            st.session_state.calc_val = "Error"
    elif val == "C":
        st.session_state.calc_val = ""
    else:
        st.session_state.calc_val += str(val)

with st.sidebar:
    st.title("🔢 Calculadora")
    # Pantalla de la calculadora
    st.text_input("Pantalla:", value=st.session_state.calc_val, disabled=True)
    
    # Grid de botones
    cols = st.columns(4)
    btns = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', 'x'],
        ['1', '2', '3', '-'],
        ['0', '.', 'C', '+']
    ]
    
    for row in btns:
        for i, b_val in enumerate(row):
            if cols[i].button(b_val, key=f"btn_{b_val}_{row}"):
                click_button(b_val)
    
    if st.button("=", key="btn_equal"):
        click_button("=")

    st.write("
