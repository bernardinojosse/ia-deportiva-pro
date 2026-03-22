import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="NuviCore VIP", layout="centered", page_icon="🛡️")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
        border: 1px solid #00ff88;
    }
    .pick-box {
        background-color: #00ff88;
        color: #000;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    .premium-card {
        background: linear-gradient(135deg, #00ff88 0%, #0077ff 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0, 255, 136, 0.3);
    }
    .premium-card h2 { color: white !important; margin-bottom: 5px; }
    .disclaimer {
        font-size: 0.85rem;
        color: #8b949e;
        text-align: justify;
        line-height: 1.4;
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tab1, tab2, tab3 = st.tabs(["⚽ Picks Hoy", "💎 VIP Premium", "⚖️ Info Legal"])

# --- PESTAÑA 1: PICKS GRATUITOS ---
with tab1:
    st.title("🛡️ NuviCore Intelligence")
    
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    seleccion = st.selectbox("Seleccionar Mercado:", list(ligas.values()))
    id_l = [k for k, v in ligas.items() if v == seleccion][0]

    path = f"campionati/campionato{id_l}.csv"

    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if df.empty:
                st.info("🔄 El bot está analizando nuevos datos. Regresa en un momento.")
            else:
                for _, row in df.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <div style="font-size: 1.1rem; font-weight: bold;">{row['match']}</div>
                            <div style="color: #8b949e; font-size: 0.9rem; margin-top:5px;">
                                Casa: {row['bookie']} | <b>L: {row['quota1']} - V: {row['quota2']}</b>
                            </div>
                            <div class="pick-box">{row['pick']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        except:
            st.error("Sincronizando base de datos...")
    else:
        st.warning("No hay partidos detectados para esta liga hoy.")

# --- PESTAÑA 2: PREMIUM (CON TU PAYPAL) ---
with tab2:
    st.title("🚀 Acceso Exclusivo")
    
    st.markdown("""
    <div class="premium-card">
        <h2>MEMBRESÍA PRO</h2>
        <p style="font-size: 1.4rem; font-weight: bold;">$299.00 MXN / Mes</p>
        <div style="text-align: left; display: inline-block; margin-top: 10px;">
            <li>🎯 Picks de Alta Probabilidad</li>
            <li>📊 Análisis de Marcador Exacto</li>
            <li>🏀 NBA y MLB Incluidos</li>
            <li>📱 Alertas Directas a tu Celular</li>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # BOTÓN DE PAYPAL CON TU CORREO
    paypal_url = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=Suscripcion%20NuviCore%20Pro&amount=299.00&currency_code=MXN"
    
    st.link_button("💳 Pagar vía PayPal", paypal_url, use_container_width=True)
    
    st.divider()
    
    # CONTACTO WHATSAPP
    st.subheader("¿Dudas o Pago por Transferencia?")
    # Recuerda cambiar el número 5216771316056 por tu número real
    wa_link = "https://wa.me/521XXXXXXXXXX?text=Hola%20Jose,%20acabo%20de%20ver%20la%20App%20NuviCore%20y%20quiero%20el%20Plan%20Premium"
    st.link_button("💬 Hablar con Jose (Soporte)", wa_link, use_container_width=True)

# --- PESTAÑA 3: LEGAL ---
with tab3:
    st.subheader("Aviso de Responsabilidad")
    st.markdown("""
    <div class="disclaimer">
        <b>IMPORTANTE:</b> Esta aplicación es una herramienta de análisis estadístico basada en inteligencia de datos. 
        Toda la información proporcionada es únicamente <b>informativa y con fines de entretenimiento</b>.
        <br><br>
        1. <b>No somos operadores de juego:</b> NuviCore no acepta apuestas ni gestiona depósitos.<br>
        2. <b>Sin Garantías:</b> El deporte es impredecible. Los análisis no garantizan resultados positivos al 100%.<br>
        3. <b>Riesgo Financiero:</b> El usuario es el único responsable de sus decisiones financieras y apuestas realizadas en plataformas externas.<br>
        4. <b>Uso Prohibido:</b> Prohibido el uso para menores de 18 años.
        <br><br>
        <i>Al usar NuviCore, liberas a los desarrolladores de cualquier responsabilidad por pérdidas económicas. Juega con responsabilidad.</i>
    </div>
    """, unsafe_allow_html=True)
