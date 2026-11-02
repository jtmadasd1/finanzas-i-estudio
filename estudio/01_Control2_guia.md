# Guía Finanzas I: Control 2 y control de la tarea

Finanzas I (ENFIN415), Prof. Alejandro Bernales · Control 2: lunes 2 de noviembre de 2026, 18:30, sala P-307 (adecuaciones: sala 1002 de la Torre), + 5 minutos para subir a Canvas [aviso del profesor]

*Versión del 01-11-2026. Todo sale del material del curso en Canvas; cada afirmación lleva entre corchetes el archivo del que sale.*

**Cómo está organizada:**

- **Parte 1 · Control 2 (secciones 1 a 10):** derivados (forwards y futuros, opciones, estrategias, cotas y paridad, árboles binomiales, Black-Scholes) y VaR. Qué entra, qué preguntaron antes, recetas paso a paso, trampas, 32 comentes con respuesta, 35 ejercicios con pauta y un plan de estudio.
- **Parte 2 · Control de la tarea (secciones 11 a 17):** las preguntas más probables sobre la tarea (frontera media-varianza, portafolio de tangencia y alfa de Jensen, Nelson-Siegel y curva de tasas) con sus respuestas, 8 ejercicios numéricos y 10 comentes.
- **Para el día del control:** calculadora (el celular está prohibido) y practicar e^x, ln y raíz en ella [Programa].

**Abreviaturas:** [Sesión II L n] = Sesiones (material del curso)/Sesion\_II\_ENFIN415.pdf, lámina n; [A8], [A9] y [A10] = Ayudantías 8, 9 y 10 (enunciado y pauta); [C2 2024] y [C2 2025] = Pauta Control 2 de esos años; [Ex 2020] … [Ex 2025] = pautas de exámenes; [Repo] = Repositorio\_Finanzas\_I.pdf (material de otoño 2026), con [Ay8 Oto26], [Ay9 Oto26], [Ay10 Oto26], [C3 Oto26] = Control 3 y [Ex Oto26] = Examen; [Fórmulas] = Formulas\_FinanzasI\_FinanzasII.pdf; [Programa] = Programa/ENFIN415\_2026.pdf; c = comente, Mat = matemático.

# Parte 1 · Control 2

> **Actualización (lunes 2): el profesor dijo que VaR NO entra en el Control 2.** Salta la sección 4.6, las trampas 14 a 16, los comentes 6.4, los ejercicios 34 y 35 y el bloque de VaR del plan.

## 1. Resumen

- **Qué entra:** lo de las ayudantías 8, 9 y 10 y la segunda parte de la Sesión II: forwards y futuros, opciones (pagos, estrategias, cotas y paridad put-call), árboles binomiales, Black-Scholes con dividendos y VaR (paramétrico, de portafolio y backtesting). Son las unidades 4 y 5 del [Programa]. Es una estimación mía: el aviso no dice la materia.
- **Cuándo y cuánto vale:** lunes 2 de noviembre, 18:30, P-307 (adecuaciones: 1002 Torre), con 5 minutos extra para subirlo a Canvas. Los controles valen 20% de la nota final en conjunto; el programa no dice cuántos son ni cuánto pesa cada uno. Solo cuentan si el promedio entre Solemne y Examen es 3,95 o más [Programa].
- **Lo que preguntaron antes:** los Controles 2 de 2024 y 2025 fueron la misma pregunta: precio de una call europea con Black-Scholes, sin dividendos y luego con un dividendo de $20 en 5 meses [C2 2024], [C2 2025]. En otoño 2026 este tema cayó en el Control 3: un forward de divisas [C3 Oto26].
- **Tabla normal y calculadora:** la pauta dice que no hace falta interpolar; basta el valor más cercano de la tabla [C2 2024]. Lleva calculadora (celular prohibido) [Programa] y practica e^x, ln y raíz en ella.
- **Material de práctica disponible:** 32 comentes y 35 ejercicios de derivados y VaR entre clases, ayudantías, controles, exámenes y el Repositorio (secciones 6 y 7).

## 2. Mapa de archivos por tema

| **Tema** | **Teoría** | **Resueltos paso a paso** | **Para practicar** |
| --- | --- | --- | --- |
| Forwards y futuros | [Sesión II L 3–7]; [Fórmulas] pág. 2 (acción, divisas, dividendos, valor del contrato) | [A8] Mat I, II y III; [Ay8 Oto26] Mat 1 | [C3 Oto26] P1; [Ay9 Oto26] Mat 3; [Ay8 Oto26] Mat 2 y 3; [Ex Oto26] Ej 1 |
| Opciones: pagos y estrategias | [Sesión II L 8–19 y 31–45] | [A8] Mat IV y V; [A10] Mat IV (call cubierta) | [Ex 2024] P2; [Ex 2022] P3; [Ex 2023] P2; [Ex Oto26] Ej 3; [Ay10 Oto26] Mat 1–3 |
| Cotas, paridad y arbitraje | [Sesión II L 21–29]; [Fórmulas] pág. 3 (paridad con dividendos y casos) | [A9] Mat I c); [A10] Mat III 5) | [Ex 2025] P2; [Ex 2024] P4b; [Ex Oto26] Ej 2c |
| Árboles binomiales | [Sesión II L 47–58] | [A9] Mat I; [A10] Mat III (europea, americana y Δ) | [Ex 2025] P3; [Ex 2024] P3; [Ex 2021–2023] P3; [Ex Oto26] Ej 2a |
| Black-Scholes | [Sesión II L 60–65] | [A9] Mat II (con dividendo); [C2 2024] | [C2 2025]; [Ex 2020] P1; [Ex 2025] P4; [Ex 2024] P4a; [Ex Oto26] Ej 2b |
| VaR | [Sesión II L 67–85] (paramétrico L 76–77, GARCH L 78–80, simulación histórica L 81–82, Kupiec L 83–85) | [A10] Mat I y II | Comentes [A10] 1–4; [Ex 2024] 1b; [Ex 2025] 1b |

