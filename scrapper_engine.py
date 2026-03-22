import requests
import pandas as pd
import os

# Configuración de llaves desde Secrets
ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY')

def scaricaCampionato(id_liga):
    deportes = {
        "0": "soccer_italy_serie_a", 
        "01": "soccer_mexico_ligamx", 
        "02": "soccer_uefa_champions_league", 
        "04": "soccer_england_league_1", 
        "06": "soccer_spain_la_liga"
    }
    sport = deportes.get(id_liga, "soccer_mexico_ligamx")
    
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=eu&markets=h2h'
    
    try:
        response = requests.get(url)
        res = response.json()
        partidos = []
        
        # Validamos que la respuesta sea una lista con datos
        if isinstance(res, list) and len(res) > 0:
            for e in res:
                if e.get('bookmakers') and len(e['bookmakers']) > 0:
                    outcomes = e['bookmakers'][0]['markets'][0]['outcomes']
                    # Evitamos errores si falta algún equipo en la lista de cuotas
                    try:
                        q1 = next(o['price'] for o in outcomes if o['name'] == e['home_team'])
                        q2 = next(o['price'] for o in outcomes if o['name'] == e['away_team'])
                        
                        partidos.append({
                            "match": f"{e['home_team']} vs {e['away_team']}",
                            "quota1": q1,
                            "quota2": q2,
                            "bookie": e['bookmakers'][0]['title'],
                            "pick": "🔥 Analizando Pick..." 
                        })
                    except StopIteration:
                        continue
        
        if len(partidos) > 0:
            df = pd.DataFrame(partidos)
            os.makedirs('campionati', exist_ok=True)
            df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
            print(f"✅ Liga {id_liga} guardada con {len(partidos)} partidos.")
            return df
        else:
            print(f"⚠️ No hay partidos disponibles para {sport}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Error en scrapper_engine: {e}")
        return pd.DataFrame()

# Función requerida por main_scraper
def allFromCampionato(df):
    return df
