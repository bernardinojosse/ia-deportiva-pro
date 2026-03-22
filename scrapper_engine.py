import requests
import pandas as pd
import os

# Lee la llave directamente desde el entorno de GitHub
API_KEY = os.getenv('ODDS_API_KEY') 
REGION = 'eu' # Cámbialo a 'us' si prefieres casas americanas/mexicanas
MARKET = 'h2h' 

def scaricaCampionato(id_liga):
    deportes = {
        "02": "soccer_uefa_champions_league",
        "06": "soccer_spain_la_liga",
        "04": "soccer_england_league_1",
        "0": "soccer_italy_serie_a",
        "01": "soccer_mexico_ligamx"
    }
    
    sport_key = deportes.get(id_liga, "soccer_mexico_ligamx")
    url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds/'
    
    params = {
        'apiKey': API_KEY,
        'regions': REGION,
        'markets': MARKET,
        'oddsFormat': 'decimal'
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error de API ({response.status_code}): {response.json().get('message')}")
            return pd.DataFrame()

        data = response.json()
        partidos_list = []

        for entry in data:
            if entry['bookmakers']:
                bookie_data = entry['bookmakers'][0]
                outcomes = bookie_data['markets'][0]['outcomes']
                
                try:
                    q1 = next(o['price'] for o in outcomes if o['name'] == entry['home_team'])
                    q2 = next(o['price'] for o in outcomes if o['name'] == entry['away_team'])
                    
                    partidos_list.append({
                        "match": f"{entry['home_team']} vs {entry['away_team']}",
                        "quota1": q1,
                        "quota2": q2,
                        "bookie": bookie_data['title']
                    })
                except Exception:
                    continue

        df = pd.DataFrame(partidos_list)
        os.makedirs('campionati', exist_ok=True)
        df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
        print(f"✅ ¡Conseguidos {len(partidos_list)} partidos reales!")
        return df

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return pd.DataFrame()

def allFromCampionato(df):
    pass