## 3. Qué preguntaron los controles pasados (solo derivados y VaR)

Método: calculé qué parte del puntaje de cada control corresponde a cada tema, contando solo derivados y VaR (la P2 de [C3 Oto26], de eficiencia, no se cuenta). El Control 2 de otoño 2026 fue de CAPM y APT porque ese semestre tuvo otro calendario [Repo]. Es una estimación mía.

| **Control** | **Preguntas de derivados y VaR** | **Black-Scholes** | **Otros derivados** | **VaR** |
| --- | --- | --- | --- | --- |
| Control 2 2024 | a) Call europea Soquimik (S0 = 182, K = 180, r = 6%, σ = 50%, 6 meses); b) la misma con dividendo de $20 en 5 meses | 100% | 0% | 0% |
| Control 2 2025 | Idéntico al de 2024 (mismo enunciado y mismos datos) | 100% | 0% | 0% |
| Control 3 Otoño 2026 | P1 (30 pts): forward de divisas para un importador: precio, valor a los 6 meses y arbitraje a los 7 | 0% | 100% | 0% |

Además, hay derivados en todos los exámenes pasados: [Ex 2020] P1 (put Soquimik con Black-Scholes), [Ex 2021–2023] P3 (árbol), [Ex 2022] P3 y [Ex 2023] P2 (estrategias), [Ex 2024] P1–P4, [Ex 2025] P1–P4 y [Ex Oto26] Ej 1–3. Sirven como práctica extra. Lo más probable es otro Black-Scholes, pero este semestre las ayudantías 9 y 10 trabajaron árboles, paridad y VaR, así que prepara también esos temas.

## 4. Tipos de pregunta

### 4.1 Black-Scholes (call o put, con o sin dividendo)

(1) T en años (6 meses = 0,5; 7 meses = 7/12) y r continua. (2) Si hay dividendos antes del vencimiento: S\* = S0 − Σ D·e^(−r·tD), con tD = fecha de cada dividendo [Sesión II L 65]. (3) d1 = [ln(S/K) + (r + σ²/2)·T] / (σ√T) y d2 = d1 − σ√T. (4) Redondea d1 y d2 a 2 decimales y busca N(·) en la tabla; N(−x) = 1 − N(x). (5) c = S·N(d1) − K·e^(−rT)·N(d2) y p = K·e^(−rT)·N(−d2) − S·N(−d1), o la put por paridad. (6) Interpreta: el dividendo baja la call (de $7,40 a $6,23 en [A9] Mat II) y sube la put.

### 4.2 Árbol binomial (europea o americana)

(1) Δt = T / n° de pasos; u = e^(σ√Δt) y d = 1/u, salvo que te den u y d (+25%/−20% en [Ex 2024] P3, ±30% en [Ex 2025] P3). (2) p = (e^(rΔt) − d) / (u − d): probabilidad neutral al riesgo, no la real. (3) Árbol de precios y pagos al vencimiento. (4) Hacia atrás: f = e^(−rΔt)·[p·fu + (1 − p)·fd]. (5) Americana: en cada nodo intermedio, máx(continuar, ejercer ahora), y di en qué nodo conviene ejercer [A10] Mat III 3). (6) Δ = (fu − fd) / (Su − Sd) [A10] Mat III 6). Atajo para una europea de 2 pasos: f0 = e^(−rT)·[p²·fuu + 2p(1 − p)·fud + (1 − p)²·fdd].

### 4.3 Cotas, paridad put-call y arbitraje

(1) Calcula los dos lados: c + K·e^(−rT) y p + S0 (con dividendos, c + K·e^(−rT) + D = p + S0, con D = VP de los dividendos) [Fórmulas]. (2) Vende el lado caro y compra el barato; pide prestado o invierte a r para que el flujo en t = 0 sea cero. (3) Tabla de flujos con columnas t = 0, ST &lt; K y ST ≥ K: la ganancia debe salir igual en ambos casos [A9] Mat I c), [A10] Mat III 5). (4) Call cara: vender call, comprar put, comprar acción, pedir prestado. Put cara: vender put, vender corto la acción, comprar call, invertir [Ex 2025] P2. Cotas: máx(S0 − K·e^(−rT), 0) ≤ c ≤ S0 y máx(K·e^(−rT) − S0, 0) ≤ p ≤ K·e^(−rT) [Sesión II L 25–27].

### 4.4 Forwards y futuros

(1) Sin ingresos: F0 = S0·e^(rT); con dividendos: F0 = (S0 − I)·e^(rT), con I = VP de los dividendos [A8] Mat II. (2) El contrato vale cero al inicio; en t, para el largo: f = (Ft − F0)·e^(−r(T − t)) [Sesión II L 4], [Fórmulas]. (3) Divisas: F = S·e^((r − r\*)·T), o con tasas simples F = S·(1 + rCLP·t) / (1 + rUSD·t) si el enunciado lo dice [C3 Oto26]. (4) Futuros: ajuste diario (mark-to-market); cambio en la cuenta = n° de unidades × ΔF [A8] Mat III. (5) Arbitraje: si el forward de mercado está sobre el teórico, pedir prestado, comprar el activo y vender el forward; si está bajo, lo contrario [Ex Oto26] Ej 1c.

### 4.5 Estrategias con opciones

