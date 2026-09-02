import pandas as pd
import os


# ==========================================
# 1. RUTA DEL DATASET
# ==========================================

ruta = "/home/fabian/.cache/kagglehub/datasets/analystmasters/world-soccer-live-data-feed/versions/2"

archivos = [
    "analystm_mode_1_v1.csv",
    "analystm_mode_2_v1.csv",
    "analystm_mode_3_v1.csv",
    "analystm_mode_4_v1.csv"
]


# ==========================================
# 2. UNIR LOS 4 ARCHIVOS
# ==========================================

lista_datos = []

for archivo in archivos:

    ruta_archivo = os.path.join(
        ruta,
        archivo
    )

    datos = pd.read_csv(
        ruta_archivo,
        low_memory=False
    )

    lista_datos.append(datos)


datos = pd.concat(
    lista_datos,
    ignore_index=True
)


print("==============================")
print("DATOS CARGADOS")
print("==============================")

print("Cantidad total de partidos:", len(datos))


# ==========================================
# 3. CALCULAR RESULTADO REAL
# ==========================================

def obtener_resultado_real(fila):

    goles_local = fila["Results_1"]
    goles_visitante = fila["Results_2"]

    if goles_local > goles_visitante:
        return "S"

    elif goles_local < goles_visitante:
        return "A"

    else:
        return "H"


datos["resultado_real"] = datos.apply(
    obtener_resultado_real,
    axis=1
)


# ==========================================
# 4. PREDICCIÓN DE LAS PERSONAS
# ==========================================

def obtener_prediccion_personas(fila):

    votos_local = fila["Votes_for_Home"]
    votos_empate = fila["Votes_for_Draw"]
    votos_visitante = fila["Votes_for_Away"]

    if (
        votos_local >= votos_empate
        and votos_local >= votos_visitante
    ):
        return "S"

    elif (
        votos_empate >= votos_local
        and votos_empate >= votos_visitante
    ):
        return "H"

    else:
        return "A"


datos["prediccion_personas"] = datos.apply(
    obtener_prediccion_personas,
    axis=1
)


# ==========================================
# 5. SABER SI LA GENTE ACERTÓ
# ==========================================

datos["acierto_personas"] = (
    datos["prediccion_personas"]
    == datos["resultado_real"]
)


# ==========================================
# 6. CALCULAR RESULTADOS
# ==========================================

total_partidos = len(datos)

aciertos = datos[
    "acierto_personas"
].sum()

errores = (
    total_partidos
    - aciertos
)

porcentaje_acierto = (
    aciertos
    / total_partidos
) * 100


# ==========================================
# 7. MOSTRAR RESULTADOS
# ==========================================

print("\n==============================")
print("PREDICCIÓN DE LAS PERSONAS")
print("==============================")

print(
    "Partidos analizados:",
    total_partidos
)

print(
    "Aciertos:",
    aciertos
)

print(
    "Errores:",
    errores
)

print(
    f"Exactitud de las personas: "
    f"{porcentaje_acierto:.2f}%"
)


# ==========================================
# 8. MOSTRAR ALGUNOS EJEMPLOS
# ==========================================

print("\n==============================")
print("EJEMPLOS")
print("==============================")

columnas_mostrar = [
    "Team_1",
    "Team_2",
    "Votes_for_Home",
    "Votes_for_Draw",
    "Votes_for_Away",
    "prediccion_personas",
    "Results_1",
    "Results_2",
    "resultado_real",
    "acierto_personas"
]

print(
    datos[
        columnas_mostrar
    ].head(20).to_string(
        index=False
    )
)


# ==========================================
# 9. GUARDAR RESULTADOS
# ==========================================

datos.to_csv(
    "predicciones_personas.csv",
    index=False
)

print(
    "\nArchivo guardado como:"
)

print(
    "predicciones_personas.csv"
)

