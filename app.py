import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NuviCore Pro", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILO APPLE SPORTS (DARK MODE FORZADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; color: #ffffff !important; }
    * { font-family: 'Inter', sans-serif !important; }
    .iphone-shell { max-width: 500px; margin: 0 auto; background-color: #000000; min-height: 100vh; }
    .apple-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 15px; }
    .app-title { font-size: 28px; font-weight: 700; color: #ffffff; }
    .match-row { background-color: #1C1C1E; border-radius: 14px; padding: 18px; margin: 10px 15px; display: flex; align-items: center; justify-content: space-between; border: 1px solid rgba(255,255,255,0.05); }
    .team-box { display: flex; align-items: center; gap: 12px; width: 38%; }
    .team-logo { width: 30px; height: 30px; object-fit: contain; }
    .team-name { font-weight: 600; font-size: 15px; color: #fff; }
    .score-box { font-size: 26px; font-weight: 700; color: #fff; width: 10%; text-align: center; }
    .status-mid { width: 14%; text-align: center; color: #8E8E93; font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .btn-update { background: #333; color: white; border-radius: 20px; padding: 10px; text-align: center; margin: 10px 15px; cursor: pointer; border: none; width: 94%; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES (CONEXIÓN API-SPORTS) ---
class NuviCoreEngine:
    def __init__(self):
        # USANDO TUS NOMBRES EXACTOS DE GITHUB
        self.fb_key = st.secrets.get("AF_API_KEY")
        self.odds_key = st.secrets.get("ODDS_API_KEY")
        self.mx_tz = pytz.timezone('America/Mexico_City')

        if not self.fb_key:
            st.error("❌ Error: No se encuentra 'AF_API_KEY' en los Secrets de Streamlit.")
            st.stop()

    def get_live_scores(self):
        """Conexión real a API-SPORTS para resultados en vivo"""
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "x-rapidapi-key": self.fb_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
        }
        # League 262 es Liga MX. Traemos los partidos de hoy.
        params = {"league": "262", "season": "2025", "live": "all"}
        try:
            res = requests.get(url, headers=headers, params=params).json()
            return res.get('response', [])
        except:
            return []

engine = NuviCoreEngine()

# --- INTERFAZ ---
st.markdown('<div class="iphone-shell">', unsafe_allow_html=True)

st.markdown("""
    <div class="apple-header">
        <div class="app-title">NuviCore</div>
        <div style="color: #10b981; font-size: 12px; font-weight: 700;">● LIVE LIGA MX</div>
    </div>
""", unsafe_allow_html=True)

if st.button("🔄 SINCRONIZAR MARCADORES REALES"):
    with st.spinner("Accediendo a API-SPORTS..."):
        data = engine.get_live_scores()
        
        if not data:
            st.info("No hay partidos en vivo en este momento en la Liga MX.")
        
        for match in data:
            h = match['teams']['home']
            a = match['teams']['away']
            goals = match['goals']
            status = match['fixture']['status']['elapsed']
            
            st.markdown(f"""
                <div class="match-row">
                    <div class="team-box">
                        <img src="{h['logo']}" class="team-logo">
                        <span class="team-name">{h['name']}</span>
                    </div>
                    <div class="score-box">{goals['home'] if goals['home'] is not None else 0}</div>
                    <div class="status-mid">{status}'<br>EN VIVO</div>
                    <div class="score-box">{goals['away'] if goals['away'] is not None else 0}</div>
                    <div class="team-box" style="justify-content: flex-end;">
                        <span class="team-name">{a['name']}</span>
                        <img src="{a['logo']}" class="team-logo">
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div style="text-align: center; padding: 80px 20px; color: #8E8E93;">
            <p>Bienvenido, Luis Enrique.</p>
            <p style="font-size: 13px;">Presiona el botón para conectar con el servidor de API-SPORTS.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
