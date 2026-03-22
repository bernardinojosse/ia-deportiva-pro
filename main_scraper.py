import scrapper_engine as seg

# Lista de ligas a procesar
ligas = ["0", "01", "02", "04", "06"]

for liga in ligas:
    print(f"🔍 Procesando liga ID: {liga}...")
    df = seg.scaricaCampionato(liga)
    
    if not df.empty:
        seg.allFromCampionato(df)
        print(f"✨ Éxito en liga {liga}")
    else:
        print(f"⏭️ Saltando liga {liga} (sin datos)")
