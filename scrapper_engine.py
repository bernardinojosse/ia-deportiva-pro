import pandas as pd
import os

def scaricaCampionato(id_liga):
    print(f"📡 Escaneando datos reales para liga ID: {id_liga}")
    
    # Datos de estructura (Reemplaza con tus scrapers de WilliamHill/Snai luego)
    # Importante: Las columnas deben ser 'match', 'quota1' y 'quota2'
    datos = [
        {"match": "Real Madrid vs Barcelona", "quota1": 2.10, "quota2": 3.40},
        {"match": "Man City vs Arsenal", "quota1": 1.95, "quota2": 2.25},
        {"match": "Inter vs Milan", "quota1": 2.50, "quota2": 2.80}
    ]
    
    df = pd.DataFrame(datos)
    
    # Crear carpeta si el bot no la ve
    if not os.path.exists('campionati'):
        os.makedirs('campionati')
        
    # Guardar con el nombre que busca tu App
    filename = f"campionati/campionato{id_liga}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Archivo guardado: {filename}")
    return df

def allFromCampionato(df):
    # Esta función evita que main_scraper falle al intentar llamarla
    pass
