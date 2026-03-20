import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE INTERFAZ PROFESIONAL ---
st.set_page_config(page_title="IA Parlay Pro", page_icon="💰", layout="centered")

# Estilos CSS inyectados para el modo oscuro y tarjetas neón
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; font-family: 'Inter', sans-serif; }
    .card-pro {
        background-color: #161b22;
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .status-header { color: #00ff88; font-size: 1.2rem; font-weight: 800; margin-bottom: 10px; }
    .strategy-box { background-color: #0d1117; border-radius: 10px; padding: 15px; margin-top: 15px; }
    .profit-text { color: #00ff88; font-weight: 700; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO (TU VARIABLE VAR) ---
def calcular_inversion(q1, q2, total):
    # Tu fórmula exacta: var = (1/q1) + (1/q2)
    var = (1/q1) + (1/q2)
    inv1 = total / (q1 * var)
    inv2 = total / (q2 * var)
    profit = (inv1 * q1) - total
    yield_perc = (profit / total) * 100
    return round(inv1, 2), round(inv2, 2), round(profit, 2), round(yield_perc, 2)

# --- ENCABEZADO ---
st.markdown('<h1 style="text-align:center;">💰 IA Parlay Pro</h1>', unsafe_allow_html=True)

# Panel de entrada
col1, col2 = st.columns([2, 1])
with col1:
    campionatos = {"0": "Serie A", "01": "Serie B", "02": "Champions", "04": "Premier League", "06": "La Liga"}
    seleccion = st.selectbox("Mercado Escaneado:", list(campionatos.values()))
    id_camp = [k for k, v in campionatos.items() if v == seleccion][0]
with col2:
    capital = st.number_input("Inversión ($):", min_value=10, value=1000)

# --- CARGA DE DATOS DESDE CARPETA CAMPIONATI ---
file_path = f'campionati/campionato{id_camp}.csv'

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.success(f"Sincronizado: {len(df)} eventos analizados.")
    
    for _, row in df.iterrows():
        try:
            # Extraemos cuotas (ajusta los nombres de columna si tu CSV usa otros)
            q1, q2 = float(row['quota1']), float(row['quota2'])
            v1, v2, profit, y_perc = calcular_inversion(q1, q2, capital)
            
            # SOLO MOSTRAR SI HAY GANANCIA (SUREBET)
            if profit > 0:
                # RENDERIZADO HTML SEGURO (Esto evita que se vea el código)
                html_card = f"""
                <div class="card-pro">
                    <div class="status-header">🔥 OPORTUNIDAD DETECTADA</div>
                    <div style="color: #8b949e; margin-bottom: 15px;">{row['match']}</div>
                    
                    <div style="font-family: monospace; color: #00ff88; background: #0d1117; padding: 8px; border-radius: 5px;">
                        Cálculo: ({q1} - 1) * ({q2} - 1) = {round((q1-1)*(q2-1), 4)}
                    </div>

                    <div class="strategy-box">
                        <b style="color: #8b949e; font-size: 0.8rem;">ESTRATEGIA:</b><br>
                        <div style="margin: 10px 0;">
                            💰 Apostar <b style="color: #fff;">${v1}</b> (Cuota {q1})<br>
                            💰 Apostar <b style="color: #fff;">${v2}</b> (Cuota {q2})
                        </div>
                        <div style="border-top: 1px solid #30363d; padding-top: 10px;">
                            <span class="profit-text">GANANCIA: ${profit}</span> | 
                            <span style="color: #4facfe;">RETORNO: {y_perc}%</span>
                        </div>
                    </div>
                </div>
                """
                # ESTA LÍNEA ES LA CLAVE: interpreta el HTML y oculta las etiquetas
                st.markdown(html_card, unsafe_allow_html=True)
        except:
            continue
else:
    st.info(f"Esperando datos de {seleccion}. El bot de GitHub actualizará el CSV en la carpeta 'campionati' cada 3 horas.")

st.sidebar.markdown("---")
st.sidebar.caption("NUVI-CORE ENGINE v12.5")
