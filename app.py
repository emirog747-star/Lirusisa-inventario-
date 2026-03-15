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

    st.write("---")
    st.title("📝 Notas")
    nota_t = st.text_area("Apuntes:", value=db.get("notas", ""), height=150)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nota_t
        save_data(db)
        st.toast("Guardado")

# --- LÓGICA DE INVENTARIO (IGUAL QUE ANTES) ---
def generar_pdf(datos_reporte):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Reporte de Inventario - Bitacora", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    for concepto, valor in datos_reporte.items():
        pdf.cell(95, 10, f" {concepto}", border=1)
        pdf.cell(95, 10, f" {valor}", border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

st.title("🍕 Bitácora")
taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}

def sec_peso(nombre, lb_c, lb_b, lb_cam=None):
    with st.expander(f"📦 {nombre}", expanded=False):
        c = st.number_input(f"Cajas ({lb_c} lb)", min_value=0, step=1, key=f"{nombre}_c")
        b = st.number_input(f"Bolsas ({lb_b} lb)", min_value=0, step=1, key=f"{nombre}_b")
        total = (c * lb_c) + (b * lb_b)
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

with t2:
    def sec_u(n, u, k):
        st.subheader(n)
        c1, c2 = st.columns(2)
        p = c1.number_input("Paq", min_value=0, step=1, key=k+"p")
        s = c2.number_input("Sue", step=1, key=k+"s")
        st.success(f"Total {n}: {(p*u)+s}")
        return (p*u)+s
    v_c14 = sec_u("Cajas 14''", 50, "c14")
    v_cd = sec_u("Deep Dish", 50, "cd")
    v_cp = sec_u("Crazy Puff", 100, "cp")
    v_ci = sec_u("Pan Italiano", 100, "ci")
    v_pl = sec_u("Pan Loco", 50, "pl")
    v_dips = sec_u("Dips", 189, "dips")

with t3:
    v_r6 = sec_u("600ml", 12, "r6")
    v_r15 = sec_u("1.5L", 12, "r15")
    v_r2 = sec_u("2L", 8, "r2")
    v_a = sec_u("Agua", 12, "agua")

with t4:
    hc = st.number_input("Costales", min_value=0, step=1)
    h18 = st.number_input("Bol 18 oz", min_value=0, step=1)
    h10 = st.number_input("Bol 10 oz", min_value=0, step=1)
    v_h = hc + (h18/38) + (h10/59)
    st.success(f"Total: {v_h:.2f}")

with t5:
    res = {"Harina": f"{v_h:.2f}", "Cajas 14": v_c14, "Queso": f"{v_que:.2f}", "Piña": f"{v_pin:.2f}"}
    if st.button("💾 GUARDAR"):
        db["historial"].append({"fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "datos": res})
        save_data(db)
        st.balloons()
    st.download_button("📄 PDF", generar_pdf(res), "inv.pdf")
    for h in reversed(db.get("historial", [])):
        st.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")
