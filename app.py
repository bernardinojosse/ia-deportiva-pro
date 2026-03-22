import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

# Estilo para el Pick Imperdible
st.markdown("""
    <style>
    .pick-box {
        background-color: #00ff88;
        color: black;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        font-size: 1.1rem;
        box-shadow: 0px 4px 15px rgba(0, 255, 136, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ... (Tu código de selección de liga) ...

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        with st.container():
            st.subheader(row['match'])
            c1, c2 = st.columns(2)
            c1.metric("Local", row['quota1'])
            c2.metric("Visita", row['quota2'])
            
            # EL PICK REAL
            st.markdown(f'<div class="pick-box">{row["pick"]}</div>', unsafe_allow_html=True)
            st.divider()
