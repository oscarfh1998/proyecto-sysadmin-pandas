
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

print("=" * 60)
print("GENERACIÓN DE GRÁFICOS CICIDS2017")
print("=" * 60)

# Crear carpeta para guardar los gráficos
os.makedirs("images", exist_ok=True)

# Cargar el dataset
df = pd.read_parquet("data/processed/cicids2017_completo.parquet")

# Eliminar duraciones negativas para el análisis
df_duracion = df[df["Flow Duration"] >= 0].copy()

# Configuración visual
sns.set_theme(style="whitegrid")

# ============================================================
# GRÁFICO 1: DISTRIBUCIÓN DE ATAQUES
# ============================================================

print("\nGenerando gráfico 1...")

ataques = df["Label"].value_counts()
ataques = ataques.drop("Benign", errors="ignore")
ataques = ataques.sort_values(ascending=True)

plt.figure(figsize=(12, 7))

ataques.plot(
    kind="barh",
    color="steelblue"
)

plt.title("Distribución de los tipos de ataques", fontsize=16)
plt.xlabel("Número de registros")
plt.ylabel("Tipo de ataque")
plt.tight_layout()

plt.savefig(
    "images/01_distribucion_ataques.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# GRÁFICO 2: DURACIÓN DEL TRÁFICO POR CATEGORÍA
# ============================================================

print("Generando gráfico 2...")

# Seleccionar como máximo 1.000 registros por categoría.
# Se utiliza pd.concat para evitar problemas de compatibilidad
# con groupby.apply en versiones recientes de Pandas.

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

plt.figure(figsize=(14, 8))

sns.boxplot(
    data=muestra,
    x="Flow Duration",
    y="Label"
)

plt.xscale("symlog")
plt.title("Duración de los flujos de red por categoría", fontsize=16)
plt.xlabel("Duración del flujo (microsegundos)")
plt.ylabel("Tipo de tráfico")
plt.tight_layout()

plt.savefig(
    "images/02_duracion_trafico.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# GRÁFICO 3: VISUALIZACIÓN INTERACTIVA CON PLOTLY
# ============================================================

print("Generando gráfico 3...")

# Seleccionar como máximo 1.500 registros por categoría
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

fig = px.scatter(
    muestra_interactiva,
    x="Flow Duration",
    y="Total Fwd Packets",
    color="Label",
    hover_data=[
        "Total Backward Packets",
        "Protocol"
    ],
    title="Visualización interactiva del tráfico de red",
    labels={
        "Flow Duration": "Duración del flujo (microsegundos)",
        "Total Fwd Packets": "Paquetes enviados",
        "Label": "Tipo de tráfico"
    }
)

fig.update_xaxes(type="log")

fig.update_layout(
    width=1200,
    height=700,
    legend_title_text="Categoría de tráfico"
)

fig.write_html(
    "images/03_trafico_interactivo.html"
)

# ============================================================
# FINALIZACIÓN
# ============================================================

print("\n" + "=" * 60)
print("GRÁFICOS GENERADOS CORRECTAMENTE")
print("=" * 60)

print("\nArchivos creados:")
print("- images/01_distribucion_ataques.png")
print("- images/02_duracion_trafico.png")
print("- images/03_trafico_interactivo.html")
