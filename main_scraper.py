import scrapper_engine as seg

# Ligas que queremos trackear
ids_ligas = ["0", "01", "02", "04", "06"]

print("🚀 Iniciando escaneo NuviCore...")

for l_id in ids_ligas:
    df_resultado = seg.scaricaCampionato(l_id)
    if not df_resultado.empty:
        seg.allFromCampionato(df_resultado)

print("🏁 Proceso finalizado.")
