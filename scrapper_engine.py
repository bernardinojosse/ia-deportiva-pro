import requests
import pandas as pd
import os

ODDS_KEY = os.getenv('ODDS_API_KEY')

def generar_pick_dinamico(q1, q2):
    if not q1 or not q2: return "⚠️ ANALIZANDO..."
    if q1 <= 1.55: return "🔥 LOCAL FAVORITO"
    if q2 <= 1.55: return "🚀 VISITA FAVORITA"
    p1, p2 = 1/q1, 1/q2
    if abs(p1 - p2) < 0.10: return "⚖️ EMPATE / AMBOS ANOTAN"
    return "✅ LOCAL FAVORITO" if q1 < q2 else "✅ VISITA FAVORITA"

def scaricaCampionato(id_liga):
    deportes = {
        "0": "soccer_italy_serie_a", 
        "01": "soccer_mexico_ligamx", 
        "02": "soccer_uefa_champions_league", 
        "06": "soccer_spain_la_liga"
    }
    sport = deportes.get(id_liga)
    if not sport: return pd.DataFrame()
    
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=us&markets=h2h'
    try:
        response = requests.get(url)
        data = response.json()
        if not isinstance(data, list): return pd.DataFrame()

        partidos = []
        for evento in data:
            if not evento.get('bookmakers'): continue
            try:
                outcomes = evento['bookmakers'][0]['markets'][0]['outcomes']
                h, a = evento['home_team'], evento['away_team']
                q1 = next(o['price'] for o in outcomes if o['name'] == h)
                q2 = next(o['price'] for o in outcomes if o['name'] == a)
                partidos.append({
                    "match": f"{h} vs {a}", 
                    "quota1": q1, "quota2": q2,
                    "bookie": evento['bookmakers'][0]['title'],
                    "pick": generar_pick_dinamico(q1, q2)
                })
            except: continue

        if partidos:
            df = pd.DataFrame(partidos)
            os.makedirs('campionati', exist_ok=True)
            df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
            return df
        return pd.DataFrame()
    except: return pd.DataFrame()
