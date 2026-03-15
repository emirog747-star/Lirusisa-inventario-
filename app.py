import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bitácora Hamlet y Ofelia", layout="wide")

# Estilos para que se vea bien en celular (Botones grandes)
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 18px; font-weight: bold; border-radius: 10px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
DATA_FILE = "bitacora_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"historial": []}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()

# --- CALCULADORA LATERAL ---
with st.sidebar:
    st.title("🔢 Calculadora")
    n1 = st.number_input("Valor A", value=0.0)
    n2 = st.number_input("Valor B", value=0.0)
    operacion = st.radio("Operación", ["Suma", "Resta", "Multi", "Divi"])
    if st.button("Calcular"):
        if operacion == "Suma": st.write(f"Res: {n1+n2}")
        if operacion == "Resta": st.write(f"Res: {n1-n2}")
        if operacion == "Multi": st.write(f"Res: {n1*n2}")
        if operacion == "Divi": st.write(f"Res: {n1/n2 if n2 != 0 else 'Error'}")

st.title("🍕 Bitácora de Hamlet y Ofelia")

# --- LÓGICA DE CÁLCULO ---
taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}

def seccion_peso(nombre, lb_caja, lb_bolsa, lb_cambro=None):
    st.subheader(nombre)
    c = st.number_input(f"Cajas ({lb_caja} lb)", min_value=0, key=f"{nombre}_c")
    b = st.number_input(f"Bolsas ({lb_bolsa} lb)", min_value=0, key=f"{nombre}_b")
    total = (c * lb_caja) + (b * lb_bolsa)
    
    if lb_cambro:
        cam = st.number_input(f"Cambros Llenos ({lb_cambro} lb)", min_value=0, key=f"{nombre}_cam")
        total += (cam * lb_cambro)
    
    # Sección de Sobras con resta de Cambro
    st.write("---")
    st.write("⚖️ Pesaje de Sobras")
    peso_bascula = st.number_input("Peso en Báscula", value=0.0, step=0.1, key=f"{nombre}_sobra")
    tipo_tara = st.selectbox("Tipo de Cambro usado", list(taras.keys()), key=f"{nombre}_tara")
    
    peso_neto_sobra = max(0.0, peso_bascula - taras[tipo_tara]) if peso_bascula > 0 else 0
    total_final = total + peso_neto_sobra
    st.warning(f"Total {nombre}: {total_final:.2f} lbs")
    return total_final

# --- PESTAÑAS ---
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
    def entrada_ajustable(nombre, base):
        paqs = st.number_input(f"Paquetes de {nombre} ({base} u)", min_value=0)
        ajuste = st.number_input(f"Ajuste manual +/- (Unidades sueltas)", value=0, key=f"adj_{nombre}")
        total = (paqs * base) + ajuste
        st.info(f"Total {nombre}: {total} unidades")
        return total

    t_c14 = entrada_ajustable("Cajas 14''", 50)
    t_deep = entrada_ajustable("Cajas Deep Dish", 50)
    t_puff = entrada_ajustable("Cajas Puff", 100)
    t_it_ch = entrada_ajustable("Italian Cheese", 100)
    
    st.write("---")
    d_cajas = st.number_input("Dips (Cajas de 189)", min_value=0)
    d_sueltos = st.number_input("Dips (Unidades sueltas)", min_value=0)
    total_dips = (d_cajas * 189) + d_sueltos
    st.info(f"Total Dips: {total_dips}")

with tab_masas:
    st.header("Cálculo de Harina")
    b18 = st.number_input("Bolitas de 18 oz", min_value=0)
    b10 = st.number_input("Bolitas de 10 oz", min_value=0)
    costales = (b18 / 38) + (b10 / 59)
    st.success(f"Equivalente a: {costales:.2f} costales de harina")
    costales_cerrados = st.number_input("Costales cerrados (Unidad)", min_value=0)

with tab_hist:
    if st.button("🗑️ BORRAR TODO (Reset)"):
        st.rerun()
    
    if st.button("💾 FINALIZAR Y GUARDAR"):
        resumen = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "datos": {"Jamón (lb)": t_jamon, "Harina (costales)": round(costales, 2), "Cajas 14": t_c14}
        }
        db["historial"].append(resumen)
        save_data(db)
        st.success("¡Inventario guardado!")

    st.write("### Historial de Inventarios")
    for i, h in enumerate(reversed(db["historial"])):
        col1, col2 = st.columns([4, 1])
        col1.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina (costales)']} cst")
        if col2.button("Eliminar", key=f"del_{i}"):
            db["historial"].pop(-(i+1))
            save_data(db)
            st.rerun()
