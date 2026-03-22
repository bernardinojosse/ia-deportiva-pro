import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card {
        background-color: #1c2128;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #30363d;
        margin-bottom: 5px;
    }
    .pick-header {
        color: #00ff88;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ NuviCore Intelligence")

ligas = {"01": "Liga MX", "02": "Champions", "06": "La Liga", "0": "Serie A"}
sel = st.selectbox("Selecciona la Liga", list(ligas.values()))
id_l = [k for k, v in ligas.items() if v == sel][0]

path = f"campionati/campionato{id_l}.csv"

if os.path.exists(path):
    try:
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            with st.container():
                # Caja principal del partido
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 1.2rem; font-weight:bold;">⚽ {row['match']}</div>
                    <div style="color: #8b949e;">L: {row['quota1']} | V: {row['quota2']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Desplegable interactivo
                with st.expander(f"🎯 RECOMENDACIÓN: {row['pick']}"):
                    q1, q2 = row['quota1'], row['quota2']
                    
                    # Lógica dinámica para la explicación
                    if q1 < 1.65:
                        pros = "Local dominante, racha positiva en casa."
                        contras = "Exceso de confianza o rotación de plantilla."
                        sug = "Hándicap Asiático -1 para mejorar momio."
                    elif q2 < 1.65:
                        pros = "Visitante con mejor plantilla y xG alto."
                        contras = "Factor campo en contra y fatiga de viaje."
                        sug = "Apuesta directa a favor del visitante."
                    else:
                        pros = "Equipos equilibrados, alta probabilidad de gol."
                        contras = "Defensas cerradas podrían forzar un 0-0."
                        sug = "Baja de 3.5 goles o Ambos Anotan."

                    st.markdown(f"**✅ Pros:** {pros}")
                    st.markdown(f"**❌ Contras:** {contras}")
                    st.info(f"💡 **Sugerencia:** {sug}")
                st.divider()
    except:
        st.error("Sincronizando base de datos...")
else:
    st.warning("No hay datos disponibles. El bot está escaneando.")
