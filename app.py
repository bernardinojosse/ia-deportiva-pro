import streamlit as st
import pandas as pd
import os

# 1. Configuración base
st.set_page_config(page_title="NuviCore | Sharp Terminal", layout="centered")

# --- ESTILOS CORREGIDOS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    
    .btn-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .vip-link {
        flex: 1; text-align: center; padding: 15px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important; font-weight: bold; border-radius: 12px;
        text-decoration: none; font-size: 0.9rem;
    }
    .wa-link {
        flex: 1; text-align: center; padding: 15px;
        background-color: #25D366; color: #fff !important;
        font-weight: bold; border-radius: 12px; text-decoration: none; font-size: 0.9rem;
    }

    .match-card {
        background: #0a0a0a; border: 1px solid #1a1a1a;
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
    }
    .teams { font-size: 1.5rem; font-weight: 800; margin: 10px 0; }
    
    .metrics { display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #222; padding-top: 15px; }
    .metric-box { text-align: center; }
    .m-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; }
    .m-lbl { color: #555; font-size: 0.6rem; text-transform: uppercase; }

    .pick-box {
        background: #00ff88; color: #000; padding: 12px;
        border-radius: 10px; font-weight: 900; text-align: center; 
        margin-top: 20px; font-size: 1rem; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DEL AVISO LEGAL (Versión compatible) ---
if 'legal_aceptado' not in st.session_state:
    st.session_state['legal_aceptado'] = False

if not st.session_state['legal_aceptado']:
    st.warning("⚠️ AVISO LEGAL Y DE PRIVACIDAD")
    st.info("""
    **NuviCore AI** es una herramienta informativa de análisis estadístico.
    - Los resultados pasados no garantizan éxitos futuros.
    - El uso de esta información es responsabilidad exclusiva del usuario.
    - Prohibido para menores de 18 años.
    """)
    if st.button("ACEPTAR TÉRMINOS Y ENTRAR"):
        st.session_state['legal_aceptado'] = True
        st.rerun()
    st.stop()

# --- TERMINAL DE DATOS ---
st.markdown(f"""
    <div class="btn-container">
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="vip-link">🏆 ACTIVAR VIP ($299 MXN)</a>
        <a href="https://wa.me/526771316056" class="wa-link">💬 SOPORTE WHATSAPP</a>
    </div>
""", unsafe_allow_html=True)

ligas = {"01": "🇲🇽 LIGA MX", "06": "🇪🇸 LA LIGA", "0": "🇮🇹 SERIE A", "02": "🇪🇺 CHAMPIONS"}
sel = st.selectbox("", list(ligas.values()))
id_l = [k for k, v in ligas.items() if v == sel][0]

path = f"campionati/campionato{id_l}.csv"
if os.path.exists(path):
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        # La clave es envolver TODO el bloque en un solo st.markdown con unsafe_allow_html=True
        html_card = f"""
        <div class="match-card">
            <div class="teams">{row['match']}</div>
            <div style="color: #666; font-size: 0.8rem; margin-bottom: 15px;">
                Bookie: {row['bookie']} | ML: {row['quota1']} - {row['quota2']}
            </div>
            <div class="metrics">
                <div class="metric-box">
                    <div class="m-val">{row.get('probability', 50)}%</div>
                    <div class="m-lbl">Win Prob</div>
                </div>
                <div class="metric-box">
                    <div class="m-val" style="color: #00ff88;">{row.get('confidence', 'MEDIA')}</div>
                    <div class="m-lbl">Confidence</div>
                </div>
                <div class="metric-box">
                    <div class="m-val">EV+</div>
                    <div class="m-lbl">Data Status</div>
                </div>
            </div>
            <div class="pick-box">{row['pick']}</div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)
else:
    st.warning("🔄 Sincronizando datos... Ejecuta el Action en GitHub.")
