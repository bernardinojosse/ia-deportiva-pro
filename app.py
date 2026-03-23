import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuración de página y PWA
st.set_page_config(page_title="NuviCore | Sharp Betting Terminal", layout="centered")

# --- ESTILOS MAESTROS (Inspiración PicksWise image_5.png) ---
st.markdown("""
    <style>
    /* Fondo oscuro y tipografía profesional */
    .stApp { background-color: #0b111a; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem;}

    /* Contenedor de Acciones Superiores (Pagar y Soporte) */
    .action-header { display: flex; gap: 10px; margin-bottom: 25px; }
    .btn-act-premium {
        flex: 1; text-align: center; padding: 15px;
        background: linear-gradient(135deg, #00bdff 0%, #007bff 100%);
        color: white !important; font-weight: 700; border-radius: 10px;
        text-decoration: none; font-size: 0.95rem; border: none;
    }
    .btn-act-whatsapp {
        flex: 1; text-align: center; padding: 15px;
        background-color: #25D366; color: white !important;
        font-weight: 700; border-radius: 10px; text-decoration: none; font-size: 0.95rem;
    }

    /* Estilo de la Tarjeta de Partido (The Matchup image_5.png) */
    .match-card {
        background: #111827; border: 1px solid #1f2937;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
    }
    
    /* Liga y Hora */
    .league-time-info { color: #6b7280; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; display: flex; justify-content: space-between; }
    
    /* Área de Equipos y Escudos (Simulados) */
    .teams-area { display: flex; align-items: center; justify-content: space-between; margin: 15px 0 25px 0; }
    .team-display { display: flex; align-items: center; gap: 15px; }
    .team-logo-sim { width: 45px; height: 45px; background-color: #1f2937; border-radius: 50%; display: flex; align-items: center; justify-content: justify; color: #666; font-size: 0.7rem;}
    .team-name-sharp { font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px; }
    
    /* Métricas de IA Advanced */
    .metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; border-top: 1px solid #1f2937; padding-top: 15px; }
    .metric-card { background-color: #182030; border-radius: 8px; padding: 10px; text-align: center; }
    .m-label { color: #6b7280; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px; }
    .m-value-sharp { color: #ffffff; font-weight: 700; font-size: 1.1rem; }
    .m-accent { color: #00bdff !important; }

    /* El Pick Pro Neón */
    .pick-box {
        background-color: #00ff88; color: #000; padding: 12px;
        border-radius: 10px; font-weight: 900; text-align: center; 
        margin-top: 20px; font-size: 1rem; text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
    }
    
    /* Badges de Estado */
    .status-badge { background-color: #2563eb; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.6rem; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DEL AVISO LEGAL AL INICIAR (Simplified for compatibility) ---
if 'legal_aceptado' not in st.session_state:
    st.session_state['legal_aceptado'] = False

if not st.session_state['legal_aceptado']:
    st.warning("⚠️ AVISO LEGAL Y DE PRIVACIDAD")
    st.info("""
    ### Bienvenido a NuviCore AI
    Al acceder, usted acepta los siguientes términos:
    
    **1. Informativo:** NuviCore AI es una herramienta informativa de análisis estadístico. **No somos casa de apuestas**.
    
    **2. Riesgo:** Las apuestas deportivas conllevan riesgos económicos. Los resultados pasados no garantizan éxitos futuros. **El usuario es el único responsable**.
    
    **3. Edad:** Prohibido para menores de **18 años**.
    
    *Pulse 'Aceptar' para continuar.*
    """)
    if st.button("ACEPTAR TÉRMINOS Y ENTRAR", type="primary"):
        st.session_state['legal_aceptado'] = True
        st.rerun()
    st.stop()

# --- TERMINAL DE DATOS CON INTERFAZ SHARP ---
# Header de Acción (Basado en el estilo PicksWise)
st.markdown(f"""
    <div class="action-header">
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="btn-act-premium">🏆 PLAN PRO ($299)</a>
        <a href="https://wa.me/526771316056" class="btn-act-whatsapp">💬 SOPORTE</a>
    </div>
""", unsafe_allow_html=True)

# Selector de Mercado (Inspirado en la barra de deportes image_5.png)
ligas = {"01": "LIGA MX 🇲🇽", "06": "LA LIGA 🇪🇸", "0": "SERIE A 🇮🇹", "02": "CHAMPIONS 🇪🇺"}
st.markdown("<p style='color: #6b7280; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;'>Seleccionar Mercado</p>", unsafe_allow_html=True)
sel = st.selectbox("", list(ligas.values()), label_visibility="collapsed")
id_l = [k for k, v in ligas.items() if v == sel][0]

path = f"campionati/campionato{id_l}.csv"
if os.path.exists(path):
    df = pd.read_csv(path)
    if df.empty:
        st.info("🔄 Sincronizando terminal... Regresa en 5 minutos.")
    else:
        now_time = datetime.now().strftime("%H:%M local")
        
        for _, row in df.iterrows():
            # Descomponemos el nombre del partido (ej: Monterrey vs Toluca)
            teams = row['match'].split(" vs ")
            local_name = teams[0] if len(teams) > 0 else "Local"
            visit_name = teams[1] if len(teams) > 1 else "Visita"
            
            # Simulamos métricas avanzadas (Probability & EV+)
            # (Esto debería provenir de tu engine)
            prob_i = row.get('probability', 50)
            conf_i = row.get('confidence', 'MEDIA')
            ev_status = "EV+" if prob_i > 60 else "NEUTRAL"
            
            # --- RENDERIZADO DE LA TARJETA SHARP ---
            html_card = f"""
            <div class="match-card">
                <div class="league-time-info">
                    <span>{sel}</span>
                    <span>Hoy • {now_time}</span>
                </div>
                
                <div class="teams-area">
                    <div class="team-display">
                        <div class="team-logo-sim">L</div>
                        <div class="team-name-sharp">{local_name}</div>
                    </div>
                    <div style="font-weight: 300; color: #374151; font-size: 0.9rem;">vs</div>
                    <div class="team-display">
                        <div class="team-name-sharp">{visit_name}</div>
                        <div class="team-logo-sim">V</div>
                    </div>
                </div>
                
                <div style="color: #444; font-size: 0.7rem; margin-bottom: 15px; text-align: center;">
                    {row['bookie']} | ML: {row['quota1']} - {row['quota2']}
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="m-label">Win Prob</div>
                        <div class="m-value-sharp">{prob_i}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-label">Confidence</div>
                        <div class="m-value-sharp m-accent">{conf_i}</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-label">Value Status</div>
                        <div class="m-value-sharp"><span class="status-badge">{ev_status}</span></div>
                    </div>
                </div>
                
                <div class="pick-box">{row['pick']}</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
else:
    st.warning("🔄 Ejecutando scrapper... Verifica GitHub Actions.")

if st.button("← CERRAR SESIÓN"):
    st.session_state.view = 'hero'
    st.rerun()
