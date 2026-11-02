# Parte 2 · Control de la tarea

*Las cifras de esta parte son las de la tarea de nuestro grupo. Si tu grupo llegó a otras, cámbialas por las tuyas: el control es sobre tu propia tarea. Las láminas citadas son las de la Sesión I.*

## 11. Cifras clave de la tarea

El control es individual y sobre nuestra propia tarea, así que espera preguntas tipo comente que piden **explicar e interpretar nuestros resultados**, no recalcularlos. Un antecedente: en la Solemne 2022 se preguntó "¿Qué efecto tuvieron las restricciones de inversión en la frontera eficiente?". Memoriza esta tabla y practica responder cada pregunta en 4 a 6 líneas: idea central, mecanismo y un número nuestro.

| **Tema** | **Nuestro resultado** | **Pregunta** |
| --- | --- | --- |
| Datos | 50 acciones de 11 sectores; retornos diarios del 2-ago-2021 al 31-jul-2026 (1.255 obs.); retornos continuos ln(Pt/Pt−1); anualizados ×252 | Metodología |
| Tasa libre de riesgo | Tesoro a 1 año (H.15) al 31-jul-2026: 4,08% equivalente a bono → 4,04% continua | 1B |
| S&P 500 | μ = 10,7%, σ = 17,0%, Sharpe = 0,39 | 1B |
| Correlaciones | Promedio 0,23; dentro del sector 0,45; el 91% de la varianza del 1/N viene de covarianzas | 1A.1 y 1A.3 |
| Mínima varianza (GMV) | μ = 13,3%, σ = 10,8%; usa las 50 acciones, 38% en cortos | 1A.2 |
| GMV ingenuo | σ percibida 3,5% vs. σ real 12,4% | 1A.3 |
| Límite \|wᵢ\| ≤ 10% | Retorno máximo 45,1%; GMV σ = 10,83%; Sharpe máximo 2,10 | 1A.4 |
| Sin venta corta | Retorno entre −6,7% (AMT) y 46,9% (NVDA); GMV σ = 11,18%; 2 a 25 acciones; Sharpe máximo 1,46 | 1A.5 |
| + Energy/Industrials ≥ 40% | Retorno máximo 39,8% (60% NVDA + 40% CAT); GMV σ = 11,38%; Sharpe máximo 1,45 | 1A.6 |
| Tangencia M | μ = 85,9%, σ = 32,2%, Sharpe = 2,54; exposición bruta 10,2x (560% largo, −460% corto) | 1B.1 |
| Modelo índice de M | α = 0,31% diario = 78,5% anual, t = 5,64; β = 0,51; R² = 0,07 | 1B.2 |
| Simulación con α verdadero = 0 | t(α) promedio 7,09; el 100% de las simulaciones "rechaza" α = 0 | 1B.2 |
| Fuera de muestra (ago-2025 a jul-2026) | M −21,4% (Sharpe −0,46); sin venta corta +33,1%; 1/N +25,0%; S&P 500 +18,1% | 1B.2 |
| Sharpe / Treynor | M 2,54 / 161%; S&P 500 0,39 / 6,7%; 12 acciones invierten el ranking (JNJ, LMT) | 1B.3 |
| Asignación óptima | x\* = 7,90/c → 3,95 (c = 2), 1,58 (c = 5), 0,79 (c = 10) | 1B.4 |
| Nelson-Siegel / Svensson | RMSE NS 2,0 a 10,6 pb; Svensson 1,1 a 8,5 pb (mejora de 20% a 66%) | 2 |
| Junios invertidos (10A − 3M) | 2019 (−12 pb), 2023 (−162 pb), 2024 (−112 pb), 2025 (−17 pb, solo tramo corto) | 2.3 |
| Inversión más larga | 10A − 2A: 6-jul-2022 a 5-sep-2024 (26 meses, mínimo −108 pb); 10A − 3M: hasta −189 pb | 2.3 |

## 12. Pregunta 1A: frontera media-varianza

La idea que conecta toda la 1A: **la diversificación depende de las covarianzas, y cada restricción achica el conjunto factible y crea una "mini-frontera" dentro de la original.**

**P1. ¿Por qué usaron retornos continuos y cómo los anualizaron?**

