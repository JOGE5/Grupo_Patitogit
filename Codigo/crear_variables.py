import pandas as pd


# ==========================================
# 1. LEER LOS PARTIDOS LIMPIOS
# ==========================================

datos = pd.read_csv("partidos_limpios.csv")

# Convertimos fecha a formato fecha
datos["fecha"] = pd.to_datetime(datos["fecha"])

# Ordenamos cronológicamente
datos = datos.sort_values("fecha").reset_index(drop=True)


# ==========================================
# 2. BUSCAR TODOS LOS EQUIPOS
# ==========================================

equipos = set(datos["equipo_local"]) | set(datos["equipo_visitante"])


# Todos empiezan con ELO 1500
elo_actual = {
    equipo: 1500
    for equipo in equipos
}


# K controla cuánto cambia el ELO
K = 32


# Aquí guardaremos el ELO que tenía cada equipo
# ANTES de jugar cada partido
elos_locales = []
elos_visitantes = []


# ==========================================
# 3. RECORRER LOS PARTIDOS
# ==========================================

for _, partido in datos.iterrows():

    local = partido["equipo_local"]
    visitante = partido["equipo_visitante"]

    # ELO antes del partido
    elo_local = elo_actual[local]
    elo_visitante = elo_actual[visitante]

    # Guardamos esos valores
    elos_locales.append(elo_local)
    elos_visitantes.append(elo_visitante)


    # ======================================
    # 4. CALCULAR RESULTADO ESPERADO
    # ======================================

    esperado_local = 1 / (
        1 + 10 ** (
            (elo_visitante - elo_local) / 400
        )
    )

    esperado_visitante = 1 - esperado_local


    # ======================================
    # 5. CONVERTIR RESULTADO A PUNTOS
    # ======================================

    if partido["resultado"] == "S":

        puntos_local = 1.0
        puntos_visitante = 0.0

    elif partido["resultado"] == "H":

        puntos_local = 0.5
        puntos_visitante = 0.5

    else:

        puntos_local = 0.0
        puntos_visitante = 1.0


    # ======================================
    # 6. ACTUALIZAR ELO
    # ======================================

    nuevo_elo_local = (
        elo_local
        + K * (puntos_local - esperado_local)
    )

    nuevo_elo_visitante = (
        elo_visitante
        + K * (
            puntos_visitante
            - esperado_visitante
        )
    )


    elo_actual[local] = round(nuevo_elo_local)

    elo_actual[visitante] = round(
        nuevo_elo_visitante
    )


# ==========================================
# 7. AGREGAR ELO A LA TABLA
# ==========================================

datos["elo_local"] = elos_locales
datos["elo_visitante"] = elos_visitantes


# ==========================================
# 8. GUARDAR
# ==========================================

datos.to_csv(
    "partidos_modelo.csv",
    index=False
)


# ==========================================
# 9. MOSTRAR RESULTADO
# ==========================================

print("ELO calculado correctamente.\n")

print(
    datos[[
        "fecha",
        "equipo_local",
        "equipo_visitante",
        "elo_local",
        "elo_visitante",
        "resultado"
    ]].head(30)
)

print(
    "\nCantidad de partidos:",
    len(datos)
)