
import pandas as pd
# Utilizamos Pandas para trabajar con los datos en forma de tablas.

import os
# Utilizamos OS para acceder a las carpetas y archivos del sistema.


# Carpeta donde se encuentran los datasets originales.
carpeta = "data/raw"


# Buscamos todos los archivos que tengan formato Parquet.
archivos = [
    f for f in os.listdir(carpeta)
    if f.endswith(".parquet")
]


print("=" * 60)
print("ANÁLISIS INICIAL DEL DATASET CICIDS2017")
print("=" * 60)


for archivo in sorted(archivos):
    # Recorremos todos los archivos encontrados para analizarlos individualmente.

    ruta = os.path.join(carpeta, archivo)

    print("\n" + "=" * 60)
    print("ARCHIVO:", archivo)
    print("=" * 60)


    # Cargamos el archivo Parquet en un DataFrame de Pandas.
    df = pd.read_parquet(ruta)


    # Consultamos el número de filas y columnas del dataset.
    print("\n1. DIMENSIONES")
    print("Filas:", df.shape[0])
    print("Columnas:", df.shape[1])


    # Mostramos los tres primeros registros para conocer su contenido.
    print("\n2. PRIMEROS REGISTROS")
    print(df.head(3))


    # Consultamos los nombres, tipos de datos y valores disponibles de las columnas.
    print("\n3. INFORMACIÓN")
    df.info()


    # Contamos los valores nulos que existen en el dataset.
    print("\n4. VALORES NULOS")
    print(df.isnull().sum().sum())


    # Comprobamos cuántas filas están duplicadas.
    print("\n5. REGISTROS DUPLICADOS")
    print(df.duplicated().sum())


    # Comprobamos si existe la columna Label antes de analizarla.
    if "Label" in df.columns:

        print("\n6. DISTRIBUCIÓN DE ATAQUES")

        # Contamos los registros de cada categoría de tráfico de red.
        print(df["Label"].value_counts())


    # Liberamos el DataFrame antes de analizar el siguiente archivo.
    del df


print("\nANÁLISIS FINALIZADO")
