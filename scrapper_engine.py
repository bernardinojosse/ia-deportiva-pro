# Archivo: scrapper_engine.py
import requests
import pandas as pd
import os

# Carga de llaves desde Secrets
ODDS_KEY = os.getenv('ODDS_API_KEY')
AF_KEY = os.getenv('AF_API_KEY')

# --- LÓGICA DE ANÁLISIS ---
def generar_pick_dinamico(q1, q2):
    """
    Analiza cuotas decimales para generar un pick estadístico.
    No es garantía, es análisis de probabilidad.
    """
    # Si falta alguna cuota, no generamos pick
    if not q1 or not q2: return "⚠️ ANALIZANDO..."
    
    # Cuotas muy bajas = Favorito muy claro
    if q1 <= 1.50: return "🔥 LOCAL IMPERDIBLE"
    if q2 <= 1.50: return "🚀 VISITA IMPERDIBLE"
    
    # Probabilidad implícita (p1 y p2 son porcentajes decimales)
    p1 = 1 / q1
    p2 = 1 / q2
    
    # Si la diferencia de probabilidad es menor al 10%, el juego es muy parejo
    if abs(p1 - p2) < 0.10:
        return "⚖️ EMPATE / AMBOS ANOTAN"
    
    # Favoritos moderados
    if q1 < q2: return "✅ LOCAL FAVORITO"
    if q2 < q1: return "✅ VISITA FAVORITA"
    
    return "⚽ OVER 2.5 GOLES"

# --- RASPADO DE DATOS ---
def scaricaCampionato(id_liga):
    # DICCIONARIO CORREGIDO DE LIGAS
    # Usamos nombres que la API de Odds acepte
    deportes = {
        "0": "soccer_italy_serie_a", 
        "01": "soccer_mexico_ligamx", 
        "02": "soccer_uefa_champions_league", # Verificamos este nombre en docs
        "06": "soccer_spain_la_liga"
    }
    
    sport = deportes.get(id_liga)
    if not sport:
        print(f"⚠️ ID de liga desconocido: {id_liga}")
        return pd.DataFrame()
    
    print(f"🔍 Pidiendo cuotas para {sport}...")
    
    # URL de The Odds API
    # Usamos region 'us' que suele cubrir bien casas latinas como Caliente
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={ODDS_KEY}&regions=us&markets=h2h'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Validación de respuesta
        if not isinstance(data, list):
            print(f"❌ Error de API en {sport}: {data}")
            return pd.DataFrame()

        partidos = []
        for evento in data:
            # Buscamos la primera casa de apuestas disponible
            if not evento.get('bookmakers'): continue
            
            try:
                # Obtenemos el primer bookie
                bookie = evento['bookmakers'][0]
                outcomes = bookie['markets'][0]['outcomes']
                
                # Buscamos las cuotas de Local y Visita por nombre de equipo
                h_team = evento['home_team']
                a_team = evento['away_team']
                
                q1 = next(o['price'] for o in outcomes if o['name'] == h_team)
                q2 = next(o['price'] for o in outcomes if o['name'] == a_team)
                
                partidos.append({
                    "match": f"{h_team} vs {a_team}",
                    "quota1": q1,
                    "quota2": q2,
                    "bookie": bookie['title'],
                    "pick": generar_pick_dinamico(q1, q2)
                })
            except Exception as e:
                # Si un partido falla, no detenemos el script
                print(f"⚠️ Error procesando partido en {sport}: {e}")
                continue

        # Si encontramos partidos, los guardamos en CSV
        if partidos:
            df = pd.DataFrame(partidos)
            os.makedirs('campionati', exist_ok=True)
            file_path = f"campionati/campionato{id_liga}.csv"
            df.to_csv(file_path, index=False)
            print(f"✅ {sport} actualizado con {len(partidos)} partidos.")
            return df
        else:
            print(f"⚠️ No se encontraron partidos activos para {sport}")
            return pd.DataFrame()

    except Exception as e:
        print(f"❌ Error crítico en {sport}: {e}")
        return pd.DataFrame()

# Soporte para main_scraper.py
def allFromCampionato(df):
    return df
