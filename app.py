import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore Pro", layout="wide")

st.title("💰 NuviCore: Arbitraje Deportivo")

# Diccionario de ligas
ligas = {"0": "Serie A", "01": "Serie B", "02": "Champions", "04": "Premier", "06": "La Liga"}
seleccion = st.sidebar.selectbox("Selecciona la Liga", list(ligas.values()))
id_liga = [k for k, v in ligas.items() if v == seleccion][0]

file_path = f"campionati/campionato{id_liga}.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.success(f"Datos actualizados de {seleccion}")
    
    for _, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"### {row['match']}")
            col2.metric("Casa A", row['quota1'])
            col3.metric("Casa B", row['quota2'])
            st.divider()
else:
    st.warning(f"Aún no hay datos para {seleccion}. Ejecuta el bot en GitHub Actions.")
