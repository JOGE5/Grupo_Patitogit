import pandas as pd
import os

ruta = "/home/fabian/.cache/kagglehub/datasets/analystmasters/world-soccer-live-data-feed/versions/2"

archivos = [
    "analystm_mode_1_v1.csv",
    "analystm_mode_2_v1.csv",
    "analystm_mode_3_v1.csv",
    "analystm_mode_4_v1.csv"
]

for archivo in archivos:

    print("\n==============================")
    print(archivo)
    print("==============================")

    datos = pd.read_csv(
        os.path.join(ruta, archivo),
        low_memory=False
    )

    print("Filas:", len(datos))

    print("\nColumnas:")
    for columna in datos.columns:
        print("-", columna)

