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

# --- SIDEBAR: CALCULADORA Y NOTAS ---
with st.sidebar:
    st.title("🔢 Calculadora")
    operacion_input = st.text_input("Operación (ej: 10+5)", placeholder="0", key="calc_input")
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
    col1, col2 = st.columns(2)
    with col1: c14_p = st.number_input("Paquetes 14'' (50 u)", min_value=0, step=1, key="c14p")
    with col2: c14_u = st.number_input("Sueltas 14''", step=1, key="c14u")
    t_c14 = (c14_p * 50) + c14_u
    
    col3, col4 = st.columns(2)
    with col3: cd_p = st.number_input("Paquetes Deep (50 u)", min_value=0, step=1, key="cdp")
    with col4: cd_u = st.number_input("Sueltas Deep", step=1, key="cdu")
    t_c_deep = (cd_p * 50) + cd_u
    
    col5, col6 = st.columns(2)
    with col5: cp_p = st.number_input("Paquetes Puff (100 u)", min_value=0, step=1, key="cpp")
    with col6: cp_u = st.number_input("Sueltas Puff", step=1, key="cpu")
    t_c_puff = (cp_p * 100) + cp_u
    
    col7, col8 = st.columns(2)
    with col7: ci_p = st.number_input("Paquetes Ital (100 u)", min_value=0, step=1, key="cip")
    with col8: ci_u = st.number_input("Sueltas Ital", step=1, key="ciu")
    t_c_ital = (ci_p * 100) + ci_u
    
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1: pl_p = st.number_input("Paquetes Pan Loco (50 u)", min_value=0, step=1, key="plp")
    with col_pl2: pl_u = st.number_input("Sueltas Pan Loco", step=1, key="plu")
    t_pl = (pl_p * 50) + pl_u
    
    st.write("---")
    col9, col10 = st.columns(2)
    with col9: d_c = st.number_input("Dips (Caja 189)", min_value=0, step=1, key="dcj")
    with col10: d_s = st.number_input("Dips (Sueltos)", step=1, key="dsj")
    t_dips = (d_c * 189) + d_s

with tab_bev:
    st.header("Bebidas")
    colb1, colb2 = st.columns(2)
    with colb1: r600p = st.number_input("Paq 600ml (12u)", min_value=0, step=1, key="b600p")
    with colb2: r600u = st.number_input("Sueltas 600ml", step=1, key="b600u")
    t_r600 = (r600p * 12) + r600u

    colb3, colb4 = st.columns(2)
    with colb3: r15p = st.number_input("Paq 1.5L (12u)", min_value=0, step=1, key="b15p")
    with colb4: r15u = st.number_input("Sueltas 1.5L", step=1, key="b15u")
    t_r15 = (r15p * 12) + r15u

    colb5, colb6 = st.columns(2)
    with colb5: r2p = st.number_input("Paq 2L (8u)", min_value=0, step=1, key="b2p")
    with colb6: r2u = st.number_input("Sueltas 2L", step=1, key="b2u")
    t_r2 = (r2p * 8) + r2u

    colb7, colb8 = st.columns(2)
    with colb7: wp = st.number_input("Paq Agua (12u)", min_value=0, step=1, key="bwp")
    with colb8: wu = st.number_input("Sueltas Agua", step=1, key="bwu")
    t_water = (wp * 12) + wu

with tab_masas:
    st.header("Harina")
    h_c = st.number_input("Costales Cerrados", min_value=0, step=1, key="hcerr")
    h_18 = st.number_input("Bolitas 18 oz", min_value=0, step=1, key="h18oz")
    h_10 = st.number_input("Bolitas 10 oz", min_value=0, step=1, key="h10oz")
    total_h = h_c + (h_18 / 38) + (h_10 / 59)
    st.success(f"Total: {total_h:.2f} costales")

with tab_hist:
    res_dict = {
        "Harina": f"{total_h:.2f}", "Cajas 14": t_c14, "Deep": t_c_deep, "Puff": t_c_puff,
        "Ital": t_c_ital, "Pan Loco": t_pl, "Dips": t_dips, "Ref 600": t_r600,
        "Ref 1.5": t_r15, "Ref 2L": t_r2, "Agua": t_water, "Queso": f"{t_queso:.2f}",
        "Pepe": f"{t_pepe:.2f}", "Jamon": f"{t_jamon:.2f}", "Tocino": f"{t_tocino:.2f}",
        "Salchicha": f"{t_salchicha:.2f}", "Piña": f"{t_pina:.2f}"
    }
    
    c_s, c_p = st.columns(2)
    with c_s:
        if st.button("💾 GUARDAR"):
            db["historial"].append({"fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "datos": res_dict})
            save_data(db)
            st.balloons()
    with c_p:
        try:
            p_data = generar_pdf(res_dict)
            st.download_button("📄 PDF", data=p_data, file_name="inventario.pdf", mime="application/pdf")
        except Exception as e: st.error(f"Error PDF: {e}")

    for i, h in enumerate(reversed(db.get("historial", []))):
        st.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")
