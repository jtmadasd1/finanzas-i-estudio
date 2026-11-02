# =============================================================================
#  06_informe_extendido.py
#  Version EXTENDIDA del informe (todas las figuras, robusteces y analisis
#  adicionales).  No es la que se entrega: sirve como material de estudio para
#  el control.  Se guarda en resultados/Informe_extendido_referencia.docx.
# =============================================================================
from informe_utils import *  # noqa: F401,F403  (datos, formatos y funciones de escritura)

# =============================================================================
# PORTADA
# =============================================================================
for _ in range(5):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("UNIVERSIDAD DE CHILE · FACULTAD DE ECONOMÍA Y NEGOCIOS"); r.font.size = Pt(10); r.bold = True
r.font.color.rgb = RGBColor(0xB0, 0x8D, 0x1A)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Finanzas I – ENFIN415"); r.font.size = Pt(13); r.font.color.rgb = AZUL
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Informe de Tarea"); r.font.size = Pt(28); r.bold = True; r.font.color.rgb = AZUL
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Frontera media-varianza, Línea de Mercado de Capitales y desempeño,\n"
              "y modelos de estructura de tasas (Nelson-Siegel y Svensson)")
r.font.size = Pt(13); r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
for _ in range(4):
    doc.add_paragraph()
for linea in ["Profesor: Alejandro Bernales",
              "Integrantes: ______________________________  y  ______________________________",
              "Fecha de entrega: 21 de octubre de 2026"]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(linea); r.font.size = Pt(11.5)
for _ in range(6):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Todos los cálculos se encuentran en los archivos de código adjuntos (Python), "
              "junto con los datos descargados y planillas Excel con los resultados.")
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
SALTO()

# =============================================================================
# RESUMEN EJECUTIVO
# =============================================================================
H("Resumen ejecutivo", 1)
P(f"Se trabajó con **50 acciones del S&P 500 de los 11 sectores GICS** (al menos dos de Energy, Financials, "
  f"Health Care, Industrials, Information Technology y Utilities) y con **5 años de precios diarios** "
  f"(retornos del {corr['inicio']} al {corr['fin']}, {miles(corr['T_dias'])} observaciones). Los principales hallazgos son:")
BUL([
    f"**Frontera media-varianza (P1A.2).** El portafolio de mínima varianza global tiene σ = {pc(gl['sigma'])} y "
    f"μ = {pc(gl['mu'])}, menos riesgo que la acción menos volátil (KO, {pc(est.loc['KO', 'Volatilidad anual'])}) "
    f"y que el S&P 500 ({pc(s_sp)}). Con el mismo riesgo del S&P 500, la frontera promete un retorno de "
    f"{pc(mu_frontera_en_sp)} versus {pc(B['sp500']['mu'])} del índice: el valor de la diversificación *in-sample*.",
    f"**Covarianzas (P1A.3).** La correlación promedio es {nu(corr['corr_promedio'])} ({nu(corr['corr_mismo_sector'])} "
    f"dentro de un mismo sector). Ignorarlas produce una ilusión de diversificación: el portafolio de mínima varianza "
    f"\"ingenuo\" cree tener σ = {pc(gi['sigma_percibida'])}, pero su volatilidad real es {pc(gi['sigma_real'])}.",
    f"**Restricciones (P1A.4–6).** Toda restricción genera una \"mini-frontera\" dentro de la original. El límite |wᵢ| ≤ 10% "
    f"casi no afecta la zona de mínima varianza pero acota el retorno máximo ({pc(fr['limite']['rango'][1])}); "
    f"prohibir ventas cortas cuesta mucho para retornos altos (la frontera termina en 100% NVDA) y deja solo "
    f"{fr['sin_vc']['n_acciones_min']} a {fr['sin_vc']['n_acciones_max']} acciones "
    f"en cada portafolio eficiente; exigir ≥ 40% en Energy + Industrials cuesta poco en la zona intermedia "
    f"y mucho en los extremos.",
    f"**Portafolio de tangencia (P1B.1).** Con rf = {pc(rf, 2)} (Tesoro a 1 año al 31-jul-2026, continua), M tiene "
    f"μ = {pc(M['mu'])}, σ = {pc(M['sigma'])} y Sharpe = {nu(M['sharpe'])}, pero exige una exposición bruta de "
    f"{nu(M['exp_bruta'], 1)} veces el patrimonio, con pares largo-corto dentro de cada sector: es un "
    f"\"maximizador de errores de estimación\".",
    f"**Alfa de Jensen (P1B.2).** α = {pc(mi['alfa_anual'])} anual, β = {nu(mi['beta'])}, t(α) = {nu(mi['t_alfa'])}. "
    f"Sin embargo, una simulación de Monte Carlo con α verdadero = 0 produce t(α) promedio de {nu(sim['t_alfa_media'])}: "
    f"el alfa es un artefacto de usar los mismos datos para construir y evaluar M, no evidencia contra la eficiencia. "
    f"Fuera de muestra, M estimado hasta jul-2025 perdió {pc(-fm['M (sin restricciones)']['retorno_acumulado'])} en el año siguiente.",
    f"**Sharpe y Treynor (P1B.3).** M supera al S&P 500 en ambas medidas, pero {n_inv_rank} de las 50 acciones "
    f"(p. ej. JNJ y LMT) invierten el ranking: bajo β y mucho riesgo idiosincrásico.",
    f"**Asignación óptima (P1B.4).** x* = {nu(asig.loc[0, 'x* (en M)'])} (c = 2, pide prestado), "
    f"{nu(asig.loc[1, 'x* (en M)'])} (c = 5, pide prestado) y {nu(asig.loc[2, 'x* (en M)'])} (c = 10, presta).",
    f"**Nelson-Siegel y Svensson (P2).** Óptimo global verificado con cientos de puntos iniciales aleatorios. "
    f"RMSE de NS entre {pb(par['RMSE NS (pb)'].min(), 1)} y {pb(par['RMSE NS (pb)'].max(), 1)} pb; Svensson lo reduce "
    f"entre {pb(par['Mejora RMSE (%)'].min())}% y {pb(par['Mejora RMSE (%)'].max())}%, sobre todo en el extremo corto (1–6 meses) "
    f"y en el tramo de 20 años desde 2021.",
    "**Curva 2017–2026.** Normalización (2017–18) → inversión (2019) → tasas cero por COVID (2020–21) → shock inflacionario "
    "y alzas récord (2022) → inversión más larga y profunda en 40 años (2022–24) → aranceles y \"bañera\" (2025) → "
    "curva positiva con tasas largas al alza por la guerra con Irán, inflación sobre 4% y nueva alza de la Fed (2026). "
    "Las inversiones anticiparon correctamente recortes de la Fed; la recesión solo llegó en 2020 (por la pandemia) y "
    "la inversión de 2022–24 no ha sido seguida, al menos hasta octubre de 2026, por una recesión.",
])
SALTO()

# =============================================================================
# 1. DATOS Y METODOLOGIA
# =============================================================================
H("1. Datos y metodología general", 1)
H("1.1 Acciones, índice y ventana de estimación", 2)
cuenta = est["Sector"].value_counts()
P("**Fuente.** Precios diarios de cierre desde Yahoo Finance (descargados con el paquete *yfinance* de Python) "
  "para las 50 acciones y para el índice S&P 500 (^GSPC). Se usa el **cierre ajustado** por *splits* y dividendos: "
  "en la ventana hubo varios *splits* (NVDA 10:1 y AVGO 10:1 en 2024, AMZN 20:1 y GOOGL 20:1 en 2022, TSLA 3:1 en 2022, "
  "WMT 3:1 en 2024, NFLX 10:1 en 2025) que con el cierre sin ajustar aparecerían como caídas ficticias de 67% a 95% en un día.")
P("**Selección.** " + ", ".join(f"{s} ({n})" for s, n in cuenta.items()) +
  ". Se eligieron empresas grandes y líquidas que pertenecieron al índice durante toda la ventana (series completas, sin "
  "datos faltantes). Se incluyen los cinco sectores no exigidos para que el universo se parezca más al mercado completo.")
P(f"**Ventana: 5 años** ({corr['inicio']} a {corr['fin']}; {miles(corr['T_dias'])} retornos diarios), el máximo permitido. " +
  "La razón es estadística: con 50 acciones hay que estimar 50 medias, 50 varianzas y 1.225 covarianzas. Con un año "
  "(≈252 datos) la matriz Ω sería muy imprecisa y casi singular (N/T ≈ 0,20); con cinco años N/T ≈ 0,04. Aun así, "
  "como se verá, las **medias** siguen siendo muy imprecisas.")
P("**Retornos y anualización.** Siguiendo la clase (Sesión I, lámina 10) se usan retornos con capitalización continua "
  "rₜ = ln(Pₜ/Pₜ₋₁). Bajo independencia en el tiempo, la media y la varianza crecen linealmente con el horizonte, "
  "por lo que se anualiza con 252 días transados:")
EQ("μ_anual = 252 · μ_diaria ;   Ω_anual = 252 · Ω_diaria ;   σ_anual = √252 · σ_diaria")
P(f"**Tasa libre de riesgo.** Serie *Treasury constant maturities* del H.15 de la Reserva Federal, plazo 1 año, al "
  f"31-jul-2026: {pc(B['y1_publicada'], 2)} (rendimiento \"equivalente a bono\", capitalización semestral). Para ser "
  f"coherentes con retornos continuos se convierte a rf = 2·ln(1 + y/2) = **{pc(rf, 3)}**.")
P("**Software.** Todos los cálculos se hicieron en Python (el enunciado permite cualquier lenguaje): numpy, pandas, cvxpy con el solver Clarabel para los problemas cuadráticos con restricciones, "
  "statsmodels para las regresiones y scipy para Nelson-Siegel/Svensson). La frontera sin restricciones se calculó con la "
  f"fórmula analítica de clase y se verificó con el optimizador numérico: la diferencia máxima fue {A['chequeo_analitico_vs_qp']:.0e}.")

# =============================================================================
# PREGUNTA 1A
# =============================================================================
SALTO()
H("2. Pregunta 1A: Frontera media-varianza", 1)
H("2.1 (P1A.1) Retornos esperados, volatilidades y covarianzas anuales", 2)
P(f"La Tabla del Anexo A reporta μ, σ y β de cada acción; la matriz de covarianzas anual completa (50×50) está en "
  f"*Resultados_Pregunta1A.xlsx*. Los retornos esperados (medias históricas anualizadas) van desde "
  f"{pc(est['Retorno esperado anual'].min())} (AMT) hasta {pc(est['Retorno esperado anual'].max())} (NVDA) y las "
  f"volatilidades desde {pc(est['Volatilidad anual'].min())} (KO) hasta {pc(est['Volatilidad anual'].max())} (TSLA). "
  f"En la misma ventana el S&P 500 rindió {pc(B['sp500']['mu'])} con σ = {pc(s_sp)}: casi todas las acciones son más "
  f"volátiles que el índice, primera señal del beneficio de diversificar.")
