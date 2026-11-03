
import pandas as pd
import numpy as np

archivo = "data/processed/cicids2017_completo.parquet"
df = pd.read_parquet(archivo)

print("=" * 60)
print("COMPROBACIÓN DE CALIDAD DE LOS DATOS")
print("=" * 60)

# 1. Duraciones negativas
negativos = df[df["Flow Duration"] < 0]

print("\n1. DURACIONES NEGATIVAS")
print("Registros encontrados:", len(negativos))

if len(negativos) > 0:
    print("\nEtiquetas de esos registros:")
    print(negativos["Label"].value_counts())

    print("\nValores de duración:")
    print(negativos["Flow Duration"].value_counts().head(10))

# 2. Valores infinitos
numericas = df.select_dtypes(include="number")
infinitos = np.isinf(numericas).sum()

print("\n2. VALORES INFINITOS")
print("Total:", infinitos.sum())

# 3. Valores nulos
print("\n3. VALORES NULOS")
print("Total:", df.isnull().sum().sum())

# 4. Duplicados sin tener en cuenta el archivo de origen
duplicados = df.drop(columns=["Dataset_Source"]).duplicated().sum()

print("\n4. DUPLICADOS SIN DATASET_SOURCE")
print("Total:", duplicados)

# 5. Distribución de duración por tipo de tráfico
print("\n5. DURACIÓN POR TIPO DE TRÁFICO")
resumen = df.groupby("Label")["Flow Duration"].agg(
    ["count", "mean", "median", "min", "max"]
)

print(resumen.sort_values("median", ascending=False))

print("\nCOMPROBACIÓN FINALIZADA")
