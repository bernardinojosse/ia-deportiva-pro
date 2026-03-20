import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de la App
st.set_page_config(page_title="IA: PARLAY MAESTRO", page_icon="💰")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .parlay-card { 
        background: linear-gradient(145deg, #1e2530, #161b22);
        padding: 20px; border-radius: 15px; border: 2px solid #3fb950; margin-bottom: 25px;
    }
    .odds-val { color: #3fb950; font-weight: bold; }
    .total-gain { font-size: 1.6rem; color: #f1c40f; text-align: center; margin-top: 15px; border-top: 1px solid #333; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Llave desde Secrets (Usa la de The Odds API: aa1b6ba3...)
API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_datos_seguros():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        'apiKey': API_KEY,
        'regions': 'us,eu',
        'markets': 'h2h',
        'oddsFormat': 'decimal'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        ahora = datetime.utcnow()
        # Extendemos a 48 horas para asegurar que encuentre juegos si la zona horaria varía
        limite = ahora + timedelta(hours=48)
        
        partidos_hoy = []
        if isinstance(data, list):
            for p in data:
                p_time = datetime.strptime(p['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                if ahora <= p_time <= limite:
                    partidos_hoy.append(p)
        return partidos_hoy
    except:
        return []

st.title("💰 Parlay Real de Hoy")
st.write(f"Buscando partidos para el: **{datetime.now().strftime('%d/%m/%Y')}**")

num_picks = st.selectbox("¿Cuántos picks quieres en tu parlay?", [3, 4, 5, 8], index=2)

if st.button("🎰 GENERAR PARLAY AHORA"):
    with st.spinner("Escaneando ligas mundiales..."):
        partidos = obtener_datos_seguros()
        
        if not partidos:
            st.warning("No se detectaron partidos cercanos. La API podría estar limitada o no hay juegos en las ligas principales ahora.")
        else:
            favoritos = []
            for p in partidos:
                if p['bookmakers']:
                    outcomes = p['bookmakers'][0]['markets'][0]['outcomes']
                    fav = min(outcomes, key=lambda x: x['price'])
                    favoritos.append({
                        'equipo': fav['name'],
                        'cuota': fav['price'],
                        'liga': p['sport_title'],
                        'vs': f"{p['home_team']} vs {p['away_team']}"
                    })

            # Seleccionar los más seguros
            parlay = sorted(favoritos, key=lambda x: x['cuota'])[:num_picks]

            st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; color:#3fb950; font-weight:bold;">🏆 PARLAY SELECCIONADO</div>', unsafe_allow_html=True)
            
            total = 1.0
            for item in parlay:
                # Corregido el error de comillas que causaba el SyntaxError
                st.markdown(f"✅ **{item['equipo']}** <span class='odds-val'>{item['cuota']}</span><br><small>{item['liga']} | {item['vs']}</small><br>", unsafe_allow_html=True)
                total *= item['cuota']
            
            st.markdown(f'<div class="total-gain">MOMIO TOTAL: {total:.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