Tabla por tramos de ST (un corte en cada K), suma de pagos menos el costo neto, y gráfico. Identifica el costo neto, la pérdida y la ganancia máximas y los puntos de equilibrio. Han salido: bull spread [A8] Mat V, strangle [A8] Mat IV, straddle (volatilidad alta) [Sesión II L 41], butterfly [Ex Oto26] Ej 3, call cubierta [A10] Mat IV y collar [Ex 2022] P3. Si hablan de contratos, cada uno es por 100 acciones [Sesión II L 14].

### 4.6 VaR (no entra en el Control 2)

(1) Lleva la volatilidad al horizonte: σ·√(días/250), o la base que diga el enunciado [A10]. (2) VaR = P0·α·σ·√t, con α95% = 1,645 y α99% = 2,33; con media: VaR = P0·(α·σ·√t − μ·t). (3) Dos activos: σp² = wA²σA² + wB²σB² + 2·wA·wB·ρ·σA·σB; beneficio de diversificación = VaRA + VaRB − VaRp, que es cero solo con ρ = 1 [A10] Mat II. (4) Backtesting: excepciones esperadas = T·(1 − c); muchas más significa que el modelo subestima el riesgo y muy pocas, que lo sobrestima [A10] Mat I 4). (5) La lámina usa VaR = (e^((u − σ²/2) + σψ) − 1)·M con ψ = −1,64 o −2,33, y da un número negativo (la pérdida) [Sesión II L 76].

### 4.7 Comentes

En los exámenes son de 20 puntos cada uno: di si es verdadero, falso o incierto y justifica con el concepto y, si puedes, con una fórmula o un número [Ex 2024] P1, [Ex 2025] P1. Muchos son falsos por una sola palabra ("siempre", "estrictamente", "ambas"): búscala.

### 4.8 Ejercicios reciclados

- [C2 2024] = [C2 2025] (mismo enunciado y datos); [Ex 2020] P1 usa la misma Soquimik con una put.
- [Ex 2021] = [Ex 2022] = [Ex 2023] P3: el mismo derivado con pago [máx(30 − ST, 0)]².
- [A8] c1 = [Ex 2025] 1a (bull spread y volatilidad); [A9] c2 = [Ex 2024] 1a; [A9] c3 = [Ex 2024] 1c.
- [Ex 2024] 1b = [Ay9 Oto26] comente A (VaR que nunca se excede).
- [A9] Mat II y [Ex Oto26] Ej 2 usan S0 = 60 y K = 58; [A10] Mat III y [Ex Oto26] Ej 2a tienen los mismos u, d y p (σ = 30%, r = 6%, Δt = 0,25).
- [C3 Oto26] P1 y [Ay9 Oto26] Mat 3: misma estructura (forward de divisas, valor a los 6 meses, arbitraje a los 7).

## 5. Trampas típicas

1. **T en años y tasa continua:** 9 meses = 0,75; 7 meses = 0,5833. Usa e^(rT) salvo que digan tasa simple o compuesta [Sesión II L 6], [C3 Oto26]. [A8] Mat I usa (1 + r)^T y da 41,20; con continua, 41,22.
2. **Dividendo:** se descuenta desde su fecha (5 meses: e^(−0,06·5/12)), no desde T, y solo cuentan los que caen antes del vencimiento [C2 2024], [Sesión II L 65]. K·e^(−rT) no cambia [A9] Mat II c).
3. **Tabla normal:** redondea d a 2 decimales y usa el valor más cercano, sin interpolar [C2 2024]. Por eso la pauta da c = 28,85 y con tabla puede darte 28,60: las dos sirven (sección 8).
4. **d negativo:** N(−x) = 1 − N(x). Pasa en la parte con dividendo, donde d1 y d2 quedan negativos [C2 2024] b).
5. **Paridad solo para europeas:** con la put americana ($4,12) la call daría $3,36, que está mal [A10] Mat III 4). Para americanas solo hay cotas: S0 − K &lt; C − P &lt; S0 − K·e^(−rT) [A10] c6.
6. **Sensibilidades:** σ sube la call y la put; r sube la call y baja la put; los dividendos bajan la call y suben la put; T sube ambas [A10] c5 (tabla).
7. **Americanas:** sin dividendos, la call americana vale lo mismo que la europea; la put americana puede valer más [A10] c6, [A8] c3.
8. **Árbol:** p es neutral al riesgo (la probabilidad real no se usa) y se descuenta por paso, e^(−rΔt) [A9] c1.
9. **Ejercicio anticipado:** compara en cada nodo; en [A10] Mat III conviene ejercer en el nodo bajo (7,57 &gt; 6,95).
10. **Arbitraje:** la ganancia tiene que salir igual para ST &lt; K y ST ≥ K; si no, la tabla está mal [A9] Mat I c).
11. **Contratos:** 1 contrato = 100 acciones; multiplica primas y pagos por 100 [Sesión II L 14], [Ex 2022] P3.
12. **Forward:** el precio F0 no es el valor del contrato, que parte en cero [Sesión II L 4], [A8] c4.
13. **Cobertura:** un exportador que recibirá dólares toma posición corta (vende futuros o forwards de dólar) [Ay8 Oto26] comente B.
14. **VaR y horizonte:** escala con √t, no con t: el VaR a 10 días es √10 ≈ 3,16 veces el diario [A10] c1. Usa 250 días hábiles si el enunciado lo dice; el resumen del [Repo] usa 365.
15. **VaR con media:** se resta μ·t; a 1 día casi no cambia (14,74 → 14,54) [A10] Mat I 3).
16. **Signo del VaR:** con la fórmula de la lámina (ψ negativo) sale negativo; con la de la ayudantía, positivo. Ambos son una pérdida [Sesión II L 74–76], [A10].
17. **Backtesting:** cero excepciones no es buen modelo: está sobrestimando el riesgo [Ex 2024] 1b. Kupiec rechaza si K &gt; 3,84 [Sesión II L 85].
18. **Simulación histórica:** da el mismo peso a datos antiguos y nuevos; el que pondera más lo reciente es GARCH [Sesión II L 80–82], [Ex 2025] 1b.
19. **Márgenes:** los deposita quien vende (escribe) la opción, no quien la compra [Sesión II L 18–19], [Ex 2025] 1c.

