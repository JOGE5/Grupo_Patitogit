import kagglehub
import os

print("Descargando dataset...")

path = kagglehub.dataset_download(
    "analystmasters/world-soccer-live-data-feed"
)

print("\nRuta del dataset:")
print(path)

print("\nArchivos encontrados:")

for archivo in os.listdir(path):
    print("-", archivo)
