import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Bitácora", layout="wide")

# ESTE BLOQUE FUERZA LAS 4 COLUMNAS EN MÓVIL
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 23% !important;
        flex: 1 1 23% !important;
        min-width: 23% !important;
    }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

DB_F = "bitacora_data.json"
def load():
    if os.path.exists(DB_F):
        try:
            with open(DB_F, "r") as f: return json.load(f)
        except: pass
    return {"historial": [], "notas": ""}
db = load()

# --- CALCULADORA ---
if "cv" not in st.session_state: st.session_state.cv = ""

def calc(v):
    if v == "=":
        try: st.session_state.cv = str(eval(st.session_state.cv.replace('x', '*')))
        except: st.session_state.cv = "Error"
    elif v == "C": st.session_state.cv = ""
    else: st.session_state.cv += str(v)

with st.sidebar:
    st.title("🔢 Calculadora")
    st.text_input("Resultado:", value=st.session_state.cv, disabled=True)
    
    # Lista de botones
    btns = ['7','8','9','/', '4','5','6','x', '1','2','3','-', '0','.','C','+']
    
    # Dibujar filas de 4
    for i in range(0, len(btns), 4):
        cols = st.columns(4)
        for j in range(4):
            b = btns[i+j]
            if cols[j].button(b, key=f"btn_{b}_{i+j}"):
                calc(b)
    
    if st.button("ENTER (=)", key="btn_ent"):
        calc("=")

    st.write("---")
    nt = st.text_area("Notas:", value=db.get("notas", ""), height=150)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nt
        with open(DB_F, "w") as f: json.dump(db, f)
        st.toast("Guardado")

# --- APP PRINCIPAL ---
st.title("🍕 Bitácora")
t1, t2, t3, t4, t5 = st.tabs(["🥩 Prot", "📦 Emp", "🥤 Beb", "🥖 Masas", "📜 Hist"])

def s_u(n, u, k):
    st.subheader(n)
    c1, c2 = st.columns(2)
    p = c1.number_input("Paq", 0, step=1, key=k+"p")
    s = c2.number_input("Sue", 0, step=1, key=k+"s")
    st.info(f"Total: {(p*u)+s}")
    return (p*u)+s

with t1:
    def s_p(n, lc, lb, lcam=None):
        with st.expander(f"📦 {n}"):
            c1, c2 = st.columns(2)
            ca = c1.number_input(f"Caj({lc})", 0, step=1, key=n+"c")
            bo = c2.number_input(f"Bol({lb})", 0, step=1, key=n+"b")
            total = (ca*lc) + (bo*lb)
            if lcam: total += st.number_input(f"Cam({lcam})", 0, step=1, key=n+"m") * lcam
            pb = st.number_input("Báscula", 0.0, step=0.1, key=n+"s")
            tr = st.selectbox("Tara", [0.0, 2.5, 1.5, 1.0, 0.5], key=n+"t")
            res = total + max(0.0, pb - tr)
            st.success(f"{res:.2f} lbs"); return res

    v_que = s_p("Queso Pizza", 20, 20, 20)
    v_pep = s_p("Peperoni", 25, 12.5, 6.25)
    v_pin = s_p("Piña", 26.8, 6.7, 6.7)

with t2:
    v_c14 = s_u("Cajas 14", 50, "c14")
    v_dip = s_u("Dips", 189, "dp")

with t3:
    v_r6 = s_u("600ml", 12, "r6")
    v_r15 = s_u("1.5L", 12, "r15")

with t4:
    hc = st.number_input("Costales", 0, step=1)
    h18 = st.number_input("Bol 18oz", 0, step=1)
    v_h = hc + (h18/38)
    st.success(f"Total Harina: {v_h:.2f}")

with t5:
    if st.button("💾 GUARDAR TODO"):
        db["historial"].append({"fecha": datetime.now().strftime("%d/%m %H:%M"), "harina": f"{v_h:.2f}"})
        with open(DB_F, "w") as f: json.dump(db, f)
        st.balloons()
    for h in reversed(db["historial"]):
        st.write(f"📅 {h['fecha']} - Harina: {h['harina']}")
