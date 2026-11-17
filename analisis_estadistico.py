# analisis_estadistico_comentado_por_bloques.py
# Guia de exposicion: cada bloque explica SU OBJETIVO, no cada instruccion.
# Las lineas de codigo originales se conservan; solo se añaden comentarios encima.

# =====================================================================
# BLOQUE: 1. Cargar los datos y preparar duraciones válidas
# Función: abrir el Parquet y crear un subconjunto sin duraciones negativas para el primer resumen.
# Explicación : «Separamos las duraciones válidas para comparar ataques sin que entren valores físicamente imposibles».
# =====================================================================
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

# =====================================================================
# BLOQUE: 2. Agrupar por ataque y calcular estadísticas
# Función: formar un grupo por cada Label y comparar recuentos, duración media y mediana, y paquetes medios.
# Explicación : «Con groupby y agg resumimos millones de filas en una tabla comparable por tipo de tráfico».
# =====================================================================
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

# =====================================================================
# BLOQUE: 3. Comparación general Benigno / Malicioso
# Función: reducir las distintas etiquetas a dos grupos y comparar sus recuentos y métricas.
# Explicación : «Con apply creamos la categoría general y repetimos las estadísticas para comparar ambos grupos». AVISO: este bloque usa df, no df_duracion; por tanto no excluye aquí las 88 duraciones negativas.
# =====================================================================
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

# =====================================================================
# BLOQUE: 4. Tabla dinámica: ataque frente a protocolo
# Función: cruzar Label con Protocol y mostrar la media de paquetes enviados en cada combinación.
# Explicación : «pivot_table nos deja comparar el comportamiento de cada ataque según el protocolo». Ojo: fill_value=0 muestra cero incluso en combinaciones que no tenían datos.
# =====================================================================
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

# =====================================================================
# BLOQUE: 5. Seleccionar ataques DoS y DDoS
# Función: buscar etiquetas con esos nombres y quedarse solo con cuatro columnas relevantes.
# Explicación : «Con loc aplicamos un filtro y centramos el análisis en ataques de denegación de servicio».
# =====================================================================
# 4. LOC: filtrar ataques DoS y DDoS
print("\n4. FILTRO LOC: ATAQUES DoS Y DDoS")

ataques_dos = df.loc[
    df["Label"].str.contains("DoS|DDoS", case=False, na=False),
    ["Label", "Protocol", "Flow Duration", "Total Fwd Packets"]
]

print(ataques_dos.head(10))

# =====================================================================
# BLOQUE: 6. Selección por posición: iloc
# Función: mostrar una pequeña muestra de cinco filas y cinco columnas por posición.
# Explicación: «iloc nos sirve para inspeccionar una parte concreta de la tabla, sin usar nombres de columna».
# =====================================================================
# 5. ILOC: seleccionar las primeras cinco filas y columnas
print("\n5. SELECCIÓN ILOC")

print(df.iloc[:5, :5])

# =====================================================================
# BLOQUE: 7. Búsqueda de flujos largos
# Función: localizar flujos de más de 60 segundos Y más de 100 paquetes enviados.
# Explicación : «Usamos dos condiciones al mismo tiempo para aislar conexiones interesantes». Superar ese umbral no significa automáticamente que sea un ataque.
# =====================================================================
# 6. CONDICIONES AVANZADAS
print("\n6. FLUJOS DE LARGA DURACIÓN")

flujos_largos = df.loc[
    (df["Flow Duration"] > 60_000_000) &
    (df["Total Fwd Packets"] > 100),
    ["Label", "Flow Duration", "Total Fwd Packets"]
]

print("Flujos encontrados:", len(flujos_largos))
print(flujos_largos.head(10))

# =====================================================================
# BLOQUE: 8. Final y lectura duplicada del archivo
# Función: mostrar el aviso de cierre. Al final del .py original se vuelve a importar Pandas y leer el mismo Parquet.
# Explicación: «Estas dos últimas instrucciones están repetidas y podrían eliminarse para evitar trabajo innecesario». Las conservamos aquí para reflejar literalmente el código que me pasaste.
# =====================================================================
print("\nANÁLISIS ESTADÍSTICO FINALIZADO")
import pandas as pd

df = pd.read_parquet(
    "data/processed/cicids2017_completo.parquet"
)