La clase prefiere retornos continuos, r = ln(Pt/Pt−1), porque se suman en el tiempo y se parecen a los aritméticos cuando los cambios son pequeños. Si los retornos diarios son independientes, la media y la varianza crecen linealmente con el horizonte: μ anual = 252 · μ diaria, Ω anual = 252 · Ω diaria y σ anual = √252 · σ diaria. Usamos el cierre ajustado: sin ajuste, los splits (NVDA 10:1, AMZN 20:1, NFLX 10:1) aparecerían como caídas falsas de 67% a 95%.

**P2. ¿Por qué eligieron 5 años?**

Con 50 acciones hay que estimar 50 medias y 1.275 varianzas y covarianzas. Con 1 año (252 datos) la matriz Ω sería imprecisa y casi singular (N/T ≈ 0,20); con 5 años, N/T ≈ 0,04. Aun así las medias quedan ruidosas: su error estándar es σ/√5, por ejemplo ±23 puntos para NVDA. El costo de una ventana larga es que datos antiguos pueden no representar el futuro.

**P3. ¿Cómo se construye la frontera media-varianza?**

Para cada retorno objetivo se minimiza la varianza (Sesión I, lámina 17), con ventas cortas permitidas:

> mín w′Ωw   sujeto a   w′μ = μ̄  y  w′1 = 1   ⇒   w\* = Ω⁻¹(λ₁·1 + λ₂·μ)

> σ²(μ̄) = (A·μ̄² − 2B·μ̄ + C) / D,   con A = 1′Ω⁻¹1,  B = 1′Ω⁻¹μ,  C = μ′Ω⁻¹μ  y  D = AC − B²

Es una hipérbola. El GMV tiene μ = B/A = 13,3% y σ = 1/√A = 10,8%; solo la rama sobre el GMV es eficiente. Con restricciones no hay fórmula y se resuelve con programación cuadrática.

**P4. ¿Por qué la frontera queda a la izquierda de todas las acciones?**

Porque las correlaciones son menores que 1: la volatilidad de un portafolio es menor que el promedio ponderado de las volatilidades. El GMV (10,8%) tiene menos riesgo que KO, la acción menos volátil (16,6%), y que el S&P 500 (17,0%). Con el riesgo del S&P 500 la frontera promete 44,7% contra 10,7% del índice, pero eso es *in-sample*: usa medias que ya conocemos.

**P5. ¿Qué rol juegan las covarianzas en la diversificación? (muy probable)**

- **Fijan el piso de riesgo.** Para 1/N, σ²p = σ²/N + (1 − 1/N)·cov promedio: cuando N crece el riesgo converge a la covarianza promedio, no a cero. En nuestros datos el 91% de la varianza del 1/N viene de covarianzas.
- **Ignorarlas crea una ilusión de diversificación.** El GMV ingenuo cree tener σ = 3,5% pero tiene 12,4%. La frontera ingenua real siempre queda a la derecha de la completa, porque la completa minimiza la varianza verdadera.
- **Permiten cubrirse.** Con acciones muy correlacionadas (COP–EOG, ρ = 0,87) una posición larga y otra corta cancelan el factor común. Por eso, en retornos altos, la frontera ingenua "percibida" cruza a la completa: en portafolios largo-corto las covarianzas positivas reducen el riesgo.

**P6. ¿Qué efecto tienen las restricciones sobre la frontera? (pregunta de la Solemne 2022)**

Toda restricción reduce el conjunto factible, así que la nueva frontera es una "mini-frontera" dentro de la original: nunca puede ofrecer menos riesgo para el mismo retorno *in-sample*. El costo es pequeño cerca del GMV y crece con el retorno objetivo, y el retorno máximo queda acotado. Orden de costo: |w| ≤ 10% (permite cortos) &lt; sin venta corta &lt; sin venta corta + sector.

**P7. ¿Por qué el límite de 10% casi no cambia el GMV pero sí la parte alta?**

El GMV libre ya era diversificado: solo DUK (14,8%), JNJ (14,3%) y XOM (10,6%) pasaban el 10%, y se reemplazan con acciones parecidas (σ sube de 10,81% a 10,83%). Los retornos altos, en cambio, necesitaban posiciones gigantes (KO, SO y XOM sobre 75% en M). El techo es 45,1%: +10% en las 30 acciones de mayor μ y −10% en las 20 de menor μ.

**P8. Sin venta corta, ¿por qué el máximo es NVDA y los portafolios son tan concentrados?**

