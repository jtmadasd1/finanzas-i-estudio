# Mapa Examen Finanzas I

Finanzas I (ENFIN415), Prof. Alejandro Bernales · Examen: materia posterior a la Solemne (derivados y VaR) · esta semana (fecha y hora por confirmar)

*Versión del 24-11-2026. Todo sale de tu carpeta Finanzas; cada afirmación lleva entre corchetes el archivo del que sale. Si algo no está en el material, lo digo.*

**Abreviaturas:** [Sesión II L n] = Sesiones (material del curso)/Sesion\_II\_ENFIN415.pdf, lámina n; [A8], [A9] y [A10] = Ayudantías 8, 9 y 10 (enunciado y pauta); [A11] = Ayudantía 11 (no está en la carpeta); [C2 2024] y [C2 2025] = Pauta Control 2 de esos años; [Ex 2020] … [Ex 2025] = pautas de exámenes; [Repo] = Repositorio\_Finanzas\_I.pdf (material de otoño 2026), con [Ay8 Oto26], [Ay9 Oto26], [Ay10 Oto26], [C3 Oto26] = Control 3 y [Ex Oto26] = Examen; [Fórmulas] = Formulas\_FinanzasI\_FinanzasII.pdf; [Programa] = Programa/ENFIN415\_2026.pdf; c = comente, Mat = matemático.

## 1. Resumen

- **Qué entra:** lo visto después de la Solemne: la Sesión II completa, es decir, derivados [Sesión II L 3–65] y VaR [Sesión II L 67–85], más las ayudantías 8, 9, 10 y 11 (esto último según tú). El VaR, que no entró en el Control 2, **sí entra** aquí.
- **Qué no entra:** la materia de la Solemne: portafolios, CAPM, modelo índice, APT, eficiencia, desempeño y renta fija, incluidos los swaps [Sesión I], [A3]–[A7], [Solemne 2024] y [Solemne 2025]. Los exámenes de 2020 a 2023 traen algunas preguntas de esa materia; están marcadas en la sección 3 y no se usan.
- **Cuánto vale:** 30% de la nota final, igual que la Solemne. Ojo: los controles y la tarea solo cuentan si el promedio entre Solemne y Examen es 3,95 o más [Programa].
- **Formato esperado:** los exámenes de 2024 y 2025 tuvieron la misma estructura, 4 preguntas de 60 puntos: P1 tres comentes de 20 puntos (siempre uno de VaR), P2 estrategias (2024) o paridad y arbitraje (2025), P3 árbol binomial y P4 Black-Scholes [Ex 2024], [Ex 2025]. Sección 3.
- **Lo que más se repite:** el árbol binomial salió en 6 de 7 exámenes y Black-Scholes en 4 de 7. Hay preguntas recicladas de un año a otro (sección 4.8).
- **Para el día:** calculadora (el celular está prohibido) [Programa]; practica e^x, ln y raíz en ella. La tabla normal se lee con 2 decimales, sin interpolar [C2 2024].
- **Falta material:** la Ayudantía 11 no está en la carpeta (sección 2).

## 2. Mapa de archivos por tema

| **Tema** | **Teoría** | **Resueltos paso a paso** | **Para practicar** |
| --- | --- | --- | --- |
| Forwards y futuros | [Sesión II L 3–7]; [Fórmulas] pág. 2 (acción, divisas, dividendos, valor del contrato) | [A8] Mat I, II y III; [Ay8 Oto26] Mat 1 | [C3 Oto26] P1; [Ay9 Oto26] Mat 3; [Ay8 Oto26] Mat 2 y 3; [Ex Oto26] Ej 1 |
| Opciones: pagos y estrategias | [Sesión II L 8–19 y 31–45] | [A8] Mat IV y V; [A10] Mat IV (call cubierta) | [Ex 2024] P2; [Ex 2022] P3; [Ex 2023] P2; [Ex Oto26] Ej 3; [Ay10 Oto26] Mat 1–3 |
| Cotas, paridad y arbitraje | [Sesión II L 21–29]; [Fórmulas] pág. 3 (paridad con dividendos y casos) | [A9] Mat I c); [A10] Mat III 5) | [Ex 2025] P2; [Ex 2024] P4b; [Ex Oto26] Ej 2c |
| Árboles binomiales | [Sesión II L 47–58] | [A9] Mat I; [A10] Mat III (europea, americana y Δ) | [Ex 2025] P3; [Ex 2024] P3; [Ex 2021–2023] P3; [Ex Oto26] Ej 2a |
| Black-Scholes | [Sesión II L 60–65] | [A9] Mat II (con dividendo); [C2 2024] | [C2 2025]; [Ex 2020] P1; [Ex 2025] P4; [Ex 2024] P4a; [Ex Oto26] Ej 2b |
| VaR | [Sesión II L 67–85] (paramétrico L 76–77, GARCH L 78–80, simulación histórica L 81–82, Kupiec L 83–85) | [A10] Mat I y II | Comentes [A10] 1–4; [Ex 2024] 1b; [Ex 2025] 1b |

