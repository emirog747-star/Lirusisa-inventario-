import streamlit as st
import json, os
from datetime import datetime

# --- SEGURIDAD ---
def validar_acceso():
    if "autenticado" not in st.session_state:
        st.title("🔒 Acceso Restringido")
        clave = st.text_input("Contraseña:", type="password")
        if st.button("Entrar"):
            if clave == "patricioquemado123":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
        return False
    return True

if validar_acceso():
    st.set_page_config(page_title="Bitácora", layout="wide")

    # CSS para forzar las 4 columnas de la calculadora en móvil
    st.markdown("""
        <style>
        [data-testid="column"] { width: 23% !important; flex: 1 1 23% !important; min-width: 23% !important; }
        .stButton>button { width: 100%; height: 3em; font-weight: bold; border-radius: 8px; }
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
        st.text_input("Res:", value=st.session_state.cv, disabled=True)
        btns = ['7','8','9','/', '4','5','6','x', '1','2','3','-', '0','.','C','+']
        for i in range(0, len(btns), 4):
            cols