Con w ≥ 0 y pesos que suman 1, el retorno del portafolio es un promedio ponderado: no puede superar a la mejor acción (46,9%, NVDA) ni bajar de la peor (−6,7%, AMT). Sin cortos no hay apalancamiento ni coberturas. La solución tiene "portafolios esquina": muchas acciones quedan en w = 0 y cada tramo eficiente usa entre 2 y 25 acciones.

**P9. ¿Por qué la restricción sectorial cuesta poco en la zona media y mucho en los extremos?**

Es activa en toda la frontera, porque sin ella Energy + Industrials pesaban entre 0% y ~32%. En la zona media cuesta poco: XOM, CAT y RTX tuvieron buenos retornos y la energía tiene baja correlación con tecnología (el Sharpe máximo baja solo de 1,455 a 1,447). En los extremos cuesta mucho: arriba el máximo cae de 46,9% a 39,8% (60% NVDA + 40% CAT) y abajo hay que usar WM y LMT en vez de consumo básico.

**P10. Entonces, ¿las restricciones son malas?**

*In-sample* sí cuestan, pero fuera de muestra suelen ayudar: impiden apostar fuerte a diferencias de medias que son ruido (Jagannathan y Ma, 2003). En nuestra prueba fuera de muestra, la tangencia sin venta corta ganó 33,1% y la tangencia libre perdió 21,4%.

## 13. Pregunta 1B: LMC, alfa de Jensen y desempeño

La idea que conecta toda la 1B: **M es óptimo con los datos que lo construyeron, por eso su alfa enorme y significativo es un artefacto y no evidencia contra la eficiencia de mercado.**

**P11. ¿Cómo se obtiene el portafolio de tangencia y la LMC?**

M es el portafolio de la frontera que maximiza el Sharpe, es decir, la pendiente de la línea que sale de rf:

> wM = Ω⁻¹(μ − rf·1) / [1′Ω⁻¹(μ − rf·1)]          LMC: E[Rp] = rf + SRM·σp = 4,04% + 2,54·σp

Por el teorema de separación (Sesión I, lámina 28): (A) frontera y (B) M no dependen de las preferencias; solo (C), cuánto invertir en M, depende de la aversión al riesgo.

**P12. ¿Por qué M tiene pesos tan extremos (560% largo, −460% corto)?**

M arma pares dentro de cada sector: largo KO / corto PEP y PG; largo SO / corto DUK, SRE y NEE; largo XOM / corto SLB, COP y CVX. Como esas acciones están muy correlacionadas, cada par tiene poco riesgo y el optimizador lo apalanca para explotar diferencias de medias históricas (KO 11,6% vs. PEP 0,8%). Pero cada media tiene un error de ~8 puntos, así que la diferencia no es significativa: el optimizador es un "maximizador de errores de estimación" (Michaud, 1989).

**P13. ¿Por qué rf = 4,04% y no 4,08%?**

El H.15 publica rendimientos equivalentes a bono (capitalización semestral). Como los retornos de las acciones son continuos, se convierte con rc = 2 · ln(1 + y/2) = 2 · ln(1,0204) = 4,04%.

**P14. Interpreta α, β y R² del modelo índice de M.**

Se estimó por MCO con datos diarios:

> rM,t − rf = α + β·(rSP500,t − rf) + εt

- **α = 0,00311 diario ≈ 78,5% anual:** retorno por sobre lo que el CAPM predice para su β.
- **β = 0,51:** M se mueve la mitad que el mercado; es un portafolio largo-corto casi neutral.
- **R² = 0,07:** el 93% de su varianza es idiosincrásica (σ de ε = 31% anual).

**P15. ¿Cómo es el test-t de α = 0 y qué concluyen?**

t = α̂ / ee(α̂) = 0,00311 / 0,00055 = 5,64. Como 5,64 &gt; 1,96 (5%) y &gt; 2,58 (1%), formalmente se rechaza α = 0. Con errores robustos (Newey-West) t = 5,48: la conclusión formal no cambia.

**P16. ¿Es el resultado consistente con la eficiencia de mercado? (muy probable)**

Sí. El rechazo no es evidencia de ineficiencia, por cuatro razones:

