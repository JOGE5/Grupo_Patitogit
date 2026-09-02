import pandas as pd


# ==========================================
# 1. LEER LOS DATOS REALES
# ==========================================

datos = pd.read_csv("la_liga.csv")


# ==========================================
# 2. ELEGIR SOLO LAS COLUMNAS NECESARIAS
# ==========================================

datos_limpios = datos[[
    "Date",       # Fecha del partido
    "HomeTeam",   # Equipo local
    "AwayTeam",   # Equipo visitante
    "FTHG",       # Goles del local
    "FTAG",       # Goles del visitante
    "FTR"         # Resultado final
]].copy()


# ==========================================
# 3. CAMBIAR NOMBRES A ESPAÑOL
# ==========================================

datos_limpios = datos_limpios.rename(columns={
    "Date": "fecha",
    "HomeTeam": "equipo_local",
    "AwayTeam": "equipo_visitante",
    "FTHG": "goles_local",
    "FTAG": "goles_visitante",
    "FTR": "resultado"
})


# ==========================================
# 4. CONVERTIR LA FECHA
# ==========================================

datos_limpios["fecha"] = pd.to_datetime(
    datos_limpios["fecha"],
    format="%d/%m/%Y"
)


# ==========================================
# 5. CAMBIAR LAS ETIQUETAS DEL RESULTADO
# ==========================================

# En el dataset original:
# H = gana local
# D = empate
# A = gana visitante
#
# En nuestro proyecto:
# S = gana local
# H = empate
# A = gana visitante

datos_limpios["resultado"] = datos_limpios[
    "resultado"
].replace({
    "H": "S",
    "D": "H",
    "A": "A"
})


# ==========================================
# 6. ORDENAR POR FECHA
# ==========================================

datos_limpios = datos_limpios.sort_values(
    "fecha"
).reset_index(drop=True)


# ==========================================
# 7. GUARDAR LOS DATOS LIMPIOS
# ==========================================

datos_limpios.to_csv(
    "partidos_limpios.csv",
    index=False
)


# ==========================================
# 8. MOSTRAR RESULTADO
# ==========================================

print("Datos preparados correctamente.\n")

print(datos_limpios.head())

print(
    "\nCantidad de partidos:",
    len(datos_limpios)
)

print("\nResultados:")

print(
    datos_limpios["resultado"].value_counts()
)