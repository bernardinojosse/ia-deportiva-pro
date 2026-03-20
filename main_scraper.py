import scrapper_engine as engine
import os
import time

def auto_scan_all():
    # Escaneamos todas las ligas de tu lista
    ligas = ["0", "01", "02", "04", "06"]
    
    for id_l in ligas:
        try:
            print(f"🔍 Iniciando liga {id_l}...")
            tabella = engine.scaricaCampionato(id_l)
            engine.allFromCampionato(tabella)
            time.sleep(1) # Evita bloqueos
        except Exception as e:
            print(f"❌ Error en liga {id_l}: {e}")

if __name__ == "__main__":
    auto_scan_all()