Falta la **Ayudantía 11**: no está en la carpeta Finanzas, y el A11\_Pauta.pdf de Descargas es de Economía Aplicada (Primavera 2025). Cuando la agregues a Finanzas/Ayudantias, la sumo al mapa.

## 3. Qué preguntaron los exámenes pasados (solo derivados y VaR)

Método: separé en cada examen las preguntas de derivados y VaR de las de materia de la Solemne, que no se usan. Los exámenes de 2020 a 2023 tenían 3 preguntas del mismo peso (en 2023 eran 4 y se contestaban 3); los de 2024 y 2025, 4 preguntas de 60 puntos. [Ex Oto26] es el examen de otoño 2026 que trae el Repositorio.

| **Examen** | **Preguntas de derivados y VaR** | **Peso** | **No entra (materia de la Solemne o fuera del material)** |
| --- | --- | --- | --- |
| [Ex 2020] | P1: put Soquimik con Black-Scholes, call con las mismas características y ambas con dividendo de $20 en 5 meses | 1 de 3 | P2: comentes de presentaciones del profesor (volatilidad y valor fundamental; spreads de CDS), que no están en el material. P3: valorar un swap con FRAs (renta fija) |
| [Ex 2021] | P2a: características de una buena medida de riesgo (VaR); P2b: vencimiento de las opciones del CBOE; P3: árbol de 2 pasos para un derivado con pago [máx(30 − ST, 0)]² y si conviene ejercerlo antes | 2 de 3 | P1: betas y CAPM |
| [Ex 2022] | P1: el mismo árbol de [Ex 2021] P3; P2: comentes (valoración neutral al riesgo; por qué aprender opciones en Chile); P3: collar con contratos (100 acciones, vender una call y comprar una put) | 3 de 3 | — |
| [Ex 2023] | Ic: pagos no lineales de las opciones; P2: estrategia vender la acción y la put y comprar la call (tabla y gráfico); P3: el mismo árbol de [Ex 2021] P3 | 2 de 4, más un comente | Ia y Ib: tasas y duración; P4: CAPM |
| [Ex 2024] | P1: comentes (volatilidad y precio de call y put; VaR nunca excedido en 1.000 días; Black-Scholes vs. árbol); P2: 4 gráficos con 100 o 200 acciones y 1, 2 o 4 calls vendidas; P3: árbol call y put europeas (S0 = 400, +25%/−20%, K = 375); P4: call con Black-Scholes (S0 = 40, K = 45, 7 meses) y arbitraje con la put a $3 | 4 de 4 | — |
| [Ex 2025] | P1: comentes (bull spread y volatilidad; simulación histórica; márgenes en opciones); P2: paridad put-call y arbitraje (S0 = 50, K = 52, put a $7); P3: árbol put americana (S0 = 40, ±30%, K = 40, 2 años); P4: put Andina con Black-Scholes (S0 = 95, K = 100) y la call | 4 de 4 | — |
| [Ex Oto26] | Ej 1: forward sobre un bono; Ej 2: árbol de 2 pasos, Black-Scholes y arbitraje con la put (S0 = 60, K = 58); Ej 3: butterfly; comentes c3 a c6 (put americana, forward de dólar, straddle, futuros vs. forwards) | Todo | — |

**Cuántas veces salió cada tema (de 7 exámenes):**