top = est.sort_values("Retorno esperado anual", ascending=False)
P("Los mayores retornos se concentran en la temática de inteligencia artificial (NVDA "
  f"{pc(est.loc['NVDA', 'Retorno esperado anual'])}, AVGO {pc(est.loc['AVGO', 'Retorno esperado anual'])}), en LLY "
  f"({pc(est.loc['LLY', 'Retorno esperado anual'])}, medicamentos contra la obesidad) y en CAT "
  f"({pc(est.loc['CAT', 'Retorno esperado anual'])}). Los menores, en sectores sensibles a tasas (AMT, PLD, utilities) "
  "y en farmacéuticas que perdieron ingresos post-COVID (PFE). Utilities y consumo básico tienen las menores volatilidades.")
P(f"**Advertencia clave: las medias se estiman con mucho error.** El error estándar de la media anual es σ/√(años) ≈ "
  f"σ/√5. Para NVDA es {pc(est.loc['NVDA', 'Error est. de la media'])}, de modo que un intervalo de 95% para su retorno esperado "
  f"va aproximadamente de {pc(est.loc['NVDA', 'Retorno esperado anual'] - 1.96 * est.loc['NVDA', 'Error est. de la media'], 0)} "
  f"a {pc(est.loc['NVDA', 'Retorno esperado anual'] + 1.96 * est.loc['NVDA', 'Error est. de la media'], 0)}; incluso para KO "
  f"el error es {pc(est.loc['KO', 'Error est. de la media'])}. En cambio, varianzas y covarianzas se estiman con mucha más "
  "precisión porque dependen de la frecuencia de los datos y no solo del largo de la ventana. Esta asimetría explicará "
  "buena parte de los resultados de las preguntas siguientes.")
FIG("F01_correlaciones.png", 13.5,
    "Matriz de correlaciones de los retornos diarios, ordenada por sector. Se observan bloques de alta correlación "
    "dentro de Energy, Utilities, Financials y Consumer Staples.")
P(f"La correlación promedio entre pares es **{nu(corr['corr_promedio'])}**: {nu(corr['corr_mismo_sector'])} dentro de un "
  f"mismo sector y {nu(corr['corr_distinto_sector'])} entre sectores. El par más correlacionado es "
  f"{corr['par_corr_max'][0]}–{corr['par_corr_max'][1]} ({nu(corr['corr_max'])}) y el menos, "
  f"{corr['par_corr_min'][0]}–{corr['par_corr_min'][1]} ({nu(corr['corr_min'])}); solo {pc(corr['pct_corr_negativas'])} "
  f"de los 1.225 pares tiene correlación negativa. Para un portafolio 1/N, el {pc(corr['share_var_cov_1N'], 0)} de su "
  f"varianza proviene de las covarianzas: su volatilidad es {pc(corr['sigma_1N'])}, mientras que si las acciones no "
  f"estuvieran correlacionadas sería {pc(corr['sigma_1N_sin_cov'])}. Es exactamente el resultado de clase: cuando N crece, "
  "el riesgo converge a la covarianza promedio (riesgo sistemático o no diversificable).")

H("2.2 (P1A.2) Frontera media-varianza con 50 acciones", 2)
P("Siguiendo la clase (Sesión I, lámina 17), para cada retorno objetivo μ̄ se resuelve el problema de mínima varianza "
  "con ventas cortas permitidas:")
EQ("min_w  σ²ₚ = w′Ωw     s.a.   w′μ = μ̄ ,   w′1 = 1")
P("Con el Lagrangiano se obtiene la solución cerrada w* = Ω⁻¹(λ₁·1 + λ₂·μ). Definiendo A = 1′Ω⁻¹1, B = 1′Ω⁻¹μ, "
  "C = μ′Ω⁻¹μ y D = AC − B², la frontera es la hipérbola:")
EQ("σ²(μ̄) = (A·μ̄² − 2B·μ̄ + C) / D ,   con   μ_GMV = B/A  y  σ_GMV = 1/√A")
P(f"Con nuestros datos A = {nu(Fa)}, B = {nu(Fb)}, C = {nu(A['C'])} y D = {nu(Fd)}. El portafolio de **mínima varianza "
  f"global (GMV)** tiene μ = {pc(gl['mu'])} y σ = {pc(gl['sigma'])}.")
FIG("F02_frontera_mv.png", 14.5,
    "Frontera media-varianza con ventas cortas. La rama superior al GMV (línea continua) es la frontera eficiente; la "
    "rama inferior (discontinua) es ineficiente.")
P("**Discusión.**")
BUL([
    f"**La frontera queda muy a la izquierda de todas las acciones.** El GMV tiene menos riesgo que la acción menos volátil "
    f"(KO, {pc(est.loc['KO', 'Volatilidad anual'])}) y que el propio S&P 500 ({pc(s_sp)}). Con el mismo riesgo del índice "
    f"(σ = {pc(s_sp)}) la frontera promete μ = {pc(mu_frontera_en_sp)} frente a {pc(B['sp500']['mu'])} del S&P 500. "
    "Es el beneficio de la diversificación de Markowitz, pero medido *in-sample*: usa medias que ya conocemos ex post.",
    f"**El GMV usa las 50 acciones y vende corto.** Sus mayores pesos son DUK ({pc(gmvw.loc['DUK', 'GMV sin restricciones'])}), "
    f"JNJ ({pc(gmvw.loc['JNJ', 'GMV sin restricciones'])}), XOM ({pc(gmvw.loc['XOM', 'GMV sin restricciones'])}), MCD y KO: "
    f"acciones de baja volatilidad y baja correlación con el resto. Tiene {pc(-gl['suma_cortos'])} en posiciones cortas "
    f"(p. ej. COP {pc(gmvw.loc['COP', 'GMV sin restricciones'])}, PLD {pc(gmvw.loc['PLD', 'GMV sin restricciones'])}), "
    "que se usan para cubrir el riesgo de acciones muy correlacionadas que sí se mantienen largas (XOM vs. COP).",
    f"**Los retornos altos requieren apalancamiento.** Para μ̄ = 20%, 30% y 50% la exposición bruta (Σ|wᵢ|) es "
    f"{nu(ing.loc[1, 'exposicion_bruta_completa'], 1)}, {nu(ing.loc[2, 'exposicion_bruta_completa'], 1)} y "
    f"{nu(ing.loc[3, 'exposicion_bruta_completa'], 1)} veces el patrimonio. La rama eficiente no tiene techo porque "
    "las ventas cortas ilimitadas permiten escalar indefinidamente las apuestas largo-corto (supuesto 5 de la Sesión I).",
    "**Por qué la frontera es una hipérbola y no una recta:** al combinar activos imperfectamente correlacionados la "
    "volatilidad del portafolio crece menos que proporcionalmente; solo la combinación con el activo libre de riesgo "
    "(LMC, P1B) es lineal en el plano σ–μ.",
])

H("2.3 (P1A.3) Frontera \"ingenua\" (σᵢⱼ = 0) y el rol de las covarianzas", 2)
P("La frontera ingenua resuelve el mismo problema reemplazando Ω por su diagonal Ω_D = diag(σ²₁,…,σ²₅₀), es decir, "
  "suponiendo que todas las covarianzas son cero. Con Ω_D los pesos tienen la forma wᵢ ∝ (λ₁ + λ₂μᵢ)/σᵢ²: cada acción "
  "se pondera solo por su propio retorno y varianza. Luego se calcula la volatilidad **real** de esos pesos con la Ω completa, "
  "σ_real = √(w′Ωw), y también la volatilidad **percibida** por quien ignora las covarianzas, √(w′Ω_D w).")
FIG("F03_frontera_ingenua.png", 14.5,
    "Frontera con Ω completa (azul), frontera ingenua evaluada con su volatilidad real (rojo) y volatilidad percibida "
    "por quien ignora las covarianzas (naranjo).")
ing_tab = pd.DataFrame({
    "μ̄ objetivo": ing["mu_objetivo"],
    "σ frontera completa": ing["sigma_frontera_completa"],
    "σ ingenua real": ing["sigma_ingenua_real"],
    "σ ingenua percibida": ing["sigma_ingenua_percibida"],
    "Costo de ignorar Ω (pp)": 100 * (ing["sigma_ingenua_real"] - ing["sigma_frontera_completa"]),
}).set_index("μ̄ objetivo")
ing_tab.index = [f"{pc(m)}" + (" (GMV)" if k == 0 else "") for k, m in enumerate(ing["mu_objetivo"])]
ing_tab.index.name = "μ̄ objetivo"
TAB(ing_tab, "Volatilidad anual para un mismo retorno objetivo: frontera completa vs. frontera ingenua",
    fmt={"σ frontera completa": pc, "σ ingenua real": pc, "σ ingenua percibida": pc,
         "Costo de ignorar Ω (pp)": lambda v: pb(v, 1)})
P("**¿Qué rol juegan las covarianzas en la diversificación?**")
BUL([
    f"**Determinan cuánto riesgo se puede eliminar.** Con 1/N y σᵢⱼ = 0 el riesgo tendería a cero (Sesión I, lámina 15). "
    f"Pero las correlaciones son mayoritariamente positivas, así que el riesgo converge a un piso sistemático. Quien "
    f"ignora las covarianzas sufre una **ilusión de diversificación**: su GMV ingenuo cree tener σ = {pc(gi['sigma_percibida'])}, "
    f"pero en realidad tiene {pc(gi['sigma_real'])}, unas {nu(gi['sigma_real'] / gi['sigma_percibida'], 1)} veces más. "
    "Subestimar así el riesgo lleva a apalancarse de más.",
    f"**Ignorarlas produce portafolios ineficientes.** La curva roja está siempre a la derecha de la azul: para el mismo "
    f"μ̄, el portafolio ingenuo tiene entre {pb(ing_tab['Costo de ignorar Ω (pp)'].min(), 1)} y "
    f"{pb(ing_tab['Costo de ignorar Ω (pp)'].max(), 1)} puntos porcentuales más de volatilidad. Esto es así por "
    "construcción: la frontera completa minimiza la varianza verdadera, y cualquier otro vector de pesos (como el ingenuo) "
    "tiene igual o más varianza.",
    "**Las covarianzas permiten cubrir riesgos.** El optimizador con Ω completa aprovecha que COP y EOG (ρ = "
    f"{nu(corr['corr_max'])}), o KO y PEP, se mueven juntas: una posición larga en una y corta en otra cancela el factor "
    "común y deja poco riesgo. Por eso, para μ̄ altos (portafolios largo-corto apalancados) la curva naranja *cruza* a la "
    "azul: en posiciones cubiertas las covarianzas positivas *reducen* el riesgo, y quien las ignora lo sobreestima. "
    "Las covarianzas actúan en ambas direcciones: penalizan la concentración en activos parecidos y premian las coberturas.",
    "**Lo que importa no es el número de activos sino cómo se correlacionan.** La matriz Ω⁻¹ de la solución de clase "
    "(Sesión I, lámina 27) muestra que no basta con dividir por la varianza de cada activo: la covarianza con el resto "
    "determina el aporte marginal de cada acción al riesgo del portafolio. Esta es la misma lógica del CAPM: solo se paga "
    "por el riesgo que no se diversifica (la covarianza con el mercado).",
])

