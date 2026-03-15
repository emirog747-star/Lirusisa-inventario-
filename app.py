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
    st.header("Cajas y Dips")
    
    st.subheader("Cajas 14''")
    c1, c2 = st.columns(2)
    with c1: c14p = st.number_input("Paq 14'' (50u)", min_value=0, step=1, key="c14p")
    with c2: c14u = st.number_input("Sueltas 14''", step=1, key="c14u")
    v_c14 = (c14p * 50) + c14u
    st.success(f"Total 14'': {v_c14}")

    st.subheader("Cajas Deep Dish")
    c3, c4 = st.columns(2)
    with c3: cdp = st.number_input("Paq Deep (50u)", min_value=0, step=1, key="cdp")
    with c4: cdu = st.number_input("Sueltas Deep", step=1, key="cdu")
    v_cd = (cdp * 50) + cdu
    st.success(f"Total Deep: {v_cd}")

    st.subheader("Cajas Crazy Puff")
    c5, c6 = st.columns(2)
    with c5: cpp = st.number_input("Paq Puff (100u)", min_value=0, step=1, key="cpp")
    with c6: cpu = st.number_input("Sueltas Puff", step=1, key="cpu")
    v_cp = (cpp * 100) + cpu
    st.success(f"Total Puff: {v_cp}")

    st.subheader("Pan Italiano")
    c7, c8 = st.columns(2)
    with c7: cip = st.number_input("Paq Ital (100u)", min_value=0, step=1, key="cip")
    with c8: ciu = st.number_input("Sueltas Ital", step=1, key="ciu")
    v_ci = (cip * 100) + ciu
    st.success(f"Total Ital: {v_ci}")

    st.subheader("Bolsas Pan Loco")
    c9, c10 = st.columns(2)
    with c9: plp = st.number_input("Paq Pan Loco (50u)", min_value=0, step=1, key="plp")
    with c10: plu = st.number_input("Sueltas Pan Loco", step=1, key="plu")
    v_pl = (plp * 50) + plu
    st.success(f"Total Pan Loco: {v_pl}")

    st.subheader("Dips")
    c11, c12 = st.columns(2)
    with c11: dp = st.number_input("Cajas Dips (189u)", min_value=0, step=1, key="dcp")
    with c12: du = st.number_input("Sueltas Dips", step=1, key="dcu")
    v_dips = (dp * 189) + du
    st.success(f"Total Dips: {v_dips}")

with t3:
    st.header("Bebidas")
    st.subheader("600ml")
    b1, b2 = st.columns(2)
    with b1: r6p = st.number_input("Paq 600ml (12u)", min_value=0, key="r6p")
    with b2: r6u = st.number_input("Sueltas 600ml", key="r6u")
    v_r6 = (r6p * 12) + r6u
    st.success(f"Total 600ml: {v_r6}")

    st.subheader("1.5L")
    b3, b4 = st.columns(2)
    with b3: r15p = st.number_input("Paq 1.5L (12u)", min_value=0, key="r15p")
    with b4: r15u = st.number_input("Sueltas 1.5L", key="r15u")
    v_r15 = (r15p * 12) + r15u
    st.success(f"Total 1.5L: {v_r15}")

    st.subheader("2L")
    b5, b6 = st.columns(2)
    with b5: r2p = st.number_input("Paq 2L (8u)", min_value=0, key="r2p")
    with b6: r2u = st.number_input("Sueltas 2L", key="r2u")
    v_r2 = (r2p * 8) + r2u
    st.success(f"Total 2L: {v_r2}")

    st.subheader("Agua 600ml")
    b7, b8 = st.columns(2)
    with b7: ap = st.number_input("Paq Agua (12u)", min_value=0, key="ap")
    with b8: au = st.number_input("Sueltas Agua", key="au")
    v_a = (ap * 12) + au
    st.success(f"Total Agua: {v_a}")

with t4:
    st.header("Harina")
    hc = st.number_input("Costales", min_value=0, step=1, key="hc")
    h18 = st.number_input("Bol 18 oz", min_value=0, step=1, key="h18")
    h10 = st.number_input("Bol 10 oz", min_value=0, step=1, key="h10")
    v_h = hc + (h18/38) + (h10/59)
    st.success(f"Total: {v_h:.2f} costales")

with t5:
    res = {
        "Harina": f"{v_h:.2f}", "Cajas 14": v_c14, "Deep": v_cd, "Puff": v_cp, "Ital": v_ci,
        "Pan Loco": v_pl, "Dips": v_dips, "600ml": v_r6, "1.5L": v_r15, "2L": v_r2, "Agua": v_a,
        "Queso": f"{v_que:.2f}", "Pepe": f"{v_pep:.2f}", "Jamon": f"{v_jam:.2f}", 
        "Tocino": f"{v_toc:.2f}", "Salchicha": f"{v_sal:.2f}", "Piña": f"{v_pin:.2f}"
    }
    if st.button("💾 GUARDAR"):
        db["historial"].append({"fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "datos": res})
        save_data(db)
        st.balloons()
    try:
        p_f = generar_pdf(res)
        st.download_button("📄 PDF", data=p_f, file_name="inventario.pdf", mime="application/pdf")
    except: st.error("Error PDF")
    for h in reversed(db.get("historial", [])):
        st.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")

 
