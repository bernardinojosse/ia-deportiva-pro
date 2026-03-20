import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURACIÓN DE SISTEMA ---
st.set_page_config(page_title="NUVI-CORE OS", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* Header & Branding */
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #ff0055 0%, #ff5500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: 5px; }
    
    /* Alerta de Super Parlay (+10) */
    .alert-premium { 
        background: linear-gradient(145deg, #450000, #1a0000); 
        border: 2px solid #ff0000; border-radius: 15px; padding: 20px; 
        margin-bottom: 25px; text-align: center; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); } }

    /* Tarjetas de Partidos */
    .match-card { 
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 15px; margin-bottom: 12px;
    }
    .odd-badge { background: #00ff88; color: #000; padding: 3px 8px; border-radius: 5px; font-weight: 900; font-family: 'Orbitron'; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    .stTabs [data-baseweb="tab"] { font-family: 'Orbitron'; font-size: 0.7rem; color: #666; }
    .stTabs [aria-selected="true"] { color: #ff0055 !important; border-bottom-color: #ff0055 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS CON AUTO-REFRESH (6 HORAS) ---
API_KEY = st.secrets["ODDS_API_KEY"]

@st.cache_data(ttl=21600) # 21600 segundos = 6 Horas exactas
def fetch_global_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {'apiKey': API_KEY, 'regions': 'us,eu', 'markets': 'h2h'}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except: return []

# --- MOTOR DE PREDICCIÓN Y NOTIFICACIÓN ---
data = fetch_global_data()

def scan_super_parlay(matches):
    if not matches or not isinstance(matches, list): return None
    # Buscamos 5 partidos con cuotas medias para llegar al +10 (aprox cuotas de 1.6 a 2.0)
    picks = []
    for m in matches[:25]: # Escaneamos los primeros 25 para calidad
        if m['bookmakers']:
            outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
            fav = min(outcomes, key=lambda x: x['price'])
            if 1.5 <= fav['price'] <= 2.2: # Rango ideal para parlay agresivo pero posible
                picks.append({'name': fav['name'], 'price': fav['price']})
    
    if len(picks) >= 5:
        selected = picks[:5]
        total = 1.0
        for s in selected: total *= s['price']
        if total >= 10.0:
            return {'total': total, 'items': selected}
    return None

# --- UI: BIENVENIDA Y ALERTA ---
st.markdown('<div class="main-logo">NUVI-CORE</div>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size:0.7rem; color:#666; margin-bottom:20px;'>SISTEMA DE ANÁLISIS GLOBAL ACTUALIZADO CADA 6H</div>", unsafe_allow_html=True)

# Notificación de Super Parlay al abrir
super_parlay = scan_super_parlay(data)
if super_parlay:
    st.markdown(f"""
        <div class="alert-premium">
            <h3 style="margin:0; color:#fff; font-family:'Orbitron';">🚨 ALERTA: SUPER PARLAY DETECTADO</h3>
            <p style="color:#ff5555; font-size:0.8rem;">PROBABILIDAD DETECTADA CON CUOTA SUPERIOR A +10</p>
            <div style="font-size:2.5rem; font-weight:900; color:#fff;">x{super_parlay['total']:.2f}</div>
            <small style="color:#aaa;">Haz clic en SMART PARLAY para ver los detalles.</small>
        </div>
    """, unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["🚀 SMART PARLAY", "🔍 EXPLORER (TODO)"])

with tab1:
    if super_parlay:
        st.write("### Composición del Super Parlay")
        for item in super_parlay['items']:
            st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #222;">
                    <span><b>{item['name']}</b></span>
                    <span style="color:#00ff88;">{item['price']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Buscando combinaciones óptimas para +10... No hay parlay seguro de ese rango en este bloque de 6h.")

with tab2:
    st.markdown("### Todos los Partidos Disponibles (Global)")
    if data and isinstance(data, list):
        for p in data:
            if p['bookmakers']:
                fav = min(p['bookmakers'][0]['markets'][0]['outcomes'], key=lambda x: x['price'])
                st.markdown(f"""
                    <div class="match-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-size:0.6rem; color:#ff0055; font-weight:bold;">{p['sport_title'].upper()}</div>
                                <div style="font-weight:700;">{p['home_team']} vs {p['away_team']}</div>
                                <div style="font-size:0.8rem; color:#888;">Predicción IA: <span style="color:#fff;">{fav['name']}</span></div>
                            </div>
                            <div class="odd-badge">{fav['price']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Error al sincronizar con el nodo de datos global.")

# --- BARRA LATERAL ---
st.sidebar.markdown(f"**STATUS:** ONLINE")
st.sidebar.markdown(f"**PRÓXIMA ACTUALIZACIÓN:** En {6} horas")
st.sidebar.caption("NUVI-CORE ENGINE v6.0")
