import streamlit as st
import requests
from datetime import datetime, timedelta

# Configuración de App Móvil
st.set_page_config(page_title="IA Parlay Pro", page_icon="💰", layout="centered")

# Script de Notificaciones Nativas (JavaScript)
st.components.v1.html("""
<script>
    function pedirPermiso() {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                alert("✅ ¡Notificaciones activadas!");
            }
        });
    }

    function enviarNotificacion(titulo, cuerpo) {
        if (Notification.permission === "granted") {
            new Notification(titulo, {
                body: cuerpo,
                icon: "https://cdn-icons-png.flaticon.com/512/2652/2652218.png"
            });
        }
    }
    
    // Escuchar eventos desde Streamlit
    window.parent.addEventListener('message', (event) => {
        if (event.data.type === 'NOTIFICAR') {
            enviarNotificacion(event.data.title, event.data.msg);
        }
    });
</script>
""", height=0)

# Estilo Visual
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .parlay-card { 
        background: linear-gradient(145deg, #1e2530, #161b22);
        padding: 20px; border-radius: 15px; border: 2px solid #3fb950; margin-bottom: 20px;
    }
    .odds-val { color: #3fb950; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_parlay_real():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {'apiKey': API_KEY, 'regions': 'us,eu', 'markets': 'h2h'}
    try:
        res = requests.get(url, params=params).json()
        candidatos = []
        for p in res:
            if p['bookmakers']:
                outcomes = p['bookmakers'][0]['markets'][0]['outcomes']
                fav = min(outcomes, key=lambda x: x['price'])
                candidatos.append({
                    'equipo': fav['name'], 'cuota': fav['price'], 'liga': p['sport_title']
                })
        return sorted(candidatos, key=lambda x: x['cuota'])[:5]
    except: return []

st.title("💰 IA Parlay Pro")

# Botón para activar el permiso en el Android
if st.button("🔔 Activar Notificaciones en mi Celular"):
    st.components.v1.html("<script>pedirPermiso();</script>", height=0)

if st.button("🚀 GENERAR PARLAY Y NOTIFICARME"):
    picks = obtener_parlay_real()
    if picks:
        total = 1.0
        msg_texto = ""
        for i in picks:
            total *= i['cuota']
            msg_texto += f"- {i['equipo']} "
        
        # Mostrar en pantalla
        st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
        st.write(f"### Momio Total: {total:.2f}")
        for i in picks:
            st.write(f"✅ {i['equipo']} ({i['cuota']})")
        st.markdown('</div>', unsafe_allow_html=True)

        # LANZAR NOTIFICACIÓN AL SISTEMA ANDROID
        st.components.v1.html(f"""
        <script>
            window.parent.postMessage({{
                type: 'NOTIFICAR', 
                title: '🔥 PARLAY LISTO ({total:.2f})', 
                msg: 'Picks: {msg_texto}'
            }}, '*');
        </script>
        """, height=0)
    else:
        st.error("No hay datos disponibles.")
