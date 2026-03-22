import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore | IA Predictiva", layout="centered")

# --- DISEÑO MINIMALISTA NEGRO ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .vip-link {
        display: block; text-align: center; padding: 15px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important; font-weight: bold; border-radius: 10px;
        text-decoration: none; margin-bottom: 25px;
    }
    .match-card {
        background: #111111; border: 1px solid #333;
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
    }
    .pick-box {
        background: #00ff88; color: #000; padding: 12px;
        border-radius: 8px; font-weight: 900; text-align: center; margin-top: 10px;
    }
    .legal-text {
        font-size: 0.7rem; color: #444; text-align: center;
        margin-top: 60px; line-height: 1.3;
    }
    div.stButton > button:first-child {
        background: #ffffff; color: #000; border: none;
        width: 100%; font-weight: bold; padding: 18px; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'view' not in st.session_state:
    st.session_state.view = 'hero'

# --- PANTALLA 1: BIENVENIDA ---
if st.session_state.view == 'hero':
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 3.5rem;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ff88; font-size: 1.3rem; font-weight: bold;'>LA IA DE PREDICCIÓN MÁS POTENTE DEL MERCADO</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Analizamos miles de datos en tiempo real para darte el pick con mayor probabilidad de éxito.</p><br>", unsafe_allow_html=True)
    
    if st.button("DESBLOQUEAR PICKS DE HOY"):
        st.session_state.view = 'dashboard'
        st.rerun()

    st.markdown("""<div class="legal-text">NuviCore es una herramienta informativa. No somos casa de apuestas. Los resultados pasados no garantizan éxitos futuros. El uso de esta información es responsabilidad del usuario. +18 Juega con responsabilidad.</div>""", unsafe_allow_html=True)

# --- PANTALLA 2: DASHBOARD ---
else:
    paypal_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN"
    st.markdown(f'<a href="{paypal_url}" class="vip-link">🏆 OBTENER ACCESO VIP COMPLETO ($299 MXN)</a>', unsafe_allow_html=True)

    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    sel = st.selectbox("", list(ligas.values()))
    id_liga = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_liga}.csv"

    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if df.empty:
                st.info("🔄 El bot está escaneando los partidos... Regresa en 5 min.")
            else:
                for _, row in df.iterrows():
                    st.markdown(f"""
                        <div class="match-card">
                            <div style='text-align: center; font-size: 1.3rem; font-weight: bold;'>{row['match']}</div>
                            <div style='text-align: center; color: #888; font-size: 0.9rem;'>{row['bookie']} | L: {row['quota1']} - V: {row['quota2']}</div>
                            <div class="pick-box">{row['pick']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        except:
            st.error("Error al leer datos. Espera a que el bot termine el escaneo.")
    else:
        st.warning("Aún no hay datos. Ve a GitHub Actions y dale a 'Run Workflow'.")

    if st.button("← VOLVER AL INICIO"):
        st.session_state.view = 'hero'
        st.rerun()
