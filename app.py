import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        border-left: 5px solid #00ff88;
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

st.title("🛡️ NuviCore Unit")

ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
seleccion = st.selectbox("Seleccionar Mercado", list(ligas.values()))
id_liga = [k for k, v in ligas.items() if v == seleccion][0]

file_path = f"campionati/campionato{id_liga}.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            st.warning("Esperando actualización de datos del bot...")
        else:
            for _, row in df.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size: 1.2rem; margin-bottom: 10px;">⚽ {row['match']}</div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Casa: {row.get('bookie', 'Global')}</span>
                            <span style="color:#58a6ff;">L: {row['quota1']} | V: {row['quota2']}</span>
                        </div>
                        <div class="pick-box">
                            {row.get('pick', 'Analizando...')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    except Exception as e:
        st.error("Los datos se están sincronizando. Recarga en un momento.")
else:
    st.info(f"No hay datos para {seleccion}. Inicia el bot en GitHub Actions.")