1. **Sesgo de anticipación:** los pesos usan medias de 2021–2026 que nadie conocía en 2021. La eficiencia dice que no se gana anormalmente con la información disponible en ese momento.
2. **Sobreajuste:** maximizar el Sharpe muestral con 50 pesos maximiza también α/σ(ε); el t-test deja de tener la distribución t de Student.
3. **Fuera de muestra se cae:** M estimado hasta jul-2025 perdió 21,4% el año siguiente (Sharpe −0,46, prometido 2,80).
4. **Hipótesis conjunta (Fama):** un test de α = 0 evalúa a la vez la eficiencia y el CAPM con el S&P 500 como proxy del mercado (crítica de Roll).

**P17. ¿Qué rol juega usar los mismos datos para construir M y evaluarlo?**

Hace que el α sea mecánico. Se cumple SR²M ≈ SR²SP + (α/σε)², es decir 2,54² ≈ 0,39² + 2,51², y t(α) ≈ (α/σε) · √años = 2,53 × √4,98 ≈ 5,6. Lo comprobamos simulando 1.000 muestras con α verdadero = 0: el t promedio fue 7,09 y el 100% "rechazó". Nuestro t = 5,64 es justo lo esperable en un mercado eficiente. Para evaluar bien: datos fuera de muestra, ventanas móviles o corregir por pruebas múltiples.

**P18. Compara Sharpe y Treynor de M y del S&P 500. ¿Por qué el ranking puede diferir?**

> SRp = (E[Rp] − rf) / σp          TRp = (E[Rp] − rf) / βp          SRp = TRp·ρp,M / σM

M gana en ambas (Sharpe 2,54 vs. 0,39; Treynor 161% vs. 6,7%). El ranking puede diferir porque Sharpe usa riesgo total y Treynor solo riesgo sistemático: un portafolio con R² bajo se ve bien en Treynor y mal en Sharpe. Ejemplo nuestro: JNJ tiene Sharpe 0,39 (bajo el índice) pero Treynor 40,6% (seis veces el índice), porque β = 0,17 y R² = 2,6%. Pasa en 12 de las 50 acciones.

**P19. ¿Cuál medida usar?**

Sharpe si el portafolio es toda la inversión riesgosa (importa el riesgo total; es lo que maximiza M). Treynor si es una parte pequeña de un portafolio diversificado (el riesgo idiosincrásico se diversifica). Con β cercano a 0 el Treynor explota y con β &lt; 0 pierde sentido. Relación útil: αp = βp · (TRp − TRM).

**P20. Deriva x\* y calcula la asignación para c = 2, 5 y 10.**

Con U = E[Rc] − (c/2)σ²c y Rc = x·RM + (1 − x)·rf (Sesión I, láminas 24–25):

> máx  rf + x·(E[RM] − rf) − (c/2)·x²·σM²   ⇒   x\* = (E[RM] − rf) / (c·σM²) = (0,859 − 0,0404) / (c·0,1037) = 7,90 / c

| **c** | **x\*** | **Posición en la LMC** |
| --- | --- | --- |
| 2 | 3,95 | Borrowing: pide prestado 295% a rf, a la derecha de M |
| 5 | 1,58 | Borrowing: pide prestado 58% a rf, a la derecha de M |
| 10 | 0,79 | Lending: 79% en M y 21% prestado a rf, entre rf y M |

A mayor c, menor x\*: la curva de indiferencia es más convexa y toca la LMC más cerca de rf. Los tres tienen el mismo portafolio riesgoso (separación). Ojo: el apalancamiento es extremo porque el μ de M (85,9%) es irreal; con el S&P 500 sería 1,15, 0,46 y 0,23.

## 14. Pregunta 2: estructura de tasas

La idea que conecta toda la P2: **el extremo corto de la curva lo fija la Fed y el largo las expectativas de inflación y la prima por plazo; NS lo resume en nivel, pendiente y curvatura, y las inversiones anticiparon bien los recortes pero no siempre las recesiones.**

**P21. Escribe Nelson-Siegel e interpreta sus parámetros.**

> R(t) = β₀ + β₁·(1 − e^(−t/α₁)) / (t/α₁) + β₂·[(1 − e^(−t/α₁)) / (t/α₁) − e^(−t/α₁)]

