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
    pdf.cell(190, 10, "Reporte de Inventario", ln=True, align="C")
    pdf.ln(10)
    for k, v in datos_reporte.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(90, 10, f" {k}", border=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(100, 10, f" {v}", border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

st.title("🍕 Bitácora")

t1, t2, t3, t4, t5 = st.tabs(["🥩 Proteínas", "📦 Empaques", "🥤 Bebidas", "🥖 Masas", "📜 Historial"])

with t1:
    taras = {"Ninguno": 0.0, "Cambro Queso": 2.5, "Cambro Peperoni": 1.5, "Cambro Jamón": 1.0, "Cambro Mantequilla": 0.5}
    def seccion_peso(nombre, lb_caja, lb_bolsa, lb_cambro=None):
        with st.expander(f"📦 {nombre}"):
            c = st.number_input(f"Cajas", 0, step=1, key=nombre+"_c")
            b = st.number_input(f"Bolsas", 0, step=1, key=nombre+"_b")
            total = (c * lb_caja) + (b * lb_bolsa)
            if lb_cambro:
                cam = st.number_input(f"Cambros", 0, step=1, key=nombre+"_cam")
                total += (cam * lb_cambro)
            st.write("---")
            pb = st.number_input("Báscula", 0.0, step=0.1, key=nombre+"_s")
            tt = st.selectbox("Tara", list(taras.keys()), key=nombre+"_t")
            neto = max(0.0, pb - taras[tt]) if pb > 0 else 0
            final = total + neto
            st.success(f"Total {nombre}: {final:.2f} lbs")
            return final
    v_tocino = seccion_peso("Tocino", 19.8, 2.2, 4.4)
    v_jamon = seccion_peso("Jamón", 17.6, 2.2, 4.4)
    v_pepe = seccion_peso("Peperoni", 25.0, 12.5, 6.25)
    v_queso = seccion_peso("Queso Pizza", 20.0, 20.0, 20.0)

with t2:
    def seccion_unidades(nombre, u_por_paq, clave):
        st.subheader(nombre)
        col1, col2 = st.columns(2)
        p = col1.number_input("Paquetes", 0, step=1, key=clave+"p")
        s = col2.number_input("Sueltas", 0, step=1, key=clave+"s")
        total = (p * u_por_paq) + s
        st.success(f"Total {nombre}: {total}")
        return total
    v_c14 = seccion_unidades("Cajas 14''", 50, "c14")
    v_cd = seccion_unidades("Deep Dish", 50, "cd")
    v_cp = seccion_unidades("Crazy Puff", 100, "cp")
    v_pl = seccion_unidades("Pan Loco", 50, "pl")
    v_dips = seccion_unidades("Dips", 189, "dips")

with t3:
    st.header("Refrescos y Agua")
    v_r600 = seccion_unidades("600ml", 12, "r600")
    v_r15 = seccion_unidades("1.5L", 12, "r15")
    v_r2l = seccion_unidades("2L", 8, "r2l")
    v_agua = seccion_unidades("Agua", 12, "agua")

with t4:
    st.header("Harina")
    hc = st.number_input("Costales", 0, step=1, key="hcost")
    h18 = st.number_input("Bolitas 18oz", 0, step=1, key="h18oz")
    h10 = st.number_input("Bolitas 10oz", 0, step=1, key="h10oz")
    v_h = hc + (h18/38) + (h10/59)
    st.success(f"Total: {v_h:.2f} costales")

with t5:
    res = {
        "Harina": f"{v_h:.2f}", "Cajas 14": v_c14, "Deep": v_cd, "600ml": v_r600, 
        "1.5L": v_r15, "2L": v_r2l, "Agua": v_agua, "Queso": f"{v_queso:.2f}",
        "Peperoni": f"{v_pepe:.2f}", "Jamon": f"{v_jamon:.2f}", "Tocino": f"{v_tocino:.2f}"
    }
    if st.button("💾 GUARDAR"):
        db["historial"].append({"fecha": datetime.now().strftime("%d/%m %H:%M"), "datos": res})
        save_data(db)
        st.balloons()
    try:
        st.download_button("📄 PDF", generar_pdf(res), "inventario.pdf")
    except: st.error("Error PDF")
    for h in reversed(db.get("historial", [])):
        st.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")