## 6. Banco de comentes con respuesta (32)

Son todos los comentes de derivados y VaR de las ayudantías, controles, exámenes y el Repositorio. Tapa la respuesta (en azul) y contesta primero como en la prueba: verdadero, falso o incierto, con una justificación corta. Las respuestas siguen la pauta indicada; las dos que no traen pauta están marcadas.

### 6.1 Forwards y futuros (7)

1. En un contrato forward justo, el valor inicial del contrato para ambas partes es distinto de cero. [A8 c4]

<details><summary>Ver respuesta</summary>

**Falso.** F0 se fija justamente para que el contrato valga cero para ambas partes al inicio: nadie paga nada al firmarlo. Después su valor cambia; para el largo, f = (Ft − F0)·e^(−r(T − t)) [A8 c4].

</details>

2. Los futuros y los forwards son equivalentes en todo sentido, ya que ambos fijan precios futuros y eliminan el riesgo de contraparte. [A8 c5]

<details><summary>Ver respuesta</summary>

**Falso.** Ambos fijan un precio futuro, pero solo los futuros mitigan el riesgo de contraparte: se transan en bolsa, con cámara de compensación, márgenes y ajuste diario (mark-to-market). El forward es OTC, a la medida y se liquida al vencimiento, así que queda expuesto al incumplimiento de la contraparte [A8 c5].

</details>

3. Explique en qué consiste el marking-to-market (liquidación diaria) de los futuros y cómo los diferencia de un forward en términos de riesgo de contraparte. [Ay8 Oto26 cA]

<details><summary>Ver respuesta</summary>

**Respuesta.** Cada día la ganancia o pérdida por el cambio del precio futuro se abona o carga en la cuenta de margen; si el saldo cae bajo el margen de mantención, hay llamada de margen y se repone hasta el margen inicial. Así las pérdidas se pagan día a día y la exposición a la contraparte es de un día como máximo. En el forward todo se paga al vencimiento y el riesgo de crédito se acumula [A8] Mat III.

</details>

4. Dado que un exportador chileno recibirá flujos en dólares en el futuro, para mitigar el riesgo de tipo de cambio le convendría tomar una posición larga en futuros sobre el dólar (USD/CLP). [Ay8 Oto26 cB]

<details><summary>Ver respuesta</summary>

**Falso.** El exportador ya está largo en dólares: pierde si el dólar cae (si el peso se aprecia). Se cubre con una posición corta, vendiendo futuros (o forwards) de dólar, y así fija hoy el tipo de cambio al que venderá sus dólares [Repo].

</details>

5. Liquidar (o cerrar) una posición larga de un contrato de forwards de dólares es más fácil que si fuera en el mercado de futuros. [Ay9 Oto26 cB]

<details><summary>Ver respuesta</summary>

**Falso.** Es al revés. El futuro se cierra en el acto tomando la posición contraria en bolsa (neteo), porque es estandarizado y líquido. El forward es bilateral: hay que negociar con la contraparte original, que puede cobrar por salir, o pactar un forward opuesto con otra y quedar con el riesgo de crédito de ambas [Repo].

</details>

6. Un tesorero observa que el dólar forward a 12 meses cotiza por sobre el spot actual y concluye que el mercado anticipa una depreciación del peso. [Ex Oto26 c4]

<details><summary>Ver respuesta</summary>

**Falso.** Por la paridad cubierta de tasas, F = S·(1 + rCLP) / (1 + rUSD): un forward sobre el spot solo refleja que la tasa en pesos es mayor que la tasa en dólares. Es una condición de no arbitraje, no una predicción del tipo de cambio [Repo].

</details>

7. Una AFP cubre su exposición al cobre y el área de riesgo recomienda futuros en la LME en vez de forwards OTC, argumentando que tienen mayor liquidez, pero también mayor riesgo de contraparte que los forwards. [Ex Oto26 c6]

<details><summary>Ver respuesta</summary>

**Falso (la segunda parte).** Los futuros sí son más líquidos, pero tienen menos riesgo de contraparte, no más: la cámara de compensación, los márgenes y el ajuste diario lo mitigan. Su costo es la estandarización: montos, fechas y calidad pueden no calzar con la exposición (riesgo de base). [Sin pauta: respuesta propia.]

</details>

### 6.2 Opciones, estrategias y paridad (14)

1. Cuando se espera que la volatilidad del subyacente aumente, es posible explotar ese aumento con una estrategia "bull spread". [A8 c1], [Ex 2025 1a]

<details><summary>Ver respuesta</summary>

**Falso.** El bull spread (comprar una call K1 y vender una call K2 &gt; K1) es una apuesta direccional al alza, con ganancia y pérdida acotadas: no gana con la volatilidad. Para explotar un aumento de volatilidad sin apostar a una dirección se usa un straddle largo (comprar call y put con el mismo K y vencimiento) [A8 c1].

</details>

2. Un alza de la tasa libre de riesgo afecta en forma negativa la tenencia de calls. [A8 c2]

