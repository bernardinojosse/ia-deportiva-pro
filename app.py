import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA (APPLE SPORTS CLONE) ---
st.set_page_config(page_title="NuviCore Multi", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; color: #ffffff !important; }
    * { font-family: 'Inter', sans-serif !important; }
    .iphone-shell { max-width: 500px; margin: 0 auto; background-color: #000000; min-height: 100vh; padding-bottom: 50px; }
    .apple-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 15px; }
    .app-title { font-size: 28px; font-weight: 700; color: #ffffff; }
    .match-row { background-color: #1C1C1E; border-radius: 14px; padding: 18px; margin: 10px 15px; display: flex; align-items: center; justify-content: space-between; border: 1px solid rgba(255,255,255,0.05); }
    .team-box { display: flex; align-items: center; gap: 12px; width: 38%; }
    .team-logo { width: 30px; height: 30px; object-fit: contain; }
    .team-name { font-weight: 600; font-size: 14px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .score-box { font-size: 24px; font-weight: 700; color: #fff; width: 10%; text-align: center; }
    .status-mid { width: 14%; text-align: center; color: #8E8E93; font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .section-label { color: #8E8E93; font-size: 11px; font-weight: 700; padding: 15px 25px 5px; text-transform: uppercase; }
    /* Estilo para los selectores de Streamlit en Dark Mode */
    .stSelectbox div[data-baseweb="select"] { background-color: #1C1C1E !important; color: white !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MAPEO DE LIGAS (IDS REALES API-SPORTS Y THE ODDS) ---
LIGAS = {
    "🇲🇽 Liga MX": {"af_id": "262", "odds_id": "soccer_mexico_ligamx"},
    "🇬🇧 Premier League": {"af_id": "39", "odds_id": "soccer_epl"},
    "🇪🇸 La Liga": {"af_id": "140", "odds_id": "soccer_spain_la_liga"},
    "🇮🇹 Serie A": {"af_id": "135", "odds_id": "soccer_italy_serie_a"},
    "🇪🇺 Champions League": {"af_id": "2", "odds_id": "soccer_uefa_champs_league"},
    "🏀 NBA": {"af_id": "standard", "odds_id": "basketball_nba", "type": "basketball"}
}

class NuviCoreEngine:
    def __init__(self):
        self.fb_key = st.secrets.get("AF_API_KEY")
        self.odds_key = st.secrets.get("ODDS_API_KEY")
        self.mx_tz = pytz.timezone('America/Mexico_City')

    def fetch_data(self, af_id):
        """Petición real a API-Sports"""
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {"x-rapidapi-key": self.fb_key, "x-rapidapi-host": "api-football-v1.p.rapidapi.com"}
        params = {"league": af_id, "season": "2025", "live": "all"}
        try:
            res = requests.get(url, headers=headers, params=params).json()
            return res.get('response', [])
        except: return []

engine = NuviCoreEngine()

# --- INTERFAZ ---
st.markdown('<div class="iphone-shell">', unsafe_allow_html=True)

st.markdown("""
    <div class="apple-header">
        <div class="app-title">NuviCore</div>
        <div style="background: #1C1C1E; padding: 5px 12px; border-radius: 15px; font-size: 12px;">PRO</div>
    </div>
""", unsafe_allow_html=True)

# Selector de Liga (Estilo Apple)
seleccion = st.selectbox("Seleccionar Liga", list(LIGAS.keys()), label_visibility="collapsed")
config = LIGAS[seleccion]

if st.button(f"⚡ ESCANEAR {seleccion.upper()}"):
    with st.spinner("Conectando con servidores..."):
        data = engine.fetch_data(config['af_id'])
        
        if not data:
            st.markdown('<div class="section-label">Sin partidos en vivo ahora</div>', unsafe_allow_html=True)
            st.info(f"No hay actividad en vivo para {seleccion}. Intenta con otra liga.")
        else:
            st.markdown(f'<div class="section-label">En vivo: {seleccion}</div>', unsafe_allow_html=True)
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
                        <div class="status-mid">{status}'<br>LIVE</div>
                        <div class="score-box">{goals['away'] if goals['away'] is not None else 0}</div>
                        <div class="team-box" style="justify-content: flex-end;">
                            <span class="team-name">{a['name']}</span>
                            <img src="{a['logo']}" class="team-logo">
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