H("2.4 (P1A.4) Límite de concentración: −10% ≤ wᵢ ≤ 10%", 2)
P("Se resuelve min w′Ωw s.a. w′μ = μ̄, w′1 = 1 y −0,10 ≤ wᵢ ≤ 0,10 con programación cuadrática para una grilla de "
  "retornos objetivo dentro del rango factible (calculado por programación lineal).")
FIG("F04_frontera_limite10.png", 14.0, "Frontera con límite de concentración |wᵢ| ≤ 10% (verde) vs. frontera sin restricciones (azul).")
P("**Diferencias con la frontera del punto 2:**")
BUL([
    f"**Cerca del GMV casi no hay diferencia** (σ = {pc(fr['limite']['gmv']['sigma'], 2)} vs. {pc(gl['sigma'], 2)}). "
    f"El GMV sin restricciones ya era diversificado: solo DUK ({pc(gmvw.loc['DUK', 'GMV sin restricciones'])}), JNJ "
    f"({pc(gmvw.loc['JNJ', 'GMV sin restricciones'])}) y XOM ({pc(gmvw.loc['XOM', 'GMV sin restricciones'])}) superaban el "
    "10%, y el optimizador los sustituye con acciones parecidas casi sin costo.",
    f"**La brecha crece con el retorno objetivo.** Para μ̄ = 30% la volatilidad sube de {pc(sig_en('σ para μ̄=30%', 0))} a "
    f"{pc(sig_en('σ para μ̄=30%', 1))}; para μ̄ = 40%, de {pc(sig_en('σ para μ̄=40%', 0))} a {pc(sig_en('σ para μ̄=40%', 1))}. "
    "Los retornos altos de la frontera libre provenían de posiciones gigantes (KO, SO y XOM sobre 75% en el portafolio "
    "de tangencia), que ahora están prohibidas.",
    f"**La frontera tiene un techo:** el retorno máximo factible es {pc(fr['limite']['rango'][1])}, que se logra con +10% "
    "en las 30 acciones de mayor μ y −10% en las 20 de menor μ (3,0 − 2,0 = 1). Por eso la curva se aplana y termina. "
    "Como la exposición bruta queda acotada a 5 veces el patrimonio, desaparecen las apuestas extremas.",
    f"**Sigue habiendo ventas cortas y se usan casi todas las acciones** ({fr['limite']['n_acciones_min']}–{fr['limite']['n_acciones_max']}), lo que mantiene la frontera cerca de la "
    f"original en la zona relevante. El Sharpe máximo cae de {nu(M['sharpe'])} a {nu(tang['limite']['sharpe'])}.",
    "**Interpretación.** Límites de este tipo son comunes en la regulación (fondos mutuos, AFP, reglas de diversificación). "
    "Formalmente reducen el conjunto factible, por lo que la frontera restringida **no puede** estar a la izquierda de la "
    "original: es una \"mini-frontera\" dentro de ella. Pero también evitan que el optimizador apueste fuerte a diferencias "
    "de medias que son puro ruido de estimación (ver P1B.2).",
])

H("2.5 (P1A.5) Sin ventas cortas: wᵢ ≥ 0", 2)
FIG("F05_frontera_sin_vc.png", 14.0, "Frontera sin ventas cortas (morado) vs. frontera sin restricciones (azul).")
P("**Diferencias con la frontera del punto 2:**")
BUL([
    f"**El GMV empeora levemente** (σ = {pc(fr['sin_vc']['gmv']['sigma'], 2)} vs. {pc(gl['sigma'], 2)}, μ = "
    f"{pc(fr['sin_vc']['gmv']['mu'])}): ya no se pueden usar los cortos que cubrían riesgos. El GMV sin ventas cortas "
    f"invierte en {fr['sin_vc']['gmv']['n_activos']} acciones, con JNJ ({pc(gmvw.loc['JNJ', 'GMV sin venta corta'])}), "
    f"MCD ({pc(gmvw.loc['MCD', 'GMV sin venta corta'])}), VZ, KO, LMT y WMT como principales pesos.",
    f"**El costo crece rápido con μ̄.** Para μ̄ = 30%, σ pasa de {pc(sig_en('σ para μ̄=30%', 0))} a "
    f"{pc(sig_en('σ para μ̄=30%', 2))}; para μ̄ = 40%, de {pc(sig_en('σ para μ̄=40%', 0))} a {pc(sig_en('σ para μ̄=40%', 2))}.",
    f"**El retorno queda acotado entre el de la peor y la mejor acción:** [{pc(fr['sin_vc']['rango'][0])} (AMT), "
    f"{pc(fr['sin_vc']['rango'][1])} (NVDA)]. Sin cortos no hay apalancamiento, así que el extremo superior de la frontera "
    "es 100% NVDA. La frontera ya no es una hipérbola: es una sucesión de tramos (\"portafolios esquina\") que se unen "
    "cada vez que una acción entra o sale.",
    f"**Los portafolios eficientes son concentrados:** usan entre {fr['sin_vc']['n_acciones_min']} y "
    f"{fr['sin_vc']['n_acciones_max']} acciones, y en toda la rama eficiente solo aparecen "
    f"{len(fr['sin_vc']['acciones_usadas_eficiente'])} de las 50. La Figura 6 muestra la transición: de defensivas (consumo "
    "básico, salud, utilities, industriales de baja volatilidad) cerca del GMV, hacia tecnología (NVDA, AVGO), LLY y "
    "energía (XOM) a medida que sube el retorno objetivo.",
    f"**El Sharpe máximo cae de {nu(M['sharpe'])} a {nu(tang['sin_vc']['sharpe'])}** con solo {tang['sin_vc']['n_acciones']} acciones "
    "(XOM 20%, LLY 18%, WMT 14%, AVGO 13%, ABBV 12%, RTX, NVDA, CAT, SO y KO).",
    "**Interpretación.** La restricción es realista: vender corto tiene costos (préstamo de títulos, márgenes, riesgo de "
    "*recall*) y muchos inversionistas institucionales (fondos de pensiones, fondos mutuos) no pueden hacerlo. La frontera "
    "resultante es una \"mini-frontera\" dentro de la original. Sin embargo, como muestran Jagannathan y Ma (2003), "
    "prohibir los cortos equivale a \"encoger\" las covarianzas estimadas y suele *mejorar* el desempeño fuera de muestra; "
    "lo confirmamos en la P1B.2 (Tabla 4).",
])
FIG("F08_composicion_sin_vc.png", 16.5,
    "Composición sectorial de los portafolios eficientes sin ventas cortas (izquierda) y con la restricción sectorial (derecha). "
    "La línea punteada marca el 40% mínimo en Energy + Industrials.")

H("2.6 (P1A.6) Sin ventas cortas y Energy + Industrials ≥ 40%", 2)
FIG("F06_frontera_sector.png", 14.0,
    "Frontera sin ventas cortas (morado) vs. sin ventas cortas con al menos 40% en Energy + Industrials (dorado).")
P("**Diferencias con la frontera del punto 5:**")
BUL([
    f"**La restricción es activa en toda la frontera.** En la frontera sin ventas cortas, Energy + Industrials pesaban "
    f"entre 0% y ~32% (en el GMV, {pc(fr['sin_vc']['gmv']['peso_energy_ind'])}), así que ahora siempre se invierte "
    f"exactamente 40% en esos sectores. El GMV sube de σ = {pc(fr['sin_vc']['gmv']['sigma'], 2)} a "
    f"{pc(fr['sin_vc_sector']['gmv']['sigma'], 2)}.",
    f"**El costo es pequeño en la zona intermedia** (μ̄ = 20%: σ {pc(sig_en('σ para μ̄=20%', 2), 2)} vs. "
    f"{pc(sig_en('σ para μ̄=20%', 3), 2)}; μ̄ = 30%: {pc(sig_en('σ para μ̄=30%', 2), 2)} vs. "
    f"{pc(sig_en('σ para μ̄=30%', 3), 2)}). Energy e Industrials tienen acciones atractivas en el periodo: XOM "
    f"({pc(est.loc['XOM', 'Retorno esperado anual'])}), CAT ({pc(est.loc['CAT', 'Retorno esperado anual'])}) y RTX "
    f"({pc(est.loc['RTX', 'Retorno esperado anual'])}), además de industriales de baja volatilidad (WM, LMT). Además, "
    "la energía tiene baja correlación con tecnología, por lo que diversifica. Por eso el Sharpe máximo casi no cambia "
    f"({nu(tang['sin_vc']['sharpe'], 3)} → {nu(tang['sin_vc_sector']['sharpe'], 3)}): el portafolio tangente sin ventas "
    "cortas ya tenía ~30% en estos sectores.",
    f"**El costo es grande en los extremos.** Arriba, el retorno máximo cae de {pc(fr['sin_vc']['rango'][1])} a "
    f"{pc(fr['sin_vc_sector']['rango'][1])} (60% NVDA + 40% CAT, la mejor acción de esos sectores): se pierde la opción de "
    "concentrarse en tecnología. Abajo, el GMV debe reemplazar consumo básico y salud por WM y LMT (Figura 6).",
    "**El relleno del 40% cambia con μ̄:** con retornos bajos se cumple con industriales defensivos (WM, LMT, UNP); con "
    "retornos altos, con XOM, CVX y CAT. El optimizador elige *qué* acciones del sector usar para minimizar el daño.",
    "**Interpretación.** Una restricción sectorial representa un mandato (fondo temático, política de inversión, "
    "preferencia del cliente). Su costo es la distancia horizontal entre las dos fronteras: es bajo si la restricción se "
    "parece a lo que el optimizador haría de todos modos, y alto cuando lo obliga a alejarse de él.",
])
TAB(res_front.set_index("Frontera")[["Retorno máximo factible", "GMV μ", "GMV σ", "GMV n° acciones",
                                      "σ para μ̄=15%", "σ para μ̄=20%", "σ para μ̄=30%", "σ para μ̄=40%"]],
    "Resumen comparativo de las cuatro fronteras (volatilidad mínima para cada retorno objetivo)",
    fmt={c: (lambda v: pc(v) if np.isfinite(v) else "sin límite") for c in
         ["Retorno máximo factible", "GMV μ", "GMV σ", "σ para μ̄=15%", "σ para μ̄=20%", "σ para μ̄=30%", "σ para μ̄=40%"]}
    | {"GMV n° acciones": lambda v: f"{int(v)}"}, size=7.8,
    nota="“–”: retorno objetivo no factible bajo esa restricción.")
FIG("F07_resumen_fronteras.png", 14.0, "Todas las fronteras eficientes en la zona relevante.")
P("**Conclusión de la P1A.** Cada restricción reduce el conjunto factible y desplaza la frontera hacia la derecha "
  "(\"mini-frontera\"). El orden de los costos es intuitivo: el límite de 10% permite cortos y por eso es la menos costosa; "
  "prohibir los cortos elimina las coberturas y el apalancamiento; la restricción sectorial suma un costo adicional que "
  "depende de cuán lejos está del óptimo sin ella. Que las fronteras con restricciones sean \"peores\" *in-sample* no "
  "significa que sean peores en la práctica: las restricciones disciplinan la sobre-reacción del optimizador a medias mal estimadas.")

