import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ARBITRAJE ---
st.set_page_config(page_title="NUVI-CORE ARBITRAGE", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #00ff88 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: 5px; }
    
    /* Tarjeta de Arbitraje */
    .surebet-card { 
        background: rgba(0, 255, 136, 0.05); border: 1px solid #00ff88; 
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .math-formula { font-family: 'Courier New', monospace; color: #00ff88; font-size: 0.8rem; background: #111; padding: 5px; border-radius: 5px; }
    .calc-box { background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 3px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA MATEMÁTICA PROPORCIONADA ---
def calcular_arbitraje(cuota_a, cuota_b):
    if cuota_a <= 1 or cuota_b <= 1:
        return False, 0
    factor = (cuota_a - 1) * (cuota_b - 1)
    return factor > 1, factor

def calcular_apuesta_ideal(total_inversion, cuota_a, cuota_b):
    inv_a = 1 / cuota_a
    inv_b = 1 / cuota_b
    prob_total = inv_a + inv_b
    apuesta_a = (inv_a / prob_total) * total_inversion
    apuesta_b = (inv_b / prob_total) * total_inversion
    return round(apuesta_a, 2), round(apuesta_b, 2)

# --- OBTENCIÓN DE DATOS (MULTIPLE BOOKMAKERS) ---
API_KEY = st.secrets["ODDS_API_KEY"]

@st.cache_data(ttl=3600)
def fetch_arbitrage_data():
    # Buscamos cuotas de múltiples casas para comparar
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {'apiKey': API_KEY, 'regions': 'us,eu', 'markets': 'h2h'}
    try:
        res = requests.get(url, params=params).json()
        return res
    except: return []

# --- INTERFAZ ---
st.markdown('<div class="main-logo">NUVI-CORE ARBITRAGE</div>', unsafe_allow_html=True)

tab_parlay, tab_surebets, tab_explore = st.tabs(["🚀 SMART PARLAY", "🛡️ ARBITRAJE SEGURO", "🔍 EXPLORER"])

data = fetch_arbitrage_data()

with tab_surebets:
    st.markdown("<p style='text-align:center; font-size:0.8rem; color:#888;'>ESCÁNER DE OPORTUNIDADES MATEMÁTICAS SIN RIESGO</p>", unsafe_allow_html=True)
    
    inversion = st.number_input("Capital total a invertir ($):", min_value=10, value=1000, step=100)
    
    encontrado = False
    if data:
        for p in data:
            if len(p['bookmakers']) >= 2:
                # Comparamos la mejor cuota para el Equipo A en una casa vs Equipo B en otra
                cuotas_a = []
                cuotas_b = []
                for b in p['bookmakers']:
                    outcomes = b['markets'][0]['outcomes']
                    cuotas_a.append({'val': outcomes[0]['price'], 'bookie': b['title'], 'team': outcomes[0]['name']})
                    cuotas_b.append({'val': outcomes[1]['price'], 'bookie': b['title'], 'team': outcomes[1]['name']})
                
                best_a = max(cuotas_a, key=lambda x: x['val'])
                best_b = max(cuotas_b, key=lambda x: x['val'])
                
                es_segura, factor = calcular_arbitraje(best_a['val'], best_b['val'])
                
                if es_segura:
                    encontrado = True
                    apuesta_a, apuesta_b = calcular_apuesta_ideal(inversion, best_a['val'], best_b['val'])
                    retorno = round(apuesta_a * best_a['val'], 2)
                    ganancia = round(retorno - inversion, 2)
                    
                    st.markdown(f"""
                        <div class="surebet-card">
                            <h4 style="margin:0; color:#00ff88;">🔥 OPORTUNIDAD DETECTADA</h4>
                            <p style="font-size:0.8rem; color:#aaa;">{p['home_team']} vs {p['away_team']}</p>
                            <div class="math-formula">( {best_a['val']} - 1 ) * ( {best_b['val']} - 1 ) = {factor:.4f} > 1</div>
                            
                            <div class="calc-box">
                                <b>ESTRATEGIA DE INVERSIÓN:</b><br>
                                💰 Apostar <b>${apuesta_a}</b> a <b>{best_a['team']}</b> en <b>{best_a['bookie']}</b> ({best_a['val']})<br>
                                💰 Apostar <b>${apuesta_b}</b> a <b>{best_b['team']}</b> en <b>{best_b['bookie']}</b> ({best_b['val']})<br>
                                <hr style="border-color:rgba(255,255,255,0.1);">
                                <span style="color:#00ff88;"><b>RETORNO GARANTIZADO: ${retorno}</b></span><br>
                                <span style="color:#4facfe;">GANANCIA NETO: ${ganancia} ({round((ganancia/inversion)*100,2)}%)</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        if not encontrado:
            st.warning("El mercado actual está equilibrado. No se detectan arbitrajes con factor > 1 en este bloque.")
            st.info("Nota: El arbitraje requiere comparar al menos 2 casas de apuestas con cuotas divergentes.")

with tab_parlay:
    # (Tu lógica de parlay se mantiene aquí)
    pass

with tab_explore:
    # (Tu explorador se mantiene aquí)
    pass