<details><summary>Ver respuesta</summary>

**Falso.** Un alza de r reduce el valor presente del precio de ejercicio, K·e^(−rT), que pagará quien ejerza la call; por eso la call sube (y la put baja) [A8 c2].

</details>

3. Una call americana y una call europea sobre el mismo subyacente, con el mismo precio de ejercicio y vencimiento, valen lo mismo. [A8 c3]

<details><summary>Ver respuesta</summary>

**Falso (en general).** La americana da todos los derechos de la europea más el ejercicio anticipado, así que C ≥ c. Solo valen lo mismo si la acción no paga dividendos, porque entonces nunca conviene ejercer antes una call; con dividendos, C puede ser mayor [A8 c3].

</details>

4. Un aumento en la volatilidad del subyacente incrementa el valor de una call, pero reduce el de una put sobre el mismo activo. [A9 c2], [Ex 2024 1a]

<details><summary>Ver respuesta</summary>

**Falso.** La volatilidad sube ambas. El pago de una opción es asimétrico: la pérdida del comprador está acotada a la prima y la ganancia no, así que más dispersión aumenta la probabilidad de terminar dentro del dinero sin castigar los malos escenarios [A9 c2].

</details>

5. El precio de una call europea sobre una acción que no paga dividendos podría, en algún escenario, ser mayor que el precio de la acción. [A9 c4]

<details><summary>Ver respuesta</summary>

**Falso.** c ≤ S0: la call da el derecho a comprar la acción, así que no puede valer más que ella. Si c &gt; S0, se vende la call y se compra la acción: hay ganancia hoy y la acción cubre la obligación al vencimiento (arbitraje) [A9 c4].

</details>

6. Si en el mercado se verifica la paridad put-call, c + K·e^(−rT) = p + S0, entonces existe una oportunidad de arbitraje. [A9 c5]

<details><summary>Ver respuesta</summary>

**Falso.** La paridad es la condición de no arbitraje: una call más K·e^(−rT) en caja y una put más la acción pagan lo mismo en T, máx(ST, K), así que deben valer lo mismo hoy. Hay arbitraje cuando no se cumple [A9 c5].

</details>

7. Un alza en la tasa libre de riesgo reduce el valor de una call y aumenta el de una put, ambas sobre una acción que no paga dividendos. [A10 c5]

<details><summary>Ver respuesta</summary>

**Falso.** Es al revés: un alza de r sube la call y baja la put, porque reduce el valor presente de K, que el dueño de la call paga y el de la put recibe [A10 c5].

</details>

8. Sobre una acción que no paga dividendos nunca es óptimo ejercer anticipadamente una opción americana, de modo que C = c y P = p. [A10 c6]

<details><summary>Ver respuesta</summary>

**Falso.** Vale para la call (sin dividendos, C = c), pero no para la put: si está muy dentro del dinero puede convenir ejercerla antes para recibir K hoy y ganar intereses, así que P ≥ p. En [A10] Mat III la put americana vale $4,12 y la europea $3,82 [A10 c6].

</details>

9. Los márgenes en opciones de compra (o de venta) son efectivo o valores depositados tanto por quien compra como por quien vende la opción. [Ex 2025 1c]

<details><summary>Ver respuesta</summary>

**Falso.** Solo deposita margen quien vende (escribe) la opción, porque tiene una obligación futura. Quien compra paga la prima completa al inicio y no tiene obligaciones [Ex 2025 1c], [Sesión II L 18–19].

</details>

10. El pago que genera tanto una put como una call es una función no lineal del precio del subyacente en la madurez. [Ex 2023 Ic]

<details><summary>Ver respuesta</summary>

**Verdadero.** La call paga máx(ST − K, 0) y la put máx(K − ST, 0): son lineales por tramos, con un quiebre en K, así que no son lineales en ST (a diferencia de un forward, cuyo pago ST − K sí es lineal) [Ex 2023 Ic].

</details>

11. El vencimiento de las opciones del CBOE es siempre el último día de negociación del mes de vencimiento. ¿Cuál es la razón? [Ex 2021 2b]

<details><summary>Ver respuesta</summary>

**Falso.** Como se vio en clases, las opciones del CBOE vencen el tercer viernes del mes de vencimiento, no el último día de negociación [Ex 2021 2b].

</details>

12. ¿Por qué los estudiantes en Chile deberían aprender opciones aunque no haya mercados de opciones desarrollados en Chile? [Ex 2022 2b]

<details><summary>Ver respuesta</summary>

**Respuesta (basta una razón).** Todos los seguros son opciones y en Chile hay muchas aseguradoras (Isapres, seguros de auto, de viaje), así que igual habrá que modelar y valorar opciones. Otra: una opción se puede replicar en forma sintética con la acción y un bono, sin necesitar un mercado de opciones [Ex 2022 2b].

</details>

13. Codelco compra una put americana sobre cobre para protegerse. Un analista sostiene que la put americana siempre vale menos que una europea equivalente, porque tiene menos flexibilidad al poder ejercerse en cualquier momento. [Ex Oto26 c3]

<details><summary>Ver respuesta</summary>

**Falso.** La estrategia de Codelco sí es una buena cobertura (comprar puts protege una posición larga en cobre), pero la americana da más flexibilidad, no menos: se puede ejercer en cualquier momento, incluso al vencimiento, así que P ≥ p. En una put, el ejercicio anticipado puede tener un valor estrictamente positivo [Repo].

</details>

14. Ante baja incertidumbre y baja volatilidad del IPSA, un gestor compra una call y una put sobre el IPSA con el mismo strike y vencimiento, argumentando que la estrategia es ideal. [Ex Oto26 c5]

