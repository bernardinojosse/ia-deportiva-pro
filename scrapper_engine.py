import requests
import pandas as pd
import os

ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY')

def generar_pick_pro(q1, q2):
    if q1 < 1.65: return "🔥 LOCAL FAVORITO"
    if q2 < 1.65: return "🚀 VISITA FAVORITA"
    return "⚖️ AMBOS ANOTAN / EMPATE"

def scaricaCampionato(id_liga):
    # Nombres técnicos exactos para la API
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
        
        if not isinstance(data, list):
            print(f"❌ Error API en {sport}: {data}")
            return pd.DataFrame()

        partidos = []
        for evento in data:
            if not evento.get('bookmakers'): continue
            try:
                bookie = evento['bookmakers'][0]
                outcomes = bookie['markets'][0]['outcomes']
                home = evento['home_team']
                away = evento['away_team']
                
                q1 = next(o['price'] for o in outcomes if o['name'] == home)
                q2 = next(o['price'] for o in outcomes if o['name'] == away)
                
                partidos.append({
                    "match": f"{home} vs {away}",
                    "quota1": q1,
                    "quota2": q2,
                    "bookie": bookie['title'],
                    "pick": generar_pick_pro(q1, q2)
                })
            except: continue

        if partidos:
            df = pd.DataFrame(partidos)
            os.makedirs('campionati', exist_ok=True)
            df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
            print(f"✅ {sport} actualizado con {len(partidos)} partidos.")
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        return pd.DataFrame()

def allFromCampionato(df):
    return df
