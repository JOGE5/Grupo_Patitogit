# ==========================================
# MODELO REAL DE PREDICCIÓN DE FÚTBOL
# ==========================================

# Pandas sirve para trabajar con los datos
import pandas as pd

# Random Forest será nuestro modelo de Machine Learning
from sklearn.ensemble import RandomForestClassifier

# Herramientas para evaluar el modelo
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# 1. LEER LOS DATOS REALES
# ==========================================

# Este archivo fue creado previamente por crear_variables.py
datos = pd.read_csv("partidos_modelo.csv")

print("==============================")
print("DATOS CARGADOS")
print("==============================")

print("Cantidad total de partidos:", len(datos))


# ==========================================
# 2. VARIABLES DE ENTRADA
# ==========================================

# X contiene la información que el modelo
# utilizará para intentar predecir el resultado.
#
# Por ahora usamos:
# - ELO del equipo local antes del partido
# - ELO del equipo visitante antes del partido

X = datos[[
    "elo_local",
    "elo_visitante"
]]


# ==========================================
# 3. VARIABLE OBJETIVO
# ==========================================

# y representa lo que queremos predecir:
#
# S = gana el equipo local
# H = empate
# A = gana el equipo visitante

y = datos["resultado"]


# ==========================================
# 4. DIVIDIR ENTRENAMIENTO Y PRUEBA
# ==========================================

# Usamos:
# 80% de los partidos para entrenar
# 20% para probar
#
# NO mezclamos los partidos porque son datos
# cronológicos. Queremos entrenar con partidos
# antiguos y probar con partidos posteriores.

punto_division = int(
    len(datos) * 0.80
)


# Primer 80%
X_entrenamiento = X.iloc[
    :punto_division
]

y_entrenamiento = y.iloc[
    :punto_division
]


# Último 20%
X_prueba = X.iloc[
    punto_division:
]

y_prueba = y.iloc[
    punto_division:
]


print("\n==============================")
print("DIVISIÓN DE DATOS")
print("==============================")

print(
    "Partidos para entrenamiento:",
    len(X_entrenamiento)
)

print(
    "Partidos para prueba:",
    len(X_prueba)
)


# ==========================================
# 5. CREAR EL MODELO
# ==========================================

modelo = RandomForestClassifier(

    # Cantidad de árboles
    n_estimators=200,

    # Profundidad máxima
    max_depth=10,

    # Permite obtener resultados reproducibles
    random_state=42
)


# ==========================================
# 6. ENTRENAR EL MODELO
# ==========================================

print("\nEntrenando modelo...")

modelo.fit(
    X_entrenamiento,
    y_entrenamiento
)

print("Modelo entrenado correctamente.")


# ==========================================
# 7. REALIZAR PREDICCIONES
# ==========================================

# El modelo intenta predecir los partidos
# que NO utilizó durante el entrenamiento.

predicciones = modelo.predict(
    X_prueba
)


# ==========================================
# 8. FUNCIÓN PARA EVALUAR
# ==========================================

def evaluar_predicciones(
    resultados_reales,
    resultados_predichos
):

    # Total de partidos evaluados
    total = len(resultados_reales)

    # Convertimos los datos para compararlos
    reales = resultados_reales.reset_index(
        drop=True
    )

    predichos = pd.Series(
        resultados_predichos
    )

    # Contamos los aciertos
    acertados = (
        reales == predichos
    ).sum()

    # Los demás son errores
    fallados = total - acertados

    # Porcentajes
    porcentaje_acierto = (
        acertados / total
    ) * 100

    porcentaje_error = (
        fallados / total
    ) * 100


    print("\n==============================")
    print("RESULTADOS DEL MODELO")
    print("==============================")

    print(
        "Partidos evaluados:",
        total
    )

    print(
        f"Partidos acertados: "
        f"{acertados} "
        f"({porcentaje_acierto:.2f}%)"
    )

    print(
        f"Partidos fallados: "
        f"{fallados} "
        f"({porcentaje_error:.2f}%)"
    )


    return (
        porcentaje_acierto,
        porcentaje_error
    )


# Ejecutamos la función
porcentaje_acierto, porcentaje_error = (
    evaluar_predicciones(
        y_prueba,
        predicciones
    )
)


# ==========================================
# 9. REPORTE DE CLASIFICACIÓN
# ==========================================

print("\n==============================")
print("REPORTE DE CLASIFICACIÓN")
print("==============================")

print(
    classification_report(
        y_prueba,
        predicciones,
        zero_division=0
    )
)


# ==========================================
# 10. MATRIZ DE CONFUSIÓN
# ==========================================

print("==============================")
print("MATRIZ DE CONFUSIÓN")
print("==============================")

print(
    confusion_matrix(
        y_prueba,
        predicciones,
        labels=["A", "H", "S"]
    )
)


# ==========================================
# 11. MODELO BASE PARA COMPARACIÓN
# ==========================================

# Creamos una comparación muy sencilla:
# predecir SIEMPRE que gana el equipo local.
#
# Esto nos permite saber si nuestro modelo
# realmente supera una estrategia básica.

prediccion_base = [
    "S"
    for _ in range(len(y_prueba))
]

acierto_base = accuracy_score(
    y_prueba,
    prediccion_base
)


print("\n==============================")
print("COMPARACIÓN CON MODELO BASE")
print("==============================")

print(
    f"Modelo base (siempre local): "
    f"{acierto_base * 100:.2f}%"
)

print(
    f"Random Forest: "
    f"{porcentaje_acierto:.2f}%"
)


# ==========================================
# 12. RESUMEN FINAL
# ==========================================

print("\n==============================")
print("RESUMEN")
print("==============================")

print(
    f"Acierto del modelo: "
    f"{porcentaje_acierto:.2f}%"
)

print(
    f"Margen de error: "
    f"{porcentaje_error:.2f}%"
)