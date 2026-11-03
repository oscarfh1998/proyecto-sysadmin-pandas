
import pandas as pd
import os

# Carpeta donde están los datasets
carpeta = "data/raw"

# Obtener archivos Parquet
archivos = [
    f for f in os.listdir(carpeta)
    if f.endswith(".parquet")
]

print("=" * 60)
print("ANÁLISIS INICIAL DEL DATASET CICIDS2017")
print("=" * 60)

for archivo in sorted(archivos):

    ruta = os.path.join(carpeta, archivo)

    print("\n" + "=" * 60)
    print("ARCHIVO:", archivo)
    print("=" * 60)

    # Cargar archivo
    df = pd.read_parquet(ruta)

    # Dimensiones
    print("\n1. DIMENSIONES")
    print("Filas:", df.shape[0])
    print("Columnas:", df.shape[1])

    # Primeros registros
    print("\n2. PRIMEROS REGISTROS")
    print(df.head(3))

    # Información de columnas
    print("\n3. INFORMACIÓN")
    df.info()

    # Valores nulos
    print("\n4. VALORES NULOS")
    print(df.isnull().sum().sum())

    # Duplicados
    print("\n5. REGISTROS DUPLICADOS")
    print(df.duplicated().sum())

    # Distribución de etiquetas
    if "Label" in df.columns:
        print("\n6. DISTRIBUCIÓN DE ATAQUES")
        print(df["Label"].value_counts())

    del df

print("\nANÁLISIS FINALIZADO")
