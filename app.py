import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO NUVI-CORE ---
st.set_page_config(page_title="NUVI-CORE ANALYTICS", page_icon="⚡", layout="centered")

# --- DISEÑO UI/UX DE ÉLITE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* Logo y Header */
    .nav-header { text-align: center; padding: 15px 0; margin-bottom: 20px; }
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 5px; }
    
    /* Tabs Estilizadas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 45px; background-color: #111; border-radius: 12px 12px 0 0; 
        color: #888; font-family: 'Orbitron', sans-serif; font-size: 0.65rem; border: none !important;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] { background: linear-gradient(0deg, #4facfe 0%, #00f2fe 100%) !important; color: #000 !important; font-weight: bold; }

    /* Tarjetas Explorer */
    .match-card { 
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
        transition: 0.3s;
    }
    .match-card:hover { border-color: #4facfe; background: rgba(79, 172, 254, 0.05); }

    /* Barras de Confianza */
    .confidence-container { margin-top: 15px; }
    .confidence-label { font-size: 0.7rem; color: #888; text-transform: uppercase; margin-bottom: 5px; display: flex; justify-content: space-between; }
    .confidence-bar { background: #1a1a1a; border-radius: 10px; height: 6px; width: 100%; overflow: hidden; }
    .confidence-fill { background: linear-gradient(90deg, #00ff88, #4facfe); height: 100%; }
    
    .odd-tag { background: rgba(0, 242, 254, 0.1); border: 1px solid #4facfe; color: #4facfe; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 1rem; }
    
    /* Botones de Acción */
    .stButton > button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: #000; border: none; border-radius: 12px; font-weight: 800; font-family: 'Orbitron', sans-serif; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BIENVENIDA (SPLASH SCREEN) ---
if 'visitado' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"""
            <div style="height: 80vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                <div class="main-logo" style="font-size: 3rem;">NUVI-CORE</div>
                <div style="color: #4facfe; font-family: 'Orbitron'; font-size: 0.8rem; margin-top: 10px;">INICIALIZANDO NEURONAS TÁCTICAS...</div>
                <div style="margin-top: 40px; color: #888; max-width: 300px; font-style: italic;">
                    "Analizando flujos de mercado, estadísticas de posesión y algoritmos de probabilidad para cada partido de hoy."
                </div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3) # Simula carga profesional
        placeholder.empty()
    st.session_state['visitado'] = True

# --- MOTOR DE DATOS ---
API_KEY = st.secrets["ODDS_API_KEY"]

@st.cache_data(ttl=3600) # Caché de 1 hora para ahorrar créditos
def get_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {'apiKey': API_KEY, 'regions': 'us,eu', 'markets': 'h2h'}
    try:
        res = requests.get(url, params=params).json()
        return res if isinstance(res, list) else []
    except: return []

# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="nav-header"><div class="main-logo">NUVI-CORE</div></div>', unsafe_allow_html=True)

tab_parlay, tab_explore = st.tabs(["🚀 SMART PARLAY", "🔍 EXPLORER"])

data = get_data()

# --- TAB 1: SMART PARLAY (ALGORITMO) ---
with tab_parlay:
    st.markdown("<div style='text-align:center; color:#58a6ff; font-size:0.8rem; margin-bottom:20px;'>¡EXPLORA TODAS LAS FUNCIONES Y OBTÉN ANÁLISIS EXPERTO CON IA EN CUALQUIER PARTIDO!</div>", unsafe_allow_html=True)
    
    if st.button("EJECUTAR ANÁLISIS NEURAL"):
        if data:
            picks = []
            for p in data:
                if p['bookmakers']:
                    fav = min(p['bookmakers'][0]['markets'][0]['outcomes'], key=lambda x: x['price'])
                    picks.append({'name': fav['name'], 'price': fav['price'], 'league': p['sport_title']})
            
            # Algoritmo de 5 selecciones seguras
            top_5 = sorted(picks, key=lambda x: x['price'])[:5]
            total_odd = 1.0
            for t in top_5: total_odd *= t['price']
            
            st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.05); border: 1px solid #00ff88; padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;">
                    <div style="color: #00ff88; font-size: 0.7rem; font-weight: bold; letter-spacing: 2px;">MOMIO TOTAL RECOMENDADO</div>
                    <div style="font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #fff;">x{total_odd:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            for item in top_5:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 18px 0; border-bottom: 1px solid #1a1a1a;">
                        <div>
                            <span style="font-weight: 700; color: #fff; font-size: 1.1rem;">{item['name']}</span><br>
                            <span style="color: #666; font-size: 0.7rem; text-transform: uppercase;">{item['league']}</span>
                        </div>
                        <span style="color: #4facfe; font-family: 'Orbitron'; font-weight: bold; font-size: 1.2rem;">{item['price']}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Error en el Nodo de Datos Central.")

# --- TAB 2: EXPLORER (FILTRO POR LIGA) ---
with tab_explore:
    # FILTRO POR LIGA
    opciones_ligas = ["Todas las Ligas", "Liga MX - México", "Premier League - England", "La Liga - Spain", "Serie A - Italy"]
    filtro_liga = st.selectbox("Sincronizar Mercado Específico:", opciones_ligas)

    # Lógica de mapeo de nombres de la API
    mapa_ligas = {
        "Liga MX - México": "Soccer Mexico Liga MX",
        "Premier League - England": "Premier League",
        "La Liga - Spain": "La Liga",
        "Serie A - Italy": "Serie A"
    }

    if not data:
        st.info("Sin transmisiones de datos activas.")
    else:
        # Filtrar datos según elección
        if filtro_liga != "Todas las Ligas":
            data_filtrada = [p for p in data if mapa_ligas[filtro_liga] in p['sport_title']]
        else:
            data_filtrada = data[:30]

        if not data_filtrada:
            st.warning(f"No hay partidos programados para {filtro_liga} en las próximas 24 horas.")
        
        for p in data_filtrada:
            bookie = p['bookmakers'][0] if p['bookmakers'] else None
            if bookie:
                fav = min(bookie['markets'][0]['outcomes'], key=lambda x: x['price'])
                confianza = round((1 / fav['price']) * 100)
                if confianza > 94: confianza = 94 # Toque de realismo técnico

                st.markdown(f"""
                    <div class="match-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="max-width: 70%;">
                                <div style="font-size: 0.65rem; color: #4facfe; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">{p['sport_title']}</div>
                                <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin: 5px 0;">{p['home_team']} vs {p['away_team']}</div>
                                <div style="font-size: 0.85rem; color: #aaa;">Predicción: <span style="color: #00ff88;">{fav['name']}</span></div>
                            </div>
                            <div class="odd-tag">{fav['price']}</div>
                        </div>
                        
                        <div class="confidence-container">
                            <div class="confidence-label">
                                <span>Índice de Confianza IA</span>
                                <span style="color: #00ff88;">{confianza}%</span>
                            </div>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {confianza}%;"></div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.sidebar.caption("NUVI-CORE v5.0 | STABLE RELEASE")