| **Tema** | **Exámenes** | **Veces** |
| --- | --- | --- |
| Árbol binomial | 2021, 2022, 2023, 2024, 2025, Oto26 | 6 |
| Estrategias y gráficos | 2022, 2023, 2024, Oto26 | 4 |
| Black-Scholes | 2020, 2024, 2025, Oto26 | 4 |
| Paridad put-call y arbitraje | 2024, 2025, Oto26 | 3 |
| VaR (como comente) | 2021, 2024, 2025 | 3 |
| Forwards y futuros | Oto26 (ejercicio y 2 comentes) | 1 |

**Lo más probable para este examen:** el formato de 2024 y 2025. P1 con un comente de VaR y dos de opciones; P2 estrategias o paridad y arbitraje; P3 un árbol de 2 pasos con europea y americana; P4 Black-Scholes con call o put y, posiblemente, dividendo o paridad. Es una estimación mía a partir de las pautas.

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

### 4.6 VaR

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

## 6. Banco de comentes (32)

Todos los comentes de derivados y VaR de las ayudantías, controles, exámenes y el Repositorio, sin respuesta y con su fuente. Contesta como en el examen: verdadero, falso o incierto, con una justificación corta, y te corrijo en el chat. Si los necesitas, las respuestas están en Estudio Controles/Guia Finanzas I - Control 2 y Control Tarea.pdf, sección 6.

### 6.1 Forwards y futuros (7)

1. En un contrato forward justo, el valor inicial del contrato para ambas partes es distinto de cero. [A8 c4]

2. Los futuros y los forwards son equivalentes en todo sentido, ya que ambos fijan precios futuros y eliminan el riesgo de contraparte. [A8 c5]

3. Explique en qué consiste el marking-to-market (liquidación diaria) de los futuros y cómo los diferencia de un forward en términos de riesgo de contraparte. [Ay8 Oto26 cA]

4. Dado que un exportador chileno recibirá flujos en dólares en el futuro, para mitigar el riesgo de tipo de cambio le convendría tomar una posición larga en futuros sobre el dólar (USD/CLP). [Ay8 Oto26 cB]

5. Liquidar (o cerrar) una posición larga de un contrato de forwards de dólares es más fácil que si fuera en el mercado de futuros. [Ay9 Oto26 cB]

6. Un tesorero observa que el dólar forward a 12 meses cotiza por sobre el spot actual y concluye que el mercado anticipa una depreciación del peso. [Ex Oto26 c4]

7. Una AFP cubre su exposición al cobre y el área de riesgo recomienda futuros en la LME en vez de forwards OTC, argumentando que tienen mayor liquidez, pero también mayor riesgo de contraparte que los forwards. [Ex Oto26 c6]

### 6.2 Opciones, estrategias y paridad (14)

1. Cuando se espera que la volatilidad del subyacente aumente, es posible explotar ese aumento con una estrategia "bull spread". [A8 c1], [Ex 2025 1a]

2. Un alza de la tasa libre de riesgo afecta en forma negativa la tenencia de calls. [A8 c2]

3. Una call americana y una call europea sobre el mismo subyacente, con el mismo precio de ejercicio y vencimiento, valen lo mismo. [A8 c3]

4. Un aumento en la volatilidad del subyacente incrementa el valor de una call, pero reduce el de una put sobre el mismo activo. [A9 c2], [Ex 2024 1a]

5. El precio de una call europea sobre una acción que no paga dividendos podría, en algún escenario, ser mayor que el precio de la acción. [A9 c4]

6. Si en el mercado se verifica la paridad put-call, c + K·e^(−rT) = p + S0, entonces existe una oportunidad de arbitraje. [A9 c5]

7. Un alza en la tasa libre de riesgo reduce el valor de una call y aumenta el de una put, ambas sobre una acción que no paga dividendos. [A10 c5]

8. Sobre una acción que no paga dividendos nunca es óptimo ejercer anticipadamente una opción americana, de modo que C = c y P = p. [A10 c6]

9. Los márgenes en opciones de compra (o de venta) son efectivo o valores depositados tanto por quien compra como por quien vende la opción. [Ex 2025 1c]

10. El pago que genera tanto una put como una call es una función no lineal del precio del subyacente en la madurez. [Ex 2023 Ic]

11. El vencimiento de las opciones del CBOE es siempre el último día de negociación del mes de vencimiento. ¿Cuál es la razón? [Ex 2021 2b]

12. ¿Por qué los estudiantes en Chile deberían aprender opciones aunque no haya mercados de opciones desarrollados en Chile? [Ex 2022 2b]

