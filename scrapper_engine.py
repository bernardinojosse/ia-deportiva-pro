import requests
import pandas as pd
import os

# Carga de llaves desde el entorno de GitHub
ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY')

def generar_pick_pro(q1, q2):
    """Lógica matemática para definir el pick"""
    prob_l = 1 / q1
    prob_v = 1 / q2
    
    if q1 < 1.60:
        return "🔥 PICK: Victoria Local (Alta Probabilidad)"
    elif q2 < 1.60:
        return "🚀 PICK: Victoria Visitante (Favorito)"
    elif abs(prob_l - prob_v) < 0.10:
        return "⚖️ PICK: Empate o Ambos Anotan (Juego Cerrado)"
    else:
        return "⚽ PICK: Más de 2.5 Goles (Valor Estadístico)"

def scaricaCampionato(id_liga):
    # Diccionario de ligas
    ligas_dict = {
        "0": "soccer_italy_serie_a", 
        "01": "soccer_mexico_ligamx", 
        "02": "soccer_uefa_champions_league", 
        "04": "soccer_england_league_1", 
        "06": "soccer_spain_la_liga"
    }
    sport = ligas_dict.get(id_liga, "soccer_mexico_ligamx")
    
    # Usamos region 'us' para asegurar cobertura de Liga MX y casas latinas
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=us&markets=h2h'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ No hay datos para {sport}")
            return pd.DataFrame()

        lista_partidos = []
        for evento in data:
            if evento.get('bookmakers'):
                outcomes = evento['bookmakers'][0]['markets'][0]['outcomes']
                try:
                    q1 = next(o['price'] for o in outcomes if o['name'] == evento['home_team'])
                    q2 = next(o['price'] for o in outcomes if o['name'] == evento['away_team'])
                    
                    lista_partidos.append({
                        "match": f"{evento['home_team']} vs {evento['away_team']}",
                        "quota1": q1,
                        "quota2": q2,
                        "bookie": evento['bookmakers'][0]['title'],
                        "pick": generar_pick_pro(q1, q2)
                    })
                except: continue

        if lista_partidos:
            df = pd.DataFrame(lista_partidos)
            os.makedirs('campionati', exist_ok=True)
            df.to_csv(f"campionati/campionato{id_liga}.csv", index=False)
            print(f"✅ {sport} guardado con {len(lista_partidos)} partidos.")
            return df
        return pd.DataFrame()

    except Exception as e:
        print(f"❌ Error en motor: {e}")
        return pd.DataFrame()

def allFromCampionato(df):
    """Función de soporte para el scraper principal"""
    return df
