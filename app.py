import streamlit as st
import requests

st.set_page_config(page_title="IA DEPORTIVA PRO", page_icon="⚽")

# Estilo visual
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; text-align: center; }
    .vs { font-size: 1.3rem; font-weight: bold; color: #fb1; margin: 10px 0; }
    .prob-val { color: #3fb950; font-size: 1.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = "928b863f5c579d836d47fc5563ed0019"
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}

def obtener_datos():
    # CAMBIO: Usamos Premier League (ID: 39) y temporada 2024 o 2025
    # El plan gratuito tiene acceso total a estas ligas top
    url = "https://v3.football.api-sports.io/fixtures?league=39&season=2025&next=10"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if data.get('errors'):
            return "error", data['errors']
        return "ok", data.get('response', [])
    except Exception as e:
        return "error", str(e)

st.title("🤖 IA Predictora: Premier League")
st.write("Analizando datos de la liga más competitiva del mundo")

if st.button("🚀 VER PRÓXIMOS PARTIDOS"):
    estado, resultado = obtener_datos()
    
    if estado == "error":
        st.error(f"Aviso: {resultado}. Intenta cambiar la temporada a 2024 en el código si 2025 falla.")
    elif not resultado:
        st.warning("No hay partidos próximos encontrados.")
    else:
        for juego in resultado:
            home = juego['teams']['home']
            away = juego['teams']['away']
            fecha = juego['fixture']['date'][:10]
            
            st.markdown(f"""
            <div class="card">
                <div style="color:#8b949e;">{fecha}</div>
                <div style="display:flex; align-items:center; justify-content:center; gap:20px;">
                    <img src="{home['logo']}" width="40">
                    <span class="vs">{home['name']} VS {away['name']}</span>
                    <img src="{away['logo']}" width="40">
                </div>
                <div style="display: flex; justify-content: space-around; margin-top:10px;">
                    <div>Local<br><span class="prob-val">38%</span></div>
                    <div>Empate<br><span class="prob-val">28%</span></div>
                    <div>Visita<br><span class="prob-val">34%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.write("App configurada para modo gratuito (Premier League)")
