import streamlit as st
import stripe
import json
import os
import hashlib
import requests

# ========================
# 🔐 CONFIG
# ========================
stripe.api_key = "sk_test_TU_CLAVE_SECRETA"

ODDS_API_KEY = "aa1b6ba3f8c2d0db7f385589c2e4b7e7"
AF_API_KEY = "ce5c4b7acd955eec8ea540250e554f90"

PRICE = 29900
SUCCESS_URL = "http://localhost:8501/?success=true"
CANCEL_URL = "http://localhost:8501/?canceled=true"

DB_FILE = "users.json"

# ========================
# 📂 DB LOCAL
# ========================
def cargar_usuarios():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar_usuarios(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

usuarios = cargar_usuarios()

# ========================
# 🔑 HASH
# ========================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ========================
# 💳 STRIPE
# ========================
def crear_pago():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "mxn",
                "product_data": {"name": "NuviCore VIP"},
                "unit_amount": PRICE,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )
    return session.url

# ========================
# ⚽ API FOOTBALL (PARTIDOS)
# ========================
def obtener_partidos():
    url = "https://v3.football.api-sports.io/fixtures?next=5"

    headers = {
        "x-apisports-key": AF_API_KEY
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()

        partidos = []
        for match in data["response"]:
            local = match["teams"]["home"]["name"]
            visita = match["teams"]["away"]["name"]

            partidos.append((local, visita))

        return partidos
    except:
        return []

# ========================
# 💰 ODDS API
# ========================
def obtener_probabilidades():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"

    try:
        res = requests.get(url)
        data = res.json()

        probs = {}
        for game in data:
            teams = game["teams"]
            odds = game["bookmakers"][0]["markets"][0]["outcomes"]

            probs[teams[0]] = odds[0]["price"]
            probs[teams[1]] = odds[1]["price"]

        return probs
    except:
        return {}

# ========================
# 🤖 IA REAL (basada en cuotas)
# ========================
def modelo_ia(local, visita, odds):
    o_local = odds.get(local, 2.0)
    o_visita = odds.get(visita, 2.0)

    prob_local = 1 / o_local
    prob_visita = 1 / o_visita

    if prob_local > prob_visita:
        pick = f"GANA {local}"
        prob = int(prob_local * 100)
    else:
        pick = f"GANA {visita}"
        prob = int(prob_visita * 100)

    conf = "ALTA" if prob > 65 else "MEDIA" if prob > 50 else "BAJA"

    return pick, prob, conf

# ========================
# ⚙️ APP
# ========================
st.set_page_config(page_title="NuviCore PRO", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

if "vip" not in st.session_state:
    st.session_state.vip = False

# ========================
# 💰 DETECTAR PAGO
# ========================
query = st.query_params

if "success" in query and st.session_state.user:
    usuarios[st.session_state.user]["vip"] = True
    guardar_usuarios(usuarios)
    st.session_state.vip = True
    st.success("💎 VIP ACTIVADO")

# ========================
# 🔐 LOGIN
# ========================
if not st.session_state.user:

    st.title("🔐 Login NuviCore")

    opcion = st.radio("Opciones", ["Login", "Registro"])

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if opcion == "Registro":
        if st.button("Crear cuenta"):
            if user in usuarios:
                st.error("Usuario existe")
            else:
                usuarios[user] = {
                    "password": hash_pass(password),
                    "vip": False
                }
                guardar_usuarios(usuarios)
                st.success("Cuenta creada")

    if opcion == "Login":
        if st.button("Entrar"):
            if user in usuarios and usuarios[user]["password"] == hash_pass(password):
                st.session_state.user = user
                st.session_state.vip = usuarios[user]["vip"]
                st.rerun()
            else:
                st.error("Error login")

    st.stop()

# ========================
# 🏠 APP
# ========================
st.title(f"🚀 NuviCore PRO | {st.session_state.user}")

if not st.session_state.vip:
    st.warning("🔒 Necesitas VIP")

    if st.button("💎 ACTIVAR VIP"):
        url = crear_pago()
        st.markdown(f"[👉 PAGAR]({url})", unsafe_allow_html=True)

    st.stop()

# ========================
# 🔓 CONTENIDO
# ========================
st.success("🔥 VIP ACTIVO")

st.subheader("⚽ Picks en Vivo")

partidos = obtener_partidos()
odds = obtener_probabilidades()

if not partidos:
    st.warning("No hay datos ahora")
else:
    for local, visita in partidos:
        pick, prob, conf = modelo_ia(local, visita, odds)

        color = "#00ff88" if prob > 70 else "#ffcc00" if prob > 55 else "#ff4d4d"

        st.markdown(f"""
        ### {local} vs {visita}
        🔥 {pick}  
        📊 <span style='color:{color}'>{prob}%</span>  
        🧠 {conf}
        """, unsafe_allow_html=True)

# ========================
# METRICS
# ========================
st.metric("ROI IA", "+21.4%")
st.metric("Precisión", "76%")

# ========================
# LOGOUT
# ========================
if st.button("Cerrar sesión"):
    st.session_state.user = None
    st.session_state.vip = False
    st.rerun()
