import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    .pick-box {
        background-color: #238636;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        font-weight: bold;
        text-align: center;
        border-left: 5px solid #00ff88;
    }
    .cuota { font-size: 1.2rem; color: #58a6ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 NuviCore: Picks Imperdibles")

# Selector de Ligas
ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
sel = st.selectbox("Seleccionar Liga:", list(ligas.values()))
id_l = [k for k, v in ligas.items() if v == sel][0]

file = f"campionati/campionato{id_l}.csv"

# --- LÓGICA DEL PICK IMPERDIBLE ---
def generar_pick(q1, q2, match):
    # Lógica basada en probabilidad implícita y valor
    if q1 < q2 and q1 < 2.0:
        return f"🔥 PICK: Victoria Local ({q1}) - Alta Probabilidad"
    elif q2 < q1 and q2 < 2.0:
        return f"🔥 PICK: Victoria Visitante ({q2}) - Favorito Claro"
    elif abs(q1 - q2) < 0.5:
        return f"⚖️ PICK: Doble Oportunidad o Empate - Juego Cerrado"
    else:
        return f"⭐ PICK: Más de 1.5 Goles - Valor en Mercado"

# --- RENDERIZADO DE PARTIDOS ---
if os.path.exists(file):
    df = pd.read_csv(file)
    st.info(f"Mostrando {len(df)} partidos analizados hoy.")
    
    for _, row in df.iterrows():
        # Creamos la tarjeta visual
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 1.3rem; margin-bottom: 10px;">⚽ {row['match']}</div>
                <div style="display: flex; justify-content: space-around; margin-bottom: 10px;">
                    <div>Local: <span class="cuota">{row['quota1']}</span></div>
                    <div>Visitante: <span class="cuota">{row['quota2']}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #8b949e;">Casa: {row.get('bookie', 'Global')}</div>
                <div class="pick-box">
                    {generar_pick(row['quota1'], row['quota2'], row['match'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("No hay datos disponibles. Ejecuta el bot en GitHub.")
