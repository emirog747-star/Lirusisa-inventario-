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
                if "historial" not in data: data["historial"] = []
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

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔢 Calculadora")
    op_in = st.text_input("Operación:", placeholder="0", key="calc_input")
    if st.button("="):
        try:
            res_calc = eval(op_in.replace('x', '*').replace('X', '*'))
            st.success(f"Res: {res_calc}")
        except: st.error("Error")
    
    st.write("---")
    st.title("📝 Notas")
    nota_t = st.text_area("Apuntes:", value=db.get("notas", ""), height=200)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nota_t
        save_data(db)
        st.toast("Guardado")

st.title("🍕 Bitácora")

taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}

def sec_peso(nombre, lb_c, lb_b, lb_cam=None):
    with st.expander(f"📦 {nombre}", expanded=False):
        # Campos de Cajas y Cambros solo si se proporcionan valores (Boneless no los usa)
        total = 0.0
        if lb_c > 0:
            c = st.number_input(f"Cajas ({lb_c} lb)", min_value=0, step=1, key=f"{nombre}_c")
            total += (c * lb_c)
        
        b = st.number_input(f"Bolsas ({lb_b} lb)", min_value=0, step=1, key=f"{nombre}_b")
        total += (b * lb_b)
        
        if lb_cam:
            cam = st.number_input(f"Cambros ({lb_cam} lb)", min_value=0, step=1, key=f"{nombre}_cam")
            total += (cam * lb_cam)
            
        st.write("---")
        p_bas = st.number_input("Peso Báscula", value=0.0, step=0.1, key=f"{nombre}_s")
        t_tara = st.selectbox("Tipo de Cambro", list(taras.keys()), key=f"{nombre}_t")
        p_neto = max(0.0, p_bas - taras[t_tara]) if p_bas > 0 else 0
        tot_f = total + p_neto
        st.success(f"Total {nombre}: {tot_f:.2f} lbs")
        return tot_f

t1, t2, t3, t4, t5 = st.tabs(["🥩 Proteínas", "📦 Empaques", "🥤 Bebidas", "🥖 Masas", "📜 Historial"])

with t1:
    v_toc = sec_peso("Tocino", 19.8, 2.2, 4.4)
    v_jam = sec_peso("Jamón", 17.6, 2.2, 4.4)
    v_pep = sec_peso("Peperoni", 25.0, 12.5, 6.25)
    v_que = sec_peso("Queso Pizza", 20.0, 20.0, 20.0)
    v_sal = sec_peso("Salchicha", 20.0, 5.0, 5.0)
    v_bar = sec_peso("Barra Queso", 20.0, 5.0)
    v_pin = sec_peso("Piña", 26.8, 6.7, 6.7)
    # Agregado Boneless: Sin cajas (0), Bolsa 4.4 lb, Sin cambros (None)
    v_bon = sec_peso("Boneless", 0, 4.4, None) 

with t2:
    st.header("Cajas y Dips")
    
    st.subheader("Cajas 14''")
    c1, c2 = st.columns(2)
    with c1: c14p = st.number_input("Paq 14'' (50u)", min_value=0, step=1, key="c14p")
    with c2: c14u = st.number_input("Sueltas 14''", min_value=0, step=1, key="c14u")
    v_c14 = (c14p * 50) + c14u
    st.success(f"Total 14'': {v_c14}")

    st.subheader("Cajas Deep Dish")
    c3, c4 = st.columns(2)
    with c3: cdp = st.number_input("Paq Deep (50u)", min_value=0, step=1, key="cdp")
    with c4: cdu = st.number_input("Sueltas Deep", min_value=0, step=1, key="cdu")
    v_cd = (cdp * 50) + cdu
    st.success(f"Total Deep: {v_cd}")

    # ... (Resto del código de empaques, bebidas y masas se mantiene igual)

# NOTA: Asegúrate de completar las secciones de bebidas y masas si vas a reemplazar todo el archivo.
