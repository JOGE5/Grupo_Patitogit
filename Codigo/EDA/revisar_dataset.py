from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]

ruta = (
    RAIZ
    / "Data"
    / "raw"
    / "predicciones_personas.csv"
)

archivos = [
    "predicciones_personas.csv"
]

for archivo in archivos:

    print("\n==============================")
    print(archivo)
    print("==============================")

    datos = pd.read_csv(
        ruta.parent / archivo,
        low_memory=False
    )

    print("Filas:", len(datos))

    print("\nColumnas:")
    for columna in datos.columns:
        print("-", columna)

