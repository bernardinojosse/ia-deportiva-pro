import streamlit as st
import requests

# Configuración de la App
st.set_page_config(page_title="IA DEPORTIVA: PARLAYS REALES", page_icon="💰")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .parlay-card { 
        background: linear-gradient(145deg, #1e2530, #161b22);
        padding: 20px; border-radius: 15px; border: 2px solid #238636; margin-bottom: 25px;
    }
    .match-card { background-color: #161b22; padding: 12px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .team-name { color: #58a6ff; font-weight: bold; }
    .odds-val { color: #3fb950; font-weight: bold; }
    .parlay-header { color: #f1c40f; font-weight: bold; font-size: 1.5rem; text-align: center; margin-bottom: 15px; }
    .total-odds { font-size: 1.4rem; color: #f1c40f; text-align: right; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Llave desde Secrets
try:
    API_KEY = st.secrets["ODDS_API_KEY"]
except:
    st.error("⚠️ Configura 'ODDS_API_KEY' en los Secrets de Streamlit.")
    st.stop()

def obtener_datos():
    # Buscamos en todas las ligas de fútbol disponibles (soccer)
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=us,eu&markets=h2h"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return []

st.title("💰 Generador de Parlays Pro")
num_selecciones = st.slider("Número de selecciones para el parlay:", 3, 10, 5)

if st.button("🚀 GENERAR PARLAY MÁS SEGURO"):
    with st.spinner("Analizando mercados reales..."):
        datos = obtener_datos()
        
        if isinstance(datos, dict) and "msg" in datos:
            st.error(f"Error de API: {datos['msg']}")
        elif not datos:
            st.warning("No hay suficientes partidos activos.")
        else:
            # --- PROCESAMIENTO DE PARLAY ---
            lista_favoritos = []
            
            for p in datos:
                if p['bookmakers']:
                    # Obtenemos las cuotas del primer proveedor
                    outcomes = p['bookmakers'][0]['markets'][0]['outcomes']
                    # Encontramos la cuota más baja (el favorito del partido)
                    fav = min(outcomes, key=lambda x: x['price'])
                    
                    lista_favoritos.append({
                        'liga': p['sport_title'],
                        'equipo': fav['name'],
                        'cuota': fav['price'],
                        'versus': f"{p['home_team']} vs {p['away_team']}"
                    })

            # Ordenamos por cuota (de menor a mayor = más probable)
            seguros = sorted(lista_favoritos, key=lambda x: x['cuota'])[:num_selecciones]

            if len(seguros) < num_selecciones:
                st.warning(f"Solo se encontraron {len(seguros)} partidos disponibles.")

            # --- MOSTRAR PARLAY ---
            st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="parlay-header">🏆 PARLAY SUGERIDO ({len(seguros)} SELECCIONES)</div>', unsafe_allow_html=True)
            
            cuota_total = 1.0
            for item in seguros:
                st.markdown(f"""
                <div style="border-bottom: 1px solid #333; padding: 10px 0;">
                    <span style="color:#f1c40f;">●</span> <b>{item['equipo']}</b> - <span class="odds-val">{item['cuota']}</span><br>
                    <small style="color:#8b949e;">{item['liga']} | {item['versus']}</small>
                </div>
                """, unsafe_allow_html=True)
                cuota_total *= item['cuota']
            
            st.markdown(f'<div class="total-odds">MOMIO TOTAL: {cuota_total:.2f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- LISTADO GENERAL ---
            with st.expander("Ver todos los partidos analizados"):
                for p in datos[:20]:
                    st.write(f"**{p['sport_title']}**: {p['home_team']} vs {p['away_team']}")
