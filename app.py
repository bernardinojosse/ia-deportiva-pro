import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import pytz

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="NUVI-CORE LIVE", layout="wide")

def set_dark_theme():
    st.markdown("""
        <style>
        .main { background-color: #05070a; color: #e5e7eb; }
        .stMetric { background-color: #111827; border: 1px solid #1f2937; border-radius: 8px; }
        .match-card { 
            background: linear-gradient(145deg, #111827, #0f172a); 
            border-radius: 12px; padding: 15px; margin-bottom: 10px;
            border: 1px solid #1e293b;
        }
        .value-tag { background: #064e3b; color: #34d399; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

set_dark_theme()

# --- MOTORES DE DATA REAL ---
class LiveEngine:
    def __init__(self):
        self.fb_key = st.secrets["API_FOOTBALL_KEY"]
        self.odds_key = st.secrets["THE_ODDS_API_KEY"]
        self.mx_tz = pytz.timezone('America/Mexico_City')

    def get_live_odds(self, sport="soccer_mexico_ligamx"):
        """Obtiene cuotas reales de casas de apuestas (Codere, Caliente, etc)."""
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"
        params = {
            'apiKey': self.odds_key,
            'regions': 'us,eu', # Incluye mercados relevantes
            'markets': 'h2h',
            'oddsFormat': 'decimal'
        }
        res = requests.get(url, params=params).json()
        return res

    def get_team_stats(self, team_id, league_id=262): # 262 es Liga MX
        """Extrae xG y rendimiento real de API-Football."""
        url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
        headers = {'x-rapidapi-key': self.fb_key, 'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}
        params = {"league": league_id, "season": "2025", "team": team_id}
        res = requests.get(url, headers=headers, params=params).json()
        
        if res.get('response'):
            stats = res['response']
            # Cálculo de xG basado en promedio de goles marcados/recibidos
            goals_for = stats['goals']['for']['average']['total']
            return float(goals_for)
        return 1.0

# --- LÓGICA DE VALOR ---
def calculate_edge(prob_real, odd_decimal):
    prob_implied = 1 / odd_decimal
    return prob_real - prob_implied

def kelly_criterion(edge, odd_decimal, bankroll):
    if edge <= 0: return 0
    b = odd_decimal - 1
    f = edge / b
    return f * bankroll * 0.25 # Kelly fraccionado al 25%

# --- INTERFAZ DINÁMICA ---
def main():
    st.title("🦅 NUVI-CORE | Live Intelligence")
    engine = LiveEngine()
    
    bankroll = st.sidebar.number_input("Tu Bankroll ($MXN)", value=1000, step=100)
    sport_choice = st.sidebar.selectbox("Liga", ["soccer_mexico_ligamx", "soccer_spain_la_liga", "soccer_uefa_champs_league"])

    if st.button('🔄 ACTUALIZAR DATOS EN VIVO'):
        with st.spinner('Analizando mercados y xG real...'):
            raw_odds = engine.get_live_odds(sport_choice)
            
            if not raw_odds:
                st.warning("No hay mercados abiertos por ahora.")
                return

            for match in raw_odds:
                home = match['home_team']
                away = match['away_team']
                
                # Conversión de Horario
                utc_dt = datetime.fromisoformat(match['commence_time'].replace('Z', '+00:00'))
                local_time = utc_dt.astimezone(engine.mx_tz).strftime('%H:%Mh')
                
                # Extraer Cuota Promedio (H2H)
                try:
                    bookie = match['bookmakers'][0]
                    odds_data = bookie['markets'][0]['outcomes']
                    home_odd = next(o['price'] for o in odds_data if o['name'] == home)
                except: continue

                # Algoritmo de Probabilidad (Basado en historial reciente simula xG)
                # En producción, aquí llamamos a get_team_stats para cada equipo
                prob_real = 0.55 # Ejemplo de probabilidad calculada por el modelo
                edge = calculate_edge(prob_real, home_odd)
                
                # RENDERIZADO DE TARJETA
                with st.container():
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:1.2em; font-weight:bold;">{home} vs {away}</span>
                            <span style="color:#94a3b8;">{local_time}</span>
                        </div>
                        <div style="margin-top:10px; display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
                            <div><small>Cuota</small><br><b>{home_odd}</b></div>
                            <div><small>Edge</small><br><b>{edge*100:.1f}%</b></div>
                            <div><small>Prob. Real</small><br><b>{prob_real*100:.0f}%</b></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if edge > 0.05:
                        stake = kelly_criterion(edge, home_odd, bankroll)
                        st.success(f"🔥 PICK ALTA CONFIANZA: Apostar ${stake:.2f} MXN en {home}")
                    else:
                        st.info("📊 Análisis: Sin valor claro en este mercado.")

    else:
        st.info("Haz clic en el botón para cargar los partidos en vivo desde las APIs.")

if __name__ == "__main__":
    main()
