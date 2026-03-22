import scrapper_engine as seg

ligas = ["0", "01", "02", "04", "06"]

for liga in ligas:
    print(f"🔍 Iniciando liga {liga}...")
    df = seg.scaricaCampionato(liga)
    if not df.empty:
        seg.allFromCampionato(df)
        print(f"✅ Liga {liga} completada.")
    else:
        print(f"⚠️ Liga {liga} sin datos.")
