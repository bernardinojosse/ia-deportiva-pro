import streamlit as st
import pandas as pd
import os

# Configuración de página limpia
st.set_page_config(page_title="NuviCore | IA Deportiva", layout="centered", page_icon="🛡️")

# --- DISEÑO DE ALTO NIVEL (CSS) ---
st.markdown("""
    <style>
    /* Fondo total oscuro */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Ocultar elementos basura de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Botón VIP Moderno */
    .vip-link {
        display: block;
        text-align: center;
        padding: 12px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        margin-bottom: 20px;
    }

    /* Tarjetas de Partidos Estilo "Glassmorphism" */
    .match-card {
        background: #111111;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .match-title { font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
    .match-subtitle { font-size: 0.9rem; color: #888; margin-bottom: 15px; }
    
    /* El Pick: Lo más llamativo */
    .pick-box {
        background: #00ff88;
        color: #000;
        padding: 10px;
        border-radius: 6px;
        font-weight: 900;
        letter-spacing: 1px;
    }

    /* Texto Legal Miniatura */
    .legal-text {
        font-size: 0.7rem;
        color: #444;
        text-align: center;
        margin-top: 50px;
        line-height: 1.2;
    }
    
    /* Botón de Entrada */
    div.stButton > button:first-child {
        background: #ffffff;
        color: #000;
        border: none;
        width: 100%;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'hero'

# --- PANTALLA 1: BIENVENIDA (HERO) ---
if st.session_state.view == 'hero':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem;'>La mejor Inteligencia Artificial predictiva del mercado.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("ACCEDER AL PANEL DE HOY"):
        st.session_state.view = 'dashboard'
        st.rerun()

    st.markdown("""
        <div class="legal-text">
            NuviCore es una herramienta informativa de análisis estadístico. No somos casa de apuestas. 
            El éxito pasado no garantiza resultados futuros. Juega con responsabilidad (+18).
        </div>
    """, unsafe_allow_html=True)

# --- PANTALLA 2: DASHBOARD DE PICKS ---
else:
    # Botón VIP arriba siempre
    paypal_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN"
    st.markdown(f'<a href="{paypal_url}" class="vip-link">🏆 ACTIVAR ACCESO VIP ($299 MXN)</a>', unsafe_allow_html=True)

    # Selector de ligas
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    sel = st.selectbox("", list(ligas.values()), label_visibility="collapsed")
    id_liga = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_liga}.csv"

    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if df.empty:
                st.info("El bot está procesando los datos...")
            else:
                for index, row in df.iterrows():
                    st.markdown(f"""
                        <div class="match-card">
                            <div class="match-title">{row['match']}</div>
                            <div class="match-subtitle">{row['bookie']} | L: {row['quota1']} - V: {row['quota2']}</div>
                            <div class="pick-box">{row['pick']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error("Sincronizando base de datos... Refresca en 1 minuto.")
    else:
        st.warning("No hay partidos para esta liga hoy.")

    if st.button("← VOLVER"):
        st.session_state.view = 'hero'
        st.rerun()
