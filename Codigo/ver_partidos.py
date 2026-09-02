import pandas as pd

ruta = "/home/fabian/.cache/kagglehub/datasets/analystmasters/world-soccer-live-data-feed/versions/2/analystm_mode_1_v1.csv"

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
