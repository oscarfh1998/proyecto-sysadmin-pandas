
import pandas as pd
# Utilizamos Pandas para analizar y comprobar la calidad de los datos.

import numpy as np
# Utilizamos NumPy para detectar valores infinitos.


# Indicamos la ubicación del dataset que hemos unificado anteriormente.
archivo = "data/processed/cicids2017_completo.parquet"


# Cargamos el dataset completo en un DataFrame.
df = pd.read_parquet(archivo)


print("=" * 60)
print("COMPROBACIÓN DE CALIDAD DE LOS DATOS")
print("=" * 60)


# Buscamos registros cuya duración de conexión sea negativa.
negativos = df[df["Flow Duration"] < 0]


print("\n1. DURACIONES NEGATIVAS")
print("Registros encontrados:", len(negativos))


# Si encontramos duraciones negativas, mostramos sus categorías.
if len(negativos) > 0:

    print("\nEtiquetas de esos registros:")
    print(negativos["Label"].value_counts())

    # Mostramos los diez valores de duración más frecuentes.
    print("\nValores de duración:")
    print(negativos["Flow Duration"].value_counts().head(10))


# Seleccionamos únicamente las columnas que contienen datos numéricos.
numericas = df.select_dtypes(include="number")


# Detectamos y contamos los valores infinitos de las columnas numéricas.
infinitos = np.isinf(numericas).sum()


print("\n2. VALORES INFINITOS")
print("Total:", infinitos.sum())


# Contamos todos los valores nulos que existen en el dataset.
print("\n3. VALORES NULOS")
print("Total:", df.isnull().sum().sum())


# Ignoramos la columna de procedencia para detectar registros repetidos
# aunque procedan de archivos originales diferentes.
duplicados = df.drop(columns=["Dataset_Source"]).duplicated().sum()


print("\n4. DUPLICADOS SIN DATASET_SOURCE")
print("Total:", duplicados)


# Agrupamos los registros según su tipo de tráfico y analizamos su duración.
print("\n5. DURACIÓN POR TIPO DE TRÁFICO")


# Calculamos el número de registros, la media, la mediana,
# la duración mínima y la duración máxima de cada categoría.
resumen = df.groupby("Label")["Flow Duration"].agg(
    ["count", "mean", "median", "min", "max"]
)


# Ordenamos los resultados de mayor a menor según la duración mediana.
print(resumen.sort_values("median", ascending=False))


print("\nCOMPROBACIÓN FINALIZADA")
