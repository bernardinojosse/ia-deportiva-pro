import streamlit as st
import requests
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="IA DEPORTIVA: NCAAM", page_icon="🏀")

# Estilo visual premium (Fondo oscuro y tarjetas azules)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .card { 
        background-color: #161b22; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 5px solid #0056b3; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .team-name { font-size: 1.1rem; font-weight: bold; color: #ffffff; }
    .vs { color: #58a6ff; font-weight: bold; font-size: 0.9rem; }
    .prob-bar { background-color: #30363d; border-radius: 5px; height: 10px; margin: 10px 0; }
    .prob-fill { background-color: #238636; height: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Cargar API KEY desde Secrets de Streamlit
# Asegúrate de que el nombre sea EXACTAMENTE 'SPORTS_API_KEY'
try:
    API_KEY = st.secrets["SPORTS_API_KEY"]
except:
    st.error("⚠️ No se encontró la llave 'SPORTS_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# Sportradar usa el formato AAAA/MM/DD
FECHA_HOY = datetime.now().strftime("%Y/%m/%d")

def obtener_calendario_ncaa():
    # Endpoint para Baloncesto Universitario (NCAAM) v8
    url = f"https://api.sportradar.us/ncaam/trial/v8/en/games/{FECHA_HOY}/schedule.json"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('games', [])
        elif response.status_code == 403:
            st.error("🚫 Error 403: Tu llave no tiene permiso para NCAAM o expiró.")
            return []
        else:
            st.warning(f"Aviso: La API respondió con código {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

# --- INTERFAZ PRINCIPAL ---
st.title("🏀 IA Predictora NCAAM")
st.subheader(f"Jornada: {datetime.now().strftime('%d/%m/%Y')}")

if st.button("🚀 ANALIZAR PARTIDOS DE HOY"):
    with st.spinner("Consultando Sportradar..."):
        partidos = obtener_calendario_ncaa()
        
        if not partidos:
            st.info("No hay partidos programados para hoy en el sistema de Sportradar.")
        else:
            for juego in partidos:
                home = juego['home']['name']
                away = juego['away']['name']
                status = juego.get('status', 'Programado')
                
                # Diseño de la tarjeta de predicción
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="width: 40%; text-align: left;">
                            <span class="team-name">{away}</span><br>
                            <span style="font-size: 0.8rem; color: #8b949e;">Visitante</span>
                        </div>
                        <div class="vs">VS</div>
                        <div style="width: 40%; text-align: right;">
                            <span class="team-name">{home}</span><br>
                            <span style="font-size: 0.8rem; color: #8b949e;">Local</span>
                        </div>
                    </div>
                    <div class="prob-bar"><div class="prob-fill" style="width: 60%;"></div></div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                        <span style="color: #ff4b4b;">Prob. {away}: 40%</span>
                        <span style="color: #3fb950;">Prob. {home}: 60%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write("⚡ **Modo:** Sportradar Trial")
st.sidebar.write(f"📅 **Fecha API:** {FECHA_HOY}")
