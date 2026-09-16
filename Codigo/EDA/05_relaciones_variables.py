from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[2]

datos = pd.read_csv(
    RAIZ
    / "Data"
    / "processed"
    / "partidos_modelo.csv"
)

fig, ejes = plt.subplots(1, 2, figsize=(13, 5))

# Relación entre ELO y goles del equipo local
sns.scatterplot(
    data=datos,
    x="elo_local",
    y="goles_local",
    hue="resultado",
    alpha=0.6,
    ax=ejes[0]
)
ejes[0].set_title("Relación entre ELO y goles del equipo local")
ejes[0].set_xlabel("ELO local")
ejes[0].set_ylabel("Goles locales")

# Relación entre ELO y goles del equipo visitante
sns.scatterplot(
    data=datos,
    x="elo_visitante",
    y="goles_visitante",
    hue="resultado",
    alpha=0.6,
    ax=ejes[1]
)
ejes[1].set_title("Relación entre ELO y goles del visitante")
ejes[1].set_xlabel("ELO visitante")
ejes[1].set_ylabel("Goles visitantes")

plt.tight_layout()
plt.show()