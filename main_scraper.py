# Archivo: main_scraper.py
import scrapper_engine as seg

# Ligas que queremos actualizar
ligas = ["0", "01", "02", "06"]

print("🚀 Iniciando Raspador NuviCore...")

for liga_id in ligas:
    print(f"--- Procesando ID: {liga_id} ---")
    seg.scaricaCampionato(liga_id)

print("🏁 Proceso de raspado finalizado.")
