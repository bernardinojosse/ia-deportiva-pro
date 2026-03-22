import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

# Estilo visual para que parezca una App Pro
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #00ff88;
    }
    .pick-box {
        background-color: #00ff88;
        color: black;
        padding: 8px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ NuviCore Intelligence")

# Mapeo de ligas
ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
seleccion = st.selectbox("Selecciona la Liga", list(ligas.values()))
id_liga = [k for k, v in ligas.items() if v == seleccion][0]

file_path = f"campionati/campionato{id_liga}.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            st.warning("🔄 El bot está actualizando los datos. Regresa en 5 minutos.")
        else:
            for _, row in df.iterrows():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 1.2rem;">⚽ {row['match']}</div>
                    <div style="color: #8b949e; margin: 10px 0;">
                        Casa: {row['bookie']} | <b>L: {row['quota1']} - V: {row['quota2']}</b>
                    </div>
                    <div class="pick-box">{row['pick']}</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error("Error al leer los datos. El bot está trabajando...")
else:
    st.info(f"Todavía no hay datos para {seleccion}. Ejecuta el bot en GitHub Actions.")
