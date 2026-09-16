# Importamos pandas para manejar los datos
import pandas as pd

# Importamos Random Forest
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# 1. LEER LOS PARTIDOS
# ==========================================

datos = pd.read_csv("partidos.csv")

# Convertimos la fecha a formato fecha
datos["fecha"] = pd.to_datetime(datos["fecha"])

# Ordenamos los partidos por fecha
datos = datos.sort_values("fecha")


# ==========================================
# 2. CALCULAR EL ELO ACTUAL DE CADA EQUIPO
# ==========================================

# Buscamos todos los equipos que aparecen
equipos = sorted(
    set(datos["equipo_local"])
    | set(datos["equipo_visitante"])
)

# Todos comienzan con ELO 1500
elo_actual = {
    equipo: 1500
    for equipo in equipos
}

# K determina cuánto cambia el ELO
K = 32


# Recorremos todos los partidos históricos
for _, partido in datos.iterrows():

    local = partido["equipo_local"]
    visitante = partido["equipo_visitante"]

    elo_local = elo_actual[local]
    elo_visitante = elo_actual[visitante]


    # Probabilidad esperada del equipo local
    esperado_local = 1 / (
        1 + 10 ** (
            (elo_visitante - elo_local) / 400
        )
    )

    esperado_visitante = 1 - esperado_local


    # Convertimos el resultado a puntos ELO
    if partido["resultado"] == "S":

        puntos_local = 1.0
        puntos_visitante = 0.0

    elif partido["resultado"] == "H":

        puntos_local = 0.5
        puntos_visitante = 0.5

    else:

        puntos_local = 0.0
        puntos_visitante = 1.0


    # Actualizamos el ELO del local
    elo_actual[local] = round(
        elo_local
        + K * (
            puntos_local
            - esperado_local
        )
    )


    # Actualizamos el ELO del visitante
    elo_actual[visitante] = round(
        elo_visitante
        + K * (
            puntos_visitante
            - esperado_visitante
        )
    )


# ==========================================
# 3. PREPARAR LOS DATOS PARA EL MODELO
# ==========================================

# Variables que utiliza el modelo
X = datos[[
    "forma_local",
    "forma_visitante",
    "promedio_goles_local",
    "promedio_goles_visitante",
    "elo_local",
    "elo_visitante"
]]

# Variable que queremos predecir
y = datos["resultado"]


# ==========================================
# 4. CREAR Y ENTRENAR EL MODELO
# ==========================================

modelo = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

modelo.fit(X, y)


# ==========================================
# 5. MOSTRAR EQUIPOS DISPONIBLES
# ==========================================

print("\n=== EQUIPOS DISPONIBLES ===\n")

for equipo in equipos:
    print("-", equipo)


# ==========================================
# 6. PEDIR LOS EQUIPOS
# ==========================================

print("\n=== PREDICCIÓN DE PARTIDO ===\n")

equipo_local = input(
    "Nombre del equipo local: "
)

equipo_visitante = input(
    "Nombre del equipo visitante: "
)


# ==========================================
# 7. VALIDAR QUE LOS EQUIPOS EXISTAN
# ==========================================

if equipo_local not in elo_actual:

    print("\nEl equipo local no existe.")
    exit()


if equipo_visitante not in elo_actual:

    print("\nEl equipo visitante no existe.")
    exit()


if equipo_local == equipo_visitante:

    print("\nUn equipo no puede jugar contra sí mismo.")
    exit()


# ==========================================
# 8. PEDIR LOS DATOS DEL NUEVO PARTIDO
# ==========================================

forma_local = int(
    input("Forma del equipo local [0-15]: ")
)

forma_visitante = int(
    input("Forma del equipo visitante [0-15]: ")
)

promedio_goles_local = float(
    input("Promedio de goles del local: ")
)

promedio_goles_visitante = float(
    input("Promedio de goles del visitante: ")
)


# ==========================================
# 9. OBTENER EL ELO AUTOMÁTICAMENTE
# ==========================================

elo_local = elo_actual[equipo_local]
elo_visitante = elo_actual[equipo_visitante]


print("\n=== ELO ACTUAL ===\n")

print(
    equipo_local,
    "=",
    elo_local
)

print(
    equipo_visitante,
    "=",
    elo_visitante
)


# ==========================================
# 10. CREAR EL NUEVO PARTIDO
# ==========================================

nuevo_partido = pd.DataFrame([{

    "forma_local":
        forma_local,

    "forma_visitante":
        forma_visitante,

    "promedio_goles_local":
        promedio_goles_local,

    "promedio_goles_visitante":
        promedio_goles_visitante,

    "elo_local":
        elo_local,

    "elo_visitante":
        elo_visitante
}])


# ==========================================
# 11. HACER LA PREDICCIÓN
# ==========================================

prediccion = modelo.predict(
    nuevo_partido
)[0]


# ==========================================
# 12. OBTENER PROBABILIDADES
# ==========================================

probabilidades = modelo.predict_proba(
    nuevo_partido
)[0]

# Asociamos cada clase con su probabilidad
probabilidades_por_clase = dict(
    zip(modelo.classes_, probabilidades)
)


# ==========================================
# 13. MOSTRAR PROBABILIDADES
# ==========================================

print("\n=== PROBABILIDADES ===\n")

print(
    equipo_local,
    f"{probabilidades_por_clase['S'] * 100:.2f}%"
)

print(
    "Empate",
    f"{probabilidades_por_clase['H'] * 100:.2f}%"
)

print(
    equipo_visitante,
    f"{probabilidades_por_clase['A'] * 100:.2f}%"
)


# ==========================================
# 14. MOSTRAR RESULTADO FINAL
# ==========================================

print("\n=== PREDICCIÓN FINAL ===\n")


if prediccion == "S":

    print(
        "Predicción: gana",
        equipo_local
    )

elif prediccion == "H":

    print(
        "Predicción: empate"
    )

else:

    print(
        "Predicción: gana",
        equipo_visitante
    )