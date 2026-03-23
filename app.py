import streamlit as st
import pandas as pd
import os

# 1. Configuración de página y PWA
st.set_page_config(page_title="NuviCore | Sharp Terminal", layout="centered")

# --- ESTILOS SHARP INTELLIGENCE (Diseño de Lujo) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Botones Superiores Estilizados */
    .btn-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .vip-link {
        flex: 1; text-align: center; padding: 15px;
        background: linear-gradient(90deg, #00ff88, #00bdff);
        color: #000 !important; font-weight: bold; border-radius: 12px;
        text-decoration: none; font-size: 0.9rem;
    }
    .wa-link {
        flex: 1; text-align: center; padding: 15px;
        background-color: #25D366; color: #fff !important;
        font-weight: bold; border-radius: 12px; text-decoration: none; font-size: 0.9rem;
    }

    /* Tarjeta de Partido (Glassmorphism) */
    .match-card {
        background: #0a0a0a; border: 1px solid #1a1a1a;
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
    }
    .league-tag { color: #00ff88; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; }
    .teams { font-size: 1.5rem; font-weight: 800; margin: 10px 0; }
    
    /* Métricas de IA Advanced */
    .metrics { display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #222; padding-top: 15px; }
    .metric-box { text-align: center; }
    .m-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; }
    .m-lbl { color: #555; font-size: 0.6rem; text-transform: uppercase; }

    /* El Pick Pro Neón */
    .pick-box {
        background: #00ff88; color: #000; padding: 12px;
        border-radius: 10px; font-weight: 900; text-align: center; 
        margin-top: 20px; font-size: 1rem; text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 📜 GESTIÓN DEL AVISO LEGAL AL INICIAR ---
if 'legal_aceptado' not in st.session_state:
    st.session_state['legal_aceptado'] = False

# Modal que aparece al abrir la app
if not st.session_state['legal_aceptado']:
    with st.popover("📜 Aviso Legal y de Privacidad - Leer Obligatoriamente", open=True):
        st.write("""
        ### Bienvenido a NuviCore AI
        Al acceder y usar esta aplicación, usted acepta los siguientes términos:
        
        **1. Naturaleza de la Información:** NuviCore es una herramienta de análisis estadístico basada en inteligencia de datos. La información provista es **meramente orientativa** y no constituye una recomendación de apuesta.
        
        **2. Sin Garantías:** No garantizamos la exactitud de los pronósticos ni resultados futuros. Las apuestas deportivas conllevan riesgos económicos. **El usuario es el único responsable de sus decisiones financieras**.
        
        **3. Privacidad:** No recopilamos datos personales sensibles. Su actividad dentro de la app es anónima.
        
        **4. Responsabilidad:** Prohibido para menores de **18 años**. Juegue con responsabilidad.
        
        *Para continuar y ver los datos de hoy, por favor pulse en 'Aceptar'.*
        """)
        if st.button("Aceptar y Continuar", type="primary"):
            st.session_state['legal_aceptado'] = True
            st.rerun()
    st.stop() # Detiene la ejecución hasta que se acepte

# --- PANTALLA PRINCIPAL: TERMINAL DE DATOS ---
else:
    # Botones de Acción Superiores
    st.markdown(f"""
        <div class="btn-container">
            <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN" class="vip-link">🏆 ACTIVAR VIP ($299 MXN)</a>
            <a href="https://wa.me/526771316056" class="wa-link">💬 SOPORTE WHATSAPP</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Selector de Ligas (Moderno)
    ligas = {"01": "🇲🇽 LIGA MX", "06": "🇪🇸 LA LIGA", "0": "🇮🇹 SERIE A", "02": "🇪🇺 CHAMPIONS"}
    sel = st.selectbox("", list(ligas.values()))
    id_l = [k for k, v in ligas.items() if v == sel][0]

    st.write("---")

    path = f"campionati/campionato{id_l}.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        if df.empty:
            st.info("🔄 Terminal sincronizándose... Regresa en unos minutos.")
        else:
            for _, row in df.iterrows():
                # Simulamos métricas avanzadas basadas en la cuota
                prob_implied = round((1/row['quota1']) * 100)
                
                # --- AQUÍ ESTÁ LA CORRECCIÓN CLAVE ---
                # Usamos st.markdown con unsafe_allow_html=True en cada renderizado
                st.markdown(f"""
                    <div class="match-card">
                        <div class="league-tag">{sel} • SHARP DATA</div>
                        <div class="teams">{row['match']}</div>
                        <div style="color: #666; font-size: 0.8rem; margin-bottom: 15px;">
                            Bookie: {row['bookie']} | ML: {row['quota1']} - {row['quota2']}
                        </div>
                        
                        <div class="metrics">
                            <div class="metric-box">
                                <div class="m-val">{prob_implied}%</div>
                                <div class="m-lbl">Win Prob</div>
                            </div>
                            <div class="metric-box">
                                <div class="m-val" style="color: #00ff88;">ALTA</div>
                                <div class="m-lbl">Confidence</div>
                            </div>
                            <div class="metric-box">
                                <div class="m-val">EV+</div>
                                <div class="m-lbl">Data Status</div>
                            </div>
                        </div>
                        
                        <div class="pick-box">{row['pick']}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Iniciando escaneo de la liga... Asegúrate de correr el Action en GitHub.")
