import streamlit as st
import pandas as pd
import os

# Configuración de la App
st.set_page_config(page_title="NuviCore | IA Predictiva", layout="centered")

# --- DISEÑO MINIMALISTA NEGRO ---
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

if 'view' not in st.session_state:
    st.session_state.view = 'hero'

# --- PANTALLA 1: BIENVENIDA ---
if st.session_state.view == 'hero':
    st.markdown("<br><br><br><h1 style='text-align: center; font-size: 3.5rem;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ff88; font-weight: bold; font-size: 1.2rem;'>SISTEMA PREDICTIVO DE ALTA PRECISIÓN</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>La Inteligencia Artificial más avanzada para el análisis de mercados deportivos.</p><br>", unsafe_allow_html=True)
    
    if st.button("DESBLOQUEAR ACCESO"):
        st.session_state.view = 'dashboard'
        st.rerun()

    st.markdown("<p style='font-size: 0.75rem; color: #444; text-align: center; margin-top: 100px;'>© 2026 NuviCore AI Technologies. <br> Herramienta informativa. +18 Juega con responsabilidad.</p>", unsafe_allow_html=True)

# --- PANTALLA 2: DASHBOARD ---
else:
    # Botones de Acción
    paypal_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN"
    st.markdown(f'<a href="{paypal_url}" class="vip-link">🏆 ACTIVAR VIP PREMIUM ($299 MXN)</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/526771316056?text=Hola,%20vengo%20de%20la%20App%20NuviCore%20y%20quiero%20el%20VIP" class="wa-link">💬 SOPORTE WHATSAPP</a>', unsafe_allow_html=True)
    
    st.write("---")
    
    # Selector de Ligas
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    sel = st.selectbox("", list(ligas.values()))
    id_liga = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_liga}.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if df.empty:
                st.info("🔄 El bot está escaneando los partidos... Regresa en unos minutos.")
            else:
                for _, row in df.iterrows():
                    st.markdown(f"""
                        <div class="match-card">
                            <div style='text-align: center; font-size: 1.2rem; font-weight: bold;'>{row['match']}</div>
                            <div style='text-align: center; color: #666; font-size: 0.8rem;'>{row['bookie']} | L:{row['quota1']} V:{row['quota2']}</div>
                            <div class="pick-box">{row['pick']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        except:
            st.error("Sincronizando base de datos...")
    else:
        st.warning("Sin datos para hoy. Asegúrate de correr el Action en GitHub.")
    
    if st.button("← VOLVER AL INICIO"):
        st.session_state.view = 'hero'
        st.rerun()