- **β0 = nivel:** R(∞) = β0, la tasa de muy largo plazo.
- **β1 = pendiente:** R(0) = β0 + β1, así que β1 = tasa corta − tasa larga. β1 &lt; 0 es curva normal; β1 &gt; 0, invertida.
- **β2 = curvatura:** β2 &gt; 0 es una joroba y β2 &lt; 0 un valle.
- **α1 = ubicación de la joroba:** su máximo está en t ≈ 1,8 · α1 años.

Svensson agrega β3 · [(1 − e^(−t/α2))/(t/α2) − e^(−t/α2)]: una segunda joroba con su propio α2.

**P22. ¿Qué significa la convención días transados / días transados?**

Que el plazo se mide como fracción de año en días hábiles: 1 mes = 1/12, 6 meses = 0,5 y 10 años = 10, sin ajustes de calendario. Usamos las 11 series del H.15 (1M a 30A) el último día transado de junio de cada año.

**P23. ¿Cómo aseguraron el óptimo global? (muy probable)**

La función objetivo no es convexa en α y tiene varios mínimos locales, así que un optimizador local depende del punto de partida. El procedimiento:

1. **β concentrados:** dado α, el modelo es lineal en los β y se resuelven exacto por mínimos cuadrados. El problema queda en 1 dimensión (NS) o 2 (Svensson).
2. **Grilla exhaustiva:** 800 valores de α1 (NS) y 130 × 170 pares (α1, α2) (Svensson).
3. **Refinamiento local** (Nelder-Mead) desde los 5 mejores puntos.
4. **Verificación:** 300 (NS) y 200 (Svensson) optimizaciones desde puntos aleatorios; ninguna encontró un error menor. Solo el 75% (NS) y el 21% (Svensson) llegaron al óptimo, y en el peor caso el 9% y el 6,5%.

**P24. ¿Por qué impusieron β0 ≥ 0, β0 + β1 ≥ 0 y α acotado?**

Sin restricciones, el "óptimo" de 2022 tiene α1 = 0,05 y R(0) = 4,7% cuando la tasa a 1 mes era 1,28%, y el de 2026 tiene α1 = 30 y β0 = 1,1% cuando la tasa a 30 años era 4,91%. Esas soluciones mejoran solo 0,2 a 1 pb pero los parámetros pierden sentido económico: la función objetivo es muy plana en α (problema de identificación).

**P25. ¿Por qué Svensson siempre ajusta mejor y dónde mejora?**

NS es un caso particular de Svensson (β3 = 0), así que con más parámetros el error *in-sample* nunca sube: el RMSE baja entre 20% y 66%. Aun penalizando los parámetros extra (BIC), Svensson gana en las 10 fechas, aunque en 2022 por muy poco. Mejora en dos zonas:

- **Extremo corto (1 a 6 meses)** en 2017, 2018, 2020, 2025 y 2026: curvatura rápida que NS no sigue con un solo α.
- **Tramo de 20 años desde 2021:** el bono a 20 años rinde más que el de 30 (3,38% vs. 3,14% en 2022) porque desde su reintroducción en 2020 tiene menos demanda y liquidez. Es un efecto de liquidez, no de expectativas.

La peor fecha es 2022 (NS 10,6 pb): la curva subía fuerte hasta 1 año, era plana después y estaba a días de invertirse.

**P26. ¿Cómo evolucionaron β0, β1 y β2?**

- **β0:** cerca de 3% en 2017–2019, mínimo de 1,94% en 2020 (pandemia y QE) y sube hasta 5,32% en 2026, el máximo: más inflación esperada, tasas reales altas y más prima por plazo (déficit, emisión, rebajas de calificación).
- **β1:** negativo (curva normal) salvo en 2023 (+1,32) y 2024 (+0,88), los años invertidos; el más negativo es 2021 (−2,33).
- **β2:** casi 0 en 2017–2018 (curvas monótonas), muy negativo en 2019–2022 y en 2025 (−3,83, la "bañera"), y +3,61 en 2023 (joroba en 6 meses en el peak de las alzas).
- **R(0) = β0 + β1** replica la tasa de fondos federales: el extremo corto lo ancla la Fed.

**P27. Explica la evolución de la curva 2017–2026 (punto principal, 60%).**

