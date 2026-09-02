# ==========================================
# 01_ENTENDIMIENTO_NEGOCIO.PY
# EDA + BASELINE
# ==========================================

import pandas as pd


# ==========================================
# 1. CARGAR DATOS
# ==========================================

datos = pd.read_csv("partidos_modelo.csv")

print("==============================")
print("EDA - ANÁLISIS EXPLORATORIO")
print("==============================")

print("\nCantidad total de partidos:")
print(len(datos))

print("\nCantidad de columnas:")
print(len(datos.columns))

print("\nColumnas disponibles:")
print(datos.columns.tolist())


# ==========================================
# 2. DISTRIBUCIÓN DE RESULTADOS
# ==========================================

print("\n==============================")
print("DISTRIBUCIÓN DE RESULTADOS")
print("==============================")

conteo_resultados = datos["resultado"].value_counts()

print(conteo_resultados)

total = len(datos)

for clase, cantidad in conteo_resultados.items():

    porcentaje = (
        cantidad / total
    ) * 100

    if clase == "S":
        nombre = "Victoria local"

    elif clase == "H":
        nombre = "Empate"

    else:
        nombre = "Victoria visitante"

    print(
        f"{nombre}: "
        f"{cantidad} partidos "
        f"({porcentaje:.2f}%)"
    )


# ==========================================
# 3. PROMEDIOS BÁSICOS
# ==========================================

print("\n==============================")
print("PROMEDIOS BÁSICOS")
print("==============================")

print(
    "Promedio de goles local:",
    round(
        datos["goles_local"].mean(),
        2
    )
)

print(
    "Promedio de goles visitante:",
    round(
        datos["goles_visitante"].mean(),
        2
    )
)

print(
    "Promedio ELO local:",
    round(
        datos["elo_local"].mean(),
        2
    )
)

print(
    "Promedio ELO visitante:",
    round(
        datos["elo_visitante"].mean(),
        2
    )
)


# ==========================================
# 4. BASELINE
# ==========================================

print("\n==============================")
print("BASELINE")
print("==============================")

# Estrategia base:
# predecir siempre la clase más frecuente

clase_mas_frecuente = (
    datos["resultado"]
    .value_counts()
    .idxmax()
)

print(
    "Clase más frecuente:",
    clase_mas_frecuente
)

# Creamos una predicción base
predicciones_base = [
    clase_mas_frecuente
    for _ in range(len(datos))
]

# Comparamos con el resultado real
aciertos = 0

for real, predicho in zip(
    datos["resultado"],
    predicciones_base
):

    if real == predicho:
        aciertos += 1


fallos = total - aciertos

porcentaje_acierto = (
    aciertos / total
) * 100

porcentaje_error = (
    fallos / total
) * 100


print(
    f"\nPartidos analizados: "
    f"{total}"
)

print(
    f"Partidos acertados: "
    f"{aciertos} "
    f"({porcentaje_acierto:.2f}%)"
)

print(
    f"Partidos fallados: "
    f"{fallos} "
    f"({porcentaje_error:.2f}%)"
)


# ==========================================
# 5. INTERPRETACIÓN
# ==========================================

print("\n==============================")
print("INTERPRETACIÓN")
print("==============================")

print(
    "El baseline representa una estrategia "
    "simple que siempre predice el resultado "
    "más frecuente del dataset."
)

print(
    "El futuro modelo de Machine Learning "
    "deberá superar este porcentaje para "
    "demostrar una mejora real."
)