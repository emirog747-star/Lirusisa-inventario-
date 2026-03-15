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
    .stButton>button { width: 100%; height: 3.2em; font-size: 16px; font-weight: bold; border-radius: 8px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; margin-bottom: 10px; }
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

# --- CALCULADORA EN CUADRÍCULA (SIDEBAR) ---
if "calc_val" not in st.session_state:
    st.session_state.calc_val = ""

def click_button(val):
    if val == "=":
        try: st.session_state.calc_val = str(eval(st.session_state.calc_val.replace('x', '*')))
        except: st.session_state.calc_val = "Error"
    elif val == "C": st.session_state.calc_val = ""
    else: st.session_state.calc_val += str(val)

with st.sidebar:
    st.title("🔢 Calculadora")
    st.text_input("Resultado:", value=st.session_state.calc_val, disabled=True)
    
    # Botones en filas de 3 o 4
    grid = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '
 
