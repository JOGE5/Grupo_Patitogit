# Importamos pandas para leer el archivo CSV
import pandas as pd


# Leemos los datos guardados en partidos.csv
tabla = pd.read_csv("partidos.csv")


# Mostramos los datos para comprobar que se cargaron bien
print("Datos cargados:")
print(tabla)


# X contiene las variables que usaremos para predecir
# Quitamos la columna "resultado" porque esa es la respuesta
# Elegimos únicamente las variables numéricas
# que el modelo utilizará para hacer predicciones
X = tabla[[
    "forma_local",
    "forma_visitante",
    "promedio_goles_local",
    "promedio_goles_visitante",
    "elo_local",
    "elo_visitante"
]]


# y contiene únicamente la variable que queremos predecir
y = tabla["resultado"]


print("\nVariables de entrada (X):")
print(X)


print("\nVariable objetivo (y):")
print(y)

# Importamos una herramienta para dividir los datos
from sklearn.model_selection import train_test_split


# Separamos los datos:
# 80% para entrenamiento
# 20% para prueba
X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Mostramos cuántos datos quedaron en cada grupo
print("\nDatos para entrenamiento:", len(X_entrenamiento))
print("Datos para prueba:", len(X_prueba))

# Importamos el modelo Random Forest
from sklearn.ensemble import RandomForestClassifier


# Creamos el modelo
modelo = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)


# Entrenamos el modelo
modelo.fit(X_entrenamiento, y_entrenamiento)

print("\nModelo entrenado correctamente.")


# Importamos una función para medir qué porcentaje de predicciones fueron correctas
from sklearn.metrics import accuracy_score


# El modelo intenta predecir los resultados de los datos de prueba
predicciones = modelo.predict(X_prueba)


# Comparamos las predicciones con los resultados reales
exactitud = accuracy_score(y_prueba, predicciones)


# Mostramos el porcentaje de aciertos
print("\nExactitud del modelo:")
print(f"{exactitud * 100:.2f}%")