<details><summary>Ver respuesta</summary>

**Falso.** Comprar call y put con el mismo K es un straddle largo, que gana solo si el IPSA se mueve mucho en alguna dirección. Con baja volatilidad el índice queda cerca de K y se pierden ambas primas (la pérdida máxima se da en ST = K). Para ese escenario calza vender el straddle (con riesgo ilimitado) o un butterfly [Ay10 Oto26]. [Sin pauta: respuesta propia.]

</details>

### 6.3 Árboles binomiales y Black-Scholes (3)

1. Al valorar una opción con un árbol binomial, la probabilidad "real" de que el subyacente suba o baje es un dato indispensable: sin ella no es posible obtener el precio. [A9 c1]

<details><summary>Ver respuesta</summary>

**Falso.** Se usa la probabilidad neutral al riesgo, p = (e^(rΔt) − d) / (u − d), que sale de armar un portafolio sin riesgo con la acción y la opción (no arbitraje). La probabilidad real y el retorno esperado de la acción no importan: solo S0, u, d, r y el pago [A9 c1].

</details>

2. Para valorar una opción americana debe usarse Black-Scholes, mientras que para una europea es necesario recurrir a árboles binomiales. [A9 c3], [Ex 2024 1c]

<details><summary>Ver respuesta</summary>

**Falso.** Es al revés. Black-Scholes es una fórmula cerrada que supone ejercicio solo al vencimiento: sirve para europeas. El árbol permite revisar en cada nodo si conviene ejercer, así que sirve para americanas (y también para europeas) [A9 c3].

</details>

3. Las opciones se valoran con valoración neutral al riesgo, como si los agentes tuvieran aversión nula al riesgo. Explique los posibles problemas de ese supuesto. [Ex 2022 2a]

<details><summary>Ver respuesta</summary>

**Falso.** La valoración neutral al riesgo no supone que los agentes tengan aversión nula; pueden tener cualquier aversión. Es una técnica: se arma un portafolio con la opción y Δ acciones que no tiene riesgo, por eso se descuenta a la tasa libre de riesgo, y el precio que resulta vale para cualquier nivel de aversión [Ex 2022 2a].

</details>

### 6.4 VaR (8) · no entra en el Control 2

1. El VaR al 99% a 10 días es simplemente diez veces el VaR diario al 99%. Comente y defina VaR. [A10 c1]

<details><summary>Ver respuesta</summary>

**Falso.** El VaR es la pérdida máxima esperada de un portafolio con un nivel de confianza (99%) y un horizonte (10 días) dados, en condiciones normales de mercado: solo con 1% de probabilidad se pierde más. Con retornos iid normales de media cero, VaR = P0·α·σ·√t: escala con √t, así que el VaR a 10 días es √10 ≈ 3,16 veces el diario, no 10 [A10 c1].

</details>

2. Dos portafolios con la misma volatilidad tienen necesariamente el mismo VaR. [A10 c2]

<details><summary>Ver respuesta</summary>

**Falso.** La volatilidad es solo un insumo. El VaR depende también del monto invertido, la media, el nivel de confianza, el horizonte y la forma de la distribución (colas gruesas, asimetría): con la misma σ, el VaR puede ser distinto [A10 c2].

</details>

3. En el backtesting de un VaR al 95% sobre T = 510 días se observan 40 excepciones. Según Basilea, el modelo es conservador. [A10 c3]

<details><summary>Ver respuesta</summary>

**Falso.** Se esperan 510 × 5% = 25,5 excepciones y la zona de aceptación va de 16 a 36. Con 40 hay demasiadas: el modelo subestima el riesgo (es agresivo, no conservador) y se rechaza. z = (40 − 25,5) / √(510 × 0,05 × 0,95) = 2,95 &gt; 1,96 [A10 c3].

</details>

4. Como la diversificación reduce el riesgo, el VaR de un portafolio es siempre estrictamente menor que la suma de los VaR individuales. [A10 c4]

<details><summary>Ver respuesta</summary>

**Falso.** Bajo normalidad, VaRp ≤ VaRA + VaRB, con igualdad si ρ = 1, así que no es "estrictamente" menor. Además, el VaR no es subaditivo en general: con colas gruesas u opciones puede pasar que VaRp &gt; VaRA + VaRB [A10 c4].

</details>

5. Un banco calcula su VaR diario al 5% y, tras 1.000 días, sus pérdidas nunca excedieron el VaR. Por lo tanto, el cálculo fue adecuado. [Ex 2024 1b], [Ay9 Oto26 cA]

<details><summary>Ver respuesta</summary>

**Falso.** Con un VaR al 5% se esperan 1.000 × 5% = 50 excepciones. Cero excepciones significa que el modelo sobrestima el riesgo (es ultraconservador) y obliga a mantener capital de más: hay que recalibrarlo [Repo].

</details>

6. Una ventaja del método no paramétrico de simulación histórica es que da más peso a la información reciente. [Ex 2025 1b]

<details><summary>Ver respuesta</summary>

**Falso.** La simulación histórica da el mismo peso a todos los datos de la ventana. Los que dan más peso a lo reciente son RiskMetrics y GARCH. Su ventaja es otra: no supone una distribución, así que recoge las colas y la asimetría reales [Sesión II L 78–82].

</details>

7. ¿Qué características básicas debe tener una buena medida de riesgo (según lo discutido en clases)? [Ex 2021 2a]

<details><summary>Ver respuesta</summary>

**Respuesta.** Según la pauta, en clases se vieron cinco: considera el ancho de la distribución, da más peso a los datos recientes, considera la asimetría, considera las colas (eventos extremos) y es fácil de explicar [Ex 2021 2a].

