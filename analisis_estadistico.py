
import pandas as pd

# Cargar el dataset unificado
df = pd.read_parquet(
    "data/processed/cicids2017_completo.parquet"
)

print("=" * 65)
print("ANÁLISIS ESTADÍSTICO CICIDS2017")
print("=" * 65)

# Excluir duraciones negativas solamente para los análisis de duración
df_duracion = df.loc[df["Flow Duration"] >= 0].copy()

# 1. GROUPBY: estadísticas por tipo de tráfico
print("\n1. DURACIÓN Y PAQUETES POR TIPO DE TRÁFICO")

resumen = df_duracion.groupby("Label").agg(
    Registros=("Label", "size"),
    Duracion_Media=("Flow Duration", "mean"),
    Duracion_Mediana=("Flow Duration", "median"),
    Paquetes_Enviados=("Total Fwd Packets", "mean"),
    Paquetes_Recibidos=("Total Backward Packets", "mean")
)

print(resumen.sort_values(
    "Duracion_Mediana", ascending=False
).round(2))

# 2. GROUPBY: comparar tráfico benigno y malicioso
print("\n2. COMPARACIÓN BENIGNO Y MALICIOSO")

df["Tipo_Trafico"] = df["Label"].apply(
    lambda etiqueta: "Benigno" if etiqueta == "Benign"
    else "Malicioso"
)

comparacion = df.groupby("Tipo_Trafico").agg(
    Registros=("Label", "size"),
    Media_Paquetes_Enviados=("Total Fwd Packets", "mean"),
    Media_Paquetes_Recibidos=("Total Backward Packets", "mean"),
    Duracion_Mediana=("Flow Duration", "median")
)

print(comparacion.round(2))

# 3. PIVOT_TABLE: paquetes enviados por ataque y protocolo
print("\n3. TABLA DINÁMICA: PAQUETES POR ATAQUE Y PROTOCOLO")

tabla = pd.pivot_table(
    df,
    values="Total Fwd Packets",
    index="Label",
    columns="Protocol",
    aggfunc="mean",
    fill_value=0
)

print(tabla.round(2))

# 4. LOC: filtrar ataques DoS y DDoS
print("\n4. FILTRO LOC: ATAQUES DoS Y DDoS")

ataques_dos = df.loc[
    df["Label"].str.contains("DoS|DDoS", case=False, na=False),
    ["Label", "Protocol", "Flow Duration", "Total Fwd Packets"]
]

print(ataques_dos.head(10))

# 5. ILOC: seleccionar las primeras cinco filas y columnas
print("\n5. SELECCIÓN ILOC")

print(df.iloc[:5, :5])

# 6. CONDICIONES AVANZADAS
print("\n6. FLUJOS DE LARGA DURACIÓN")

flujos_largos = df.loc[
    (df["Flow Duration"] > 60_000_000) &
    (df["Total Fwd Packets"] > 100),
    ["Label", "Flow Duration", "Total Fwd Packets"]
]

print("Flujos encontrados:", len(flujos_largos))
print(flujos_largos.head(10))

print("\nANÁLISIS ESTADÍSTICO FINALIZADO")
import pandas as pd

df = pd.read_parquet(
    "data/processed/cicids2017_completo.parquet"
)
