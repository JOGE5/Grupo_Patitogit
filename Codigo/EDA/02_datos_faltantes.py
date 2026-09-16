import pandas as pd
from pathlib import Path

# ==============================
# RUTAS
# ==============================

RAIZ = Path(__file__).resolve().parents[2]

RUTA_DATOS = (
    RAIZ
    / "Data"
    / "raw"
    / "predicciones_personas.csv"
)

# ==============================
# CARGAR DATOS
# ==============================

datos = pd.read_csv(RUTA_DATOS)

# ==============================
# ANALIZAR DATOS FALTANTES
# ==============================

faltantes = datos.isnull().sum()

# Mostrar solo columnas con valores faltantes
faltantes = faltantes[faltantes > 0]

# Porcentaje de datos faltantes por columna
porcentaje = (
    faltantes / len(datos) * 100
).round(2)

# Crear tabla resumen
resumen = pd.DataFrame({
    "Valores faltantes": faltantes,
    "Porcentaje (%)": porcentaje
})

# ==============================
# RESULTADOS
# ==============================

print("\n==============================")
print("DATOS FALTANTES")
print("==============================\n")

print(resumen)

print("\n==============================")
print("RESUMEN")
print("==============================")

print(f"Total de registros: {len(datos)}")
print(f"Total de columnas: {len(datos.columns)}")
print(
    f"Total de celdas faltantes: "
    f"{datos.isnull().sum().sum()}"
)

print(
    f"Columnas con datos faltantes: "
    f"{len(faltantes)}"
)