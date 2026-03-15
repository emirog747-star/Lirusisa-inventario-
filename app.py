import streamlit as st
import pandas as pd
from datetime import datetime
import json, os
from fpdf import FPDF

st.set_page_config(page_title="Bitácora", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3em; font-weight: bold; border-radius: 8px; }
    .stNumberInput>div>div>input { font-size: 20px; }
    [data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
DB_F = "bitacora_data.json"
def load():
    if os.path.exists(DB_F):
        try:
            with open(DB_F, "r") as f: return json.load(f)
        except: pass
    return {"historial": [], "notas": ""}

db = load()

# --- CALCULADORA (SIDEBAR) ---
if "cv" not in st.session_state: st.session_state.cv = ""

def calc(v):
    if v == "=":
        try: st.session_state.cv = str(eval(st.session_state.cv.replace('x', '*')))
        except: st.session_state.cv = "Error"
    elif v == "C": st.session_state.cv = ""
    else: st.session_state.cv += str(v)

with st.sidebar:
    st.title("🔢 Calculadora")
    st.text_input("Res:", value=st.session_state.cv, disabled=True)
    grid = [['7','8','9','/'], ['4','5','6','x'], ['1','2','3','-'], ['0','.','C','+']]
    for row in grid:
        cols = st.columns(4)
        for i, b in enumerate(row):
            if cols[i].button(b): calc(b)
    if st.button("="): calc("=")
    
    st.write("---")
    nt = st.text_area("Notas:", value=db.get("notas", ""), height=150)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nt
        with open(DB_F, "w") as f: json.dump(db, f)
        st.toast("Nota guardada")

# --- APP PRINCIPAL ---
st.title("🍕 Bitácora")
t1, t2, t3, t4, t5 = st.tabs(["🥩 Prot", "📦 Emp", "🥤 Beb", "🥖 Masas", "📜 Hist"])

def s_peso(n, lc, lb, lcam=None):
    with st.expander(f"📦 {n}"):
        c1, c2 = st.columns(2)
        c = c1.number_input(f"Caj({lc})", 0, step=1, key=n+"c")
        b = c2.number_input(f"Bol({lb})", 0, step=1, key=n+"b")
        tot = (c*lc) + (b*lb)
        if lcam:
            cm = st.number_input(f"Cam({lcam})", 0, step=1, key=n+"m")
            tot += (cm*lcam)
        pb = st.number_input("Báscula", 0.0, step=0.1, key=n+"s")
        tr = st.selectbox("Tara", [0.0, 2.5, 1.5, 1.0, 0.5], key=n+"t")
        res = tot + max(0.0, pb - tr)
        st.success(f"Total {n}: {res:.2f}")
        return res

with t1:
    v_toc = s_peso("Tocino", 19.8, 2.2, 4.4)
    v_jam = s_peso("Jamón", 17.6, 2.2, 4.4)
    v_pep = s_peso("Peperoni", 25.0, 12.5, 6.25)
    v_que = s_peso("Queso Pizza", 20.0, 20.0, 20.0)
    v_bar = s_peso("Barra Queso", 20.0, 5.0)
    v_pin = s_peso("Piña", 26.8, 6.7, 6.7)

with t2:
    def s_u(n, u, k):
        st.subheader(n)
        c1, c2 = st.columns(2)
        p = c1.number_input("Paq", 0, step=1, key=k+"p")
        s = c2.number_input("Sue", 0, step=1, key=k+"s")
        st.info(f"Total: {(p*u)+s}")
        return (p*u)+s
    v_c14 = s_u("Cajas 14", 50, "c14")
    v_dip = s_u("Dips", 189, "dp")

with t3:
    v_r6 = s_u("600ml", 12, "r6")
    v_r15 = s_u("1.5L", 12, "r15")
    v_agua = s_u("Agua", 12, "ag")

with t4:
    hc = st.number_input("Costales", 0, step=1)
    h18 = st.number_input("Bol 18oz", 0, step=1)
    v_h = hc + (h18/38)
    st.success(f"Total Harina: {v_h:.2f}")

with t5:
    res = {"Harina": f"{v_h:.2f}", "Queso": f"{v_que:.2f}", "Piña": f"{v_pin:.2f}"}
    if st.button("💾 GUARDAR"):
        db["historial"].append({"fecha": datetime.now().strftime("%d/%m %H:%M"), "datos": res})
        with open(DB_F, "w") as f: json.dump(db, f)
        st.balloons()
    for h in reversed(db["historial"]):
        st.write(f"📅 {h['fecha']} - Harina: {h['datos']['Harina']}")
