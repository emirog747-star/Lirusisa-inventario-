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
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {"historial": []}
    return {"historial": []}

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

with st.sidebar:
    st.title("🔢 Calculadora")
    n1 = st.number_input("Valor A", value=0.0)
    n2 = st.number_input("Valor B", value=0.0)
    operacion = st.radio("Operación", ["Suma", "Resta", "Multi", "Divi"])
    if st.button("Calcular"):
        if operacion == "Suma": st.success(f"Res: {n1+n2}")
        if operacion == "Resta": st.success(f"Res: {n1-n2}")
        if operacion == "Multi": st.success(f"Res: {n1*n2}")
        if operacion == "Divi": st.success(f"Res: {n1/n2 if n2 != 0 else 'Error'}")

st.title("🍕 Bitácora")

taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}

def seccion_peso(nombre, lb_caja, lb_bolsa, lb_cambro=None):
    with st.expander(f"📦 {nombre}", expanded=False):
        c = st.number_input(f"Cajas ({lb_caja} lb)", min_value=0, key=f"{nombre}_c")
        b = st.number_input(f"Bolsas ({lb_bolsa} lb)", min_value=0, key=f"{nombre}_b")
        total = (c * lb_caja) + (b * lb_bolsa)
        if lb_cambro:
            cam = st.number_input(f"Cambros Llenos ({lb_cambro} lb)", min_value=0, key=f"{nombre}_cam")
            total += (cam * lb_cambro)
        st.write("---")
        st.write("⚖️ Pesaje de Sobras")
        peso_bascula = st.number_input("Peso en Báscula", value=0.0, step=0.1, key=f"{nombre}_sobra")
        tipo_tara = st.selectbox("Tipo de Cambro usado", list(taras.keys()), key=f"{nombre}_tara")
        peso_neto_sobra = max(0.0, peso_bascula - taras[tipo_tara]) if peso_bascula > 0 else 0
        total_final = total + peso_neto_sobra
        st.error(f"Total {nombre}: {total_final:.2f} lbs")
        return total_final

tab_inv, tab_cajas, tab_masas, tab_hist = st.tabs(["🥩 Carnes/Queso", "📦 Empaques/Dips", "🥖 Masas", "📜 Historial"])

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
    
    st.subheader("Cajas 14''")
    col1, col2 = st.columns(2)
    with col1: c14_p = st.number_input("Paquetes 14'' (50 u)", min_value=0, key="c14_p")
    with col2: c14_u = st.number_input("Unidades sueltas 14''", key="c14_u")
    t_c14 = (c14_p * 50) + c14_u
    st.info(f"Total Cajas 14'': {t_c14}")
    
    st.write("---")
    st.subheader("Cajas Deep Dish")
    col3, col4 = st.columns(2)
    with col3: cd_p = st.number_input("Paquetes Deep Dish (50 u)", min_value=0, key="cd_p")
    with col4: cd_u = st.number_input("Unidades sueltas Deep Dish", key="cd_u")
    t_c_deep = (cd_p * 50) + cd_u
    st.info(f"Total Deep Dish: {t_c_deep}")

    st.write("---")
    st.subheader("Cajas Crazy Puff")
    col5, col6 = st.columns(2)
    with col5: cp_p = st.number_input("Paquetes Crazy Puff (100 u)", min_value=0, key="cp_p")
    with col6: cp_u = st.number_input("Unidades sueltas Crazy Puff", key="cp_u")
    t_c_puff = (cp_p * 100) + cp_u
    st.info(f"Total Crazy Puff: {t_c_puff}")

    st.write("---")
    st.subheader("Cajas Pan Italiano")
    col7, col8 = st.columns(2)
    with col7: ci_p = st.number_input("Paquetes Pan Italiano (100 u)", min_value=0, key="ci_p")
    with col8: ci_u = st.number_input("Unidades sueltas Pan Italiano", key="ci_u")
    t_c_ital = (ci_p * 100) + ci_u
    st.info(f"Total Pan Italiano: {t_c_ital}")
    
    st.write("---")
    st.subheader("Dips")
    d_c = st.number_input("Dips (Cajas de 189)", min_value=0, key="dc")
    d_s = st.number_input("Dips (Unidades sueltas)", key="ds")
    t_dips = (d_c * 189) + d_s
    st.info(f"Total Dips: {t_dips}")

with tab_masas:
    st.header("Cálculo de Harina")
    b18 = st.number_input("Bolitas de 18 oz", min_value=0)
    b10 = st.number_input("Bolitas de 10 oz", min_value=0)
    costales = (b18 / 38) + (b10 / 59)
    st.success(f"Equivalente a: {costales:.2f} costales de harina")

with tab_hist:
    resumen_dict = {
        "Harina (Costales)": f"{costales:.2f}",
        "Cajas 14''": t_c14,
        "Cajas Deep Dish": t_c_deep,
        "Cajas Crazy Puff": t_c_puff,
        "Cajas Pan Italiano": t_c_ital,
        "Dips Totales": t_dips,
        "Queso Pizza (lbs)": f"{t_queso:.2f}",
        "Peperoni (lbs)": f"{t_pepe:.2f}",
        "Jamon (lbs)": f"{t_jamon:.2f}",
        "Tocino (lbs)": f"{t_tocino:.2f}",
        "Salchicha Ital. (lbs)": f"{t_salchicha:.2f}",
        "Piña (lbs)": f"{t_pina:.2f}"
    }

    c_save, c_pdf = st.columns(2)
    with c_save:
        if st.button("💾 GUARDAR EN HISTORIAL"):
            resumen = {"fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "datos": resumen_dict}
            db["historial"].append(resumen)
            save_data(db)
            st.balloons()
    
    with c_pdf:
        try:
            pdf_data = generar_pdf(resumen_dict)
            st.download_button(label="📄 DESCARGAR PDF", data=pdf_data, file_name=f"inventario_{datetime.now().strftime('%d%m%Y')}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error: {e}")

    st.write("### Historial")
    for i, h in enumerate(reversed(db["historial"])):
        colh1, colh2 = st.columns([4, 1])
        fecha_h = h.get('fecha', 'Sin fecha')
        datos_h = h.get('datos', {})
        harina_h = datos_h.get('Harina (Costales)', '0.00')
        colh1.write(f"📅 {fecha_h} - Harina: {harina_h}")
        if colh2.button("🗑️", key=f"del_{i}"):
            db["historial"].pop(-(i+1))
            save_data(db)
            st.rerun()
