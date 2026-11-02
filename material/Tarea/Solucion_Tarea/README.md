# Tarea Finanzas I (ENFIN415) 2026 – Solución

Informe para entregar: **Informe_Tarea_ENFIN415.docx** (completar los nombres de los integrantes en la portada).
Versión extendida, solo como material de estudio: `resultados/Informe_extendido_referencia.docx`.

Todo el código está en **Python** (el enunciado permite cualquier lenguaje); no se usó R.

## Estructura

| Carpeta / archivo | Contenido |
|---|---|
| `codigo/config.py` | Parámetros: 50 acciones y su sector, ventana (30-jul-2021 a 31-jul-2026), series del H.15 |
| `codigo/01_descargar_datos.py` | Descarga precios (Yahoo Finance), S&P 500, Fed H.15 (Treasury constant maturities y fondos federales) e IPC/desempleo (BLS) |
| `codigo/utilidades.py` | Momentos anuales, frontera analítica (A, B, C, D), fronteras con restricciones (cvxpy), tangencia |
| `codigo/02_pregunta_1A.py` | P1A: estadísticas, frontera MV, frontera ingenua, límite 10%, sin venta corta, restricción sectorial |
| `codigo/03_pregunta_1B.py` | P1B: LMC y portafolio M, modelo índice y test de alfa, simulación bajo H0, prueba fuera de muestra, Sharpe/Treynor, asignación óptima |
| `codigo/04_pregunta_2.py` | P2: Nelson-Siegel y Svensson (óptimo global + verificación multi-inicio), RMSE, parámetros, episodios de inversión |
| `codigo/05_generar_informe.py` | Genera el informe para entregar (versión breve) a partir de los resultados |
| `codigo/06_informe_extendido.py` | Genera la versión extendida (robusteces y análisis adicionales) |
| `codigo/informe_utils.py` | Funciones comunes de los dos generadores de informe |
| `datos/` | Datos descargados (CSV) |
| `resultados/tablas/` | Tablas CSV y planillas `Resultados_Pregunta1A.xlsx`, `Resultados_Pregunta1B.xlsx`, `Resultados_Pregunta2.xlsx` |
| `resultados/figuras/` | Todos los gráficos (PNG) |

## Cómo reproducir

```bash
pip install -r requirements.txt
cd codigo
python 01_descargar_datos.py
python 02_pregunta_1A.py
python 03_pregunta_1B.py
python 04_pregunta_2.py
python 05_generar_informe.py
python 06_informe_extendido.py   # opcional
```

`01_descargar_datos.py` solo es necesario si se quieren volver a bajar los datos (ya están en `datos/`).
La pregunta 2 tarda ~2 minutos por la búsqueda del óptimo global y la verificación con cientos de puntos iniciales.
