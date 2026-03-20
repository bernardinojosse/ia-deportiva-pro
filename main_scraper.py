import pandas as pd
import os
# Importamos tu lógica principal que me pasaste anteriormente
import scrapper_engine as engine 

def ejecutar_limpieza_directorios():
    """Asegura que existan las carpetas necesarias para no dar error."""
    for folder in ['campionati', 'partite']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Carpeta creada: {folder}")

def run_total_update():
    print(f"--- INICIANDO ESCANEO GLOBAL NUVI-CORE ---")
    ejecutar_limpieza_directorios()
    
    # Lista de IDs de campeonatos basada en tu función init()
    # 0: Serie A, 01: Serie B, 02: Champions, etc.
    campionatos_a_escaneares = ["0", "01", "02", "04", "06", "08", "10"]
    
    for camp_id in campionatos_a_escaneares:
        try:
            print(f"Scrapeando Campeonato ID: {camp_id}...")
            # Llamamos a tu función scaricaCampionato que ya tiene el matching y guardado de CSV
            tabella = engine.scaricaCampionato(camp_id) 
            
            # También ejecutamos la lógica de 'allFromCampionato' para actualizar archivos de partidos
            engine.allFromCampionato(tabella)
            
            print(f"Éxito: Campeonato {camp_id} actualizado.")
        except Exception as e:
            print(f"Error en campeonato {camp_id}: {str(e)}")

if __name__ == '__main__':
    run_total_update()
    print("--- ACTUALIZACIÓN FINALIZADA ---")
