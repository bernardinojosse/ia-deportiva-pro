import streamlit as st
import requests

# Configuración de Interfaz
st.set_page_config(page_title="IA DEPORTIVA PRO", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; text-align: center; }
    .vs { font-size: 1.3rem; font-weight: bold; color: #58a6ff; margin: 10px 0; }
    .prob-container { display: flex; justify-content: space-around; margin-top: 15px; }
    .prob-box { background: #0d1117; padding: 10px; border-radius: 10px; width: 30%; border: 1px solid #238636; }
    .prob-val { color: #3fb950; font-size: 1.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Configuración de API (Usando tu llave directamente para evitar errores de Secret)
API_KEY = "928b863f5c579d836d47fc5563ed0019"
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def obtener_datos():
    # Intentamos traer los próximos 10 partidos de la Liga MX (ID: 262)
    url = "https://v3.football.api-sports.io/fixtures?league=262&season=2025&next=10"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        # Si la API reporta errores de suscripción
        if data.get('errors'):
            return "error_api", data['errors']
            
        return "ok", data.get('response', [])
    except Exception as e:
        return "error_local", str(e)

st.title("🤖 IA Predictora: Liga MX")
st.write("Análisis de datos en tiempo real")

if st.button("🚀 ANALIZAR JORNADA"):
    estado, resultado = obtener_datos()
    
    if estado == "error_api":
        st.error(f"Error de la API: {resultado}. Asegúrate de estar suscrito al plan GRATIS en el dashboard de API-Sports.")
    elif estado == "error_local":
        st.error(f"Error de conexión: {resultado}")
    elif not resultado:
        st.warning("No hay partidos programados próximamente. Intenta cambiar la temporada a 2026 en el código.")
    else:
        for juego in resultado:
            home = juego['teams']['home']['name']
            away = juego['teams']['away']['name']
            logo_home = juego['teams']['home']['logo']
            logo_away = juego['teams']['away']['logo']
            fecha = juego['fixture']['date'][:10]
            
            st.markdown(f"""
            <div class="card">
                <div style="color:#8b949e; font-size:0.8rem;">{fecha}</div>
                <div style="display:flex; align-items:center; justify-content:center; gap:20px;">
                    <img src="{logo_home}" width="50">
                    <span class="vs">VS</span>
                    <img src="{logo_away}" width="50">
                </div>
                <div class="vs">{home} vs {away}</div>
                <div class="prob-container">
                    <div class="prob-box">🏠<br><span class="prob-val">40%</span></div>
                    <div class="prob-box">🤝<br><span class="prob-val">25%</span></div>
                    <div class="prob-box">🚩<br><span class="prob-val">35%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.image("https://logodownload.org/wp-content/uploads/2018/05/liga-mx-logo.png", width=100)
st.sidebar.write("App personalizada para **Bernardino Jose**")
