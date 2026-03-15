import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", layout="wide")

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

st.title("🍕 Bitácora de Hamlet y Ofelia")

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
    c14_p = st.number_input("Paquetes Cajas 14'' (50 u)", min_value=0)
    c14_a = st.number_input("Ajuste manual 14'' +/-", value=0)
    t_c14 = (c14_p * 50) + c14_a
    st.info(f"Total Cajas 14'': {t_c14}")
    
    st.write("---")
    d_c = st.number_input("Dips (Cajas de 189)", min_value=0)
    d_s = st.number_input("Dips (Unidades sueltas)", min_value=0)
    t_dips = (d_c * 189) + d_s
    st.info(f"Total Dips: {t_dips}")

with tab_masas:
    st.header("Cálculo de Harina")
    b18 = st.number_input("Bolitas de 18 oz", min_value=0)
    b10 = st.number_input("Bolitas de 10 oz", min_value=0)
    costales = (b18 / 38) + (b10 / 59)
    st.success(f"Equivalente a: {costales:.2f} costales de harina")

with tab_hist:
    if st.button("💾 FINALIZAR Y GUARDAR"):
        resumen = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "datos": {"Harina": round(costales, 2), "Cajas14": t_c14}
        }
        db["historial"].append(resumen)
        save_data(db)
        st.balloons()

    st.write("### Historial")
    for i, h in enumerate(reversed(db["historial"])):
        col1, col2 = st.columns([4, 1])
        col1.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")
        if col2.button("🗑️", key=f"del_{i}"):
            db["historial"].pop(-(i+1))
            save_data(db)
            st.rerun()
