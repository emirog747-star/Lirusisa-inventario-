import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from fpdf import FPDF

# --- CONFIG ---
st.set_page_config(page_title="Bitácora", layout="wide")
st.markdown("<style>.stButton>button { width: 100%; height: 3.5em; font-weight: bold; }.stNumberInput>div>div>input { font-size: 20px; }</style>", unsafe_allow_html=True)

DB_F = "bitacora_data.json"

def load_db():
    if os.path.exists(DB_F):
        try:
            with open(DB_F, "r") as f: 
                d = json.load(f)
                if "hist" not in d: d["hist"] = []
                return d
        except: return {"hist": []}
    return {"hist": []}

def save_db(d):
    with open(DB_F, "w") as f: json.dump(d, f, indent=4)

db = load_db()

def make_pdf(res):
    p = FPDF()
    p.add_page()
    p.set_font("Arial", "B", 14)
    p.cell(190, 10, "Inventario", ln=1, align="C")
    for k, v in res.items():
        p.set_font("Arial", "B", 11)
        p.cell(90, 8, f" {k}", 1)
        p.set_font("Arial", "", 11)
        p.cell(100, 8, f" {v}", 1, ln=1)
    return p.output(dest='S').encode('latin-1')

st.title("🍕 Bitácora")
t1, t2, t3, t4, t5 = st.tabs(["🥩 Prot", "📦 Emp", "🥤 Beb", "🥖 Mas", "📜 Hist"])

with t1:
    tr = {"N": 0.0, "Q": 2.5, "P": 1.5, "J": 1.0, "M": 0.5}
    def f_p(n, lc, lb, lca=None):
        with st.expander(f"📦 {n}"):
            c = st.number_input(f"Caj", 0, step=1, key=n+"c")
            b = st.number_input(f"Bol", 0, step=1, key=n+"b")
            tot = (c*lc)+(b*lb)
            if lca:
                ca = st.number_input(f"Cam", 0, step=1, key=n+"ca")
                tot += (ca*lca)
            st.write("---")
            pb = st.number_input("Basc", 0.0, step=0.1, key=n+"s")
            tt = st.selectbox("Tara", list(tr.keys()), key=n+"t")
            net = max(0.0, pb - tr[tt]) if pb > 0 else 0
            fin = tot + net
            st.success(f"Tot {n}: {fin:.2f}")
            return fin
    v_que = f_p("Queso", 20, 20, 20)
    v_pep = f_p("Pepe", 25, 12.5, 6.25)
    v_jam = f_p("Jamon", 17.6, 2.2, 4.4)
    v_toc = f_p("Tocin", 19.8, 2.2, 4.4)
    v_sal = f_p("Salch", 20, 5, 5)
    v_bar = f_p("Barra", 20, 5)
    v_pin = f_p("Piña", 26.8, 6.7, 6.7)

with t2:
    def f_u(n, u, k):
        st.subheader(n)
        col1, col2 = st.columns(2)
        p = col1.number_input("Paq", 0, step=1, key=k+"p")
        s = col2.number_input("Sue", 0, step=1, key=k+"s")
        t = (p*u)+s
        st.success(f"Total {n}: {t}")
        return t
    v_c14 = f_u("Caja 14", 50, "c14")
    v_cd = f_u("Deep", 50, "cd")
    v_cp = f_u("Puff", 100, "cp")
    v_pl = f_u("P.Loco", 50, "pl")
    v_di = f_u("Dips", 189, "di")

with t3:
    v_r6 = f_u("600ml", 12, "r6")
    v_r15 = f_u("1.5L", 12, "r15")
    v_r2 = f_u("2L", 8, "r2")
    v_ag = f_u("Agua", 12, "ag")

with t4:
    hc = st.number_input("Costal", 0, step=1)
    h18 = st.number_input("18oz", 0, step=1)
    h10 = st.number_input("10oz", 0, step=1)
    v_h = hc + (h18/38) + (h10/59)
    st.success(f"Total: {v_h:.2f}")

with t5:
    res = {"Masa": f"{v_h:.2f}", "C14": v_c14, "600ml": v_r6, "Queso": f"{v_que:.2f}", "Piña": f"{v_pin:.2f}"}
    if st.button("💾 GUARDAR"):
        db["hist"].append({"f": datetime.now().strftime("%d/%m %H:%M"), "d": res})
        save_db(db)
        st.balloons()
    st.download_button("📄 PDF", make_pdf(res), "inv.pdf")
    for h in reversed(db.get("hist", [])):
        st.write(f"📅 {h['f']} - Masa: {h['d']['Masa']}")
