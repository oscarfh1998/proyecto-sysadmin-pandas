
import pandas as pd
# Utilizamos Pandas para leer, manipular y unir los conjuntos de datos.

import os
# Nos permite gestionar las carpetas y las rutas de los archivos.

import glob
# Nos permite localizar archivos mediante patrones de búsqueda.

import numpy as np
# Utilizamos NumPy para trabajar con valores numéricos especiales.


# Definimos las carpetas de origen y destino de los datos.
carpeta = "data/raw"
destino = "data/processed"


# Creamos la carpeta de destino si todavía no existe.
os.makedirs(destino, exist_ok=True)


# Localizamos todos los archivos Parquet de la carpeta original.
archivos = glob.glob(os.path.join(carpeta, "*.parquet"))


# Creamos una lista donde almacenaremos los diferentes DataFrames.
datasets = []


print("=" * 60)
print("UNIFICACIÓN DEL DATASET CICIDS2017")
print("=" * 60)


# Leemos todos los archivos originales uno por uno.
for archivo in sorted(archivos):

    # Obtenemos el nombre del archivo sin incluir su ruta.
    nombre = os.path.basename(archivo)

    print(f"\nCargando: {nombre}")

    # Cargamos el archivo Parquet en un DataFrame.
    df = pd.read_parquet(archivo)


    # Añadimos una columna para identificar el archivo de procedencia.
    df["Dataset_Source"] = nombre


    # Guardamos cada DataFrame en la lista para unirlos posteriormente.
    datasets.append(df)

    print("Registros:", len(df))


# Unimos todos los DataFrames en una única tabla.
print("\nUniendo los datasets...")

df_completo = pd.concat(datasets, ignore_index=True)


# Eliminamos los espacios innecesarios de los nombres de las columnas.
df_completo.columns = df_completo.columns.str.strip()


# Sustituimos los valores infinitos por valores nulos.
df_completo.replace([np.inf, -np.inf], np.nan, inplace=True)


# Comprobamos cuántos registros duplicados existen.
duplicados = df_completo.duplicated().sum()

print("\nDuplicados encontrados:", duplicados)


# Eliminamos los registros que están completamente duplicados.
df_completo.drop_duplicates(inplace=True)


# Mostramos un resumen del dataset después de la unificación.
print("\n" + "=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print("Total de registros:", len(df_completo))
print("Total de columnas:", len(df_completo.columns))


# Mostramos la cantidad de registros de cada tipo de tráfico.
print("\nDistribución de etiquetas:")
print(df_completo["Label"].value_counts())


# Comprobamos cuántos valores nulos quedan después del procesamiento.
print("\nValores nulos por columna:")
print(df_completo.isnull().sum().sum())


# Definimos la ruta donde guardaremos el dataset unificado.
ruta_salida = os.path.join(destino, "cicids2017_completo.parquet")


# Guardamos el resultado en formato Parquet sin añadir el índice.
df_completo.to_parquet(ruta_salida, index=False)


print("\nDataset guardado en:", ruta_salida)
print("UNIFICACIÓN FINALIZADA")
