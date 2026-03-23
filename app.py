import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA (ESTILO APPLE) ---
st.set_page_config(page_title="NuviCore Sports", layout="wide", initial_sidebar_state="collapsed")

# Fondo negro profundo y tipografía limpia
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #000000;
        color: #ffffff;
    }
    
    .main { background-color: #000000; }
    
    /* Ocultar elementos estándar de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor Principal de la App */
    .app-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 10px;
    }
    
    /* Header (Clon Apple Sports) */
    .apple-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    .app-title {
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .app-title span { color: #fff; }
    
    .my-teams-btn {
        background-color: rgba(255, 255, 255, 0.1);
        color: #fff;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Selector de Tiempo (Tabs Clon) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: none;
        gap: 20px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94a3b8;
        font-weight: 600;
        border: none;
        padding: 10px 0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff;
        border-bottom: 2px solid #ffffff;
    }
    
    /* Tarjeta de Partido (Clon Apple Sports) */
    .match-card {
        background-color: #1C1C1E;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background-color 0.2s;
    }
    .match-card:hover { background-color: #2C2C2E; }
    
    .team-section {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 40%;
    }
    .team-logo { width: 30px; height: 30px; object-fit: contain; }
    .team-name { font-weight: 600; font-size: 16px; }
    .score { font-size: 28px; font-weight: 700; color: #fff; }
    .score.loser { color: #94a3b8; } /* Gris si está perdiendo */
    
    .status-section {
        text-align: center;
        width: 20%;
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* Sección 'Más Tarde Hoy' */
    .section-divider {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 25px 0 10px 0;
        padding-left: 5px;
    }
    
    /* Info de Apuesta Oculta (Analytics) */
    .bet-info {
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 10px;
        padding-top: 10px;
        font-size: 11px;
        color: #10b981;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIO DE LA APP (DENTRO DEL CONTENEDOR) ---
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# Header Clon
st.markdown("""
    <div class="apple-header">
        <div class="app-title">Nuvi<span>Core</span></div>
        <button class="my-teams-btn">★ Mis Ligas</button>
    </div>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES ---
class AppleSportsEngine:
    def __init__(self):
        self.fb_key = st.secrets.get("AF_API_KEY")
        self.odds_key = st.secrets.get("ODDS_API_KEY")
        self.mx_tz = pytz.timezone('America/Mexico_City')
        
        if not self.fb_key or not self.odds_key:
            st.error("🔑 Error de Credenciales en Secrets")
            st.stop()

    def get_mx_time(self, utc_str):
        dt = datetime.fromisoformat(utc_str.replace('Z', '+00:00')).astimezone(self.mx_tz)
        return dt.strftime('%H:%M')

engine = AppleSportsEngine()

# Selector de Tiempo (Tabs)
tabs = st.tabs(["Ayer", "Hoy", "Próximos"])

with tabs[1]: # Hoy
    
    # --- DATOS DE PRUEBA (MOCK) INTEGRADOS EN LA UI ---
    # En producción, aquí haríamos fetch_live_odds()
    matches_today = [
        {
            "home": "América", "away": "Chivas", "time": "2026-03-23T03:00:00Z",
            "home_logo": "https://media.api-sports.io/football/teams/2287.png",
            "away_logo": "https://media.api-sports.io/football/teams/2289.png",
            "home_score": 2, "away_score": 1, "status": "2nd 88:15", "prob_real": 0.65, "odd": 1.90
        },
        {
            "home": "Real Madrid", "away": "Barcelona", "time": "2026-03-23T20:00:00Z",
            "home_logo": "https://media.api-sports.io/football/teams/541.png",
            "away_logo": "https://media.api-sports.io/football/teams/529.png",
            "home_score": 1, "away_score": 1, "status": "HT", "prob_real": 0.48, "odd": 2.20
        }
    ]

    for m in matches_today:
        home_loser_class = "loser" if m['home_score'] < m['away_score'] else ""
        away_loser_class = "loser" if m['away_score'] < m['home_score'] else ""
        
        st.markdown(f"""
            <div class="match-card">
                <div class="team-section">
                    <img src="{m['home_logo']}" class="team-logo">
                    <div class="team-name">{m['home']}</div>
                </div>
                <div class="score {home_loser_class}">{m['home_score']}</div>
                
                <div class="status-section">{m['status']}</div>
                
                <div class="score {away_loser_class}">{m['away_score']}</div>
                <div class="team-section" style="justify-content: flex-end;">
                    <div class="team-name">{m['away']}</div>
                    <img src="{m['away_logo']}" class="team-logo">
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Lógica Cuantitativa Oculta Elegante
        edge = m['prob_real'] - (1/m['odd'])
        if edge > 0.05:
            st.markdown(f'<div class="bet-info">💎 Sugerencia: Gana {m["home"]} (Prob: {m["prob_real"]*100:.0f}%, Cuota: {m["odd"]})</div>', unsafe_allow_html=True)

    # --- SECCIÓN MÁS TARDE HOY ---
    st.markdown('<div class="section-divider">MÁS TARDE HOY</div>', unsafe_allow_html=True)
    
    upcoming_today = [
        {
            "home": "Man City", "away": "Liverpool", "time": "2026-03-23T14:30:00Z",
            "home_logo": "https://media.api-sports.io/football/teams/50.png",
            "away_logo": "https://media.api-sports.io/football/teams/40.png"
        }
    ]
    
    for m in upcoming_today:
        time_mx = engine.get_mx_time(m['time'])
        st.markdown(f"""
            <div class="match-card">
                <div class="team-section">
                    <img src="{m['home_logo']}" class="team-logo">
                    <div class="team-name">{m['home']}</div>
                </div>
                <div class="status-section" style="font-size: 16px; color: #fff; font-weight: 700;">{time_mx}</div>
                <div class="team-section" style="justify-content: flex-end;">
                    <div class="team-name">{m['away']}</div>
                    <img src="{m['away_logo']}" class="team-logo">
                </div>
            </div>
        """, unsafe_allow_html=True)

# Cerrar Contenedor Principal
st.markdown('</div>', unsafe_allow_html=True)
