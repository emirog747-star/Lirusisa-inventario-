import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from fpdf import FPDF

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Bitácora", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; border-radius: 10px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL ---
ARCHIVO_DB = "bitacora_data.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, "r") as f: 
                d = json.load(f)
                if "historial" not in d: d["historial"] = []
                return d
        except: return {"historial": []}
    return {"historial": []}

def guardar_datos(datos):
    with open(ARCHIVO_DB, "w") as f: json.dump(datos, f, indent=4)

db = cargar_datos()

def crear_pdf(inventario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Reporte de Inventario - Little Caesars", ln=1, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    for concepto, valor in inventario.items():
        pdf.cell(90, 10, f" {concepto}", 1)
        pdf.cell(100, 10, f" {valor}", 1, ln=1)
    return pdf.output(dest='S').encode('latin-1')

# --- DISEÑO DE LA APP ---
st.title("🍕 Bitácora")

tabs = st.tabs(["🥩 Proteínas", "📦 Empaques", "🥤 Bebidas", "🥖 Masas", "📜 Historial"])

# SECCIÓN 1: PROTEÍNAS
with tabs[0]:
    taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}
    def bloque_peso(nombre, lb_caja, lb_bolsa, lb_cambro=None):
        with st.expander(f"📦 {nombre}"):
            col
