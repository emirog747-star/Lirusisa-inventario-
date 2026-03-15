import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from fpdf import FPDF

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Bitácora", layout="wide")
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; border-radius: 10px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "bitacora_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: 
                d = json.load(f)
                if "historial" not in d: d["historial"] = []
                return d
        except: return {"historial": []}
    return {"historial": []}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()

def generar_pdf(res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Reporte de Inventario", ln=1, align="C")
    pdf.ln(5)
    for k, v in res.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(90, 10, f" {k}", 1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(100,