# =============================================================================
# PREGUNTA 1B
# =============================================================================
SALTO()
H("3. Pregunta 1B: Línea de Mercado de Capitales y desempeño", 1)
H("3.1 (P1B.1) LMC y portafolio de tangencia M", 2)
P("Con un activo libre de riesgo, el mejor portafolio riesgoso es el que maximiza la pendiente de la línea de "
  "transformación (el ratio de Sharpe). La solución con ventas cortas es:")
EQ("w_M = Ω⁻¹(μ − rf·1) / [1′Ω⁻¹(μ − rf·1)]")
EQ(f"LMC:  E[Rₚ] = rf + SR_M · σₚ = {pc(rf, 2)} + {nu(M['sharpe'])} · σₚ")
P(f"El portafolio de tangencia tiene **μ_M = {pc(M['mu'])}, σ_M = {pc(M['sigma'])} y Sharpe = {nu(M['sharpe'])}**, "
  f"frente a {nu(B['sp500']['sharpe'])} del S&P 500.")
FIG("F09_LMC_tangencia.png", 14.0,
    "Frontera eficiente, LMC y portafolio de tangencia M. Se incluye la línea de transformación del S&P 500 y los "
    "portafolios de máximo Sharpe con restricciones.")
FIG("F10_pesos_tangencia.png", 16.5, "Pesos del portafolio de tangencia M (color = sector).")
lar = M["top_largos"]; cor = M["top_cortos"]
P("**Discusión de M.**")
BUL([
    f"**Es un portafolio extremo:** {pc(M['largos'], 0)} en posiciones largas y {pc(M['cortos'], 0)} en cortas "
    f"(exposición bruta {nu(M['exp_bruta'], 1)}x). Los mayores largos son " +
    ", ".join(f"{k} ({pc(v, 0)})" for k, v in list(lar.items())[:6]) + "; los mayores cortos, " +
    ", ".join(f"{k} ({pc(v, 0)})" for k, v in list(cor.items())[::-1][:6]) + ".",
    f"**Está formado por pares dentro de cada sector:** largo KO / corto PEP y PG (consumo básico); largo SO / corto DUK, "
    f"SRE y NEE (utilities); largo XOM / corto SLB, COP y CVX (energía). Como esas acciones están muy correlacionadas, "
    f"cada par tiene poco riesgo y el optimizador lo apalanca para explotar la diferencia de medias históricas (p. ej. KO "
    f"{pc(est.loc['KO', 'Retorno esperado anual'])} vs. PEP {pc(est.loc['PEP', 'Retorno esperado anual'])}). Pero esa "
    f"diferencia no es estadísticamente significativa (cada media tiene un error de ~{pc(est.loc['KO', 'Error est. de la media'], 0)}). "
    "Michaud (1989) llamó a esto el problema del optimizador como **\"maximizador de errores de estimación\"**.",
    f"**Con restricciones, el máximo Sharpe es menor pero más creíble:** {nu(tang['limite']['sharpe'])} con |wᵢ| ≤ 10% "
    f"(μ = {pc(tang['limite']['mu'])}, σ = {pc(tang['limite']['sigma'])}), {nu(tang['sin_vc']['sharpe'])} sin ventas cortas "
    f"y {nu(tang['sin_vc_sector']['sharpe'])} con la restricción sectorial.",
    "**Teorema de separación (Sesión I, lámina 28):** todos los inversionistas con las mismas creencias mantienen el mismo "
    "portafolio riesgoso M y solo difieren en cuánto invierten en él y cuánto en rf (P1B.4). Los pasos A (frontera) y "
    "B (rf → M) no dependen de las preferencias.",
])

H("3.2 (P1B.2) Modelo índice, alfa de Jensen y eficiencia de mercado", 2)
P("Se estima por MCO, con retornos diarios del 2-ago-2021 al 31-jul-2026, el modelo índice del portafolio M (pesos de "
  f"P1B.1) contra el S&P 500, con rf diaria = rf/252 = {pc(B['rf_diaria'], 4)}:")
EQ("r_M,t − rf = α + β · (r_SP500,t − rf) + εₜ")
mi_tab = pd.DataFrame({
    "Coeficiente": ["α (diario)", "α (anualizado ×252)", "β"],
    "Estimación": [nu(mi["alfa_diario"], 5), pc(mi["alfa_anual"]), nu(mi["beta"], 3)],
    "Error estándar": [nu(mi["ee_alfa"], 5), pc(mi["ee_alfa"] * 252), nu(mi["ee_beta"], 3)],
    "Estadístico t": [nu(mi["t_alfa"]), nu(mi["t_alfa"]), f"{nu(mi['t_beta'])} (H0: β=1 → {nu(mi['t_beta_igual_1'])})"],
    "Valor p": [f"{mi['p_alfa']:.1e}", f"{mi['p_alfa']:.1e}", "< 0,001"],
}).set_index("Coeficiente")
TAB(mi_tab, "Modelo índice del portafolio de tangencia M (MCO, errores estándar clásicos)",
    nota=f"T = {miles(mi['T'])} días; R² = {nu(mi['R2'], 3)}; σ(ε) anual = {pc(mi['sigma_e_anual'])}; "
         f"t(α) con errores robustos HAC (Newey-West, 5 rezagos) = {nu(mi['t_alfa_HAC'])}. Usando el S&P 500 Total Return "
         f"como mercado: α = {pc(mi['alfa_anual_SPTR'])}, t = {nu(mi['t_alfa_SPTR'])}.")
FIG("F11_modelo_indice.png", 12.0, "Excesos de retorno diarios de M versus el S&P 500 y recta estimada.")
P(f"**Test-t de α = 0.** El estadístico es t = α̂ / ee(α̂) = {nu(mi['t_alfa'])}, muy superior al valor crítico de 1,96 "
  f"(5%) y 2,58 (1%) con {miles(mi['gl'])} grados de libertad. **Formalmente se rechaza α = 0**: *in-sample*, M habría "
  f"obtenido {pc(mi['alfa_anual'])} anual por sobre lo que predice el CAPM para su β = {nu(mi['beta'])}. " +
  f"Además, β es significativamente menor que 1 y el R² es apenas {nu(mi['R2'], 3)}: M es un portafolio largo-corto, "
  "casi neutral al mercado, cuyo riesgo es mayoritariamente idiosincrásico.")
P("**¿Es este resultado consistente con la eficiencia de mercado? Sí, y el alfa no es evidencia en su contra.** "
  "El rechazo es un artefacto del procedimiento, por cuatro razones:")
BUL([
    "**Sesgo de anticipación (look-ahead).** Los pesos de M se calcularon con las medias realizadas entre 2021 y 2026. "
    "Un inversionista en agosto de 2021 no podía conocerlas. La hipótesis de eficiencia dice que no se pueden obtener "
    "retornos anormales con la información *disponible en ese momento*; M usa información futura, así que su α no es "
    "alcanzable y no contradice la hipótesis.",
    f"**Sobreajuste y data snooping: el test-t pierde validez.** Al elegir 50 pesos para maximizar el Sharpe muestral, "
    f"el optimizador maximiza a la vez el ratio de información α/σ(ε). De hecho, SR²_M ≈ SR²_SP + (α/σε)²: "
    f"{nu(M['sharpe'])}² ≈ {nu(B['sp500']['sharpe'])}² + {nu(mi['IR_teorico'])}², y t(α) ≈ (α/σε)·√años = "
    f"{nu(mi['ratio_informacion'])} × √{nu(mi['T'] / 252, 2)} ≈ {nu(t_teorico)}, prácticamente el t obtenido. El α alto y "
    f"significativo es una consecuencia **mecánica** de la optimización. Incluso si todos los α verdaderos fueran cero, el "
    f"Sharpe *in-sample* esperado de la tangencia sería aproximadamente √(SR²_SP + N/años) = {nu(sim['sharpe_esperado_teorico'])}.",
    f"**Simulación de Monte Carlo bajo H0.** Se simularon {miles(sim['N_sim'])} muestras de 5 años con la Ω observada y medias " +
    f"\"puras CAPM\" (μᵢ = rf + βᵢ(μ_SP − rf), es decir, **todos los α verdaderos = 0**). En cada una se repitió exactamente "
    f"nuestro procedimiento. El |t(α)| promedio fue {nu(sim['t_alfa_media'])} (90% de los casos entre "
    f"{nu(sim['t_alfa_p05'])} y {nu(sim['t_alfa_p95'])}) y el {pc(sim['pct_t_mayor_196'], 0)} de las simulaciones "
    f"\"rechazó\" α = 0 al 5%. Nuestro t = {nu(mi['t_alfa'])} es *menor* que el {pc(sim['pct_t_mayor_obs'], 1)} de los "
    f"simulados (Figura 12). El tamaño real del test no es 5% sino ~100%: con datos reutilizados, el t-test no tiene la "
    f"distribución t de Student.",
    f"**Evidencia fuera de muestra.** Se estimó M con ago-2021 a jul-2025 (Sharpe prometido "
    f"{nu(fm['M_in_sample_sharpe_prometido'])}) y se evaluó en ago-2025 a jul-2026 sin reoptimizar (Tabla 4, Figura 13). "
    f"M obtuvo un retorno acumulado de {pc(fm['M (sin restricciones)']['retorno_acumulado'])} con σ = "
    f"{pc(fm['M (sin restricciones)']['sigma'], 0)} y Sharpe {nu(fm['M (sin restricciones)']['sharpe'])}; su α fuera de "
    f"muestra fue {pc(fm['M (sin restricciones)']['alfa_anual'])} (t = {nu(fm['M (sin restricciones)']['t_alfa'])}). La "
    "promesa de Sharpe 2,8 desapareció apenas cambiaron los datos.",
])
P("A esto se suma el **problema de la hipótesis conjunta** (Fama): un test de α = 0 evalúa simultáneamente la eficiencia "
  "y el modelo de equilibrio (CAPM con el S&P 500 como *proxy* del portafolio de mercado, crítica de Roll). Un α ≠ 0 "
  "podría deberse a un modelo mal especificado (p. ej. factores de Fama-French) y no a ineficiencia. Por último, los "
  "precios ajustados de las acciones incluyen dividendos y el ^GSPC no; usando el S&P 500 Total Return el α cambia "
  f"menos de un punto ({pc(mi['alfa_anual_SPTR'])}), de modo que no altera la conclusión.")
FIG("F12_simulacion_H0.png", 16.0,
    "Distribución del |t(α)| y del Sharpe *in-sample* de la tangencia estimada cuando todos los α verdaderos son cero. "
    "La línea roja es nuestro resultado.")
oos = pd.DataFrame({k: fm[k] for k in ["M (sin restricciones)", "M sin venta corta", "1/N", "S&P 500"]}).T
oos = oos[["retorno_acumulado", "mu", "sigma", "sharpe", "beta", "alfa_anual", "t_alfa"]]
oos.columns = ["Retorno acumulado", "μ anual", "σ anual", "Sharpe", "β", "α anual", "t(α)"]
oos.index.name = "Portafolio (ago-2025 a jul-2026)"
TAB(oos, "Desempeño fuera de muestra de portafolios estimados con datos hasta el 31-jul-2025",
    fmt={"Retorno acumulado": pc, "μ anual": pc, "σ anual": pc, "Sharpe": nu, "β": nu, "α anual": pc, "t(α)": nu},
    nota=f"Sharpe prometido in-sample: M {nu(fm['M_in_sample_sharpe_prometido'])}; M sin venta corta "
         f"{nu(fm['M_LO_in_sample_sharpe_prometido'])}. Retornos de portafolio calculados con rebalanceo diario exacto.")
