import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NuviCore VIP", layout="centered", page_icon="🛡️")

# Estilos Pro
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .card { background-color: #161b22; border-radius: 15px; padding: 15px; margin-bottom: 12px; border: 1px solid #00ff88; }
    .pick-box { background-color: #00ff88; color: black; padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; margin-top: 8px; }
    .premium-card { background: linear-gradient(135deg, #00ff88 0%, #0077ff 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.image("https://i.imgur.com/8zX0sXn.png", use_container_width=True)

tab1, tab2, tab3 = st.tabs(["⚽ Picks Hoy", "💎 VIP", "⚖️ Legal"])

with tab1:
    ligas = {"01": "🇲🇽 Liga MX", "06": "🇪🇸 La Liga", "0": "🇮🇹 Serie A", "02": "🇪🇺 Champions"}
    sel = st.selectbox("Mercado:", list(ligas.values()))
    id_l = [k for k, v in ligas.items() if v == sel][0]
    path = f"campionati/campionato{id_l}.csv"

    if os.path.exists(path):
        df = pd.read_csv(path)
        if not df.empty:
            for _, row in df.iterrows():
                st.markdown(f"""<div class="card"><b>{row['match']}</b><br><small>{row['bookie']} | L:{row['quota1']} V:{row['quota2']}</small><div class="pick-box">{row['pick']}</div></div>""", unsafe_allow_html=True)
        else: st.info("Actualizando datos...")
    else: st.warning("Sin partidos para hoy.")

with tab2:
    st.markdown("""<div class="premium-card"><h2>PLAN PRO</h2><h3>$299 MXN / Mes</h3><li>Picks 85% Efectividad</li><li>NBA y MLB Incluidos</li><li>Alertas WhatsApp</li></div>""", unsafe_allow_html=True)
    paypal_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=luis54ber.70@gmail.com&item_name=NuviCore%20Pro&amount=299.00&currency_code=MXN"
    st.link_button("💳 Pagar con PayPal", paypal_url, use_container_width=True)
    # PON TU NUMERO AQUÍ ABAJO:
    st.link_button("💬 Contactar Soporte", "https://wa.me/5216771316056?text=Quiero%20el%20VIP", use_container_width=True)

with tab3:
    st.caption("NuviCore es una herramienta informativa. No garantizamos resultados. El usuario es responsable de sus apuestas. Prohibido menores de 18.")
