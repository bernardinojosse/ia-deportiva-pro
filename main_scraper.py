import scrapper_engine as engine # Este debe ser el nombre de tu archivo con la lógica que me pasaste
import os
import time

def auto_scan_all():
    # 1. Definimos la lista de todas las ligas según tus IDs originales
    # 0: Serie A, 01: Serie B, 02: Champions, 03: Europa League, etc.
    ligas_a_escanear = ["0", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]
    
    print(f"🚀 Iniciando Escaneo Automático de {len(ligas_a_escanear)} ligas...")
    
    # 2. Aseguramos que las carpetas existan para evitar errores de escritura
    for folder in ['campionati', 'partite']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Carpeta creada: {folder}")

    # 3. Bucle principal de escaneo
    for id_liga in ligas_a_escanear:
        try:
            print(f"🔍 Escaneando Liga ID: {id_liga}...")
            
            # Ejecuta tu función de descarga y matching
            # Esta función ya guarda el CSV en 'campionati/campionato{id}.csv'
            tabella = engine.scaricaCampionato(id_liga) 
            
            # Genera los archivos individuales de partidos en 'partite/'
            engine.allFromCampionato(tabella)
            
            print(f"✅ Liga {id_liga} actualizada correctamente.")
            
            # Pausa de seguridad para evitar bloqueos de las casas de apuestas
            time.sleep(2) 
            
        except Exception as e:
            print(f"❌ Error en Liga {id_liga}: {str(e)}")

if __name__ == "__main__":
    auto_scan_all()
    print("🏁 PROCESO COMPLETADO: Todas las ligas han sido sincronizadas.")