</details>

8. ¿Por qué en la práctica los bancos tienden a sobrestimar su VaR? [A10 Mat I 5)]

<details><summary>Ver respuesta</summary>

**Respuesta.** Por el incentivo regulatorio asimétrico de Basilea: el capital exigido es un múltiplo del VaR y ese multiplicador sube si el backtesting da demasiadas excepciones, así que quedarse corto cuesta más que quedarse largo. Suman el costo reputacional y la prudencia frente al riesgo de modelo [A10] Mat I 5).

</details>

## 7. Banco de ejercicios (35)

| **\#** | **Ejercicio** | **Pauta** | **Qué practica** |
| --- | --- | --- | --- |
|  | **Black-Scholes** |  |  |
| 1 | [C2 2024] = [C2 2025]: call Soquimik, sin y con dividendo | Sí | El control de los dos últimos años |
| 2 | [A9] Mat II (S0 = 60, K = 58, 9 meses) | Sí | Call, put por paridad y call con dividendo |
| 3 | [Ex 2020] P1: put Soquimik | Sí | La misma Soquimik, ahora put (y luego con dividendo) |
| 4 | [Ex 2025] P4 (S0 = 95, K = 100) | Sí | Put con Black-Scholes y call por paridad |
| 5 | [Ex 2024] P4a (S0 = 40, K = 45, 7 meses, σ = 16%) | Sí | Call fuera del dinero, T en meses |
| 6 | [Ex Oto26] Ej 2b (S0 = 60, K = 58, σ = 30%) | Sí | Comparar Black-Scholes con el árbol |
|  | **Árboles binomiales** |  |  |
| 7 | [Sesión II L 47–58]: ejemplos de clase | Sí | Δ, p neutral al riesgo, put americana |
| 8 | [A9] Mat I a) y b) (S0 = 50, K = 50) | Sí | Put europea en 2 pasos y call por paridad |
| 9 | [A10] Mat III 1)–4) y 6) (S0 = 40, K = 42) | Sí | Europea vs. americana, Δ, call en el árbol |
| 10 | [Ex 2025] P3 (±30%, K = 40, 2 años) | Sí | Put americana con u y d dados |
| 11 | [Ex 2024] P3 (S0 = 400, u = 1,25, d = 0,8) | Sí | Call y put europeas a 2 años |
| 12 | [Ex 2021] = [Ex 2022] = [Ex 2023] P3: pago [máx(30 − ST, 0)]² | Sí (en inglés) | Pago no estándar y ejercicio anticipado |
| 13 | [Ex Oto26] Ej 2a (S0 = 60, K = 58) | Sí | Call en 2 pasos |
|  | **Cotas, paridad y arbitraje** |  |  |
| 14 | [Sesión II L 26, 27 y 29] | Sí | Cotas de call y put; arbitraje |
| 15 | [A9] Mat I c): call a $4 | Sí | Call cara: tabla de flujos |
| 16 | [A10] Mat III 5): call a $4,20 | Sí | Call cara: tabla de flujos |
| 17 | [Ex 2025] P2: put a $7 | Sí | Put cara: vender put y acción, comprar call |
| 18 | [Ex 2024] P4b: put a $3 | Sí | Put barata |
| 19 | [Ex Oto26] Ej 2c: put a $4 | Sí | Put cara |
|  | **Forwards y futuros** |  |  |
| 20 | [A8] Mat I (S0 = 40) | Sí | F0 y valor del forward a los 6 meses |
| 21 | [A8] Mat II (Entel, dividendos) | Sí | F0 = (S0 − I)·e^(rT) |
| 22 | [A8] Mat III (futuro LIFFE, 1.000 acciones) | Sí | Mark-to-market de la cuenta |
| 23 | [Ay8 Oto26] Mat 1 (dividendo de $50) | Sí | F0, Ft y valor con dividendo |
| 24 | [C3 Oto26] P1 (importador, US$20.000) | Sí | Forward de divisas con tasas simples y arbitraje |
| 25 | [Ay9 Oto26] Mat 3 (US$10.000) | Sí | Igual que el 24 |
| 26 | [Ay8 Oto26] Mat 2 y 3; [Ay9 Oto26] Mat 2 | Sí | Paridad cubierta de tasas y cobertura con futuros |
| 27 | [Ex Oto26] Ej 1: forward sobre un bono | Sí | Forward con cupones (nivel examen) |
|  | **Estrategias** |  |  |
| 28 | [A8] Mat IV (strangle) y Mat V (bull spread) | Sí | Gráficos y puntos de equilibrio |
| 29 | [A10] Mat IV: call cubierta | Sí | Equilibrio, ganancia y pérdida máximas |
| 30 | [Ex 2024] P2: 100 o 200 acciones y 1, 2 o 4 calls vendidas | Sí (gráficos) | Contratos de 100 |
| 31 | [Ex 2022] P3: collar con contratos | Sí (en inglés) | Contratos de 100 |
| 32 | [Ex 2023] P2: vender acción y put, comprar call | Sí (en inglés) | Tabla de pagos y gráfico |
| 33 | [Ex Oto26] Ej 3 (butterfly); [Ay10 Oto26] Mat 1–3 | Sí | Butterfly, short straddle, iron condor |
|  | **VaR** |  |  |
| 34 | [A10] Mat I (P0 = $500 millones) | Sí | VaR diario, a 10 días, con media y backtesting |
| 35 | [A10] Mat II (dos activos) | Sí | VaR de portafolio y diversificación |

## 8. Errores detectados en el material