FIG("F13_fuera_de_muestra.png", 14.0, "Valor de US$1 invertido el 31-jul-2025 en portafolios estimados con datos previos.")
P(f"Notablemente, el portafolio de máximo Sharpe **sin ventas cortas** sí tuvo un buen año fuera de muestra (Sharpe "
  f"{nu(fm['M sin venta corta']['sharpe'])}, retorno {pc(fm['M sin venta corta']['retorno_acumulado'])}), al igual que el "
  f"simple 1/N (Sharpe {nu(fm['1/N']['sharpe'])}), ambos por sobre el S&P 500 (Sharpe {nu(fm['S&P 500']['sharpe'])}). "
  f"Pero sus α no son significativos (t = {nu(fm['M sin venta corta']['t_alfa'])} y {nu(fm['1/N']['t_alfa'])}) y un año "
  "es muy poco para concluir habilidad. La lección es la de Jagannathan y Ma (2003) y DeMiguel, Garlappi y Uppal (2009): "
  "con medias tan ruidosas, las restricciones o la diversificación ingenua suelen superar al Markowitz sin restricciones "
  "fuera de muestra.")

H("3.3 (P1B.3) Ratios de Sharpe y de Treynor", 2)
EQ("Sharpe:  SRₚ = (E[Rₚ] − rf) / σₚ          Treynor:  TRₚ = (E[Rₚ] − rf) / βₚ")
d3 = desemp[["μ anual", "σ anual", "β", "R²", "Sharpe", "Treynor", "α Jensen anual"]].copy()
d3.index.name = "Portafolio"
TAB(d3, "Medidas de desempeño (ago-2021 a jul-2026, base anual)",
    fmt={"μ anual": pc, "σ anual": pc, "β": nu, "R²": nu, "Sharpe": nu, "Treynor": pc, "α Jensen anual": pc},
    resaltar=lambda i, f: i in ("Tangencia M (sin restricciones)", "S&P 500 (índice de precios)"),
    nota="β estimado contra el S&P 500 (índice de precios). El S&P 500 tiene β = 1, por lo que su Treynor es simplemente su prima por riesgo.")
P(f"**Resultado.** M domina al S&P 500 en ambas medidas: Sharpe {nu(M['sharpe'])} vs. {nu(B['sp500']['sharpe'])} y "
  f"Treynor {pc(desemp.loc['Tangencia M (sin restricciones)', 'Treynor'], 0)} vs. "
  f"{pc(desemp.loc['S&P 500 (índice de precios)', 'Treynor'])}. En este caso el ranking coincide, pero por razones muy "
  "distintas en cada medida, y en general **el ranking puede diferir**:")
BUL([
    "**Miden riesgos distintos.** Sharpe divide por el riesgo *total* (σ), Treynor solo por el riesgo *sistemático* (β). "
    "Como βₚ = ρₚ,M·σₚ/σ_M, se cumple que SRₚ = TRₚ · ρₚ,M / σ_M: dos portafolios con la misma prima por unidad de β "
    "tendrán distinto Sharpe si difieren en su correlación con el mercado (su R²).",
    f"**Un portafolio con mucho riesgo idiosincrásico (R² bajo) se ve bien en Treynor y mal en Sharpe.** Es lo que ocurre "
    f"con {n_inv_rank} de las 50 acciones frente al S&P 500 (Figura 14). Por ejemplo, JNJ tiene Sharpe "
    f"{nu(acc_st.loc['JNJ', 'Sharpe'])} (menor al {nu(B['sp500']['sharpe'], 3)} del índice) pero Treynor "
    f"{pc(acc_st.loc['JNJ', 'Treynor'])} (seis veces el del índice), porque su β es {nu(acc_st.loc['JNJ', 'β'])} y su R² "
    f"{pc(acc_st.loc['JNJ', 'R²'])}. Lo mismo con LMT (Sharpe {nu(acc_st.loc['LMT', 'Sharpe'])}, Treynor "
    f"{pc(acc_st.loc['LMT', 'Treynor'])}), DUK, AEP, NEM o WM: todas con β bajo y R² bajo.",
    f"**Cuál usar depende del contexto.** Si el portafolio es *toda* la inversión riesgosa, importa el riesgo total y la "
    f"medida correcta es Sharpe (que es la que se maximiza para obtener M). Si es una parte pequeña de un portafolio bien "
    f"diversificado, su riesgo idiosincrásico se diversifica y la medida correcta es Treynor. En el caso de M, su Treynor "
    f"de {pc(desemp.loc['Tangencia M (sin restricciones)', 'Treynor'], 0)} está inflado por su β bajo ({nu(mi['beta'])}) y "
    f"no refleja sus {pc(mi['sigma_e_anual'], 0)} de volatilidad idiosincrásica. Si β → 0 el Treynor se dispara, y con β < 0 pierde sentido.",
    "**Solo coinciden para portafolios bien diversificados** (R² ≈ 1, σₚ ≈ βₚσ_M), como el 1/N o el máximo Sharpe sin "
    "ventas cortas. Además, el alfa de Jensen se relaciona con ambos: αₚ = βₚ·(TRₚ − TR_M).",
])
FIG("F14_sharpe_vs_treynor.png", 13.0,
    "Sharpe vs. Treynor de cada acción. Las acciones en el cuadrante superior izquierdo (Treynor > S&P 500 pero "
    "Sharpe < S&P 500) invierten el ranking.")

H("3.4 (P1B.4) Asignación óptima entre M y el activo libre de riesgo", 2)
P("Con preferencias media-varianza U = E[R_C] − (c/2)σ²_C y un portafolio completo C = x·M + (1 − x)·rf, la condición "
  "de primer orden (Sesión I, láminas 24–25) entrega:")
EQ(f"x* = (E[R_M] − rf) / (c · σ²_M) = ({pc(M['mu'])} − {pc(rf, 2)}) / (c · {nu(M['sigma'] ** 2, 4)}) = "
   f"{nu((M['mu'] - rf) / M['sigma'] ** 2)} / c")
a_tab = asig.copy()
a_tab["c"] = a_tab["c"].astype(int).astype(str)
a_tab = a_tab.set_index("c")[["x* (en M)", "1 - x* (en rf)", "Posición", "E[R_C]", "σ_C", "Utilidad U = E - c/2 σ²",
                              "x* con máx. Sharpe sin VC", "x* con S&P 500"]]
a_tab.columns = ["x* en M", "1 − x* en rf", "Posición en la LMC", "E[R_C]", "σ_C", "U", "x* (máx. Sharpe sin VC)", "x* (S&P 500)"]
TAB(a_tab, "Asignación óptima para distintos coeficientes de aversión al riesgo c",
    fmt={"x* en M": nu, "1 − x* en rf": pc, "E[R_C]": pc, "σ_C": pc, "U": pc,
         "x* (máx. Sharpe sin VC)": nu, "x* (S&P 500)": nu}, size=7.8)
FIG("F15_asignacion_optima.png", 14.0,
    "Asignaciones óptimas sobre la LMC y curvas de indiferencia tangentes para c = 2, 5 y 10.")
P("**Interpretación en la LMC.**")
BUL([
    f"**c = 2 (poco averso): borrowing.** x* = {nu(asig.loc[0, 'x* (en M)'])}: por cada $1 de patrimonio pide prestado "
    f"${nu(-asig.loc[0, '1 - x* (en rf)'])} a rf e invierte ${nu(asig.loc[0, 'x* (en M)'])} en M. Se ubica en la LMC muy a la "
    f"derecha de M (σ = {pc(asig.loc[0, 'σ_C'], 0)}).",
    f"**c = 5: borrowing moderado.** x* = {nu(asig.loc[1, 'x* (en M)'])}: pide prestado {pc(-asig.loc[1, '1 - x* (en rf)'], 0)} "
    "del patrimonio; también está sobre la LMC a la derecha de M.",
    f"**c = 10 (muy averso): lending.** x* = {nu(asig.loc[2, 'x* (en M)'])}: invierte {pc(asig.loc[2, 'x* (en M)'], 0)} en M y "
    f"presta {pc(asig.loc[2, '1 - x* (en rf)'], 0)} a rf; se ubica entre rf y M.",
    "**Separación.** Los tres inversionistas tienen exactamente el mismo portafolio riesgoso (M) y solo difieren en x*; "
    "a mayor c, la curva de indiferencia es más convexa y la tangencia ocurre más cerca de rf. El punto M (x = 1) corresponde "
    f"a c = {nu((M['mu'] - rf) / M['sigma'] ** 2, 1)}.",
    f"**Advertencia.** Como M *in-sample* tiene un retorno esperado irreal ({pc(M['mu'], 0)}), las asignaciones implican "
    f"apalancamientos extremos (c = 2 implicaría σ = {pc(asig.loc[0, 'σ_C'], 0)}). Con el máximo Sharpe sin ventas cortas o "
    "con el S&P 500 (últimas columnas) las asignaciones son mucho más razonables. Además, en la práctica la tasa para pedir "
    "prestado es mayor que rf, lo que quiebra la LMC a la derecha de M y reduce el atractivo del borrowing.",
])

# =============================================================================
# PREGUNTA 2
# =============================================================================
SALTO()
H("4. Pregunta 2: Modelos de estructura de tasas", 1)
H("4.1 Datos", 2)
P("Se descargó el paquete *Treasury Constant Maturities* del H.15 de la Reserva Federal (rendimientos de mercado de los "
  "bonos del Tesoro a plazo constante, en % anual): 1, 3 y 6 meses y 1, 2, 3, 5, 7, 10, 20 y 30 años. Para cada año se "
  "tomó el **último día transado de junio**. Siguiendo el enunciado, el plazo se mide con la convención días transados / "
  "días transados, es decir, t = 1/12 para 1 mes, … , t = 30 para 30 años.")
cv = curvas.copy()
cv.index = [pd.Timestamp(f).strftime("%d-%m-%Y") for f in cv.index]
cv.index.name = "Fecha"
TAB(cv, "Curvas observadas (H.15, % anual) el último día transado de junio",
    fmt={c: (lambda v: pb(v, 2)) for c in cv.columns}, size=7.6)
H("4.2 Modelos y estimación del óptimo global", 2)
P("Nelson-Siegel (1987) y Svensson (1994), con la notación de clase (Sesión I, láminas 82–83):")
EQ("R(t) = β₀ + β₁·[(1 − e^(−t/α₁))·α₁/t] + β₂·[(1 − e^(−t/α₁))·α₁/t − e^(−t/α₁)]")
EQ("Svensson:  R(t) = NS(t) + β₃·[(1 − e^(−t/α₂))·α₂/t − e^(−t/α₂)]")
P("β₀ es el nivel (R(∞) = β₀), β₁ la pendiente (R(0) = β₀ + β₁, de modo que β₁ = tasa corta − tasa larga), β₂ la "
  "curvatura (joroba si β₂ > 0, valle si β₂ < 0) y α₁ indica dónde se ubica esa joroba (su máximo está en t ≈ 1,8·α₁). "
  "Svensson agrega una segunda joroba (β₃, α₂). Se estima por mínimos cuadrados: min Σ (R_obs(tⱼ) − R(tⱼ))².")
