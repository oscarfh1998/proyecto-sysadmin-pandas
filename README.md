# Análisis de tráfico de red CICIDS2017 — Trabajo de Pandas (ASIR)

Trabajo académico de **Arturo, Diego, Oscar y Álvaro** sobre el uso de **Python y Pandas** para la exploración, limpieza, transformación, análisis estadístico y visualización de flujos de red.

## Entregables principales

- **Informe Quarto / GitHub Pages:** https://oscarfh1998.github.io/proyecto-sysadmin-pandas/
- **Código fuente del informe:** [index.qmd](index.qmd)
- **Repositorio público:** https://github.com/oscarfh1998/proyecto-sysadmin-pandas

La [aplicación exploratoria adicional](https://sysadmin-analytics-cicids-oscar.hummingvale.chatgpt.site/) es complementaria y no sustituye al informe Quarto.

## Datos

Se ha utilizado una versión en **ocho archivos Parquet** del dataset [CICIDS2017 (Kaggle)](https://www.kaggle.com/datasets/dhoogla/cicids2017). Después de unir y procesar los archivos se obtuvieron **2.313.810 registros y 79 columnas**.

Los archivos de datos grandes no se suben al repositorio. Deben colocarse en `data/raw/`; el consolidado se guarda en `data/processed/cicids2017_completo.parquet`.

## Estructura y operaciones de Pandas

| Archivo | Función |
|---|---|
| `explorar.py` | Inspección de cada archivo de origen, previa a la unión |
| `unir_datasets.py` | Unión de Parquet con `pd.concat()` y preparación de datos |
| `analisis_exploratorio.py` | Dimensiones, tipos, `describe()`, `value_counts()` y protocolos |
| `calidad_datos.py` | Nulos, infinitos, duplicados y duraciones negativas |
| `analisis_estadistico.py` | `groupby()`, `agg()`, `pivot_table()`, `loc` e `iloc` |
| `graficos.py` | Dos visualizaciones estáticas y una interactiva con Plotly |
| `index.qmd` | **Informe completo:** código Pandas, resultados e interpretación SysAdmin |
| `_quarto.yml` | Configuración de Quarto; web generada en `docs/` |

## Reproducir el análisis localmente

Se necesita Python 3, Quarto y los ocho archivos Parquet descargados.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python unir_datasets.py
python analisis_exploratorio.py
python calidad_datos.py
python analisis_estadistico.py
python graficos.py
```

Para generar la web:

```bash
quarto render
```

El informe tiene `execute.eval: false` para permitir compilar **la documentación** en GitHub sin los grandes Parquet. Los resultados publicados corresponden a las ejecuciones documentadas del grupo. Para recalcular directamente los bloques de `index.qmd` en un equipo que sí tenga los datos, cambia `eval: false` a `eval: true`, verifica que las rutas y dependencias sean correctas y ejecuta `quarto render`.

GitHub Actions dispone de un flujo `.github/workflows/compilar-quarto.yml` para regenerar el contenido de `docs/` cuando se modifique la fuente del informe.

## Interpretación y límites

Este análisis es **descriptivo**, no un detector predictivo validado. En el informe se indica la diferencia entre tráfico benigno y malicioso, la detección de 88 duraciones negativas, la revisión de duplicados y las limitaciones para atribuir ataques o representar evolución temporal sin marcas de tiempo ni IP.

## Referencias

- [Dataset CICIDS2017 utilizado](https://www.kaggle.com/datasets/dhoogla/cicids2017)
- [Pandas](https://pandas.pydata.org/docs/)
- [Quarto](https://quarto.org/docs/)