13. Codelco compra una put americana sobre cobre para protegerse. Un analista sostiene que la put americana siempre vale menos que una europea equivalente, porque tiene menos flexibilidad al poder ejercerse en cualquier momento. [Ex Oto26 c3]

14. Ante baja incertidumbre y baja volatilidad del IPSA, un gestor compra una call y una put sobre el IPSA con el mismo strike y vencimiento, argumentando que la estrategia es ideal. [Ex Oto26 c5]

### 6.3 Árboles binomiales y Black-Scholes (3)

1. Al valorar una opción con un árbol binomial, la probabilidad "real" de que el subyacente suba o baje es un dato indispensable: sin ella no es posible obtener el precio. [A9 c1]

2. Para valorar una opción americana debe usarse Black-Scholes, mientras que para una europea es necesario recurrir a árboles binomiales. [A9 c3], [Ex 2024 1c]

3. Las opciones se valoran con valoración neutral al riesgo, como si los agentes tuvieran aversión nula al riesgo. Explique los posibles problemas de ese supuesto. [Ex 2022 2a]

### 6.4 VaR (8)

1. El VaR al 99% a 10 días es simplemente diez veces el VaR diario al 99%. Comente y defina VaR. [A10 c1]

2. Dos portafolios con la misma volatilidad tienen necesariamente el mismo VaR. [A10 c2]

3. En el backtesting de un VaR al 95% sobre T = 510 días se observan 40 excepciones. Según Basilea, el modelo es conservador. [A10 c3]

4. Como la diversificación reduce el riesgo, el VaR de un portafolio es siempre estrictamente menor que la suma de los VaR individuales. [A10 c4]

5. Un banco calcula su VaR diario al 5% y, tras 1.000 días, sus pérdidas nunca excedieron el VaR. Por lo tanto, el cálculo fue adecuado. [Ex 2024 1b], [Ay9 Oto26 cA]

6. Una ventaja del método no paramétrico de simulación histórica es que da más peso a la información reciente. [Ex 2025 1b]

7. ¿Qué características básicas debe tener una buena medida de riesgo (según lo discutido en clases)? [Ex 2021 2a]

8. ¿Por qué en la práctica los bancos tienden a sobrestimar su VaR? [A10 Mat I 5)]

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

## 10. Plan de estudio (examen esta semana)

Supuesto: 3 días de estudio antes del examen. Cuando me digas el día y las horas que tienes, lo ajusto. Cada tema sigue el método de la Fase 2: teoría desde cero → ejercicio resuelto paso a paso → ejercicio para ti (te corrijo sin darte la solución) → 3 a 5 comentes. Avanzamos con "siguiente". Los números son los de la sección 7.

| **Día** | **Tema** | **Qué hacer** |
| --- | --- | --- |
| Día 1 | 1. Opciones desde cero | Qué son, call y put, largo y corto, pagos al vencimiento [Sesión II L 8–19] → [A8] Mat IV → comentes 6.2 |
| Día 1 | 2. Black-Scholes (P4) | Teoría [Sesión II L 60–65] → resuelto 2 → práctica 4 y 5 → comentes 6.3 |
| Día 2 | 3. Árbol binomial (P3) | Teoría [Sesión II L 47–58] → resueltos 8 y 9 → práctica 10 y 11 (y 12 si sobra tiempo) |
| Día 2 | 4. Cotas, paridad y arbitraje (P2 o P4b) | Teoría [Sesión II L 21–29] → resuelto 15 → práctica 17 y 18 |
| Día 3 | 5. Estrategias y gráficos (P2) | Teoría [Sesión II L 31–45] → resueltos 28 y 29 → práctica 30 y 31 |
| Día 3 | 6. VaR y backtesting (P1) | Teoría [Sesión II L 67–85] → resueltos 34 y 35 → comentes 6.4 |
| Víspera | 7. Forwards y futuros | Teoría [Sesión II L 3–19] → resueltos 20 y 21 → comentes 6.1 |
| Víspera | Simulacro (Fase 3) | Un examen completo con el formato de 2024 y 2025 (4 preguntas de 60), corregido con puntaje |

Si el examen es antes de lo que supuse, prioriza en este orden: Black-Scholes, árbol, paridad y arbitraje, comentes de VaR y estrategias. Forwards es lo que menos ha salido.
