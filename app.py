import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #00ff88;
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

ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
sel = st.selectbox("Selecciona la Liga", list(ligas.values()))
id_l = [k for k, v in ligas.items() if v == sel][0]

path = f"campionati/campionato{id_l}.csv"

if os.path.exists(path):
    try:
        df = pd.read_csv(path)
        if df.empty or len(df.columns) < 2:
            st.info("🔄 El bot está cargando nuevos partidos. Espera un momento...")
        else:
            for _, row in df.iterrows():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 1.1rem; font-weight:bold;">{row['match']}</div>
                    <div style="color: #8b949e; font-size: 0.9rem; margin: 8px 0;">
                        Cuotas: L {row['quota1']} | V {row['quota2']}
                    </div>
                    <div class="pick-box">{row['pick']}</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.error("Sincronizando base de datos...")
else:
    st.warning("No hay partidos detectados para esta liga hoy.")
