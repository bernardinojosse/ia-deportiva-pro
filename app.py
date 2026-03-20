import streamlit as st
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE APP PREMIUM ---
st.set_page_config(page_title="IA Parlay Maestro", page_icon="📈", layout="centered")

# --- DISEÑO VISUAL AVANZADO (CSS) ---
# Fondo oscuro, fuentes limpias, tarjetas con bordes neón y degradados.
st.markdown("""
    <style>
    /* Fondo General y Texto Base */
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Título y Header */
    .premium-title { font-size: 2.2rem; font-weight: 800; color: #ffffff; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; }
    .premium-subtitle { font-size: 1rem; color: #58a6ff; text-align: center; margin-bottom: 25px; font-weight: 300; }
    .eslogan { font-size: 0.9rem; color: #8b949e; text-align: center; margin-bottom: 25px; padding: 0 10px; font-style: italic;}

    /* Tarjeta Principal de Parlay */
    .parlay-card { 
        background: linear-gradient(145deg, #1c2128, #161b22);
        padding: 25px; border-radius: 15px; 
        border: 1px solid #30363d; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        border-left: 5px solid #00D2FF; /* Azul Cyan Profesional */
        margin-bottom: 25px;
    }
    .momio-header { font-size: 1.2rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
    .momio-value { font-size: 2.8rem; font-weight: 800; color: #f1c40f; margin-top: -10px; } /* Oro */

    /* Selección Individual */
    .pick-item { border-bottom: 1px solid #2a2f37; padding: 12px 0; display: flex; justify-content: space-between; align-items: center; }
    .pick-equipo { font-weight: 700; color: #ffffff; font-size: 1.1rem; }
    .pick-liga { font-size: 0.8rem; color: #8b949e; text-transform: uppercase;}
    .pick-cuota { font-size: 1.1rem; font-weight: 700; color: #00D2FF; }

    /* Botones Estilizados */
    .stButton > button {
        background-color: #1f242d; color: #fff; border-radius: 8px; border: 1px solid #30363d;
        width: 100%; font-weight: 700; text-transform: uppercase; transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2a313d; border-color: #00D2FF; color: #00D2FF; box-shadow: 0 0 10px rgba(0,210,255,0.3);
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT DE NOTIFICACIONES ---
st.components.v1.html("""
<script>
    function pedirPermiso() {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                // Notificación de confirmación
                new Notification("✅ Notificaciones Activadas", {
                    body: "Recibirás los próximos parlays seguros.",
                    icon: "https://cdn-icons-png.flaticon.com/512/2652/2652218.png"
                });
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
    window.parent.addEventListener('message', (event) => {
        if (event.data.type === 'NOTIFICAR') {
            enviarNotificacion(event.data.title, event.data.msg);
        }
    });
</script>
""", height=0)

# Llave desde Secrets (The Odds API)
API_KEY = st.secrets["ODDS_API_KEY"]

def obtener_parlay_profesional():
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

# --- INTERFAZ MAESTRA ---
st.markdown('<div class="premium-title">PARLAY MAESTRO</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Expert AI Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="eslogan">¡Explora todas las funciones y obtén análisis experto con IA en cualquier partido!</div>', unsafe_allow_html=True)

# Botones de Acción
if st.button("🔔 ACTIVAR NOTIFICACIONES NATIVAS"):
    st.components.v1.html("<script>pedirPermiso();</script>", height=0)

if st.button("🚀 GENERAR PARLAY DEL DÍA"):
    with st.spinner("Analizando mercados globales..."):
        picks = obtener_parlay_profesional()
        if picks:
            total = 1.0
            for i in picks: total *= i['cuota']
            
            # --- MOSTRAR RESULTADO PREMIUM ---
            st.markdown('<div class="parlay-card">', unsafe_allow_html=True)
            st.markdown('<div class="momio-header">MOMIO TOTAL SUGERIDO</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="momio-value">{total:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<hr style="border-top:1px solid #30363d; margin:20px 0;">', unsafe_allow_html=True)
            
            msg_texto = ""
            for i in picks:
                st.markdown(f"""
                <div class="pick-item">
                    <div>
                        <span class="pick-equipo">{i['equipo']}</span><br>
                        <span class="pick-liga">{i['liga']}</span>
                    </div>
                    <span class="pick-cuota">{i['cuota']}</span>
                </div>
                """, unsafe_allow_html=True)
                msg_texto += f"- {i['equipo']} "
            st.markdown('</div>', unsafe_allow_html=True)

            # --- LANZAR NOTIFICACIÓN ---
            st.components.v1.html(f"""
            <script>
                window.parent.postMessage({{
                    type: 'NOTIFICAR', 
                    title: '📈 PARLAY MAESTRO ({total:.2f})', 
                    msg: 'Picks: {msg_texto}'
                }}, '*');
            </script>
            """, height=0)
        else:
            st.error("Error al conectar con la API o se agotaron los créditos.")

st.sidebar.write(f"Sincronizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
