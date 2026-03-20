import streamlit as st
import requests
import os
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA DEPORTIVA MX", page_icon="⚽", layout="wide")

# Estilos para que parezca una App móvil profesional
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card { background-color: #161b22; padding: 15px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .metric { color: #238636; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
API_KEY = "928b863f5c579d836d47fc5563ed0019"
URL = "https://v3.football.api-sports.io/predictions?league=262&season=2025"
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def cargar_predicciones():
    try:
        res = requests.get(URL, headers=HEADERS)
        return res.json()['response']
    except:
        return []

# --- INTERFAZ ---
st.title("🤖 IA Predictora Liga MX")
st.write("Análisis estadístico basado en Machine Learning")

if st.button("🚀 ACTUALIZAR ANÁLISIS"):
    datos = cargar_predicciones()
    
    if not datos:
        st.error("No hay partidos próximos o error de conexión.")
    else:
        for partido in datos:
            home = partido['teams']['home']['name']
            away = partido['teams']['away']['name']
            prob = partido['predictions']['percent']
            consejo = partido['predictions']['advice']
            
            # Tarjeta de Partido
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3 style='margin-bottom:0;'>{home} vs {away}</h3>
                    <p style='color:#8b949e;'>Recomendación: <b>{consejo}</b></p>
                    <div style='display: flex; justify-content: space-around; text-align: center;'>
                        <div><p>Local</p><span class="metric">{prob['home']}</span></div>
                        <div><p>Empate</p><span class="metric">{prob['draw']}</span></div>
                        <div><p>Visita</p><span class="metric">{prob['away']}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.sidebar.info("Esta IA analiza más de 20 variables estadísticas por equipo.")
