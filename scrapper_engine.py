import pandas as pd
import os

def scaricaCampionato(id_liga):
    print(f"📡 Generando datos para liga ID: {id_liga}")
    
    # Datos de prueba para activar la App
    datos = [
        {"match": "Real Madrid vs Barcelona", "quota1": 2.10, "quota2": 3.40},
        {"match": "Man City vs Arsenal", "quota1": 1.95, "quota2": 2.25},
        {"match": "Inter vs Milan", "quota1": 2.50, "quota2": 2.80}
    ]
    
    df = pd.DataFrame(datos)
    
    # FORZAR CREACIÓN DE CARPETA
    os.makedirs('campionati', exist_ok=True)
        
    filename = f"campionati/campionato{id_liga}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Archivo creado exitosamente: {filename}")
    return df

def allFromCampionato(df):
    pass
