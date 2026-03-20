import streamlit as st
import requests
import os

# Configuración profesional
st.set_page_config(page_title="IA DEPORTIVA PRO", page_icon="⚽")

# Estilo visual tipo App
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .vs { font-size: 1.2rem; font-weight: bold; color: #58a6ff; }
    .prob { font-size: 1.5rem; color: #3fb950; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Configuración de API
API_KEY = st.secrets["SPORTS_API_KEY"]
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def obtener_partidos():
    # Buscamos partidos de la Liga MX (ID: 262) para la temporada 2025/2026
    url = "https://v3.football.api-sports.io/fixtures?league=262&season=2025&next=10"
    try:
        response = requests.get(url, headers=HEADERS)
        return response.json().get('response', [])
    except:
        return []

st.title("🤖 IA Predictora Liga MX")
st.write("Análisis de próximos encuentros")

if st.button("🔄 CARGAR PRÓXIMOS JUEGOS"):
    partidos = obtener_partidos()
    
    if not partidos:
        st.warning("No se encontraron partidos próximos. Revisa si tu API Key está activa en el plan Free.")
    else:
        for juego in partidos:
            home = juego['teams']['home']['name']
            away = juego['teams']['away']['name']
            fecha = juego['fixture']['date'][:10]
            
            # Simulamos el cálculo de la IA basado en el estado de forma (Placeholder inteligente)
            # En un plan Pro, aquí llamaríamos al endpoint de /predictions
            st.markdown(f"""
            <div class="card">
                <div style="text-align:center;">
                    <span style="color:#8b949e;">{fecha}</span><br>
                    <span class="vs">{home} VS {away}</span>
                </div>
                <hr style="border: 0.5px solid #30363d;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div><p style="margin:0;">Local</p><span class="prob">45%</span></div>
                    <div><p style="margin:0;">Empate</p><span class="prob">25%</span></div>
                    <div><p style="margin:0;">Visita</p><span class="prob">30%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write("Desarrollado para: **Bernardino Jose**")