| **Junio** | **Forma de la curva (10A − 3M)** | **Qué pasaba** |
| --- | --- | --- |
| 2017 | Normal, aplanándose (+128 pb) | La Fed sube gradualmente e inicia la reducción del balance; inflación bajo 2% |
| 2018 | Muy plana (10A − 2A = +33 pb) | Cuatro alzas hasta 2,25–2,50%, estímulo fiscal, guerra comercial con China |
| 2019 | En U, invertida en el tramo medio (−12 pb) | Escalada arancelaria, desaceleración global; la Fed recorta tres veces |
| 2020 | En cero hasta 3 años, empinada después (+50 pb) | COVID: tasa 0–0,25%, QE ilimitado, recesión de feb–abr |
| 2021 | La más empinada (+140 pb) | Reapertura, estímulo de US$1,9 billones, inflación cerca de 5% "transitoria" |
| 2022 | Sube fuerte hasta 1 año, plana después (+126 pb; 10A − 2A = +6 pb) | Ucrania, inflación 9,1%, alza de 75 pb y QT; se invierte seis días después |
| 2023 | Máxima inversión (−162 pb) | Fed en 5,25–5,50%, quiebra de SVB, techo de deuda |
| 2024 | Invertida con valle en 5 años (−112 pb) | Desinflación; recortes desde septiembre |
| 2025 | "Bañera": corto invertido, largo empinado (−17 pb) | Aranceles de abril, rebaja de Moody's, más déficit; tres recortes en sep–dic |
| 2026 | Normal y creciente, nivel más alto (+57 pb) | Guerra con Irán y petróleo, IPC 4,2% en mayo, Warsh asume; la Fed sube el 16-sep |

**P28. ¿Cuándo estuvo invertida, qué anticipaba y ocurrió?**

Una inversión implica que el mercado espera tasas cortas futuras más bajas, lo típico antes de recortes por una desaceleración. Históricamente precedió a las recesiones con 6 a 24 meses de anticipación (Estrella y Mishkin, 1998).

| **Episodio (10A − 3M)** | **Anticipaba** | **¿Ocurrió?** |
| --- | --- | --- |
| May–oct 2019 (mínimo −52 pb) | Recortes y recesión por la guerra comercial | Recortes sí; recesión sí en 2020, pero por la pandemia |
| Ene–mar 2020 (−20 pb) | Huida a la calidad y recortes de emergencia | Sí: tasa a cero y recesión |
| Oct-2022 a dic-2024 (−189 pb; 10A − 2A invertida 26 meses) | Recesión por las alzas y recortes posteriores | Recortes sí (175 pb); recesión no, al menos hasta oct-2026 |
| Feb–sep 2025 (−27 pb) | Recortes por el golpe de los aranceles | Recortes sí (75 pb); recesión no |

**P29. ¿Por qué falló la señal de 2022–2024?**

1. La inversión reflejaba sobre todo la **baja esperada de la inflación** (tasas nominales más bajas), no necesariamente una recesión.
2. La **prima por plazo** estaba deprimida por años de QE, lo que aplanaba la curva.
3. Hogares y empresas habían **fijado tasas bajas** en 2020–2021, así que las alzas se transmitieron con menos fuerza.
4. **Déficit fiscal** de ~6% del PIB, ahorro de la pandemia, inmigración e inversión en IA sostuvieron el crecimiento.

**P30. ¿Qué dice la curva de 2026?**

Es positiva pero por un "empinamiento bajista": las tasas largas suben más que las cortas por el shock petrolero, la inflación sobre 4%, la vuelta de las alzas y el riesgo fiscal. El tramo corto (3,70% a 1 mes → 4,01% a 6 meses) ya descontaba alzas. La señal es de riesgo inflacionario y fiscal, no de recesión inminente.

## 15. Ejercicios numéricos de práctica

Si el control trae un cálculo, será corto y con calculadora: estos ocho cubren las fórmulas de la tarea. Inténtalos antes de mirar la solución.

**E1. Anualización.** Una acción tiene retorno diario promedio de 0,05% y desviación estándar diaria de 1,2%. ¿Cuáles son su μ y σ anuales?

*Solución:* μ = 252 × 0,05% = 12,6%. σ = √252 × 1,2% = 15,87 × 1,2% = 19,0%. La volatilidad escala con la raíz del tiempo porque la varianza escala lineal.

**E2. Mínima varianza con dos activos.** σA = 20%, σB = 30%, ρ = 0,2. Encuentra los pesos y la volatilidad del GMV.

