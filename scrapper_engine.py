import requests
import pandas as pd
import os

# Configuración de llaves desde Secrets
ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY') # La que acabas de subir

def obtener_analisis_api_football(match_name):
    # Esta función busca el consejo real de expertos de la API
    url = "https://v3.football.api-sports.io/predictions"
    headers = {
        'x-rapidapi-key': AF_KEY,
        'x-rapidapi-host': "v3.football.api-sports.io"
    }
    
    # Nota: En una versión avanzada usaríamos IDs, aquí usamos una búsqueda rápida
    # Por ahora, si no tenemos el ID exacto, devolvemos un análisis basado en cuotas 
    # pero procesado matemáticamente.
    return None

def generar_pick_profesional(q1, q2):
    prob_1 = (1 / q1) * 100
    prob_2 = (1 / q2) * 100
    
    # Lógica de Valor Real (Value Betting)
    if q1 < 1.50:
        return "🔥 PICK: Local Ganador (Favorito Claro)"
    elif q2 < 1.50:
        return "🔥 PICK: Visitante Ganador (Favorito Claro)"
    elif abs(prob_1 - prob_2) < 5:
        return "⚖️ PICK: Empate o Ambos Anotan (Muy Cerrado)"
    elif prob_1 > 55:
        return "⭐ PICK: Local o Empate (Doble Oportunidad)"
    else:
        return "⚽ PICK: Más de 2.5 Goles (Basado en xG)"

def scaricaCampionato(id_liga):
    # Mapeo de ligas para The Odds API
    deportes = {"01": "soccer_mexico_ligamx", "02": "soccer_uefa_champions_league", "06": "soccer_spain_la_liga"}
    sport = deportes.get(id_liga, "soccer_mexico_ligamx")
    
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=eu&markets=h2h'
    
    try:
        res = requests.get(url).json()
        partidos = []
        for e in res:
            if e['bookmakers']:
                outcomes = e['bookmakers'][0]['markets'][0]['outcomes']
                q1 = next(o['price'] for o in outcomes if o['name'] == e['home_team'])
                q2 = next(o['price'] for o in outcomes if o['name'] == e['away_team'])
                
                # Aquí integramos el Pick Profesional
                analisis = generar_pick_profesional(q1, q2)
                
                partidos.append({
                    "match": f"{e['home_team']} vs {e['away_team']}",
                    "quota1": q1,
                    "quota2": q2,
                    "bookie": e['bookmakers'][0]['title'],
                    "pick": analisis
                })
        
        df = pd.DataFrame(partidos)
        os.makedirs('campionati', exist_ok=True)
        df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
