import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de la App
st.set_page_config(page_title="IA: PARLAY DEL DÍA", page_icon="📅")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .parlay-card { 
        background: linear-gradient(145deg, #1e2530, #161b22);
        padding: 20px; border-radius: 15px; border: 2px solid #f1c40f; margin-bottom: 25px;
    }
    .match-tag { font-size: 0.8rem; color: #8b949e; }
    .odds-val { color: #3fb950; font-weight: bold; }
    .total-gain { font-size: 1.5rem; color: #f1c40f; text-align: center; margin-top: 15px; border-top: 1px dashed #333; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Llave desde Secrets
API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_partidos_hoy():
    # Definimos el rango de tiempo: Desde ahora hasta mañana a esta misma hora (24h)
    ahora = datetime.utcnow().isoformat() + 'Z'
    mañana = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        'apiKey': API_KEY,
        'regions': 'us,eu',
        'markets': 'h2h',
        'commenceTimeFrom': ahora,
        'commenceTimeTo': mañana
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

st.title("💰 Parlay de Hoy")
st.write(f"Análisis exclusivo para la jornada del: **{datetime.now().strftime('%d/%m/%Y')}**")

num_pick = st.select_slider("Selecciona cuántos fijos quieres en tu parlay:", options=[3, 4, 5, 6])

if st.button("🎰 GENERAR PARLAY DE HOY"):
    with st.spinner("Filtrando los partidos más seguros de hoy..."):
        datos = obtener_partidos_hoy()
        
        if not datos or isinstance(datos, dict):
            st.warning("No se encontraron partidos suficientes para las próximas 24 horas.")
        else:
            # Procesar solo favoritos de hoy
            hoy_favoritos = []
            for p in datos:
                if p['bookmakers']:
                    outcomes = p['bookmakers'][0]['markets'][0]['outcomes']
                    fav = min(outcomes, key=lambda x: x['price'])
                    
                    hoy_favoritos.append({
                        'liga': p['sport_title'],
                        'equipo': fav['name'],
                        'cuota': fav['price'],
                        'hora': p['commence_time'].split('T')[1][:5],
                        'vs': f"{p['home_team']} vs {p['away_team']}"
                    })

            # Seleccionamos los más seguros (cuotas más bajas) de hoy
            parlay_hoy = sorted(hoy_favoritos, key=lambda x: x['cuota'])[:num_pick]

            if len(parlay_hoy) < num_pick:
                st.info(f"Solo hay {len(parlay_hoy)} partidos seguros disponibles para hoy.")

            # Mostrar Parlay
            st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-weight:bold; color:#f1c40f;">🏆 PARLAY 100% MERCADO - {len(parlay_hoy)} SELECCIONES</div><br>', unsafe_allow_html=True)
            
            momio_total = 1.0
            for pick in parlay_hoy:
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <span class="match-tag">{pick['liga']} | {pick['hora']} UTC</span><br>
                    <b>{pick['equipo']}</b> gana a <span class="odds-val">{pick['cuota']}</span><br>
                    <small>{pick['vs']}</small>
                </div>
                """, unsafe_allow_html=True)
                momio_total *= pick['cuota']
            
            st.markdown(f'<div class="total-gain">MOMIO TOTAL: {momio_total:.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write("Nota: Este filtro solo muestra partidos que inician en las próximas 24 horas.")
