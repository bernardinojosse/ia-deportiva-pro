import streamlit as st
import requests

# Configuración de la App
st.set_page_config(page_title="IA DEPORTIVA: MERCADO REAL", page_icon="🎯")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .league-tag { background-color: #238636; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; }
    .team-name { font-size: 1.1rem; font-weight: bold; color: #58a6ff; }
    .odds-val { font-size: 1.2rem; font-weight: bold; color: #3fb950; }
    </style>
    """, unsafe_allow_html=True)

# Llave desde Secrets
API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_datos_reales():
    # Buscamos en todas las ligas de fútbol disponibles (soccer)
    # El parámetro 'regions=eu' suele dar las ligas más importantes
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=us,eu&markets=h2h"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return []

st.title("🎯 Cuotas Reales del Mercado")
st.write("Datos extraídos directamente de las casas de apuestas (Sin simulaciones)")

if st.button("🚀 BUSCAR PARTIDOS EN TODAS LAS LIGAS"):
    with st.spinner("Obteniendo datos reales..."):
        partidos = obtener_datos_reales()
        
        if isinstance(partidos, dict) and "msg" in partidos:
            st.error(f"Error: {partidos['msg']}")
        elif not partidos:
            st.warning("No se encontraron partidos activos en las ligas permitidas.")
        else:
            for p in partidos[:20]: # Mostramos los primeros 20 encontrados
                home_team = p['home_team']
                away_team = p['away_team']
                liga = p['sport_title']
                
                # Buscamos las cuotas del primer proveedor disponible (ej. DraftKings o BetMGM)
                bookmaker = p['bookmakers'][0] if p['bookmakers'] else None
                
                if bookmaker:
                    markets = bookmaker['markets'][0]['outcomes']
                    # Organizamos las cuotas: Local, Empate, Visita
                    odds_dict = {o['name']: o['price'] for o in markets}
                    
                    st.markdown(f"""
                    <div class="card">
                        <span class="league-tag">{liga}</span>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top:10px;">
                            <div style="width: 45%; text-align: center;">
                                <span class="team-name">{home_team}</span><br>
                                <span class="odds-val">{odds_dict.get(home_team, 'N/A')}</span>
                            </div>
                            <div style="color: #8b949e; font-weight: bold;">VS</div>
                            <div style="width: 45%; text-align: center;">
                                <span class="team-name">{away_team}</span><br>
                                <span class="odds-val">{odds_dict.get(away_team, 'N/A')}</span>
                            </div>
                        </div>
                        <div style="text-align: center; margin-top: 10px; font-size: 0.8rem; color: #8b949e;">
                            Empate: <span style="color:white;">{odds_dict.get('Draw', 'N/A')}</span> | Fuente: {bookmaker['title']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

st.sidebar.info("Esta versión muestra cuotas reales. Una cuota menor significa que ese equipo es el favorito.")
