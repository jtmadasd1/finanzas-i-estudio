# Finanzas I (ENFIN415) · Material de estudio

Material para el **Control 2** y el **control de la tarea** (lunes 2 de noviembre de 2026, 18:30).

> **VaR no entra en el Control 2** (lo dijo el profesor). Las partes de VaR que siguen en las guías están marcadas.

## Qué hay aquí

| Carpeta | Contenido | Para qué |
| --- | --- | --- |
| [`estudio/`](estudio) | Guías en Markdown | Leer en el celular |
| [`texto/`](texto) | Texto extraído de todos los PDF del curso | Para que un chat de Claude pueda leer el material |
| [`material/`](material) | La carpeta del curso tal cual (PDF, ayudantías, pruebas, tarea) | Respaldo y originales |

### Leer en este orden

1. [`estudio/00_clases_desde_cero.md`](estudio/00_clases_desde_cero.md): las clases desde cero, con ejemplos y ejercicios (respuestas escondidas).
2. [`estudio/01_Control2_guia.md`](estudio/01_Control2_guia.md): la guía del Control 2 con recetas, trampas típicas, 32 comentes con respuesta y el banco de ejercicios.
3. [`estudio/02_Control_tarea_guia.md`](estudio/02_Control_tarea_guia.md): la guía del control de la tarea con cifras clave, preguntas probables, ejercicios y comentes.

### Fuentes de teoría en `texto/`

- `texto/Sesiones (material del curso)/Sesion_II_ENFIN415.txt`: láminas de derivados (Control 2). Las de VaR, al final, no entran.
- `texto/Sesiones (material del curso)/Sesion 1.txt`: láminas de portafolios, CAPM y tasas (tarea).
- `texto/Formulas_FinanzasI_FinanzasII.txt` y `texto/Formulario_FinanzasI_Solemne.txt`: formularios.
- `texto/Apunte_Finanzas_I.txt` y `texto/Repositorio_Finanzas_I.txt`: apunte y repositorio de preguntas.
- `texto/Ayudantias/`: enunciados y pautas (A8, A9 y A10 son las del Control 2).

## Prompt para estudiar solo teoría en otro chat

Conecta este repositorio al chat (en claude.ai: botón **+** → **GitHub** → este repo). Selecciona `estudio/` y, si cabe, los archivos de teoría de `texto/` listados arriba. Después pega esto:

```text
Actúa como mi tutor de Finanzas I (ENFIN415, U. de Chile). Hoy lunes a las 18:30 tengo el Control 2 y el control de la tarea. Voy en el transporte público, leyendo en el celular, así que quiero SOLO TEORÍA: conceptos, intuición y fórmulas, sin ejercicios largos de calculadora.

Usa como fuente los archivos del repositorio conectado: estudio/00_clases_desde_cero.md (lo que ya vi), estudio/01_Control2_guia.md, estudio/02_Control_tarea_guia.md y las láminas en texto/ (Sesion_II para derivados; Sesion 1 para la tarea). El profesor dijo que VaR NO entra en el Control 2: no me lo expliques y salta los comentes de VaR. Cita el archivo o lámina cuando expliques algo. Si algo no está en el material, avísame.

Cómo explicarme:
1. Desde cero, un concepto por mensaje, en mensajes cortos que se lean en una pantalla de celular (máximo unas 15 líneas).
2. Para cada concepto: qué es, por qué funciona (la intuición), la fórmula con cada símbolo explicado y la trampa típica del control.
3. Al final de cada mensaje, una pregunta conceptual corta (verdadero/falso o "¿por qué…?") que pueda responder en una línea. Espera mi respuesta antes de seguir; si me equivoco, explícame el error.
4. Cada 3 conceptos, un comente del banco de estudio/01_Control2_guia.md sobre lo que acabamos de ver.

Orden: ya vi forwards y futuros (bloque ① en 00_clases_desde_cero.md). Sigue con:
② Opciones: qué son, call/put, largo/corto, pagos, americanas vs europeas, estrategias (spreads, straddle, strangle, cobertura), cotas y paridad put-call.
③ Árbol binomial: probabilidad neutral al riesgo, valoración hacia atrás, ejercicio anticipado.
④ Black-Scholes: qué supone, qué significan N(d1) y N(d2), cómo entran los dividendos, sensibilidades.
⑤ Teoría de la tarea: frontera media-varianza, GMV, cartera tangente y LMC, alfa de Jensen y su test t, Sharpe vs Treynor, asignación óptima, Nelson-Siegel/Svensson y curva invertida.

Parte con ②.
```

> Las cifras de la tarea son las de nuestro grupo.
