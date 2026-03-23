import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore AI | Terminal", layout="centered")

# --- ESTILOS SHARP INTELLIGENCE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .vip-link {
        display: block; text-align: center; padding: 15px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important; font-weight: bold; border-radius: 12px;
        text-decoration: none; margin-bottom: 10px;
    }
    .wa-link {
        display: block; text-align: center; padding: 12px;
        background-color: #25D366; color: #fff !important;
        font-weight: bold; border-radius: 12px; text-decoration: none;
    }
    .match-card {
        background: #0a0a0a; border: 1px solid #222;
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
    }
    .metrics { display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #222; padding-top: 15px; }
    .metric-box { text-align: center; }
    .m-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; }
    .m-lbl { color: #555; font-size: 0.6rem; text-transform: uppercase; }
    .pick-box {
        background: #00ff88; color: #000; padding: 12px;
        border-radius: 10px; font-weight: 900; text-align: center; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'view' not in st.session_state: st.session_state.view = 'hero'

if st.session_state.view == 'hero':
    st.markdown("<br><br><h1 style='text-align: center; font-size: 3.5rem;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ff88; font-weight: bold;'>SHARP DATA TERMINAL</p><br>", unsafe_allow_html=True)
    if st.button("ACCEDER A DATOS EN VIVO"):
        st.session_state.view = 'dashboard'
        st.rerun()
else:
    st.markdown(f'<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="vip-link">🏆 ACTIVAR VIP PREMIUM ($299 MXN)</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="https://wa.me/526771316056" class="wa-link">💬 SOPORTE WHATSAPP</a>', unsafe_allow_html=True)
    
    ligas = {"01": "🇲🇽 LIGA MX", "06": "🇪🇸 LA LIGA", "0": "🇮🇹 SERIE A", "02": "🇪🇺 CHAMPIONS"}
    sel = st.selectbox("", list(ligas.values()))
    id_l = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_l}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="match-card">
                    <div style="color: #00ff88; font-size: 0.7rem; font-weight: bold;">{sel} • LIVE DATA</div>
                    <div style="font-size: 1.4rem; font-weight: 800; margin: 5px 0;">{row['match']}</div>
                    <div style="color: #444; font-size: 0.8rem;">{row['bookie']} | ML: {row['quota1']} - {row['quota2']}</div>
                    
                    <div class="metrics">
                        <div class="metric-box">
                            <div class="m-val">{row['probability']}%</div>
                            <div class="m-lbl">Win Prob</div>
                        </div>
                        <div class="metric-box">
                            <div class="m-val">{row['confidence']}</div>
                            <div class="m-lbl">Confidence</div>
                        </div>
                        <div class="metric-box">
                            <div class="m-val">EV+</div>
                            <div class="m-lbl">Value Status</div>
                        </div>
                    </div>
                    
                    <div class="pick-box">{row['pick']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Iniciando escaneo de datos...")

    if st.button("← VOLVER"):
        st.session_state.view = 'hero'
        st.rerun()
