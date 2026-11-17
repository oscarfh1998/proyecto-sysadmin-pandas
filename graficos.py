
# ============================================================
# IMPORTACIÓN DE LIBRERÍAS
# ============================================================

# Permite trabajar con carpetas y rutas del sistema operativo.
import os

# Permite cargar, filtrar y analizar conjuntos de datos.
import pandas as pd

# Permite crear gráficos estáticos y guardarlos como imágenes.
import matplotlib.pyplot as plt

# Librería para crear gráficos estadísticos de forma sencilla.
import seaborn as sns

# Permite generar gráficos interactivos en formato HTML.
import plotly.express as px


# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

# Mostramos un encabezado por pantalla.
# El símbolo "=" se repite 60 veces para separar visualmente.
print("=" * 60)
print("GENERACIÓN DE GRÁFICOS CICIDS2017")
print("=" * 60)

# Creamos una carpeta llamada "images" donde se guardarán
# todos los gráficos generados por el programa.
# exist_ok=True evita errores si la carpeta ya existe.
os.makedirs("images", exist_ok=True)

# Cargamos el dataset CICIDS2017 desde un archivo Parquet.
# Parquet es un formato eficiente para almacenar grandes
# cantidades de datos en columnas.
# El contenido se guarda en un DataFrame llamado df.
df = pd.read_parquet("data/processed/cicids2017_completo.parquet")

# Filtramos los registros cuya duración de flujo sea negativa.
# Solo conservamos los que tienen una duración mayor o igual a 0.
# .copy() crea una copia independiente de los datos filtrados.
df_duracion = df[df["Flow Duration"] >= 0].copy()

# Establecemos el estilo visual de los gráficos de Seaborn.
# "whitegrid" utiliza un fondo blanco con líneas de cuadrícula.
sns.set_theme(style="whitegrid")


# ============================================================
# GRÁFICO 1: DISTRIBUCIÓN DE ATAQUES
# ============================================================

# Informamos de que comienza la generación del primer gráfico.
print("\nGenerando gráfico 1...")

# Contamos cuántos registros existen de cada tipo de tráfico
# utilizando la columna "Label" del dataset.
# value_counts() devuelve la frecuencia de cada categoría.
ataques = df["Label"].value_counts()

# Eliminamos la categoría "Benign", ya que representa
# tráfico legítimo y queremos visualizar únicamente ataques.
# errors="ignore" evita errores si esa categoría no existe.
ataques = ataques.drop("Benign", errors="ignore")

# Ordenamos los ataques de menor a mayor número de registros.
# ascending=True indica que el orden es ascendente.
ataques = ataques.sort_values(ascending=True)

# Creamos una figura de 12 pulgadas de ancho y 7 de alto.
plt.figure(figsize=(12, 7))

# Generamos un gráfico de barras horizontales.
# kind="barh" indica barras horizontales.
# color="steelblue" establece el color azul de las barras.
ataques.plot(
    kind="barh",
    color="steelblue"
)

# Añadimos un título al gráfico con tamaño de letra 16.
plt.title("Distribución de los tipos de ataques", fontsize=16)

# Establecemos el nombre del eje horizontal.
plt.xlabel("Número de registros")

# Establecemos el nombre del eje vertical.
plt.ylabel("Tipo de ataque")

# Ajustamos automáticamente los márgenes del gráfico
# para evitar que los textos aparezcan cortados.
plt.tight_layout()

# Guardamos el gráfico como imagen PNG.
# dpi=300 establece una resolución de alta calidad.
# bbox_inches="tight" elimina espacios innecesarios.
plt.savefig(
    "images/01_distribucion_ataques.png",
    dpi=300,
    bbox_inches="tight"
)

# Cerramos la figura para liberar memoria.
# Es especialmente útil cuando generamos varios gráficos.
plt.close()


# ============================================================
# GRÁFICO 2: DURACIÓN DEL TRÁFICO POR CATEGORÍA
# ============================================================

# Informamos del inicio del segundo gráfico.
print("Generando gráfico 2...")

# Seleccionamos como máximo 1.000 registros por categoría.
# Esto reduce la cantidad de datos que debemos representar
# y mejora el rendimiento del programa.

# groupby("Label") agrupa los registros por tipo de tráfico.
# El bucle recorre cada grupo de forma independiente.
# grupo.sample() selecciona registros aleatorios.
# min(len(grupo), 1000) evita solicitar más registros
# de los que existen dentro de una categoría.
# random_state=42 permite obtener siempre la misma muestra.
# pd.concat() une todas las muestras en un único DataFrame.
# ignore_index=True crea un índice nuevo y consecutivo.

