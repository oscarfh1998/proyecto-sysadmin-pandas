
import pandas as pd
import os
import glob
import numpy as np

# Carpeta de origen y destino
carpeta = "data/raw"
destino = "data/processed"

os.makedirs(destino, exist_ok=True)

# Buscar todos los archivos Parquet
archivos = glob.glob(os.path.join(carpeta, "*.parquet"))

datasets = []

print("=" * 60)
print("UNIFICACIÓN DEL DATASET CICIDS2017")
print("=" * 60)

# Leer cada archivo
for archivo in sorted(archivos):

    nombre = os.path.basename(archivo)

    print(f"\nCargando: {nombre}")

    df = pd.read_parquet(archivo)

    # Identificar el archivo de procedencia
    df["Dataset_Source"] = nombre

    datasets.append(df)

    print("Registros:", len(df))

# Unificar todos los archivos
print("\nUniendo los datasets...")

df_completo = pd.concat(datasets, ignore_index=True)

# Limpiar nombres de columnas
df_completo.columns = df_completo.columns.str.strip()

# Sustituir valores infinitos por nulos
df_completo.replace([np.inf, -np.inf], np.nan, inplace=True)

# Comprobar duplicados después de la unión
duplicados = df_completo.duplicated().sum()

print("\nDuplicados encontrados:", duplicados)

# Eliminar duplicados, si existen
df_completo.drop_duplicates(inplace=True)

# Resumen general
print("\n" + "=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print("Total de registros:", len(df_completo))
print("Total de columnas:", len(df_completo.columns))

print("\nDistribución de etiquetas:")
print(df_completo["Label"].value_counts())

print("\nValores nulos por columna:")
print(df_completo.isnull().sum().sum())

# Guardar dataset unificado
ruta_salida = os.path.join(destino, "cicids2017_completo.parquet")

df_completo.to_parquet(ruta_salida, index=False)

print("\nDataset guardado en:", ruta_salida)
print("UNIFICACIÓN FINALIZADA")
