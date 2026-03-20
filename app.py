import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de la App
st.set_page_config(page_title="IA: EL PARLAY DE LAS 5 GRANDES", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .parlay-card { 
        background: linear-gradient(145deg, #1e2530, #161b22);
        padding: 20px; border-radius: 15px; border: 2px solid #f1c40f; margin-bottom: 25px;
    }
    .odds-val { color: #3fb950; font-weight: bold; }
    .total-gain { font-size: 1.6rem; color: #f1c40f; text-align: center; margin-top: 15px; border-top: 1px solid #333; padding-top: 10px; }
    .league-label { background-color: #30363d; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# Llave desde Secrets (The Odds API)
API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_datos_multiliga():
    # Buscamos en 'soccer' general que abarca las ligas principales disponibles
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
        
        # Filtrar solo partidos de hoy (próximas 24-36 horas)
        ahora = datetime.utcnow()
        limite = ahora + timedelta(hours=36)
        
        partidos_validos = []
        if isinstance(data, list):
            for p in data:
                p_time = datetime.strptime(p['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
                if ahora <= p_time <= limite:
                    partidos_validos.append(p)
        return partidos_validos
    except:
        return []

st.title("🏆 Super Parlay: Top 5 Ligas")
st.write(f"Escaneando las ligas más importantes para hoy: **{datetime.now().strftime('%d/%m/%Y')}**")

if st.button("🎰 GENERAR PARLAY DE ALTA PROBABILIDAD"):
    with st.spinner("Analizando mercados europeos y americanos..."):
        partidos = obtener_datos_multiliga()
        
        if not partidos:
            st.warning("No se encontraron partidos suficientes en las ligas principales para las próximas 24 horas.")
        else:
            candidatos = []
            for p in partidos:
                if p['bookmakers']:
                    outcomes = p['bookmakers'][0]['markets'][0]['outcomes']
                    # El favorito es el de menor cuota
                    fav = min(outcomes, key=lambda x: x['price'])
                    
                    candidatos.append({
                        'equipo': fav['name'],
                        'cuota': fav['price'],
                        'liga': p['sport_title'],
                        'vs': f"{p['home_team']} vs {p['away_team']}"
                    })

            # Seleccionar los 5 más seguros de TODAS las ligas escaneadas
            parlay_final = sorted(candidatos, key=lambda x: x['cuota'])[:5]

            # --- MOSTRAR RESULTADO ---
            st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; color:#f1c40f; font-weight:bold; font-size:1.2rem;">💰 PARLAY DEL DÍA (5 PICKS)</div><br>', unsafe_allow_html=True)
            
            momio_total = 1.0
            for item in parlay_final:
                st.markdown(f"""
                <div style="margin-bottom:12px; border-bottom:1px solid #222; padding-bottom:8px;">
                    <span class="league-label">{item['liga']}</span><br>
                    ✅ <b>{item['equipo']}</b> <span class='odds-val'>{item['cuota']}</span><br>
                    <small style='color:#8b949e;'>{item['vs']}</small>
                </div>
                """, unsafe_allow_html=True)
                momio_total *= item['cuota']
            
            st.markdown(f'<div class="total-gain">MOMIO TOTAL: {momio_total:.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Esta IA analiza simultáneamente la Premier League, La Liga, Serie A, Bundesliga, Liga MX y MLS.")
