import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    .pick-box {
        background-color: #00ff88;
        color: black;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 NuviCore: Picks VIP")

# --- SELECTOR DE LIGAS ---
ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
seleccion = st.selectbox("Selecciona la Liga", list(ligas.values()))
id_liga = [k for k, v in ligas.items() if v == seleccion][0]

# --- AQUÍ ESTABA EL ERROR (Definimos bien el nombre) ---
file_path = f"campionati/campionato{id_liga}.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 1.2rem; margin-bottom: 10px;">⚽ {row['match']}</div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Casa: <b>{row.get('bookie', 'Global')}</b></span>
                    <span>L: <b>{row['quota1']}</b> | V: <b>{row['quota2']}</b></span>
                </div>
                <div class="pick-box">
                    {row.get('pick', 'Análisis en proceso...')}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning(f"Todavía no hay datos para {seleccion}. Ejecuta el bot en GitHub Actions primero.")
