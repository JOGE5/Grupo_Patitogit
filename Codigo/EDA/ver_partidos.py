from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]

ruta = (
    RAIZ
    / "Data"
    / "raw"
    / "predicciones_personas.csv"
)

datos = pd.read_csv(
    ruta,
    low_memory=False
)

columnas = [
    "Team_1",
    "Team_2",
    "Votes_for_Home",
    "Votes_for_Draw",
    "Votes_for_Away",
    "Total_Bettors",
    "Bet_Perc_on_Home",
    "Bet_Perc_on_Draw",
    "Bet_Perc_on_Away",
    "Results_1",
    "Results_2"
]

print(
    datos[columnas].head(20).to_string(index=False)
)
