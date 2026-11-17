
# =====================================================================
# BLOQUE: 1. Abrir el dataset unido
# Función: cargar el Parquet final para analizar todos los archivos como una única tabla.
# Explicación: «Partimos del archivo que creamos al unir los datos y lo cargamos con Pandas».
# =====================================================================
import pandas as pd

# Cargar el dataset unificado
archivo = "data/processed/cicids2017_completo.parquet"
df = pd.read_parquet(archivo)

print("=" * 60)
print("ANÁLISIS EXPLORATORIO DEL DATASET CICIDS2017")
print("=" * 60)

# =====================================================================
# BLOQUE: 2. Dimensiones
# Función: averiguar cuántas filas y columnas contiene el conjunto consolidado.
# Explicación: «Con shape comprobamos el tamaño del conjunto: 2.313.810 registros y 79 columnas en nuestro informe».
# =====================================================================
# 1. Dimensiones
print("\n1. DIMENSIONES DEL DATASET")
print("Filas:", df.shape[0])
print("Columnas:", df.shape[1])

# =====================================================================
# BLOQUE: 3. Tipos de datos
# Función: identificar qué variables son números y cuáles son texto, y contar los tipos.
# Explicación oral: «Revisamos el tipo de cada columna para saber qué operaciones estadísticas podemos hacer».
# =====================================================================
# 2. Tipos de datos
print("\n2. TIPOS DE DATOS")
print(df.dtypes.value_counts())
print("\nDetalle de columnas:")
print(df.dtypes)

# =====================================================================
# BLOQUE: 4. Resumen estadístico general
# Función: calcular de golpe medias, desviaciones, mínimos, cuartiles, medianas y máximos de las columnas numéricas.
# Explicación: «describe nos da una primera visión estadística; la T coloca una variable por fila».
# =====================================================================
# 3. Estadísticas descriptivas
print("\n3. ESTADÍSTICAS DESCRIPTIVAS")
print(df.describe().T)

# =====================================================================
# BLOQUE: 5. Número y porcentaje de cada etiqueta
# Función: saber qué clases son más frecuentes y qué proporción representan sobre el total.
# Explicación: «Contamos las etiquetas de Label y después calculamos su porcentaje para identificar el desequilibrio». Ojo: aquí son porcentajes de cada etiqueta, no la agrupación total Benigno/Malicioso.
# =====================================================================
# 4. Distribución de etiquetas
print("\n4. DISTRIBUCIÓN DE ATAQUES")
print(df["Label"].value_counts())

# 5. Distribución porcentual
print("\n5. PORCENTAJE POR TIPO DE TRÁFICO")
print((df["Label"].value_counts(normalize=True) * 100).round(2))

# =====================================================================
# BLOQUE: 6. Protocolos y duración
# Función: contar los valores de Protocol y resumir cómo varía Flow Duration en el conjunto original.
# Explicación: «Comprobamos qué protocolos aparecen y cómo se distribuyen las duraciones». Importante: describe aquí incluye posibles duraciones negativas.
# =====================================================================
# 6. Protocolos
print("\n6. PROTOCOLOS")
print(df["Protocol"].value_counts())

# 7. Duración de los flujos
print("\n7. DURACIÓN DE LOS FLUJOS")
print(df["Flow Duration"].describe())

# =====================================================================
# BLOQUE: 7. Procedencia y fin del análisis
# Función: comprobar cuántos registros han llegado desde cada archivo original, gracias a Dataset_Source.
# Explicación: «Así conservamos la trazabilidad: sabemos de qué archivo viene cada flujo».
# =====================================================================
# 8. Tráfico por archivo de origen
print("\n8. REGISTROS POR ARCHIVO DE ORIGEN")
print(df["Dataset_Source"].value_counts())

print("\nANÁLISIS FINALIZADO")