P("**Cómo se aseguró el óptimo global.** La función objetivo no es convexa en α y tiene múltiples mínimos locales; un "
  "optimizador local entrega soluciones distintas según el punto de partida. Se usó la siguiente estrategia:")
BUL([
    "**β concentrados.** Dado α, el modelo es lineal en los β y se resuelven exactamente por mínimos cuadrados. El problema "
    "queda reducido a 1 dimensión (α₁) en NS y a 2 (α₁, α₂) en Svensson.",
    "**Búsqueda exhaustiva** en una grilla logarítmica fina: 800 valores de α₁ (NS) y 130 × 170 pares (α₁, α₂) (Svensson).",
    "**Refinamiento local** (Nelder-Mead) desde los 5 mejores puntos de la grilla.",
    "**Verificación independiente:** 300 (NS) y 200 (Svensson) optimizaciones locales de *todos* los parámetros desde "
    f"puntos iniciales aleatorios. En las 10 fechas ninguna encontró un error menor al nuestro. Solo el "
    f"{pb(C['demo_minimos_locales']['pct_medio_ns'], 0)}% (NS) y el {pb(C['demo_minimos_locales']['pct_medio_sv'], 0)}% "
    f"(Svensson) de los intentos llegó al óptimo, y en el peor caso apenas el {pb(C['demo_minimos_locales']['pct_min_ns'], 0)}% "
    f"(NS, {pd.Timestamp(C['demo_minimos_locales']['fecha_min_ns']).year}) y el {pb(C['demo_minimos_locales']['pct_min_sv'], 1)}% "
    f"(Svensson, {pd.Timestamp(C['demo_minimos_locales']['fecha_min_sv']).year}). Una sola optimización local habría "
    "entregado frecuentemente un mínimo local.",
    "**Región admisible económicamente:** β₀ ≥ 0 (tasa larga no negativa), β₀ + β₁ ≥ 0 (tasa instantánea no negativa), "
    "0,1 ≤ α₁ ≤ 10 años y 0,1 ≤ α₂ ≤ 30 años (α₂ ≠ α₁ para evitar colinealidad). Sin estas cotas, el \"óptimo\" numérico "
    f"de NS en 2022 tiene α₁ = 0,05 y una tasa instantánea R(0) = {pc(sinr.iloc[5]['R(0)=b0+b1'] / 100)} cuando la tasa a "
    f"1 mes era 1,28%, y en 2026 tiene α₁ = 30 con β₀ = {pc(sinr.iloc[9]['b0'] / 100)} cuando la tasa a 30 años era 4,91%. "
    "Esas soluciones mejoran el ajuste en apenas 0,2 a 1 pb pero destruyen la interpretación de los parámetros: la función "
    "objetivo es muy plana en α (problema de identificación). Las soluciones sin restricción están en *2_NS_sin_restricciones_robustez.csv*.",
])
FIG("F20_funcion_objetivo_NS.png", 13.0,
    "Error cuadrático mínimo de Nelson-Siegel para cada α₁ (β concentrados). Varias fechas tienen más de un mínimo local "
    "o una función muy plana.")

H("4.3 Resultados y comparación de ajuste (RMSE)", 2)
pt = par[["NS b0", "NS b1", "NS b2", "NS a1", "SV b0", "SV b1", "SV b2", "SV b3", "SV a1", "SV a2",
          "RMSE NS (pb)", "RMSE SV (pb)", "Mejora RMSE (%)"]].copy()
pt.columns = ["β₀", "β₁", "β₂", "α₁", "β₀ ", "β₁ ", "β₂ ", "β₃", "α₁ ", "α₂", "RMSE NS", "RMSE SV", "Mejora %"]
pt.index.name = "Junio"
TAB(pt, "Parámetros estimados (Nelson-Siegel: columnas 2–5; Svensson: columnas 6–11) y RMSE en puntos base",
    fmt={c: (lambda v: pb(v, 2)) for c in pt.columns[:10]} | {"RMSE NS": lambda v: pb(v, 1), "RMSE SV": lambda v: pb(v, 1),
                                                             "Mejora %": lambda v: pb(v, 0)}, size=7.2,
    nota="RMSE = √(Σ errores²/11) × 100, en puntos base (pb). β en %, α en años.")
FIG("F16_ajustes_NS_SV.png", 16.8, "Curvas observadas (puntos) y ajustadas por Nelson-Siegel (azul) y Svensson (rojo, discontinua).")
FIG("F19_rmse_residuos.png", 16.8,
    "Izquierda: RMSE por fecha. Derecha: |error NS| − |error SV| por plazo, en pb (azul = Svensson ajusta mejor).")
bic_mejor = int((par["BIC SV"] < par["BIC NS"]).sum())
P("**¿En qué fechas y en qué parte de la curva mejora Svensson?**")
BUL([
    f"**Mejora en todas las fechas**, lo que es esperable porque NS es un caso particular de Svensson (β₃ = 0): con más "
    f"parámetros el error *in-sample* nunca puede ser mayor. La reducción del RMSE va de {pb(par['Mejora RMSE (%)'].min())}% "
    f"({par['Mejora RMSE (%)'].idxmin()}) a {pb(par['Mejora RMSE (%)'].max())}% ({par['Mejora RMSE (%)'].idxmax()}). "
    f"Penalizando por los dos parámetros extra (criterio BIC), Svensson sigue siendo preferido en {bic_mejor} de 10 fechas, "
    "aunque en 2022 la ventaja es marginal.",
    f"**Las mayores mejoras son en 2018, 2025, 2026, 2017, 2024 y 2023.** En 2017, 2018 y 2020 la segunda joroba (α pequeño, "
    "0,2–0,5 años) corrige el **extremo corto**: la curvatura muy rápida entre 1 y 6 meses que NS no puede seguir con la "
    "misma α que usa para el tramo medio. En 2025 y 2026 también mejora mucho el extremo corto (1M y 6M): en 2025 la "
    "joroba en 3 meses reflejaba recortes esperados de la Fed y en 2026 el salto de 1 a 6 meses reflejaba alzas esperadas.",
    f"**Desde 2021, Svensson mejora sobre todo el tramo de 20 años** (mejora promedio de {pb(mejora['20A'], 1)} pb en 20A y "
    f"{pb(mejora['30A'], 1)} pb en 30A, versus menos de 2 pb en los plazos de 2 a 10 años). La razón es una anomalía conocida: "
    "desde su reintroducción en mayo de 2020, el bono a 20 años rinde **más** que el de 30 años (p. ej. 3,38% vs. 3,14% en "
    "2022 y 4,06% vs. 3,85% en 2023), por su menor demanda y liquidez. Esa \"joroba\" larga (efecto de liquidez/segmentación, "
    "no de expectativas) requiere un segundo término con α₂ de 12–16 años que NS no tiene.",
    f"**2022 es la fecha peor ajustada** (NS {pb(par.loc['2022', 'RMSE NS (pb)'], 1)} pb, Svensson "
    f"{pb(par.loc['2022', 'RMSE SV (pb)'], 1)} pb): la curva subía bruscamente hasta 1 año, era plana entre 1 y 10 años, "
    "tenía el pico de 20 años y estaba a días de invertirse. Ni siquiera dos jorobas capturan todas esas irregularidades.",
])

H("4.4 Evolución de β₀, β₁ y β₂: nivel, pendiente y curvatura", 2)
FIG("F18_parametros_NS.png", 16.5,
    "Parámetros de Nelson-Siegel en el tiempo y sus contrapartes observadas. Abajo a la derecha: tasa instantánea "
    "implícita R(0) = β₀ + β₁ versus la tasa de fondos federales efectiva.")
BUL([
    f"**β₀ (nivel, tasa de largo plazo).** Cerca de 3% en 2017–2019, cae a {pb(par.loc['2020', 'NS b0'], 2)}% en 2020 "
    f"(pandemia, compras masivas de bonos de la Fed) y luego sube de forma persistente hasta {pb(par.loc['2026', 'NS b0'], 2)}% "
    f"en 2026, el mayor de la muestra. Sigue de cerca a la tasa a 30 años (correlación {nu(corr_b0)}). El alza desde 2022 "
    "refleja mayor inflación esperada y tasas reales más altas, pero también una **prima por plazo** creciente: déficit "
    "fiscal de ~6% del PIB, más emisión del Tesoro, rebaja de la calificación de EE.UU. (Fitch 2023, Moody's 2025) y dudas "
    "sobre la independencia de la Fed.",
    f"**β₁ (pendiente = R(0) − R(∞)).** Negativo (curva normal, con pendiente positiva) en 2017–2022, con su valor más negativo "
    f"en 2021 ({pb(par.loc['2021', 'NS b1'], 2)}): tasas cortas en cero y tasas largas recuperándose. Se vuelve **positivo en "
    f"2023 ({pb(par.loc['2023', 'NS b1'], 2)}) y 2024 ({pb(par.loc['2024', 'NS b1'], 2)})**: la curva invertida. Vuelve a ser negativo "
    f"en 2025 y 2026. Su correlación con el diferencial 3M − 10A observado es {nu(corr_b1)}. En 2019 β₁ es negativo pese a "
    "que 10A < 3M: la inversión estaba en el tramo medio (mínimo en 3 años) y la captura β₂.",
    f"**β₂ (curvatura).** Prácticamente 0 en 2017–2018 (curvas monótonas; matemáticamente, cuando la joroba no es necesaria el "
    f"óptimo tiene β₂ = 0 porque ∂(carga de β₁)/∂α₁ es proporcional a la carga de β₂). Muy negativo en 2019–2022 (forma de "
    f"valle o \"S\": tramo corto plano y bajo, alza fuerte después), muy **positivo en 2023 ({pb(par.loc['2023', 'NS b2'], 2)})**: "
    f"la joroba en 6 meses en el peak de las alzas de la Fed. En 2025 alcanza el valle más profundo "
    f"({pb(par.loc['2025', 'NS b2'], 2)}): la curva en forma de \"bañera\" (corto alto, medio bajo, largo alto). En 2026 vuelve "
    "a casi 0 con α₁ en su cota de 10 años: la curva es una pendiente casi lineal y creciente.",
    "**R(0) = β₀ + β₁ replica la tasa de política monetaria** (panel inferior derecho): el extremo corto de la curva está "
    "anclado por la Fed y el extremo largo por las expectativas de inflación, crecimiento y la prima por plazo.",
])

H("4.5 Análisis de la evolución de la curva 2017–2026 (punto principal)", 2)
FIG("F17_evolucion_curvas.png", 14.5, "Las diez curvas de fines de junio (ajuste Svensson y datos observados).")
FIG("F21_spreads_inversion.png", 16.5,
    "Arriba: tasas del Tesoro, tasa de fondos federales e inflación IPC (BLS). Abajo: pendientes 10A − 3M y 10A − 2A; el "
    "sombreado rojo marca los episodios de inversión (10A − 3M < 0) y el gris la recesión NBER de 2020.")
