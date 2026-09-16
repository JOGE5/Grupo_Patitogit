import pandas as pd
import numpy as np

# Para que los datos aleatorios sean siempre los mismos
np.random.seed(42)

# Cantidad de partidos
cantidad_partidos = 12000

# Equipos de ejemplo
equipos = [
    "Real Madrid",
    "Barcelona",
    "Manchester City",
    "Liverpool",
    "Arsenal",
    "Bayern Munich",
    "Inter",
    "Milan",
    "PSG",
    "Juventus"
]

# Fechas simuladas
fechas = pd.date_range(
    start="2020-01-01",
    periods=cantidad_partidos,
    freq="D"
)

# Elegimos equipos aleatoriamente
equipos_locales = np.random.choice(
    equipos,
    cantidad_partidos
)

equipos_visitantes = np.random.choice(
    equipos,
    cantidad_partidos
)

# Evitamos que un equipo juegue contra sí mismo
for i in range(cantidad_partidos):
    while equipos_locales[i] == equipos_visitantes[i]:
        equipos_visitantes[i] = np.random.choice(equipos)

# Creamos las variables del partido
datos = pd.DataFrame({

    "fecha": fechas,

    "equipo_local": equipos_locales,

    "equipo_visitante": equipos_visitantes,

    "forma_local":
        np.random.randint(0, 16, cantidad_partidos),

    "forma_visitante":
        np.random.randint(0, 16, cantidad_partidos),

    "promedio_goles_local":
        np.random.uniform(0.3, 3.0, cantidad_partidos),

    "promedio_goles_visitante":
        np.random.uniform(0.3, 3.0, cantidad_partidos),

    # Todos los equipos comienzan con un ELO base de 1500.
# Más adelante iremos actualizando este valor según ganen,
# empaten o pierdan partidos.
"elo_local": np.full(cantidad_partidos, 1500),

"elo_visitante": np.full(cantidad_partidos, 1500)
})

## -----------------------------------
# CALCULAR RESULTADOS Y ELO
# -----------------------------------

# Guardamos el ELO actual de cada equipo.
# Todos empiezan con 1500 puntos.
elo_equipos = {
    equipo: 1500
    for equipo in equipos
}

# K controla cuánto puede subir o bajar el ELO
K = 32

# Aquí guardaremos los resultados
resultados = []


# Recorremos los partidos uno por uno,
# respetando el orden de las fechas.
for i in range(cantidad_partidos):

    # Obtenemos los equipos del partido
    local = datos.loc[i, "equipo_local"]
    visitante = datos.loc[i, "equipo_visitante"]

    # Consultamos el ELO que tienen ANTES del partido
    elo_local_actual = elo_equipos[local]
    elo_visitante_actual = elo_equipos[visitante]

    # Guardamos esos ELO en la tabla
    datos.loc[i, "elo_local"] = elo_local_actual
    datos.loc[i, "elo_visitante"] = elo_visitante_actual


    # Calculamos qué equipo parece más fuerte
    puntuacion = (
        (datos.loc[i, "forma_local"]
         - datos.loc[i, "forma_visitante"]) * 0.2

        + (datos.loc[i, "promedio_goles_local"]
           - datos.loc[i, "promedio_goles_visitante"]) * 1.3

        + (elo_local_actual
           - elo_visitante_actual) / 180

        + 0.6  # pequeña ventaja por jugar de local
    )


    # Añadimos aleatoriedad porque el fútbol
    # no es completamente predecible
    puntuacion += np.random.normal(0, 1.3)


    # Determinamos el resultado
    if puntuacion > 0.8:

        resultado = "S"
        puntos_local = 1.0

    elif puntuacion < -0.8:

        resultado = "A"
        puntos_local = 0.0

    else:

        resultado = "H"
        puntos_local = 0.5


    resultados.append(resultado)


    # -----------------------------------
    # ACTUALIZACIÓN DEL ELO
    # -----------------------------------

    # Calculamos la probabilidad esperada
    # de que gane el equipo local
    esperado_local = 1 / (
        1 + 10 ** (
            (elo_visitante_actual - elo_local_actual) / 400
        )
    )

    # Para el visitante es lo contrario
    esperado_visitante = 1 - esperado_local

    # Resultado real del visitante
    puntos_visitante = 1 - puntos_local


    # Actualizamos el ELO
    nuevo_elo_local = (
        elo_local_actual
        + K * (puntos_local - esperado_local)
    )

    nuevo_elo_visitante = (
        elo_visitante_actual
        + K * (puntos_visitante - esperado_visitante)
    )


    # Guardamos los nuevos valores
    # para los próximos partidos
    elo_equipos[local] = round(nuevo_elo_local)

    elo_equipos[visitante] = round(nuevo_elo_visitante)


# Agregamos los resultados a la tabla
datos["resultado"] = resultados

# Guardamos CSV
datos.to_csv(
    "partidos.csv",
    index=False
)

# Mostramos los primeros partidos
print(datos.head())

print("\nCantidad de partidos:",
      len(datos))

print("\nResultados:")
print(
    datos["resultado"].value_counts()
)