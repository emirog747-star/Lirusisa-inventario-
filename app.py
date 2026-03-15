import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from fpdf import FPDF

# --- SEGURIDAD ---
def validar_acceso():
    if "autenticado" not in st.session_state:
        st.title("🔒 Acceso Restringido")
        clave = st.text_input("Introduce la contraseña:", type="password")
        if st.button("Entrar"):
            if clave == "patricioquemado123":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return False
    return True

if validar_acceso():
    # --- CONFIGURACIÓN ---
    st.set_page_config(page_title="Bitácora", layout="wide")

    # CSS para botones y forzar cuadrícula en móvil
    st.markdown("""
        <style>
        [data-testid="column"] { width: 23% !important; flex: 1 1 23% !important; min-width: 23% !important; }
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

    # --- CALCULADORA ---
    if "cv" not in st.session_state: st.session_state.cv = ""

    def click_calc(v):
        if v == "=":
            try: st.session_state.cv = str(eval(st.session_state.cv.replace('x', '*')))
            except: st.session_state.cv = "Error"
        elif v == "C": st.session_state.cv = ""
        else: st.session_state.cv += str(v)

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🔢 Calculadora")
        st.text_input("Res:", value=st.session_state.cv, disabled=True)
        btns = ['7','8','9','/', '4','5','6','x', '1','2','3','-', '0','.','C','+']
        for i in range(0, len(btns), 4):
            cols = st.columns(4)
            for j in range(4):
                val = btns[i+j]
                if cols[j].button(val, key=f"sb_{i+j}"): click_calc(val)
        if st.button("ENTER (=)"): click_calc("=")
        
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
            c = st.number_input(f"Cajas ({lb_c} lb)", 0, step=1, key=f"{nombre}_c")
            b = st.number_input(f"Bolsas ({lb_b} lb)", 0, step=1, key=f"{nombre}_b")
            total = (c * lb_c) + (b * lb_b)
            if lb_cam:
                cam = st.number_input(f"Cambros ({lb_cam} lb)", 0, step=1, key=f"{nombre}_cam")
                total += (cam * lb_cam)
            st.write("---")
            p_bas = st.number_input("Peso Báscula", 0.0, step=0.1, key=f"{nombre}_s")
            t_tara = st.selectbox("Tipo de Cambro", list(taras.keys()), key=f"{nombre}_t")
            p_neto = max(0.0, p_bas - taras[t_tara]) if p_bas > 0 else 0
            tot_f = total + p_neto
            st.success(f"Total {nombre}: {tot_f:.2f} lbs")
            return tot_f

    t1, t2, t3, t4, t5 = st.tabs(["🥩 Proteínas