P("La curva de tasas resume lo que el mercado espera de la política monetaria (extremo corto), de la inflación y el "
  "crecimiento (tramo medio) y el premio que exige por mantener deuda larga (extremo largo). Entre 2017 y 2026 pasó por "
  "ocho fases claramente asociadas a eventos económicos, políticos y sociales:")

fases = [
    ("2017 – Normalización gradual (curva positiva que se aplana).",
     "Con la economía en pleno empleo, la Fed subió la tasa en dic-2016, mar-2017 y jun-2017 (a 1,00–1,25% al momento de la "
     "curva) y anunció en junio de 2017 la reducción de su balance (comenzó en octubre). La inflación seguía bajo 2% y en "
     "Europa y Japón había tasas negativas, lo que contenía las tasas largas. Resultado: curva normal (10A − 3M = +128 pb) "
     "pero aplanándose, porque el extremo corto subía más rápido que el largo. En diciembre se aprobó la reforma tributaria "
     "(*Tax Cuts and Jobs Act*)."),
    ("2018 – Alzas, estímulo fiscal y guerra comercial (curva muy plana).",
     "La Fed (ya con Powell) subió cuatro veces, hasta 2,25–2,50% en diciembre, mientras el estímulo fiscal ampliaba el "
     "déficit. En julio comenzaron los aranceles a China. El 29-jun-2018 la curva iba de 1,77% (1M) a solo 2,98% (30A): "
     "el diferencial 10A − 2A era de apenas 33 pb. El mercado anticipaba que el ciclo de alzas estaba cerca de su fin. En "
     "el cuarto trimestre hubo una fuerte caída bursátil que llevó a la Fed a pausar en enero de 2019."),
    ("2019 – Inversión por la guerra comercial y desaceleración global.",
     "La escalada de aranceles (mayo y agosto), la debilidad manufacturera global, el Brexit y ~US$17 billones de deuda con "
     "rendimiento negativo en el mundo hundieron las tasas largas. El 28-jun-2019 la curva tenía forma de U: 2,18% a 1 mes, "
     "mínimo de 1,71% a 3 años y 2,52% a 30 años; 10A − 3M = −12 pb. El mercado anticipaba recortes, y la Fed recortó tres "
     "veces (julio, septiembre y octubre: el *mid-cycle adjustment*). En septiembre hubo turbulencia en el mercado repo."),
    ("2020 – Pandemia de COVID-19 (tasas cortas en cero, curva empinada).",
     "La Fed recortó de emergencia a 0–0,25% (3 y 15 de marzo), compró bonos sin límite (QE desde el 23 de marzo) y el Congreso "
     "aprobó el *CARES Act*. La NBER fechó una recesión de feb-2020 a abr-2020, la más corta de la historia. El 30-jun-2020 "
     "todo el tramo hasta 3 años estaba entre 0,13% y 0,18% (*forward guidance*: tasas en cero por largo tiempo) y la curva "
     "subía recién después, hasta 1,41% a 30 años. En agosto la Fed adoptó una meta de inflación promedio y el 10A tocó su "
     "mínimo histórico (~0,5%)."),
    ("2021 – Reapertura y reflación (la curva más empinada).",
     "Las vacunas, el *American Rescue Plan* (US$1,9 billones) y la reapertura impulsaron las expectativas de crecimiento e "
     "inflación (IPC cercano a 5% en mayo y sobre 5% desde junio, calificada como \"transitoria\"). El 30-jun-2021 las tasas cortas seguían en "
     "0,05%, pero la de 10 años llegaba a 1,45%: 10A − 3M = +140 pb, la pendiente más positiva de la muestra (β₁ = −2,33). "
     "En la reunión del 16 de junio la Fed adelantó sus alzas esperadas, lo que subió la tasa a 2 años y aplanó el tramo largo."),
    ("2022 – Shock inflacionario y las alzas más rápidas desde los 80.",
     "La invasión rusa de Ucrania (24-feb-2022) disparó la energía y los alimentos; la inflación llegó a 9,1% en junio. La Fed "
     "subió desde marzo y el 15 de junio aplicó 75 pb (la mayor alza desde 1994), además de iniciar la reducción del balance "
     "(QT). El 30-jun-2022 la curva subía violentamente hasta 1 año (1,28% → 2,80%) y era plana después (10A − 2A = +6 pb): el "
     "mercado esperaba muchas más alzas y luego recortes. Seis días después se invirtió el tramo 10A − 2A. Siguieron alzas de "
     "75 pb en julio, septiembre y noviembre."),
    ("2023–2024 – Inversión profunda y tasas en su máximo.",
     "La Fed llegó a 5,25–5,50% en julio de 2023. En marzo de 2023 quebró Silicon Valley Bank (pérdidas en bonos por el "
     "alza de tasas), seguido de Signature y First Republic, y en mayo-junio hubo una disputa por el techo de deuda que elevó "
     "las tasas de las letras de corto plazo. El 30-jun-2023 la curva estaba **máximamente invertida**: 5,47% a 6 meses y "
     "3,81% a 10 años (10A − 3M = −162 pb; 10A − 2A = −106 pb), β₁ > 0 y una gran joroba corta (β₂ = +3,6). Luego la rebaja "
     "de Fitch (agosto), la mayor emisión y la prima por plazo llevaron el 10A a 5% en octubre de 2023. En 2024 la inflación "
     "bajó a ~3% y el mercado esperaba recortes: el 28-jun-2024 la curva seguía invertida (10A − 3M = −112 pb) con valle a 5 "
     "años. La Fed recortó 50 pb en septiembre y 25 pb en noviembre y diciembre (a 4,25–4,50%). Tras la elección de "
     "noviembre las tasas largas *subieron* pese a los recortes (más déficit, aranceles e inflación esperados)."),
    ("2025 – Aranceles, incertidumbre fiscal y curva en \"bañera\".",
     "Los aranceles del *Liberation Day* (2 de abril) provocaron una venta simultánea de acciones y bonos, una señal inusual "
     "de pérdida de calidad de refugio, y una pausa de 90 días el 9 de abril. Moody's quitó a EE.UU. su última nota AAA (16 "
     "de mayo) y la ley fiscal de julio (*One Big Beautiful Bill*) amplió el déficit proyectado. Con la Fed en pausa (4,25–4,50%) "
     "por el riesgo inflacionario de los aranceles, el 30-jun-2025 la curva tenía forma de bañera: 4,41% a 3 meses, mínimo "
     "de 3,68% a 3 años y 4,79% a 20 años. El extremo corto invertido anticipaba recortes y el largo incorporaba prima por "
     "plazo (β₂ = −3,8, el valle más profundo). El PIB cayó en el primer trimestre (importaciones adelantadas), la Fed recortó "
     "en septiembre, octubre y diciembre (a 3,50–3,75%) y terminó el QT el 1 de diciembre. Entre el 1 de octubre y el 12 de "
     "noviembre hubo el cierre del gobierno más largo de la historia: el IPC de octubre no se publicó (falta en nuestros datos). "
     "Hubo además presiones sobre la independencia de la Fed (intento de remover a la gobernadora Lisa Cook)."),
    ("2026 – Guerra con Irán, shock petrolero y vuelta de las alzas (curva positiva con tasas largas al alza).",
     "En enero Trump nominó a Kevin Warsh para suceder a Powell. El 20 de febrero la Corte Suprema anuló los aranceles "
     "basados en la ley IEEPA (fueron reemplazados por un arancel global de 10% bajo la sección 122). El 28 de febrero EE.UU. "
     "e Israel atacaron Irán; la interrupción del Estrecho de Ormuz fue calificada por la AIE como la mayor disrupción de "
     "oferta petrolera de la historia y el Brent pasó de ~US$72 a cerca de US$120. El IPC subió de 2,4% en febrero a "
     "3,8% en abril y 4,2% en mayo. Warsh asumió el 22 de mayo y en la reunión del 17 de junio la Fed mantuvo 3,50–3,75% "
     "pero sus proyecciones pasaron a indicar un alza. El 30-jun-2026 la curva era normal y creciente: 3,70% a 1 mes, 4,01% a "
     "6 meses (el salto corto ya descontaba alzas) y 4,93% a 20 años (β₀ = 5,3%, el nivel más alto de la muestra). Después "
     "el PIB del segundo trimestre creció solo 1,5%, la Fed **subió la tasa el 16-sep-2026** (a 3,75–4,00%, la primera alza "
     "desde 2023) y el 10A superó 5% por primera vez desde 2007. Al 15-oct-2026: 1M = 4,17%, 2A = 4,77%, 10A = 5,10% y "
     "30A = 5,43%."),
]
for titulo, texto in fases:
    P(f"**{titulo}** {texto}")

H("4.6 ¿Cuándo estuvo invertida la curva, qué anticipaba y ocurrió?", 2)
P("Con los datos diarios del H.15 se identificaron los episodios en que la tasa a 10 años fue menor que la de 3 meses "
  "(la medida que sigue la Fed de Nueva York) o menor que la de 2 años. Entre las fechas de junio, la curva estaba "
  "invertida en **2019** (10A − 3M = −12 pb), **2023** (−162 pb, invertida en todos los tramos), **2024** (−112 pb) y "
  "**2025** (−17 pb, solo el tramo corto, con 10A − 2A = +52 pb). En junio de 2022 estaba prácticamente plana y se invirtió "
  "días después.")
ep = []
for e in inv["10A-3M"]:
    ep.append({"Spread": "10A − 3M", "Inicio": e["inicio"], "Fin": e["fin"], "Días invertida": e["dias_habiles_invertida"],
               "Mínimo (pb)": e["spread_minimo_pb"], "Fecha del mínimo": e["fecha_minimo"]})
for e in inv["10A-2A"]:
    ep.append({"Spread": "10A − 2A", "Inicio": e["inicio"], "Fin": e["fin"], "Días invertida": e["dias_habiles_invertida"],
               "Mínimo (pb)": e["spread_minimo_pb"], "Fecha del mínimo": e["fecha_minimo"]})
ep.append({"Spread": "10A − 2A", "Inicio": "2019-08-27", "Fin": "2019-08-29", "Días invertida": 3,
           "Mínimo (pb)": -4, "Fecha del mínimo": "2019-08-27"})
epd = pd.DataFrame(ep).set_index("Spread")
TAB(epd, "Episodios de inversión de la curva del Tesoro, 2017–oct-2026 (datos diarios H.15)",
    fmt={"Días invertida": lambda v: f"{int(v)}", "Mínimo (pb)": lambda v: pb(v, 0)}, size=8,
    nota="Se unen tramos negativos separados por menos de 20 días hábiles. El episodio de 2022–2024 es el más largo y "
         "profundo desde inicios de los años 80.")
