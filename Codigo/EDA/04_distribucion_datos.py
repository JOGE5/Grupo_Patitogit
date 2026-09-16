from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[2]

RUTA_DATOS = (
    RAIZ
    / "Data"
    / "raw"
    / "predicciones_personas.csv"
)

# Leer dataset
datos = pd.read_csv(RUTA_DATOS)

# Contar resultados
conteo = datos["resultado_real"].value_counts()

# Orden que queremos mostrar
orden = ["S", "H", "A"]
conteo = conteo.reindex(orden)

# Nombres entendibles
nombres = [
    "Victoria local",
    "Empate",
    "Victoria visitante"
]

# Crear gráfico
plt.figure(figsize=(8, 5))

barras = plt.bar(
    nombres,
    conteo.values
)

plt.title("Distribución de los resultados de los partidos")
plt.xlabel("Resultado")
plt.ylabel("Cantidad de partidos")

# Mostrar número encima de cada barra
for barra, cantidad in zip(barras, conteo.values):

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height(),
        str(cantidad),
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Guardar imagen
plt.savefig(
    RAIZ
    / "Presentaciones"
    / "Graficos"
    / "04_distribucion_resultados.png",
    dpi=200
)

plt.show()