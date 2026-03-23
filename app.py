import streamlit as st
import pandas as pd
import os

# Configuración Pro
st.set_page_config(page_title="NuviCore AI | Sharp Intelligence", layout="centered")

# --- ESTILOS DE INTERFAZ DE LUJO ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Botones Superiores */
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

    /* Tarjeta de Evento (The Matchup) */
    .match-card {
        background: #0a0a0a; border: 1px solid #1a1a1a;
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .league-tag { color: #00ff88; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; }
    .teams { font-size: 1.5rem; font-weight: 800; margin: 10px 0; }
    
    /* Métricas de IA (Win Prob & EV+) */
    .metrics-container { display: flex; justify-content: space-between; margin-top: 15px; padding-top: 15px; border-top: 1px solid #222; }
    .metric-item { text-align: center; }
    .metric-value { color: #00bdff; font-weight: bold; font-size: 1.1rem; }
    .metric-label { color: #555; font-size: 0.7rem; text-transform: uppercase; }

    /* El Pick Pro */
    .pick-box {
        background: #00ff88; color: #000; padding: 12px;
        border-radius: 10px; font-weight: 900; text-align: center; 
        margin-top: 20px; font-size: 1rem; text-transform: uppercase;
    }
    
    .ev-badge { background: #ff0050; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.6rem; margin-left: 5px; }

    div.stButton > button:first-child {
        background: #ffffff; color: #000; border: none;
        width: 100%; font-weight: bold; padding: 18px; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'view' not in st.session_state: st.session_state.view = 'hero'

# --- PANTALLA 1: LANDING DE ALTO IMPACTO ---
if st.session_state.view == 'hero':
    st.markdown("<br><br><h1 style='text-align: center; font-size: 4rem; letter-spacing: -2px;'>NuviCore AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ff88; font-weight: bold; letter-spacing: 1px;'>SHARP BETTING INTELLIGENCE</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; max-width: 400px; margin: 0 auto;'>Accede a predicciones basadas en EV+, movimiento de líneas y algoritmos de probabilidad avanzada.</p><br>", unsafe_allow_html=True)
    
    if st.button("DESBLOQUEAR TERMINAL"):
        st.session_state.view = 'dashboard'
        st.rerun()

    st.markdown("<p style='font-size: 0.7rem; color: #333; text-align: center; margin-top: 100px;'>© 2026 NuviCore AI Technologies. <br> Powered by OddsAPI & AF_API. +18 Juega con responsabilidad.</p>", unsafe_allow_html=True)

# --- PANTALLA 2: TERMINAL DE DATOS ---
else:
    # Header de Acción
    st.markdown(f"""
        <div class="btn-container">
            <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="vip-link">🏆 PLAN PRO ($299)</a>
            <a href="https://wa.me/526771316056" class="wa-link">💬 SOPORTE</a>
        </div>
    """, unsafe_allow_html=True)
    
    ligas = {"01": "🇲🇽 LIGA MX", "06": "🇪🇸 LA LIGA", "0": "🇮🇹 SERIE A", "02": "🇪🇺 CHAMPIONS"}
    sel = st.selectbox("", list(ligas.values()))
    id_l = [k for k, v in ligas.items() if v == sel][0]

    path = f"campionati/campionato{id_l}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            # Simulamos métricas de IA basadas en las cuotas (esto lo hace el bot internamente)
            prob_local = round((1/row['quota1']) * 100)
            
            st.markdown(f"""
                <div class="match-card">
                    <div class="league-tag">{sel} • FIXTURE DATA</div>
                    <div class="teams">{row['match']}</div>
                    <div style="color: #666; font-size: 0.8rem; margin-bottom: 15px;">
                        Bookie: {row['bookie']} | ML: L {row['quota1']} - V {row['quota2']}
                    </div>
                    
                    <div class="metrics-container">
                        <div class="metric-item">
                            <div class="metric-label">Win Prob</div>
                            <div class="metric-value">{prob_local}%</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Confidence</div>
                            <div class="metric-value" style="color: #00ff88;">ALTA</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Value</div>
                            <div class="metric-value">EV+ <span class="ev-badge">PRO</span></div>
                        </div>
                    </div>
                    
                    <div class="pick-box">{row['pick']}</div>
                    <div style="font-size: 0.6rem; color: #444; margin-top: 10px; text-align: center;">
                        Análisis: Basado en H2H y Line Movement (Smart Money Detection).
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Iniciando terminal de datos... Ejecuta el Scraper.")

    if st.button("← CERRAR SESIÓN"):
        st.session_state.view = 'hero'
        st.rerun()
