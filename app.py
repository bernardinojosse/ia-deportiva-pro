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
        padding: 18px;
        margin-bottom: 15px;
        border: 1px solid #00ff88;
        box-shadow: 0px 4px 10px rgba(0,255,136,0.1);
    }
    .pick-box {
        background-color: #00ff88;
        color: #000;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ NuviCore Intelligence")

menu_ligas = {"01": "🇲🇽 Liga MX", "02": "🇪🇺 Champions", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A"}
seleccion = st.selectbox("Seleccionar Mercado:", list(menu_ligas.values()))
id_l = [k for k, v in menu_ligas.items() if v == seleccion][0]

path_csv = f"campionati/campionato{id_l}.csv"

if os.path.exists(path_csv):
    try:
        df = pd.read_csv(path_csv)
        if df.empty:
            st.info("🔄 Los datos se están actualizando. Reintenta en 1 minuto.")
        else:
            for _, row in df.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size: 1.1rem; font-weight: bold;">{row['match']}</div>
                        <div style="color: #8b949e; font-size: 0.9rem; margin-top:5px;">
                            Casa: {row['bookie']} | <b>L: {row['quota1']} - V: {row['quota2']}</b>
                        </div>
                        <div class="pick-box">{row['pick']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("⌛ Sincronizando base de datos...")
else:
    st.warning("Aún no hay datos para esta liga. El bot los generará en su próximo ciclo.")
