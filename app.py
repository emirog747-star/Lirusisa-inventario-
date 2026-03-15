import streamlit as st
import json, os, datetime

# --- SEGURIDAD ---
if "ok" not in st.session_state:
    st.title("🔒 Acceso")
    pw = st.text_input("Clave:", type="password")
    if st.button("Entrar"):
        if pw == "patricioquemado123":
            st.session_state.ok = True
            st.rerun()
        else: st.error("Error")
    st.stop()

# --- CONFIG ---
st.set_page_config(layout="wide")
st.markdown("<style>[data-testid='column']{width:23%!important;flex:1 1 23%!important;min-width:23%!important;}.stButton>button{height:3em;font-weight:bold;}</style>", unsafe_allow_html=True)

# --- DATOS ---
DB = "data.json"
def save(d):
    with open(DB, "w") as f: json.dump(d, f)
if not os.path.exists(DB): save({"h": [], "n": ""})
with open(DB, "r") as f: db = json.load(f)

# --- CALCULADORA (SIDEBAR) ---
if "cv" not in st.session_state: st.session_state.cv = ""
def c(v):
    if v == "=":
        try: st.session_state.cv = str(eval(st.session_state.cv.replace('x', '*')))
        except: st.session_state.cv = "Err"
    elif v == "C": st.session_state.cv = ""
    else: st.session_state.cv += str(v)

with st.sidebar:
    st.title("🔢 Calc")
    st.text_input("R:", st.session_state.cv, disabled=True)
    b = ['7','8','9','/','4','5','6','x','1','2','3','-','0','.','C','+']
    for i in range(0, 16, 4):
        cols = st.columns(4)
        for j in range(4):
            val = b[i+j]
            if cols[j].button(val, key=val+str(i)): c(val)
    if st.button("ENTER (=)", use_container_width=True): c("=")
    st.write("---")
    nt = st.text_area("Notas:", db.get("n", ""), height=100)
    if st.button("💾 Guardar"):
        db["n"] = nt
        save(db)

# --- APP ---
st.title("🍕 Bitácora")
t1, t2, t3 = st.tabs(["🥩 Inv", "🥖 Masa", "📜 Hist"])

def s_u(n, u, k):
    st.subheader(n)
    c1, c2 = st.columns(2)
    p, s = c1.number_input("Paq", 0, step=1, key=k+"p"), c2.number_input("Sue", 0, step=1, key=k+"s")
    r = (p*u)+s
    st.info(f"Total: {r}"); return r

with t1:
    v_q = s_u("Queso", 20, "q")
    v_p = s_u("Pepe", 25, "p")
    v_c = s_u("Cajas", 50, "c")

with t2:
    hc = st.number_input("Costales", 0, step=1)
    h18 = st.number_input("Bol 18oz", 0, step=1)
    vh = hc + (h18/38)
    st.success(f"Harina: {vh:.2f}")

with t3:
    if st.button("💾 GUARDAR"):
        db["h"].append(f"{datetime.datetime.now().strftime('%d/%m %H:%M')} - H: {vh:.2f}")
        save(db); st.balloons()
    for i in reversed(db["h"]): st.write(i)
