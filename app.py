import streamlit as st
import pandas as pd
import os
from difflib import SequenceMatcher

# --- NÚCLEO OPERATIVO NUVI-CORE ---
st.set_page_config(page_title="NUVI-CORE X-RAY", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .main-logo { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: 5px; margin-bottom: 20px; }
    
    /* Estilo de Tarjeta de Arbitraje Real */
    .scan-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(79, 172, 254, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #00ff88;
    }
    .match-header { font-weight: 700; color: #fff; font-size: 1.1rem; margin-bottom: 10px; }
    .profit-badge { background: #00ff88; color: #000; padding: 4px 10px; border-radius: 8px; font-weight: 900; font-family: 'Orbitron'; font-size: 0.9rem; }
    
    /* Grid de Inversión */
    .invest-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
    .invest-item { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; text-align: center; }
    .invest-label { font-size: 0.6rem; color: #888; text-transform: uppercase; margin-bottom: 5px; }
    .invest-value { font-family: 'Orbitron'; font-size: 1.3rem; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CARGA DE DATOS (Tus Archivos CSV) ---
def cargar_campionato(id_campionato):
    filepath = f'campionati/campionato{id_campionato}.csv'
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def calcular_inversion(q1, q2, total):
    # Tu fórmula exacta de varianza y distribución
    var = (1/q1) + (1/q2)
    inv1 = total / (q1 * var)
    inv2 = total / (q2 * var)
    profit = (inv1 * q1) - total
    return round(inv1, 2), round(inv2, 2), round(profit, 2)

# --- INTERFAZ DE USUARIO ---
st.markdown('<div class="main-logo">NUVI-CORE X-RAY</div>', unsafe_allow_html=True)

# Panel de Control
campionatos = {
    "0": "Serie A", "01": "Serie B", "02": "Champions", 
    "04": "Premier League", "06": "La Liga", "08": "Bundesliga"
}

col_a, col_b = st.columns([2, 1])
with col_a:
    seleccion = st.selectbox("Selecciona Mercado Escaneado:", list(campionatos.values()))
    id_camp = [k for k, v in campionatos.items() if v == seleccion][0]
with col_b:
    capital = st.number_input("Inversión ($):", min_value=100, value=1000, step=100)

df = cargar_campionato(id_camp)

if df is not None:
    st.success(f"Sincronizado con éxito: {len(df)} partidos encontrados.")
    
    for index, row in df.iterrows():
        # Simulamos que el CSV tiene columnas: match, quota1, quota2 (de tu script)
        # Aquí ajustamos a los nombres de tus columnas reales
        try:
            q1, q2 = float(row['quota1']), float(row['quota2'])
            v1, v2, profit = calcular_inversion(q1, q2, capital)
            
            # Solo mostramos si hay ganancia real (Arbitraje)
            if profit > 0:
                st.markdown(f"""
                    <div class="scan-card">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <div class="match-header">{row['match']}</div>
                            <div class="profit-badge">+${profit}</div>
                        </div>
                        
                        <div class="invest-grid">
                            <div class="invest-item">
                                <div class="invest-label">Apostar en Opción 1</div>
                                <div class="invest-value">${v1}</div>
                                <div style="font-size:0.7rem; color:#4facfe;">Cuota: {q1}</div>
                            </div>
                            <div class="invest-item">
                                <div class="invest-label">Apostar en Opción 2</div>
                                <div class="invest-value">${v2}</div>
                                <div style="font-size:0.7rem; color:#00ff88;">Cuota: {q2}</div>
                            </div>
                        </div>
                        <div style="margin-top:10px; text-align:right;">
                            <small style="color:#666;">Varianza detectada: {round(((1/q1)+(1/q2))*100, 2)}%</small>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        except:
            continue
else:
    st.info("No hay datos recientes para este campeonato. Ejecuta tu script de scraping primero.")

st.sidebar.caption("NUVI-CORE v12.0 | DATABASE SYNC")
