import streamlit as st
import requests

# --- CONFIGURACIÓN VISUAL PREMIUM ---
st.set_page_config(page_title="NUVI-CORE ARBITRAGE", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* Logo Principal */
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #00ff88 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: 5px; margin-bottom: 20px; }

    /* Tarjeta de Oportunidad Estilo NuviX */
    .opportunity-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .match-header { font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 5px; text-align: center; }
    .league-tag { font-size: 0.7rem; color: #4facfe; text-transform: uppercase; letter-spacing: 2px; text-align: center; margin-bottom: 20px; }

    /* Contenedor de Apuesta (Ticket) */
    .ticket-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 20px 0;
    }
    
    .bet-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        border-top: 3px solid #00ff88;
        text-align: center;
    }

    .bet-amount { font-family: 'Orbitron'; font-size: 1.5rem; color: #fff; margin: 5px 0; }
    .bet-bookie { font-size: 0.75rem; color: #888; text-transform: uppercase; }
    .bet-team { font-size: 0.9rem; font-weight: 600; color: #00ff88; }

    /* Barra de Ganancia */
    .profit-bar {
        background: linear-gradient(90deg, #00ff88 0%, #4facfe 100%);
        color: #000;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: 800;
        font-family: 'Orbitron';
        margin-top: 15px;
    }
    
    .formula-badge {
        font-size: 0.65rem;
        color: #555;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA MATEMÁTICA ---
def calcular_apuesta_ideal(total_inversion, cuota_a, cuota_b):
    inv_a = 1 / cuota_a
    inv_b = 1 / cuota_b
    prob_total = inv_a + inv_b
    apuesta_a = (inv_a / prob_total) * total_inversion
    apuesta_b = (inv_b / prob_total) * total_inversion
    return round(apuesta_a, 2), round(apuesta_b, 2)

# --- INTERFAZ ---
st.markdown('<div class="main-logo">NUVI-CORE</div>', unsafe_allow_html=True)

# Entrada de Capital Estilizada
st.write("### 💰 Capital a Distribuir")
inversion = st.slider("", 100, 5000, 1000, step=100)

# Simulación de datos (Basado en tu lógica de Arbitraje)
# En una App real, estos datos vienen de la función fetch_data()
data_demo = [
    {
        "match": "Karlsruher SC vs Greuther Fürth",
        "league": "Bundesliga 2 - Germany",
        "cuota_a": 3.35, "bookie_a": "William Hill", "team_a": "Karlsruher SC",
        "cuota_b": 2.22, "bookie_b": "Betfair", "team_b": "Greuther Fürth"
    }
]

st.markdown("---")

for item in data_demo:
    # Aplicar tu fórmula: (a-1)*(b-1) > 1
    factor = (item['cuota_a'] - 1) * (item['cuota_b'] - 1)
    
    if factor > 1:
        apuesta_a, apuesta_b = calcular_apuesta_ideal(inversion, item['cuota_a'], item['cuota_b'])
        ganancia_neta = round((apuesta_a * item['cuota_a']) - inversion, 2)
        porcentaje = round((ganancia_neta / inversion) * 100, 2)

        # RENDERIZADO PROFESIONAL (Sin código visible)
        st.markdown(f"""
            <div class="opportunity-card">
                <div class="league-tag">{item['league']}</div>
                <div class="match-header">{item['match']}</div>
                
                <div class="ticket-container">
                    <div class="bet-box">
                        <div class="bet-bookie">{item['bookie_a']}</div>
                        <div class="bet-team">{item['team_a']}</div>
                        <div class="bet-amount">${apuesta_a}</div>
                        <div style="font-size:0.7rem; color:#666;">Cuota: {item['cuota_a']}</div>
                    </div>
                    <div class="bet-box">
                        <div class="bet-bookie">{item['bookie_b']}</div>
                        <div class="bet-team">{item['team_b']}</div>
                        <div class="bet-amount">${apuesta_b}</div>
                        <div style="font-size:0.7rem; color:#666;">Cuota: {item['cuota_b']}</div>
                    </div>
                </div>
                
                <div class="profit-bar">
                    GANANCIA GARANTIZADA: ${ganancia_neta} ({porcentaje}%)
                </div>
                
                <div class="formula-badge">
                    Análisis de Arbitraje validado por Núcleo Nuvi-Core
                </div>
            </div>
        """, unsafe_allow_html=True)

st.sidebar.caption("SISTEMA OPERATIVO NUVI-CORE v9.0")