*Solución:* Cov = 0,2 × 0,20 × 0,30 = 0,012. wA = (σ²B − Cov)/(σ²A + σ²B − 2Cov) = (0,09 − 0,012)/(0,04 + 0,09 − 0,024) = 0,078/0,106 = 0,736 y wB = 0,264. σ²p = 0,736² × 0,04 + 0,264² × 0,09 + 2 × 0,736 × 0,264 × 0,012 = 0,0326, así que σp = 18,1%: menos que el activo menos riesgoso. Con ρ = 0 (frontera ingenua) se usaría Cov = 0.

**E3. Asignación óptima.** E[RM] = 12%, rf = 4%, σM = 20%. Calcula x\* para c = 4 y c = 1, con su retorno y riesgo.

*Solución:* x\* = 0,08/(c × 0,04) = 2/c. Con c = 4: x\* = 0,5 (lending: 50% en M y 50% prestado a rf), E[Rc] = 4% + 0,5 × 8% = 8% y σc = 0,5 × 20% = 10%. Con c = 1: x\* = 2 (borrowing: pide prestado 100% del patrimonio), E[Rc] = 4% + 2 × 8% = 20% y σc = 40%.

**E4. Sharpe, Treynor y Jensen con ranking invertido.** Mercado: E[RM] = 10%, σM = 16%; rf = 4%. Portafolio Q: E[RQ] = 9%, σQ = 20%, βQ = 0,4.

*Solución:* SRM = 6%/16% = 0,375 y TRM = 6%. SRQ = 5%/20% = 0,25 (peor que el mercado) pero TRQ = 5%/0,4 = 12,5% (mejor). αQ = 9% − (4% + 0,4 × 6%) = 2,6% = β × (TRQ − TRM) = 0,4 × 6,5%. Q tiene mucho riesgo idiosincrásico: es buena como parte de un portafolio diversificado, mala como inversión única.

**E5. Test-t del alfa.** En el modelo índice diario, α̂ = 0,00311 con error estándar 0,00055. ¿Se rechaza α = 0? ¿Y si el error fuera 0,002?

*Solución:* t = 0,00311/0,00055 = 5,65 &gt; 1,96: se rechaza al 5%. El alfa anual es ≈ 0,00311 × 252 = 78%. Con error 0,002, t = 1,56 &lt; 1,96: no se rechaza. Recuerda: con datos reutilizados el rechazo no prueba ineficiencia (P16).

**E6. Nelson-Siegel.** β0 = 5%, β1 = −2%, β2 = 1%, α1 = 2. Calcula R(0), R(∞), R(2) y R(10).

*Solución:* R(0) = β0 + β1 = 3% y R(∞) = β0 = 5%: curva normal (β1 &lt; 0). Para t = 2: t/α1 = 1, carga 1 = (1 − e⁻¹)/1 = 0,632 y carga 2 = 0,632 − 0,368 = 0,264, así que R(2) = 5 − 2 × 0,632 + 1 × 0,264 = 4,00%. Para t = 10: t/α1 = 5, carga 1 = (1 − e⁻⁵)/5 = 0,199 y carga 2 = 0,192, así que R(10) = 5 − 0,397 + 0,192 = 4,79%.

**E7. Conversión de la tasa libre de riesgo.** El H.15 publica y = 4,08% (base equivalente a bono, semestral). ¿Cuál es la tasa continua?

*Solución:* rc = 2 × ln(1 + 0,0408/2) = 2 × ln(1,0204) = 4,04%. Con capitalización anual sería ln(1,0408) = 4,00%.

**E8. Un punto en la LMC.** Con rf = 4,04% y Sharpe de M = 2,54, ¿qué retorno esperado tiene un portafolio de la LMC con σ = 10%? ¿Cuánto tiene en M?

*Solución:* E[R] = 4,04% + 2,54 × 10% = 29,4%. Como σ = x × σM, x = 10%/32,2% = 0,31: 31% en M y 69% prestado a rf (lending).

## 16. Comentes tipo control

En un comente el puntaje está en la justificación: parte con Verdadero, Falso o Incierto, da el mecanismo y cierra con un dato de la tarea.

**C1. "Si agrego suficientes acciones a mi portafolio, su riesgo tiende a cero."** Falso. Solo el riesgo idiosincrásico desaparece; el riesgo converge a la covarianza promedio (riesgo sistemático). Nuestro 1/N tiene σ = 13,9%, y sería 4,2% si no hubiera covarianzas.

