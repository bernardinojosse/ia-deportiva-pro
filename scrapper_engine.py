import requests
import pandas as pd
import os

# Estas variables leen de los Secrets que acabas de poner
ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY')

def generar_pick_dinamico(q1, q2):
    if q1 < 1.65: return "🔥 LOCAL FAVORITO"
    if q2 < 1.65: return "🚀 VISITA FAVORITA"
    return "⚖️ AMBOS ANOTAN / EMPATE"

def scaricaCampionato(id_liga):
    deportes = {"0": "soccer_italy_serie_a", "01": "soccer_mexico_ligamx", "02": "soccer_uefa_champions_league", "06": "soccer_spain_la_liga"}
    sport = deportes.get(id_liga, "soccer_mexico_ligamx")
    
    # URL con region 'us' para asegurar datos de México
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=us&markets=h2h'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Si la respuesta no es una lista, hay un problema con la Key
        if not isinstance(data, list):
            print(f"❌ Error de API: {data}")
            return pd.DataFrame()

        partidos = []
        for evento in data:
            if not evento.get('bookmakers'): continue
            
            try:
                bookie = evento['bookmakers'][0]
                outcomes = bookie['markets'][0]['outcomes']
                
                # Buscamos cuotas por nombre de equipo
                q1 = next(o['price'] for o in outcomes if o['name'] == evento['home_team'])
                q2 = next(o['price'] for o in outcomes if o['name'] == evento['away_team'])
                
                partidos.append({
                    "match": f"{evento['home_team']} vs {evento['away_team']}",
                    "quota1": q1,
                    "quota2": q2,
                    "bookie": bookie['title'],
                    "pick": generar_pick_dinamico(q1, q2)
                })
            except: continue

        if partidos:
            df = pd.DataFrame(partidos)
            os.makedirs('campionati', exist_ok=True)
            df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
            print(f"✅ Liga {id_liga} actualizada.")
            return df
        
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        return pd.DataFrame()

def allFromCampionato(df):
    return df
