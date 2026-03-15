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
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "bitacora_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: 
                data = json.load(f)
                if "notas" not in data: data["notas"] = ""
                return data
        except: return {"historial": [], "notas": ""}
    return {"historial": [], "notas": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()

def generar_pdf(datos_reporte):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Reporte de Inventario - Bitacora", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(95, 10, " Concepto", border=1, fill=True)
    pdf.cell(95, 10, " Cantidad", border=1, fill=True)
    pdf.ln()
    
    for concepto, valor in datos_reporte.items():
        pdf.cell(95, 10, f" {concepto}", border=1)
        pdf.cell(95, 10, f" {valor}", border=1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR: CALCULADORA Y NOTAS ---
with st.sidebar:
    st.title("🔢 Calculadora")
    operacion_input = st.text_input("Operación (ej: 10+5)", placeholder="0")
    if st.button("="):
        try:
            calc_ready = operacion_input.replace('x', '*').replace('X', '*')
            resultado = eval(calc_ready)
            st.success(f"Res: {resultado}")
        except: st.error("Error")
    
    st.write("---")
    st.title("📝 Notas")
    nota_temp = st.text_area("Apuntes del turno:", value=db.get("notas", ""), height=200)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nota_temp
        save_data(db)
        st.toast("Notas guardadas")

st.title("🍕 Bitácora")

taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}

def seccion_peso(nombre, lb_caja, lb_bolsa, lb_cambro=None):
    with st.expander(f"📦 {nombre}", expanded=False):
        c = st.number_input(f"Cajas ({lb_caja} lb)", min_value=0, step=1, key=f"{nombre}_c")
        b = st.number_input(f"Bolsas ({lb_bolsa} lb)", min_value=0, step=1, key=f"{nombre}_b")
        total = (c * lb_caja) + (b * lb_bolsa)
        if lb_cambro:
            cam = st.number_input(f"Cambros Llenos ({lb_cambro} lb)", min_value=0, step=1, key=f"{nombre}_cam")
            total += (cam * lb_cambro)
        st.write("---")
        st.write("⚖️ Pesaje de Sobras")
        peso_bascula = st.number_input("Peso en Báscula", value=0.0, step=0.1, key=f"{nombre}_sobra")
        tipo_tara = st.selectbox("Tipo de Cambro usado", list(taras.keys()), key=f"{nombre}_tara")
        peso_neto_sobra = max(0.0, peso_bascula - taras[tipo_tara]) if peso_bascula > 0 else 0
        total_final = total + peso_neto_sobra
        st.error(f"Total {nombre}: {total_final:.2f} lbs")
        return total_final

tab_inv, tab_cajas, tab_bev, tab_masas, tab_hist = st.tabs(["🥩 Carnes/Queso", "📦 Empaques", "🥤 Bebidas", "🥖 Masas", "📜 Historial"])

with tab_inv:
    t_tocino = seccion_peso("Tocino", 19.8, 2.2, 4.4)
    t_jamon = seccion_peso("Jamón", 17.6, 2.2, 4.4)
    t_pepe = seccion_peso("Peperoni", 25.0, 12.5, 6.25)
    t_queso = seccion_peso("Queso Pizza", 20.0, 20.0, 20.0)
    t_salchicha = seccion_peso("Salchicha Italiana", 20.0, 5.0, 5.0)
    t_barra = seccion_peso("Queso en Barra", 20.0, 5.0)
    t_pina = seccion_peso("Piña", 26.8, 6.7, 6.7)

with tab_cajas:
    st.header("Cajas y Dips")
    # Cajas 14''
    col1, col2 = st.columns(2)
    with col1: c14_p = st.number_input("Paquetes 14'' (50 u)", min_value=0, step=1, key="c14p")
    with col2: c14_u = st.number_input("Sueltas 14''", step=1, key="c14u")
    t_c14 = (c14_p * 50) + c14_u
    # Deep Dish
    col3, col4 = st.columns(2)
    with col3: cd_p = st.number_input("Paquetes Deep (50 u)", min_value=0, step=1, key="cdp")
    with col4: cd_u = st.number_input("Sueltas Deep", step=1, key="cdu")
    t_c_deep = (cd_p * 50) + cd_u
    # Crazy Puff
    col5, col6 = st.columns(2)
    with col5: cp_p = st.number_input("Paquetes Puff (100 u)", min_value=0, step=1, key
 