P("**¿Qué anticipa una inversión?** Bajo la teoría de expectativas (con prima por plazo pequeña), una tasa larga menor "
  "que la corta implica que el mercado espera **tasas cortas futuras más bajas**, lo que típicamente ocurre cuando la "
  "Fed recorta frente a una desaceleración o recesión. Históricamente, la inversión de 10A − 3M precedió a todas las "
  "recesiones de EE.UU. desde los años 60, con 6 a 24 meses de anticipación (Estrella y Mishkin, 1998). Además, una curva "
  "invertida reduce el margen de los bancos (prestan largo y se financian corto) y restringe el crédito. Evaluación de cada episodio:")
tab_pred = pd.DataFrame([
    {"Episodio": "2019 (may–oct; 2s10s en agosto)",
     "Qué anticipaba": "Recortes de la Fed y riesgo de recesión por la guerra comercial y la desaceleración global",
     "¿Ocurrió?": "Recortes: SÍ (75 pb en 2019). Recesión: SÍ (feb–abr 2020), pero causada por la pandemia, un shock "
                  "exógeno que la curva no podía prever: acierto \"por las razones equivocadas\"."},
    {"Episodio": "ene–mar 2020",
     "Qué anticipaba": "Huida a la calidad al inicio de la pandemia; recortes de emergencia",
     "¿Ocurrió?": "SÍ: tasa a cero en marzo y recesión de feb–abr 2020."},
    {"Episodio": "jul-2022 a dic-2024 (2s10s 26 meses; 10A−3M hasta −189 pb)",
     "Qué anticipaba": "Recesión provocada por el alza de tasas más rápida en 40 años y recortes posteriores",
     "¿Ocurrió?": "Recortes: SÍ (175 pb entre sep-2024 y dic-2025). Recesión: NO, al menos hasta oct-2026 (\"aterrizaje "
                  "suave\"). Es la señal fallida más notable de la historia del indicador."},
    {"Episodio": "feb–sep 2025 (solo 10A−3M)",
     "Qué anticipaba": "Recortes ante la desaceleración por los aranceles (en abril se temió una recesión)",
     "¿Ocurrió?": "Recortes: SÍ (75 pb en sep–dic 2025). Recesión: NO (solo un trimestre negativo, por importaciones adelantadas)."},
]).set_index("Episodio")
TAB(tab_pred, "Qué anticipaba cada inversión y qué ocurrió", size=8, anchos=[3.6, 5.4, 8.2])
P("**¿Por qué falló la señal de 2022–2024?** Hay varias explicaciones complementarias: (i) la inversión reflejaba sobre "
  "todo la **normalización esperada de la inflación** (tasas nominales más bajas en el futuro porque la inflación bajaría) "
  "y no necesariamente una recesión; (ii) la **prima por plazo** estaba deprimida por los años de QE, lo que hacía la "
  "curva más plana que lo que implicaban las expectativas; (iii) hogares y empresas habían **fijado tasas bajas** en "
  "2020–2021 (hipotecas a 30 años, deuda corporativa a plazo), por lo que la política monetaria se transmitió con menos "
  "fuerza; (iv) el **impulso fiscal** (déficits de ~6% del PIB), el ahorro acumulado en la pandemia, la inmigración que "
  "amplió la oferta laboral y el auge de inversión en inteligencia artificial sostuvieron el crecimiento. Hay quienes "
  "notan que las recesiones suelen comenzar *después* de que la curva vuelve a tener pendiente positiva; la "
  "desaceleración de 2026 (PIB del segundo trimestre de 1,5%) mantiene abierta esa discusión, pero hasta octubre de 2026 "
  "la NBER no ha fechado una recesión.")
P("**Lectura de la curva en 2026.** La pendiente hoy es positiva y creciente, pero por razones distintas a una "
  "recuperación: es un *empinamiento bajista* (las tasas largas suben más que las cortas) impulsado por el shock "
  "petrolero, la inflación sobre 4%, la vuelta de las alzas de la Fed, los déficits fiscales y la incertidumbre sobre la "
  "independencia del banco central. La señal ya no es de recesión inminente, sino de mayor riesgo inflacionario y "
  "fiscal: los inversionistas exigen más compensación por mantener deuda de largo plazo del gobierno de EE.UU.")

# =============================================================================
# CONCLUSIONES
# =============================================================================
H("5. Conclusiones", 1)
BUL([
    "La teoría de Markowitz entrega enormes beneficios de diversificación *in-sample*, pero la frontera sin restricciones "
    "y el portafolio de tangencia son extremadamente sensibles al error de estimación de las medias: M es un conjunto de "
    "apuestas largo-corto apalancadas sobre diferencias de medias que no son estadísticamente significativas.",
    "Las covarianzas son el corazón de la diversificación: ignorarlas subestima el riesgo de los portafolios largos y "
    "elimina la posibilidad de cubrirse. Lo que importa no es el número de activos sino su correlación.",
    "Las restricciones (límite de concentración, sin ventas cortas, sectoriales) generan mini-fronteras dentro de la "
    "original. Su costo *in-sample* es el precio de evitar soluciones irreales, y fuera de muestra suelen ser beneficiosas.",
    "El alfa de Jensen de M (78% anual, t = 5,6) no contradice la eficiencia de mercado: es un resultado mecánico de "
    "evaluar un portafolio con los mismos datos con que se construyó. La simulación bajo H0 y la prueba fuera de muestra "
    "lo confirman.",
    "Sharpe y Treynor pueden ordenar distinto porque miden riesgo total y riesgo sistemático, respectivamente; la "
    "diferencia es mayor mientras más riesgo idiosincrásico tenga el portafolio.",
    "Nelson-Siegel describe bien la curva del Tesoro (RMSE de 2 a 11 pb) y sus parámetros siguen al nivel, la pendiente y "
    "la curvatura observadas. Svensson mejora sobre todo el extremo corto y el tramo de 20 años. Asegurar el óptimo global "
    "requiere explotar la estructura del problema y verificarlo con múltiples puntos iniciales.",
    "La curva 2017–2026 cuenta la historia macroeconómica reciente de EE.UU.: normalización, guerra comercial, pandemia, "
    "inflación y alzas récord, la inversión más larga en cuatro décadas sin recesión, aranceles y shocks fiscales, y en "
    "2026 un shock petrolero que devolvió a la Fed a subir tasas y llevó las tasas largas a máximos de casi dos décadas.",
])

# =============================================================================
# REFERENCIAS
# =============================================================================
H("Referencias", 1)
refs = [
    "Bodie, Z., Kane, A. y Marcus, A. (2017). *Investments*, 11.ª ed. McGraw-Hill.",
    "Copeland, T., Weston, F. y Shastri, K. (2013). *Financial Theory and Corporate Finance*, 4.ª ed. Pearson.",
    "Bernales, A. (2026). *Finanzas I – ENFIN415, Sesiones I y II*. Universidad de Chile.",
    "DeMiguel, V., Garlappi, L. y Uppal, R. (2009). Optimal versus naive diversification. *Review of Financial Studies*, 22(5).",
    "Estrella, A. y Mishkin, F. (1998). Predicting U.S. recessions: financial variables as leading indicators. *Review of Economics and Statistics*, 80(1).",
    "Fama, E. (1991). Efficient capital markets: II. *Journal of Finance*, 46(5).",
    "Gilli, M., Große, S. y Schumann, E. (2010). Calibrating the Nelson-Siegel-Svensson model. COMISEF WP 031.",
    "Jagannathan, R. y Ma, T. (2003). Risk reduction in large portfolios: why imposing the wrong constraints helps. *Journal of Finance*, 58(4).",
    "Michaud, R. (1989). The Markowitz optimization enigma: is 'optimized' optimal? *Financial Analysts Journal*, 45(1).",
    "Nelson, C. y Siegel, A. (1987). Parsimonious modeling of yield curves. *Journal of Business*, 60(4).",
    "Roll, R. (1977). A critique of the asset pricing theory's tests. *Journal of Financial Economics*, 4(2).",
    "Svensson, L. (1994). Estimating and interpreting forward interest rates: Sweden 1992–1994. NBER WP 4871.",
    "Datos: Federal Reserve Board, H.15 Selected Interest Rates (federalreserve.gov/datadownload); Yahoo Finance; "
    "U.S. Bureau of Labor Statistics (IPC, desempleo).",
    "Noticias 2025–2026: Federal Reserve, comunicado FOMC del 16-sep-2026 (federalreserve.gov/monetarypolicy/files/monetary20260916a1.pdf); "
    "BEA, GDP (Advance Estimate) 2nd Quarter 2026; CNBC, \"10-year Treasury yield hits highest level since 2007\" (15-sep-2026) y "
    "\"CPI inflation report May 2026\" (10-jun-2026); CNN, \"Kevin Warsh sworn in as Fed chair\" (22-may-2026); "
    "CNBC, \"A timeline of how the Iran war shook oil prices\" (21-abr-2026); K&L Gates, resumen del fallo de la Corte "
    "Suprema sobre los aranceles IEEPA (20-feb-2026).",
]
for r_ in refs:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(2.5)
    runs(p, r_, size=9)

# =============================================================================
# ANEXOS
# =============================================================================
SALTO()
H("Anexo A. Estadísticas anuales de las 50 acciones (ago-2021 a jul-2026)", 1)
ta = est[["Sector", "Retorno esperado anual", "Volatilidad anual", "Retorno/Volatilidad", "Beta vs S&P 500",
          "Error est. de la media"]].copy()
ta.columns = ["Sector", "μ anual", "σ anual", "μ/σ", "β", "Error est. de μ"]
TAB(ta, "Retorno esperado, volatilidad, beta y error estándar de la media de cada acción",
    fmt={"μ anual": pc, "σ anual": pc, "μ/σ": nu, "β": nu, "Error est. de μ": pc}, size=7.5,
    anchos=[1.6, 4.4, 2.0, 2.0, 1.6, 1.6, 2.4])

H("Anexo B. Archivos entregados y cómo reproducir los resultados", 1)
P("Carpeta *Solucion_Tarea*:")
BUL([
    "**codigo/config.py**: parámetros (acciones y sectores, fechas, rutas, series H.15).",
    "**codigo/01_descargar_datos.py**: descarga los precios (Yahoo Finance), el S&P 500, el H.15 de la Fed y los datos macro (H.15 semanal, BLS).",
    "**codigo/utilidades.py**: funciones comunes: momentos anuales, frontera analítica (A, B, C, D), fronteras con restricciones (cvxpy), tangencia.",
    "**codigo/02_pregunta_1A.py**, **03_pregunta_1B.py**, **04_pregunta_2.py**: cálculos, tablas y figuras de cada pregunta (comentados paso a paso).",
    "**codigo/05_generar_informe.py**: genera el informe breve para entregar; **06_informe_extendido.py**, esta versión extendida.",
    "**datos/**: todos los datos descargados (CSV). **resultados/tablas/**: tablas CSV y planillas Excel *Resultados_Pregunta1A/1B/2.xlsx*. **resultados/figuras/**: todos los gráficos.",
    "Para reproducir: instalar Python 3.11+ y `pip install -r requirements.txt`, luego ejecutar los scripts 01 a 05 en orden desde la carpeta *codigo*.",
])

salida = RESULTADOS / "Informe_extendido_referencia.docx"
doc.save(salida)
print("Informe guardado en", salida)
