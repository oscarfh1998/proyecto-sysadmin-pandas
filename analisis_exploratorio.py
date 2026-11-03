
import pandas as pd

# Cargar el dataset unificado
archivo = "data/processed/cicids2017_completo.parquet"
df = pd.read_parquet(archivo)

print("=" * 60)
print("ANÁLISIS EXPLORATORIO DEL DATASET CICIDS2017")
print("=" * 60)

# 1. Dimensiones
print("\n1. DIMENSIONES DEL DATASET")
print("Filas:", df.shape[0])
print("Columnas:", df.shape[1])

# 2. Tipos de datos
print("\n2. TIPOS DE DATOS")
print(df.dtypes.value_counts())
print("\nDetalle de columnas:")
print(df.dtypes)

# 3. Estadísticas descriptivas
print("\n3. ESTADÍSTICAS DESCRIPTIVAS")
print(df.describe().T)

# 4. Distribución de etiquetas
print("\n4. DISTRIBUCIÓN DE ATAQUES")
print(df["Label"].value_counts())

# 5. Distribución porcentual
print("\n5. PORCENTAJE POR TIPO DE TRÁFICO")
print((df["Label"].value_counts(normalize=True) * 100).round(2))

# 6. Protocolos
print("\n6. PROTOCOLOS")
print(df["Protocol"].value_counts())

# 7. Duración de los flujos
print("\n7. DURACIÓN DE LOS FLUJOS")
print(df["Flow Duration"].describe())

# 8. Tráfico por archivo de origen
print("\n8. REGISTROS POR ARCHIVO DE ORIGEN")
print(df["Dataset_Source"].value_counts())

print("\nANÁLISIS FINALIZADO")
