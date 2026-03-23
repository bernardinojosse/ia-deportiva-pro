import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NuviCore Sports", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MAESTRO (FIX DE VISIBILIDAD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Forzar fondo negro en toda la app */
    .stApp {
        background-color: #000000 !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* Contenedor central tipo iPhone */
    .app-container {
        max-width: 500px;
        margin: 0 auto;
        background-color: #000000;
        min-height: 100vh;
    }

    /* Header NuviCore */
    .apple-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 10px;
    }
    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }

    /* Tabs Estilo Apple */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #ffffff !important;
    }

    /* Tarjetas de Partidos */
    .match-card {
        background-color: #1C1C1E;
        border-radius: 14px;
        padding: 16px;
        margin: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .team-box {
        display: flex;
        align-items: center;
        gap: 12px;
        width: 35%;
    }
    .team-logo { width: 32px; height: 32px; }
    .team-name { font-weight: 600; font-size: 15px; color: #fff; }
    
    .score { font-size: 26px; font-weight: 700; color: #fff; width: 10%; text-align: center; }
    
    .status-box {
        width: 20%;
        text-align: center;
        color: #8E8E93;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* Divider */
    .section-title {
        color: #8E8E93;
        font-size: 12px;
        font-weight: 700;
        padding: 20px 15px 10px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
mx_tz = pytz.timezone('America/Mexico_City')

# --- UI RENDER ---
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="apple-header">
        <div class="app-title">NuviCore</div>
        <div style="color: #fff; background: #333; padding: 5px 12px; border-radius: 20px; font-size: 12px;">★ Ligas</div>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["Hoy", "Próximos"])

with tabs[0]:
    # Partidos de ejemplo para que veas el diseño funcionando
    matches = [
        {
            "home": "América", "home_logo": "https://media.api-sports.io/football/teams/2287.png", "home_score": 3,
            "away": "Chivas", "away_logo": "https://media.api-sports.io/football/teams/2289.png", "away_score": 1,
            "status": "Final"
        },
        {
            "home": "Real Madrid", "home_logo": "https://media.api-sports.io/football/teams/541.png", "home_score": 0,
            "away": "Barcelona", "away_logo": "https://media.api-sports.io/football/teams/529.png", "away_score": 0,
            "status": "2nd 65:10"
        }
    ]

    for m in matches:
        st.markdown(f"""
            <div class="match-card">
                <div class="team-box">
                    <img src="{m['home_logo']}" class="team-logo">
                    <span class="team-name">{m['home']}</span>
                </div>
                <div class="score">{m['home_score']}</div>
                <div class="status-box">{m['status']}</div>
                <div class="score">{m['away_score']}</div>
                <div class="team-box" style="justify-content: flex-end;">
                    <span class="team-name">{m['away']}</span>
                    <img src="{m['away_logo']}" class="team-logo">
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Más tarde hoy</div>', unsafe_allow_html=True)
    
    # Ejemplo de partido por empezar
    st.markdown(f"""
        <div class="match-card">
            <div class="team-box">
                <img src="https://media.api-sports.io/football/teams/50.png" class="team-logo">
                <span class="team-name">Man City</span>
            </div>
            <div class="status-box" style="width: 30%; color: #fff; font-size: 16px;">14:30</div>
            <div class="team-box" style="justify-content: flex-end;">
                <span class="team-name">Liverpool</span>
                <img src="https://media.api-sports.io/football/teams/40.png" class="team-logo">
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
