import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="IA DEPORTIVA REAL-TIME", page_icon="⚡")

# Estilo Profesional Oscuro
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    .team-name { font-size: 1.1rem; font-weight: bold; color: #58a6ff; }
    .live-badge { background-color: #238636; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = "928b863f5c579d836d47fc5563ed0019"
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def obtener_datos_vivos():
    # Intentamos traer partidos de HOY de cualquier liga disponible en tu plan
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data.get('response', [])
    except:
        return []

st.title("⚽ IA Deportiva en Vivo")
st.write(f"Datos actualizados: {datetime.now().strftime('%H:%M:%S')}")

if st.button("📡 ACTIVAR RADAR EN TIEMPO REAL"):
    partidos_live = obtener_datos_vivos()
    
    if not partidos_live:
        st.info("Buscando partidos en juego... Si no hay en vivo, mostraré los próximos de la liga disponible.")
        # Fallback a próximos partidos de una liga abierta (Liga de Brasil o USA suelen estar libres)
        url_next = "https://v3.football.api-sports.io/fixtures?league=71&season=2024&next=5" 
        partidos_live = requests.get(url_next, headers=HEADERS).json().get('response', [])

    if not partidos_live:
        st.error("Tu API_KEY gratuita tiene restricciones de temporada. ¿Deseas probar con una liga alternativa?")
    else:
        for p in partidos_live:
            home = p['teams']['home']
            away = p['teams']['away']
            status = p['fixture']['status']['short']
            goals_h = p['goals']['home']
            goals_a = p['goals']['away']
            
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <span class="live-badge">{status}</span>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top:10px;">
                        <div style="text-align: center; width: 40%;">
                            <img src="{home['logo']}" width="40"><br>
                            <span class="team-name">{home['name']}</span>
                        </div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{goals_h if goals_h is not None else 0} - {goals_a if goals_a is not None else 0}</div>
                        <div style="text-align: center; width: 40%;">
                            <img src="{away['logo']}" width="40"><br>
                            <span class="team-name">{away['name']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.sidebar.warning("Nota: El plan gratuito limita las ligas top en tiempo real.")
