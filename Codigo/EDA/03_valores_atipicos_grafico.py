from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[2]

RUTA_DATOS = (
    RAIZ
    / "Data"
    / "raw"
    / "predicciones_personas.csv"
)

# Leer dataset
datos = pd.read_csv(RUTA_DATOS)

# Variables numéricas para revisar valores atípicos
columnas = [
    "Votes_for_Home",
    "Votes_for_Draw",
    "Votes_for_Away",
    "Total_Bettors"
]

# Estilo
sns.set(style="whitegrid")

# Crear boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=datos[columnas], palette="Set2")

plt.title("Detección de valores atípicos")
plt.ylabel("Valores")
plt.xlabel("Variables")

plt.tight_layout()
plt.savefig(
    RAIZ
    / "Presentaciones"
    / "Graficos"
    / "03_valores_atipicos_boxplot.png",
    dpi=200
)
plt.show()