1. [C2 2024] y [C2 2025] a): dice "So, the value of the Put options is", pero lo que calcula es la call (C = 28,85).
2. [C2 2024] y [C2 2025] a): d2 aparece como −0,06107; lo correcto es 0,2929 − 0,3536 = −0,0607. N(d2) = 0,4758 sí está bien, así que el precio no cambia.
3. [C2 2025] b): usa N(d1) = 0,4882 y N(d2) = 0,3508 y obtiene $18,00. Con la normal exacta (como [C2 2024]) son 0,4889 y 0,3515, y la call vale $18,05; con la tabla a 2 decimales da $17,82. Según la nota de la pauta, cualquiera sirve.
4. [A8] Mat I y III usan capitalización discreta, F0 = S0·(1 + r)^T, mientras la clase y el Mat II usan continua. Si el enunciado no lo dice, usa continua y anótalo como supuesto.
5. [Ex 2025] P2: el enunciado dice que la call y la put "no tienen el mismo vencimiento y el mismo precio de ejercicio"; es al revés (si no los tuvieran, no se podría usar la paridad).
6. [A9] Mat II: con los N(·) redondeados de la "Ayuda" la call da $7,40 y la put $3,27; con la normal exacta, $7,33 y $3,19. Lo mismo en [Ex Oto26] Ej 2b ($6,94 vs. $6,99). No son errores: usa la tabla como la pauta.
7. [Repo] Examen otoño 2026: los comentes 5 (straddle) y 6 (futuros vs. forwards) dicen "Ver solución", pero la solución no está.
8. [Repo] Control 3 otoño 2026 b): da −75.074 porque redondea F6 − F0 a −3,81; sin redondear es ≈ −74.967.
9. [Ex 2021], [Ex 2022] y [Ex 2023]: varias respuestas (el árbol de la P3, las estrategias) están solo en la parte en inglés, como imagen; la parte en castellano quedó en blanco. El derivado de la P3 vale $5,39 (lo verifiqué). En [Ex 2021] además preguntan si convendría ejercerlo antes si fuera americano: no, porque en el nodo bajo (S = 27) ejercer da 9 y continuar 13,24.
10. [Ex 2021] 2a pregunta por "siete" características de una buena medida de riesgo, pero la pauta dice que en clases solo se vieron cinco (sección 9).

## 9. Teoría que entra y no está en las láminas

- **Buena medida de riesgo** [Ex 2021] 2a: considera el ancho de la distribución, da más peso a los datos recientes, considera la asimetría y las colas (eventos extremos) y es fácil de explicar.
- **Vencimiento en el CBOE** [Ex 2021] 2b: el tercer viernes del mes de vencimiento, no el último día hábil.
- **Paridad cubierta de tasas** [C3 Oto26], [Ex Oto26] c4, [Fórmulas]: F = S·(1 + rCLP) / (1 + rUSD), o F = S·e^((r − r\*)·T). Un forward sobre el spot refleja la diferencia de tasas, no una expectativa de depreciación.
- **Futuros:** cámara de compensación, cuenta de margen y mark-to-market [A8] c5 y Mat III, [Ay8 Oto26] cA; riesgo de base cuando el futuro no vence en la fecha de la exposición [Repo] 1.8.
- **Backtesting:** las excepciones siguen una binomial: E[N] = T·p y z = (N − T·p) / √(T·p·(1 − p)); con 9 excepciones en 250 días al 99%, z = 4,13 [A10] Mat I 4). Zona de no rechazo para T = 510 al 95%: 16 a 36 [A10] c3.
- **VaR no subaditivo:** con colas gruesas u opciones puede pasar que VaRp &gt; VaRA + VaRB [A10] c4.
- **Por qué los bancos sobrestiman su VaR:** incentivo regulatorio de Basilea, costo reputacional y prudencia frente al riesgo de modelo [A10] Mat I 5).
- **Call cubierta en las AFP:** autorizada en Chile desde 2019 [A10] Mat IV.

## 10. Plan de estudio (domingo 1 y lunes 2 hasta las 18:00)

Cada bloque: teoría → resuelto → ejercicio sin mirar la pauta → comentes de la sección 6 (primero respondes tú, después lees la respuesta). Los números de ejercicio son los de la sección 7.

| **Día** | **Tema** | **Qué hacer** |
| --- | --- | --- |
| Dom 1, bloque 1 (1,5 h) | Black-Scholes (lo más probable) | Teoría ([Sesión II L 60–65], 4.1) → resuelto 2 → practicar 1 sin mirar la pauta (con y sin dividendo) y 4 → 6.3 |
| Dom 1, bloque 2 (1,5 h) | Árboles y paridad | Teoría ([Sesión II L 21–29 y 47–58], 4.2 y 4.3) → resueltos 8 y 9 → practicar 10 y 17 → 6.2 (1 a 8) |
| Dom 1, bloque 3 (1 h) | Forwards y estrategias | Resueltos 20, 21 y 28 → practicar 24 y 30 → 6.1 y 6.2 (9 a 14) |
| Lun 2, mañana (1,5 h) | ~~VaR~~ (no entra: úsalo para opciones y Black-Scholes) | Teoría ([Sesión II L 73–85], 4.6) → resueltos 34 y 35 → 6.4 |
| Lun 2, tarde (1 h) | Simulacro | Ejercicios 13, 6 y 19 ([Ex Oto26] Ej 2 completo) en 40 minutos con tabla y calculadora → corregir → releer la sección 5 |
| Lun 2, antes de salir (45 min) | Control de la tarea | Parte 2: cifras clave (sección 11), preguntas marcadas "muy probable", ejercicios E1 a E8 y comentes C1 a C10 |

Si te sobra tiempo: ejercicios 3, 11, 12 y 33.
