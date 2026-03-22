import streamlit as st
import pandas as pd
import os

# Configuración de la página (Icono de escudo tecnológico)
st.set_page_config(page_title="NuviCore | Inteligencia Deportiva", layout="wide", page_icon="🛡️")

# --- ESTILOS CSS MAESTROS (Diseño Moderno y Profesional) ---
st.markdown("""
    <style>
    /* Fondo oscuro y tipografía limpia */
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}

    /* Contenedor principal centrado */
    .main-wrapper { max-width: 800px; margin: 0 auto; }

    /* Estilo para la Landing Page / Mensaje Gancho */
    .landing-hero {
        text-align: center;
        padding: 60px 20px;
        background: radial-gradient(circle at center, #161b22 0%, #0d1117 100%);
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ff88 0%, #00bdff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.4rem;
        color: #8b949e;
        font-weight: 400;
        margin-bottom: 30px;
        line-height: 1.4;
    }

    /* Tarjetas de Partidos Ultra-Modernas (Estilo image_3.png) */
    .match-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .match-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.1);
        border-color: #00ff88;
    }
    .match-teams {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 5px;
    }
    .match-details {
        font-size: 0.9rem;
        color: #8b949e;
        margin-bottom: 15px;
    }
    
    /* Botones de Pick (Estilo image_3.png) */
    .pick-box {
        background-color: #00ff88;
        color: #000;
        padding: 12px;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.95rem;
    }
    
    /* Botón VIP Destacado en la cabecera */
    .vip-button {
        display: inline-block;
        padding: 10px 20px;
        background: linear-gradient(135deg, #ff0050 0%, #ff6b00 100%);
        color: white;
        font-weight: 700;
        border-radius: 30px;
        text-decoration: none;
        float: right;
        font-size: 0.9rem;
        transition: opacity 0.2s;
    }
    .vip-button:hover { opacity: 0.8; color: white; }

    /* Sección Legal Integarada y Discreta */
    .legal-footer {
        font-size: 0.75rem;
        color: #484f58;
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #21262d;
        line-height: 1.5;
    }
    
    /* Botón de acceso moderno */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00ff88 0%, #00bdff 100%);
        color: black;
        border: none;
        padding: 12px 30px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: transform 0.1s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.03);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA DE LA APP ---
# Usamos columnas para poner el logo a la izquierda y el botón VIP a la derecha
header_col1, header_col2 = st.columns([1, 1])
with header_col1:
    st.image("https://i.imgur.com/8zX0sXn.png", width=180) # Reemplaza con tu logo si tienes uno
with header_col2:
    # Enlace a tu PayPal (actualizado con tu correo)
    paypal_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro%20Suscripcion&amount=299.00&currency_code=MXN"
    st.markdown(f'<a href="{paypal_url}" class="vip-button">🏆 ACTIVAR VIP</a>', unsafe_allow_html=True)

# --- INICIALIZAR ESTADO DE NAVEGACIÓN ---
if 'mostrar_picks' not in st.session_state:
    st.session_state['mostrar_picks'] = False

# --- FUNCIÓN PARA MOSTRAR LOS PICKS ---
def mostrar_interfaz_picks():
    st.session_state['mostrar_picks'] = True

# --- CONTENEDOR PRINCIPAL (Embudo de Ventas) ---
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# --- PANTALLA 1: BIENVENIDA GANCHO (Landing Page) ---
if not st.session_state['mostrar_picks']:
    st.markdown("""
        <div class="landing-hero">
            <h1 class="hero-title">El Algoritmo que Domina<br>las Apuestas Deportivas</h1>
            <p class="hero-subtitle">Bienvenido a NuviCore, la Inteligencia Artificial más avanzada<br>
            que escanea miles de datos por segundo para encontrar<br>
            las verdaderas oportunidades de valor.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn_centrar1, col_btn_centrar2, col_btn_centrar3 = st.columns([1, 2, 1])
    with col_btn_centrar2:
        st.button("🔓 Ver los Picks de Hoy", on_click=mostrar_interfaz_picks, use_container_width=True)

    # Aviso Legal al final de la Bienvenida, muy pequeño e integrado
    st.markdown("""
        <div class="legal-footer">
            <b>Información meramente orientativa.</b> NuviCore es una herramienta de análisis estadístico basada en inteligencia de datos. 
            No somos operadores de juego ni aceptamos apuestas. Los resultados pasados no garantizan el éxito futuro. 
            El uso de esta información es responsabilidad exclusiva del usuario. Juegue con responsabilidad. Prohibido para menores de 18 años.
        </div>
    """, unsafe_allow_html=True)

# --- PANTALLA 2: INTERFAZ DE PICKS (Sólo si se desbloquea) ---
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Selecciones de Hoy")
    
    # Selector de Mercado Moderno
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    seleccion_liga = st.selectbox("", list(ligas.values()), label_visibility="collapsed")
    id_liga = [k for k, v in ligas.items() if v == seleccion_liga][0]

    # Carga de Datos Segura
    path_datos = f"campionati/campionato{id_liga}.csv"
    if os.path.exists(path_datos):
        try:
            df_partidos = pd.read_csv(path_datos)
            if df_partidos.empty:
                st.info("🔄 Sincronizando nuevos datos... Regresa en un momento.")
            else:
                for _, partido in df_partidos.iterrows():
                    st.markdown(f"""
                        <div class="match-card">
                            <div class="match-teams">{partido['match']}</div>
                            <div class="match-details">
                                Casa: {partido['bookie']} | <b>L: {partido['quota1']} - V: {row['quota2']}</b>
                            </div>
                            <div class="pick-box">{partido['pick']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        except Exception:
            st.error("Error al leer la base de datos. El bot está trabajando.")
    else:
        st.warning("No hay partidos detectados para este mercado hoy.")

    # Opción para volver a la bienvenida (discreto)
    st.write("")
    if st.button("⬅️ Volver a Inicio", type="secondary"):
        st.session_state['mostrar_picks'] = False
        st.rerun()

# Cerrar contenedor principal
st.markdown('</div>', unsafe_allow_html=True)