**C2. "Ignorar las covarianzas siempre hace que un portafolio parezca menos riesgoso."** Incierto. En portafolios largos sí: el GMV ingenuo cree tener 3,5% y tiene 12,4%. En portafolios largo-corto es al revés: la covarianza positiva entre el largo y el corto reduce el riesgo, y quien la ignora lo sobreestima (por eso las fronteras se cruzan).

**C3. "Una restricción de venta corta nunca puede mejorar el desempeño."** Incierto. *In-sample* nunca mejora: la frontera restringida es una mini-frontera dentro de la original. Fuera de muestra sí puede, porque evita apostar a errores de estimación: nuestra tangencia sin venta corta ganó 33,1% y la libre perdió 21,4%.

**C4. "Un alfa de Jensen positivo y significativo demuestra que el mercado es ineficiente."** Falso. Es una prueba de hipótesis conjunta: puede fallar el CAPM o el proxy del mercado (Roll). Además, si el portafolio se construyó con los mismos datos, el alfa es mecánico: con α verdadero = 0 nuestra simulación dio t promedio de 7,09.

**C5. "Si un portafolio tiene mayor Sharpe que otro, también tendrá mayor Treynor."** Falso. Sharpe mide riesgo total y Treynor solo sistemático. JNJ tiene menor Sharpe que el S&P 500 (0,39 vs. 0,392) pero seis veces su Treynor, porque β = 0,17 y R² = 2,6%.

**C6. "Un inversionista muy averso al riesgo no invertirá en el portafolio de tangencia."** Falso. Por separación, todos tienen el mismo portafolio riesgoso M; la aversión solo cambia cuánto. Con c = 10 invierte 79% en M y presta 21% a rf.

**C7. "Svensson es mejor que Nelson-Siegel porque siempre tiene menor RMSE."** Incierto. *In-sample* siempre lo tiene porque NS está anidado en Svensson. Con dos parámetros más sobre solo 11 plazos puede sobreajustar: en 2022 el BIC casi no lo distingue de NS. Su ventaja real está en el extremo corto y en el tramo de 20 años.

**C8. "Si el optimizador converge a un mínimo, encontré los parámetros óptimos."** Falso. La función de NS no es convexa en α: en 2026 solo el 9% de los inicios aleatorios llegó al óptimo global. Hay que usar grilla, múltiples puntos iniciales o β concentrados.

**C9. "Una curva con pendiente positiva implica que el mercado espera alzas de tasas."** Falso. La pendiente también incluye la prima por plazo o liquidez que se exige por mantener bonos largos. En junio de 2020 la curva era positiva (0,13% a 1 mes, 1,41% a 30 años) aunque la Fed prometía tasas en cero por años.

**C10. "Una curva invertida siempre anticipa una recesión."** Falso. Anticipa tasas cortas más bajas. La inversión de 2022–2024, la más larga en 40 años, fue seguida de 175 pb de recortes pero no de una recesión, al menos hasta octubre de 2026.

## 17. Errores frecuentes y checklist para el día del control

La mayoría de los puntos se pierden por respuestas sin mecanismo o sin un número propio, no por cálculos. Antes de entregar cada respuesta, revisa:

- ☐ ¿Dije el mecanismo (el *por qué*), no solo el resultado?
- ☐ ¿Agregué un dato de nuestra tarea (GMV 10,8%, Sharpe 2,54, t = 5,64, β0 = 5,32%)?
- ☐ ¿Distinguí *in-sample* de fuera de muestra al hablar de M, del alfa o de las restricciones?
- ☐ ¿Usé σ²M (varianza) y no σM en x\*, y c como en la clase (U = E − (c/2)σ²)?
- ☐ ¿Dije "mini-frontera dentro de la original" al hablar de restricciones?
- ☐ ¿Recordé que β1 = tasa corta − tasa larga, de modo que β1 &gt; 0 significa curva invertida?
- ☐ ¿Separé lo que anticipó cada inversión (recortes) de si hubo recesión?

**Confusiones típicas:** LMC (eje σ, solo portafolios eficientes) vs. línea del CAPM (eje β, todos los activos); varianza vs. desviación estándar; rendimientos del H.15 (equivalentes a bono, plazo constante) vs. tasas cero; y llamar "ineficiencia" a un alfa calculado con los mismos datos que construyeron el portafolio.