muestra = pd.concat(
    [
        grupo.sample(
            n=min(len(grupo), 1000),
            random_state=42
        )
        for _, grupo in df_duracion.groupby("Label")
    ],
    ignore_index=True
)

# Creamos una figura de 14 pulgadas de ancho y 8 de alto.
plt.figure(figsize=(14, 8))

# Generamos un diagrama de cajas (boxplot).
# Este gráfico permite analizar la distribución de la
# duración de los flujos de red para cada categoría.
# También permite identificar valores atípicos.
# El eje X representa la duración de los flujos.
# El eje Y representa los distintos tipos de tráfico.
sns.boxplot(
    data=muestra,
    x="Flow Duration",
    y="Label"
)

# Aplicamos una escala logarítmica simétrica al eje X.
# Permite visualizar datos con diferencias muy grandes
# de magnitud, incluyendo valores iguales a cero.
plt.xscale("symlog")

# Añadimos el título y los nombres de los ejes.
plt.title("Duración de los flujos de red por categoría", fontsize=16)
plt.xlabel("Duración del flujo (microsegundos)")
plt.ylabel("Tipo de tráfico")

# Ajustamos los márgenes automáticamente.
plt.tight_layout()

# Guardamos el segundo gráfico en formato PNG.
# Utilizamos una resolución de 300 DPI.
plt.savefig(
    "images/02_duracion_trafico.png",
    dpi=300,
    bbox_inches="tight"
)

# Cerramos la figura para liberar recursos.
plt.close()


# ============================================================
# GRÁFICO 3: VISUALIZACIÓN INTERACTIVA CON PLOTLY
# ============================================================

# Informamos del inicio del tercer gráfico.
print("Generando gráfico 3...")

# Creamos una nueva muestra con un máximo de 1.500
# registros por cada categoría de tráfico.
# En este caso utilizamos más registros porque Plotly
# permite explorar los datos de forma interactiva.

# Agrupamos por la columna "Label".
# Seleccionamos registros aleatorios de cada grupo.
# Unimos todos los grupos en un único DataFrame.
# random_state=42 garantiza que la selección sea reproducible.
muestra_interactiva = pd.concat(
    [
        grupo.sample(
            n=min(len(grupo), 1500),
            random_state=42
        )
        for _, grupo in df_duracion.groupby("Label")
    ],
    ignore_index=True
)

# Creamos un gráfico de dispersión interactivo.
# Cada punto representa un registro de tráfico de red.
fig = px.scatter(

    # Indicamos el DataFrame que contiene los datos.
    muestra_interactiva,

    # Eje horizontal: duración del flujo de red.
    x="Flow Duration",

    # Eje vertical: número de paquetes enviados
    # en dirección de origen a destino.
    y="Total Fwd Packets",

    # Asignamos un color diferente a cada tipo de tráfico.
    color="Label",

    # Indicamos qué información adicional aparecerá
    # cuando coloquemos el ratón encima de un punto.
    hover_data=[
        "Total Backward Packets",
        "Protocol"
    ],

    # Establecemos el título del gráfico interactivo.
    title="Visualización interactiva del tráfico de red",

    # Personalizamos los nombres que aparecen en los ejes
    # y en la leyenda del gráfico.
    labels={
        "Flow Duration": "Duración del flujo (microsegundos)",
        "Total Fwd Packets": "Paquetes enviados",
        "Label": "Tipo de tráfico"
    }
)

# Aplicamos una escala logarítmica al eje horizontal.
# Esta escala facilita comparar duraciones muy diferentes.
# Los valores iguales a cero no se representan en este eje.
fig.update_xaxes(type="log")

# Configuramos las dimensiones del gráfico interactivo.
# También cambiamos el título de la leyenda.
fig.update_layout(
    width=1200,
    height=700,
    legend_title_text="Categoría de tráfico"
)

# Guardamos el gráfico en un archivo HTML.
# Este archivo puede abrirse en cualquier navegador web.
# Permite hacer zoom, mover el gráfico y consultar
# información colocando el ratón sobre los puntos.
fig.write_html(
    "images/03_trafico_interactivo.html"
)


# ============================================================
# FINALIZACIÓN
# ============================================================

# Mostramos un mensaje indicando que ha terminado
# la generación de todos los gráficos.
print("\n" + "=" * 60)
print("GRÁFICOS GENERADOS CORRECTAMENTE")
print("=" * 60)

# Mostramos por pantalla las rutas de los archivos creados.
print("\nArchivos creados:")

# Primer gráfico: distribución de los tipos de ataques.
print("- images/01_distribucion_ataques.png")

# Segundo gráfico: duración de los flujos de red.
print("- images/02_duracion_trafico.png")

# Tercer gráfico: visualización interactiva del tráfico.
print("- images/03_trafico_interactivo.html")


