import streamlit as st
import pandas as pd
import os

# Configuración y PWA
st.set_page_config(page_title="NuviCore AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .vip-link {
        display: block; text-align: center; padding: 15px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important; font-weight: bold; border-radius: 12px;
        text-decoration: none; margin-bottom: 20px;
    }
    .wa-link {
        display: block; text-align: center; padding: 12px;
        background-color: #25D366; color: #fff !important;
        font-weight: bold; border-radius: 12px; text-decoration: none;
    }
    .match-card {
        background: #111111; border: 1px solid #333;
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
    }
    .pick-box {
        background: #00ff88; color: #000; padding: 10px;
        border-radius: 8px; font-weight: 900; text-align: center; margin-top: 10px;
    }
    div.stButton > button:first-child {
        background: #ffffff; color: #000; border: none;
        width: 100%; font-weight: bold; padding: 18px; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'view' not in st.session_state: st.session_state.view = 'hero'

# PANTALLA DE BIENVENIDA
if st.session_state.view == 'hero':
    st.markdown("<br><br><h1 style='text-align: center; font-size: 3.5rem;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ff88; font-weight: bold;'>SISTEMA PREDICTIVO DE ALTA PRECISIÓN</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Bienvenido a la IA más avanzada para el análisis de mercados deportivos.</p><br>", unsafe_allow_html=True)
    
    if st.button("DESBLOQUEAR ACCESO"):
        st.session_state.view = 'dashboard'
        st.rerun()

    st.markdown("<p style='font-size: 0.7rem; color: #444; text-align: center; margin-top: 100px;'>© 2026 NuviCore AI Technologies. <br> Informativo. +18 Juega con responsabilidad.</p>", unsafe_allow_html=True)

# DASHBOARD DE PICKS
else:
    st.markdown(f'<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="vip-link">🏆 ACTIVAR VIP PREMIUM ($299 MXN)</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/526771316056?text=Hola,%20quiero%20el%20VIP%20de%20NuviCore" class="wa-link">💬 SOPORTE WHATSAPP</a>', unsafe_allow_html=True)
    
    st.write("---")
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    sel = st.selectbox("", list(ligas.values()))
    id_liga = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_liga}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            st.markdown(f"""<div class="match-card"><div style='text-align: center; font-size: 1.2rem; font-weight: bold;'>{row['match']}</div><div style='text-align: center; color: #666; font-size: 0.8rem;'>{row['bookie']} | L:{row['quota1']} V:{row['quota2']}</div><div class="pick-box">{row['pick']}</div></div>""", unsafe_allow_html=True)
    else: st.warning("Cargando datos... Ejecuta el Action en GitHub.")
    
    if st.button("← VOLVER"):
        st.session_state.view = 'hero'
        st.rerun()
