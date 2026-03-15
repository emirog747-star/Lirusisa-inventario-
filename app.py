import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Bitácora", layout="wide")

# CSS para forzar que los botones no sean gigantes
st.markdown("<style>.stButton>button {height: 3em; border-radius: 8px;}</style>", unsafe_allow_html=True)

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
    
    # Cuadrícula de 4 columnas
    btns = ['7','8','9','/', '4','5','6','x', '1','2','3','-', '0','.','C','+', '=']
    c = st.columns(4)
    for i, b in enumerate(btns):
        if c[i % 4].button(b, key=f"btn_{b}_{i}"): calc(b)

    st.write("---")
    nt = st.text_area("Notas:", value=db.get("notas", ""), height=150)
    if st.button("💾 Guardar Notas"):
        db["notas"] = nt
        with open(DB_F, "w") as f: json.dump(db, f)
        st.toast("Guardado")

# --- INTERFAZ PRINCIPAL ---
st.title("🍕 Bitácora")
t1, t2, t3, t4, t5 = st.tabs(["🥩 Prot", "📦 Emp", "🥤 Beb", "🥖 Masas", "📜 Hist"])

def s_u(n, u, k):
    st.subheader(n)
    c1, c2 = st.columns(2)
    # Step=1 asegura que suba de 1 en 1
    p = c1.number_input("Paq", 0, step=1, key=k+"p")
    s = c2.number_input("Sue", 0, step=1, key=k+"s")
    st.
 
