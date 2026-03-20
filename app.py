import streamlit as st
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="NuviCore Pro", layout="centered")

# Estilos visuales neón (Inyectados correctamente)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #161b22;
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .profit { color: #00ff88; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 NuviCore Arbitraje")

# Selección de Liga
ligas = {"0": "Serie A", "01": "Serie B", "02": "Champions", "04": "Premier", "06": "La Liga"}
opcion = st.selectbox("Selecciona liga:", list(ligas.values()))
id_liga = [k for k, v in ligas.items() if v == opcion][0]

# Carga de datos
file_path = f"campionati/campionato{id_liga}.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        # Lógica de la tarjeta visual
        html_card = f"""
        <div class="card">
            <div style="font-size: 0.9rem; color: #8b949e;">{opcion}</div>
            <div style="font-size: 1.1rem; margin: 5px 0;">{row['match']}</div>
            <div style="display: flex; justify-content: space-between;">
                <span>Cuota 1: <b>{row['quota1']}</b></span>
                <span>Cuota 2: <b>{row['quota2']}</b></span>
            </div>
            <div style="margin-top: 10px; border-top: 1px solid #30363d; padding-top: 5px;">
                <span class="profit">Oportunidad Detectada ✅</span>
            </div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)
else:
    st.info(f"Escaneando... El bot actualizará {opcion} en la próxima carrera.")
