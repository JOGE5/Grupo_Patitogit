# Importamos pandas para leer los datos
import pandas as pd

# Importamos matplotlib para crear gráficos
import matplotlib.pyplot as plt

# Importamos las herramientas del modelo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay


# Leemos el archivo con los partidos
datos = pd.read_csv("partidos.csv")


# Separamos las variables de entrada
# Elegimos solo las variables numéricas
# que realmente usa el modelo
X = datos[[
    "forma_local",
    "forma_visitante",
    "promedio_goles_local",
    "promedio_goles_visitante",
    "elo_local",
    "elo_visitante"
]]

# Separamos la variable que queremos predecir
y = datos["resultado"]


# Dividimos los datos en entrenamiento y prueba
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Creamos el modelo
modelo = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)


# Entrenamos el modelo
modelo.fit(X_entrenamiento, y_entrenamiento)


# -----------------------------
# GRÁFICA 1:
# IMPORTANCIA DE VARIABLES
# -----------------------------

# Guardamos la importancia que el modelo le da a cada variable
importancias = pd.Series(
    modelo.feature_importances_,
    index=X.columns
).sort_values()


# Creamos la gráfica
plt.figure(figsize=(9, 5))

importancias.plot(kind="barh")

plt.title("Importancia de las variables")
plt.xlabel("Importancia")

plt.tight_layout()

# Guardamos la imagen
plt.savefig("importancia_variables.png", dpi=200)

plt.close()


# -----------------------------
# GRÁFICA 2:
# MATRIZ DE CONFUSIÓN
# -----------------------------

plt.figure(figsize=(6, 5))

ConfusionMatrixDisplay.from_estimator(
    modelo,
    X_prueba,
    y_prueba,
    display_labels=["Visitante", "Empate", "Local"]
)

plt.title("Matriz de confusión")

plt.tight_layout()

# Guardamos la imagen
plt.savefig("matriz_confusion.png", dpi=200)

plt.close()


print("Gráficas generadas correctamente.")