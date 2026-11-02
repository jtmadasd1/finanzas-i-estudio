# =============================================================================
#  05_generar_informe.py
#  Construye el INFORME PARA ENTREGAR (version breve, ~13 paginas) a partir de
#  los resultados guardados por los scripts 02, 03 y 04.  Todas las cifras del
#  texto se leen de /resultados, asi que si se vuelven a correr los calculos el
#  informe se actualiza solo.  La version extendida (con robusteces y analisis
#  adicionales) la genera 06_informe_extendido.py.
# =============================================================================
from informe_utils import *  # noqa: F401,F403  (datos, formatos y funciones de escritura)

SECTOR_CORTO = {
    "Energy": "Energía", "Industrials": "Industrial", "Financials": "Financiero",
    "Health Care": "Salud", "Information Technology": "Tecnología", "Utilities": "Utilities",
    "Communication Services": "Comunicaciones", "Consumer Discretionary": "Consumo discrecional",
    "Consumer Staples": "Consumo básico", "Materials": "Materiales", "Real Estate": "Inmobiliario",
}

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
r = p.add_run("Todos los cálculos están en los archivos de código adjuntos (Python), junto con los datos "
              "descargados y planillas Excel con los resultados.")
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
SALTO()

# =============================================================================
# 1. DATOS Y METODOLOGIA
# =============================================================================
H("1. Datos y metodología", 1)
cuenta = est["Sector"].value_counts()
BUL([
    "**Acciones:** 50 del S&P 500 de los 11 sectores: " +
    ", ".join(f"{SECTOR_CORTO[s]} {n}" for s, n in cuenta.items()) +
    ". Todas pertenecieron al índice durante toda la ventana (lista en el Anexo).",
    "**Precios:** cierre diario ajustado por *splits* y dividendos, de Yahoo Finance (descargado con el paquete "
    "*yfinance* de Python). Sin ajuste, los *splits* de NVDA, AMZN, GOOGL o NFLX aparecerían como caídas falsas de 67% a 95%.",
    f"**Ventana: 5 años** (retornos del {corr['inicio']} al {corr['fin']}, {miles(corr['T_dias'])} observaciones), el máximo "
    "permitido: con 50 acciones hay que estimar 1.275 varianzas y covarianzas, y con un año la matriz Ω sería muy imprecisa.",
    "**Retornos continuos** rₜ = ln(Pₜ/Pₜ₋₁), como en la clase, anualizados con 252 días: μ×252, Ω×252 y σ×√252.",
    f"**Tasa libre de riesgo:** Treasury constant maturity a 1 año (Fed H.15) al 31-jul-2026, {pc(B['y1_publicada'], 2)} "
    f"en base equivalente a bono, convertida a continua: rf = 2·ln(1 + y/2) = {pc(rf, 2)}.",
    "**Software:** todos los cálculos se hicieron en Python (el enunciado permite cualquier lenguaje). La frontera sin "
    "restricciones usa la fórmula analítica de clase y las fronteras con restricciones, programación cuadrática.",
])

# =============================================================================
# 2. PREGUNTA 1A
# =============================================================================
H("2. Pregunta 1A: Frontera media-varianza", 1)
H("2.1 (P1A.1) Retornos esperados, volatilidades y covarianzas", 2)
P(f"Los retornos esperados anuales (medias históricas) van de {pc(est['Retorno esperado anual'].min())} (AMT) a "
  f"{pc(est['Retorno esperado anual'].max())} (NVDA) y las volatilidades de {pc(est['Volatilidad anual'].min())} (KO) a "
  f"{pc(est['Volatilidad anual'].max())} (TSLA); el S&P 500 rindió {pc(B['sp500']['mu'])} con σ = {pc(s_sp)}. "
  "Los valores de cada acción están en el Anexo y la matriz de covarianzas anual (50×50) en *Resultados_Pregunta1A.xlsx*. "
  f"La correlación promedio es {nu(corr['corr_promedio'])} ({nu(corr['corr_mismo_sector'])} dentro de un mismo sector) y "
  f"solo el {pc(corr['pct_corr_negativas'])} de los pares es negativo.")
P(f"Las medias se estiman con mucho error: su error estándar es σ/√5, por ejemplo ±{pc(est.loc['NVDA', 'Error est. de la media'], 0)} "
  "para NVDA. Las varianzas y covarianzas, en cambio, se estiman con más precisión. Esta diferencia explica varios "
  "resultados de la Pregunta 1B.")

H("2.2 (P1A.2) Frontera media-varianza", 2)
P("Como en la clase, para cada retorno objetivo μ̄ se minimiza la varianza con ventas cortas permitidas. La solución "
  "del Lagrangiano entrega la frontera en forma cerrada:")
EQ("min_w  w′Ωw   s.a.  w′μ = μ̄ ,  w′1 = 1   ⇒   σ²(μ̄) = (A·μ̄² − 2B·μ̄ + C) / D")
P(f"con A = 1′Ω⁻¹1 = {nu(Fa)}, B = 1′Ω⁻¹μ = {nu(Fb)}, C = μ′Ω⁻¹μ = {nu(A['C'])} y D = AC − B² = {nu(Fd)}. "
  f"El portafolio de mínima varianza global (GMV) tiene μ = B/A = {pc(gl['mu'])} y σ = 1/√A = {pc(gl['sigma'])}.")
FIG("F02_frontera_mv.png", 12.5, "Frontera media-varianza con 50 acciones. Sobre el GMV (rombo) está la rama eficiente.")
BUL([
    f"**La frontera queda a la izquierda de todas las acciones.** El GMV tiene menos riesgo que la acción menos volátil "
    f"(KO, {pc(est.loc['KO', 'Volatilidad anual'])}) y que el S&P 500. Con el riesgo del índice, la frontera promete "
    f"{pc(mu_frontera_en_sp)} contra {pc(B['sp500']['mu'])}: es el beneficio de diversificar, medido con medias ya conocidas (*in-sample*).",
    f"**Usa ventas cortas y apalancamiento.** El GMV tiene {pc(-gl['suma_cortos'], 0)} en posiciones cortas, que cubren el "
    f"riesgo de acciones parecidas. Para μ̄ = 20%, 30% y 50% la exposición bruta es {nu(ing.loc[1, 'exposicion_bruta_completa'], 1)}, "
    f"{nu(ing.loc[2, 'exposicion_bruta_completa'], 1)} y {nu(ing.loc[3, 'exposicion_bruta_completa'], 1)} veces el patrimonio: "
    "por eso la rama eficiente no tiene techo.",
])

H("2.3 (P1A.3) Frontera \"ingenua\" y el rol de las covarianzas", 2)
P("La frontera ingenua calcula los pesos con la diagonal de Ω (σᵢⱼ = 0), de modo que cada acción se pondera solo por su "
  "retorno y su varianza. Luego se mide la volatilidad **real** de esos pesos con la Ω completa, y también la volatilidad "
  "**percibida** por quien ignora las covarianzas.")
FIG("F03_frontera_ingenua.png", 12.5,
    "Frontera completa (azul), frontera ingenua con su volatilidad real (rojo) y con la volatilidad percibida (naranjo).")
ing_tab = pd.DataFrame({
    "σ frontera completa": ing["sigma_frontera_completa"].values,
    "σ ingenua real": ing["sigma_ingenua_real"].values,
    "σ ingenua percibida": ing["sigma_ingenua_percibida"].values,
}, index=[f"{pc(m)}" + (" (GMV)" if k == 0 else "") for k, m in enumerate(ing["mu_objetivo"])])
ing_tab.index.name = "μ̄ objetivo"
TAB(ing_tab, "Volatilidad para un mismo retorno objetivo", fmt={c: pc for c in ing_tab.columns})
P("**¿Qué rol juegan las covarianzas en la diversificación?**")
BUL([
    f"**Fijan cuánto riesgo se puede eliminar.** Con σᵢⱼ = 0 el riesgo de un portafolio 1/N tendería a cero (Sesión I), pero "
    f"como las correlaciones son positivas converge a la covarianza promedio: el {pc(corr['share_var_cov_1N'], 0)} de la "
    f"varianza del 1/N viene de covarianzas. Ignorarlas genera una ilusión de diversificación: el GMV ingenuo cree tener "
    f"σ = {pc(gi['sigma_percibida'])} y en realidad tiene {pc(gi['sigma_real'])}.",
    "**Ignorarlas produce portafolios ineficientes.** La curva roja siempre queda a la derecha de la azul: con el mismo "
    f"retorno, el portafolio ingenuo tiene entre {pb(100 * (ing['sigma_ingenua_real'] - ing['sigma_frontera_completa']).min(), 1)} y "
    f"{pb(100 * (ing['sigma_ingenua_real'] - ing['sigma_frontera_completa']).max(), 1)} puntos más de volatilidad.",
    f"**Permiten cubrirse.** Con acciones muy correlacionadas (COP y EOG, ρ = {nu(corr['corr_max'])}) una posición larga y "
    "otra corta cancelan el riesgo común. Por eso, en retornos altos (portafolios largo-corto), la curva naranja cruza a la "
    "azul: ahí las covarianzas positivas reducen el riesgo y quien las ignora lo sobreestima.",
])

H("2.4 (P1A.4–P1A.6) Fronteras con restricciones", 2)
P("Con restricciones no hay fórmula cerrada: para cada retorno objetivo se resolvió el mismo problema por programación "
  "cuadrática, agregando −0,10 ≤ wᵢ ≤ 0,10 (P1A.4), wᵢ ≥ 0 (P1A.5) o wᵢ ≥ 0 con al menos 40% en Energy + Industrials (P1A.6).")
FIG("F07_resumen_fronteras.png", 12.5, "Las cuatro fronteras eficientes y la ingenua (zona relevante).")
TAB(res_front.set_index("Frontera")[["Retorno máximo factible", "GMV μ", "GMV σ", "σ para μ̄=20%", "σ para μ̄=30%",
                                      "σ para μ̄=40%"]],
    "Volatilidad mínima para cada retorno objetivo según la restricción",
    fmt={c: (lambda v: pc(v) if np.isfinite(v) else "sin límite") for c in
         ["Retorno máximo factible", "GMV μ", "GMV σ", "σ para μ̄=20%", "σ para μ̄=30%", "σ para μ̄=40%"]},
    size=7.8, nota="“–”: retorno no alcanzable con esa restricción.")
P(f"**P1A.4: límite de concentración vs. P2.** Cerca del GMV casi no hay diferencia (σ = {pc(fr['limite']['gmv']['sigma'], 2)} "
  f"vs. {pc(gl['sigma'], 2)}): solo DUK, JNJ y XOM superaban el 10% y se reemplazan por acciones parecidas. La brecha crece "
  f"con el retorno (μ̄ = 40%: σ de {pc(sig_en('σ para μ̄=40%', 0))} a {pc(sig_en('σ para μ̄=40%', 1))}) y la frontera tiene "
  f"un techo de {pc(fr['limite']['rango'][1])} (+10% en las 30 mejores acciones y −10% en las 20 peores), porque ya no se "
  "pueden tomar las posiciones gigantes que daban los retornos altos.")
P(f"**P1A.5: sin venta corta vs. P2.** El GMV empeora levemente (σ = {pc(fr['sin_vc']['gmv']['sigma'], 2)}), pero el costo "
  f"crece rápido con el retorno (μ̄ = 30%: σ de {pc(sig_en('σ para μ̄=30%', 0))} a {pc(sig_en('σ para μ̄=30%', 2))}). Sin "
  "cortos no hay apalancamiento ni coberturas: el retorno queda entre el de la peor y la mejor acción "
  f"({pc(fr['sin_vc']['rango'][0])} a {pc(fr['sin_vc']['rango'][1])}, 100% NVDA). Los portafolios eficientes son "
  f"concentrados (entre {fr['sin_vc']['n_acciones_min']} y {fr['sin_vc']['n_acciones_max']} acciones) y la frontera es una "
  "sucesión de tramos que cambian cuando una acción entra o sale.")
P(f"**P1A.6: restricción sectorial vs. P1A.5.** La restricción es activa en toda la frontera, porque sin ella Energy + "
  f"Industrials pesaban entre 0% y ~32%. Cuesta poco en la zona media (μ̄ = 20%: σ de {pc(sig_en('σ para μ̄=20%', 2), 2)} a "
  f"{pc(sig_en('σ para μ̄=20%', 3), 2)}), porque XOM, CAT y RTX tuvieron buenos retornos y la energía tiene baja correlación "
  f"con tecnología. Cuesta mucho en los extremos: el retorno máximo cae a {pc(fr['sin_vc_sector']['rango'][1])} (60% NVDA + "
  "40% CAT) y el GMV debe usar industriales defensivos (WM, LMT) en vez de consumo básico.")
P("**En síntesis**, cada restricción achica el conjunto factible y genera una \"mini-frontera\" dentro de la original, con "
  "un costo bajo cerca del GMV y alto en retornos altos. Ese costo es *in-sample*: las restricciones también evitan que el "
  "optimizador apueste fuerte a diferencias de medias que son ruido, lo que suele ayudar fuera de muestra.")

# =============================================================================
# 3. PREGUNTA 1B
# =============================================================================
H("3. Pregunta 1B: Línea de Mercado de Capitales y desempeño", 1)
H("3.1 (P1B.1) LMC y portafolio de tangencia", 2)
P("El portafolio de tangencia M maximiza el ratio de Sharpe, es decir, la pendiente de la línea que sale de rf:")
EQ(f"w_M = Ω⁻¹(μ − rf·1) / [1′Ω⁻¹(μ − rf·1)]        LMC:  E[Rₚ] = {pc(rf, 2)} + {nu(M['sharpe'])} · σₚ")
FIG("F09_LMC_tangencia.png", 12.5, "Frontera eficiente, LMC y portafolio de tangencia M.")
lar, cor = M["top_largos"], M["top_cortos"]
P(f"M tiene **μ = {pc(M['mu'])}, σ = {pc(M['sigma'])} y Sharpe = {nu(M['sharpe'])}** (S&P 500: {nu(B['sp500']['sharpe'])}). "
  f"Pero es extremo: {pc(M['largos'], 0)} en posiciones largas y {pc(M['cortos'], 0)} en cortas. Está formado por pares dentro "
  "de cada sector (largo KO / corto PEP y PG; largo SO / corto DUK y SRE; largo XOM / corto SLB y COP): como esas acciones "
  "están muy correlacionadas, cada par tiene poco riesgo y el optimizador lo apalanca para explotar diferencias de medias "
  f"históricas (KO {pc(est.loc['KO', 'Retorno esperado anual'])} vs. PEP {pc(est.loc['PEP', 'Retorno esperado anual'])}) "
  "que no son estadísticamente significativas. El optimizador actúa como un \"maximizador de errores de estimación\". "
  f"Sin ventas cortas el Sharpe máximo cae a {nu(tang['sin_vc']['sharpe'])}.")

H("3.2 (P1B.2) Modelo índice y alfa de Jensen", 2)
EQ("r_M,t − rf = α + β · (r_SP500,t − rf) + εₜ")
mi_tab = pd.DataFrame({
    "Estimación": [nu(mi["alfa_diario"], 5), pc(mi["alfa_anual"]), nu(mi["beta"], 3)],
    "Error estándar": [nu(mi["ee_alfa"], 5), pc(mi["ee_alfa"] * 252), nu(mi["ee_beta"], 3)],
    "Estadístico t": [nu(mi["t_alfa"]), nu(mi["t_alfa"]), nu(mi["t_beta"])],
}, index=["α (diario)", "α (anual, ×252)", "β"])
mi_tab.index.name = "Coeficiente"
TAB(mi_tab, "Modelo índice del portafolio M (MCO, retornos diarios ago-2021 a jul-2026)",
    nota=f"T = {miles(mi['T'])} días; R² = {nu(mi['R2'], 3)}; rf diaria = rf/252.")
P(f"**Test-t de α = 0:** t = α̂/ee(α̂) = {nu(mi['t_alfa'])} > 1,96, por lo que formalmente se rechaza α = 0 al 5%: M "
  f"habría ganado {pc(mi['alfa_anual'])} anual por sobre lo que predice el CAPM para su β = {nu(mi['beta'])}. El R² de "
  f"{nu(mi['R2'], 2)} muestra que M es un portafolio largo-corto casi neutral al mercado, con riesgo mayoritariamente idiosincrásico.")
P("**¿Es consistente con la eficiencia de mercado? Sí: este α no es evidencia de ineficiencia, porque:**")
BUL([
    "**Usa información futura.** Los pesos de M se calcularon con las medias de 2021–2026, que un inversionista no "
    "conocía en 2021. La eficiencia solo dice que no se gana anormalmente con la información disponible en ese momento.",
    "**Se usaron los mismos datos para construir y evaluar M.** Al maximizar el Sharpe muestral con 50 pesos, el "
    "optimizador maximiza también α/σ(ε), así que el α alto y significativo es mecánico y el test-t pierde validez. Como "
    f"verificación simulamos {miles(sim['N_sim'])} muestras con α verdadero = 0 para todas las acciones: repitiendo el "
    f"procedimiento, el t(α) promedio fue {nu(sim['t_alfa_media'])}, más que el nuestro.",
    f"**Fuera de muestra el α desaparece.** M estimado con datos hasta jul-2025 prometía Sharpe "
    f"{nu(fm['M_in_sample_sharpe_prometido'])}, pero entre ago-2025 y jul-2026 rindió "
    f"{pc(fm['M (sin restricciones)']['retorno_acumulado'])}.",
    "**Hipótesis conjunta (Fama):** un α ≠ 0 también puede indicar que el CAPM, o el S&P 500 como proxy del "
    "portafolio de mercado (crítica de Roll), no es el modelo correcto.",
])

H("3.3 (P1B.3) Ratios de Sharpe y de Treynor", 2)
EQ("SRₚ = (E[Rₚ] − rf) / σₚ          TRₚ = (E[Rₚ] − rf) / βₚ")
d3 = desemp.loc[["Tangencia M (sin restricciones)", "S&P 500 (índice de precios)"],
                ["μ anual", "σ anual", "β", "Sharpe", "Treynor"]].copy()
d3.index = ["Portafolio de tangencia M", "S&P 500"]
d3.index.name = "Portafolio"
TAB(d3, "Sharpe y Treynor (base anual)", fmt={"μ anual": pc, "σ anual": pc, "β": nu, "Sharpe": nu, "Treynor": pc})
P(f"M supera al S&P 500 en ambas medidas. Sin embargo, **el ranking puede diferir** porque Sharpe usa el riesgo total (σ) "
  "y Treynor solo el sistemático (β). Como βₚ = ρₚ,M·σₚ/σ_M, se cumple SRₚ = TRₚ·ρₚ,M/σ_M: un portafolio con mucho riesgo "
  f"idiosincrásico (R² bajo) se ve bien en Treynor y mal en Sharpe. Ejemplo en nuestros datos: JNJ tiene Sharpe "
  f"{nu(acc_st.loc['JNJ', 'Sharpe'])} (bajo el índice) pero Treynor {pc(acc_st.loc['JNJ', 'Treynor'])} (seis veces el del "
  f"índice), porque su β es {nu(acc_st.loc['JNJ', 'β'])}. Sharpe es la medida correcta si el portafolio es toda la inversión "
  "riesgosa (el caso de M, por el teorema de separación); Treynor, si es una parte pequeña de un portafolio diversificado. "
  f"El Treynor de M está inflado por su β bajo ({nu(mi['beta'])}).")

H("3.4 (P1B.4) Asignación óptima entre M y rf", 2)
P("Maximizando U = E[R_C] − (c/2)σ²_C con R_C = x·R_M + (1 − x)·rf (Sesión I):")
EQ(f"x* = (E[R_M] − rf) / (c·σ²_M) = ({pc(M['mu'])} − {pc(rf, 2)}) / (c · {nu(M['sigma'] ** 2, 4)}) = "
   f"{nu((M['mu'] - rf) / M['sigma'] ** 2)} / c")
a_tab = asig.copy()
a_tab["c"] = a_tab["c"].astype(int).astype(str)
a_tab = a_tab.set_index("c")[["x* (en M)", "1 - x* (en rf)", "Posición", "E[R_C]", "σ_C"]]
a_tab.columns = ["x* en M", "1 − x* en rf", "Posición en la LMC", "E[R_C]", "σ_C"]
TAB(a_tab, "Asignación óptima para c = 2, 5 y 10",
    fmt={"x* en M": nu, "1 − x* en rf": pc, "E[R_C]": pc, "σ_C": pc})
BUL([
    f"**c = 2 y c = 5 (borrowing):** x* > 1, piden prestado {pc(-asig.loc[0, '1 - x* (en rf)'], 0)} y "
    f"{pc(-asig.loc[1, '1 - x* (en rf)'], 0)} del patrimonio a rf para invertir más de 100% en M; se ubican en la LMC a la derecha de M.",
    f"**c = 10 (lending):** x* = {nu(asig.loc[2, 'x* (en M)'])}, invierte {pc(asig.loc[2, 'x* (en M)'], 0)} en M y presta "
    f"{pc(asig.loc[2, '1 - x* (en rf)'], 0)} a rf; se ubica entre rf y M.",
    "**Separación:** los tres tienen el mismo portafolio riesgoso M y solo cambia x*; a mayor aversión, más cerca de rf. "
    f"Los apalancamientos son extremos porque el μ de M ({pc(M['mu'], 0)}) es irreal; con el S&P 500 serían "
    f"{nu(asig.loc[0, 'x* con S&P 500'])}, {nu(asig.loc[1, 'x* con S&P 500'])} y {nu(asig.loc[2, 'x* con S&P 500'])}.",
])

# =============================================================================
# 4. PREGUNTA 2
# =============================================================================
H("4. Pregunta 2: Modelos de estructura de tasas", 1)
H("4.1 Datos, modelos y óptimo global", 2)
P("Se usaron las 11 series *Treasury constant maturities* del H.15 de la Fed (1, 3 y 6 meses; 1, 2, 3, 5, 7, 10, 20 y "
  "30 años) el último día transado de junio de 2017 a 2026. Con la convención días transados / días transados, el plazo "
  "se mide en años (1 mes = 1/12). Los modelos, con la notación de clase:")
EQ("NS:  R(t) = β₀ + β₁·[(1 − e^(−t/α₁))·α₁/t] + β₂·[(1 − e^(−t/α₁))·α₁/t − e^(−t/α₁)]")
EQ("Svensson:  R(t) = NS(t) + β₃·[(1 − e^(−t/α₂))·α₂/t − e^(−t/α₂)]")
P("β₀ es el nivel (R(∞) = β₀), β₁ la pendiente (R(0) = β₀ + β₁, así que β₁ = tasa corta − tasa larga y β₁ > 0 indica "
  "curva invertida), β₂ la curvatura (joroba si es positiva, valle si es negativa) y α₁ ubica esa joroba. Svensson "
  "agrega una segunda joroba (β₃, α₂).")
P(f"**Óptimo global.** La función de error no es convexa en α y tiene mínimos locales. Por eso: (i) dado α, el modelo "
  "es lineal en los β y se resuelven exacto por mínimos cuadrados; (ii) se recorrió una grilla fina de α₁ (y de α₁, α₂ en "
  "Svensson) y se refinó desde los mejores puntos; (iii) se verificó con cientos de optimizaciones desde puntos iniciales "
  f"aleatorios: ninguna encontró un error menor, y solo el {pb(C['demo_minimos_locales']['pct_medio_ns'], 0)}% (NS) y el "
  f"{pb(C['demo_minimos_locales']['pct_medio_sv'], 0)}% (Svensson) llegaron al óptimo. Se exigió β₀ ≥ 0 y β₀ + β₁ ≥ 0 "
  "(tasas larga y corta no negativas) y α acotado, porque sin esas condiciones en 2022 y 2026 el ajuste mejoraba apenas "
  "0,2 a 1 pb con parámetros sin sentido económico.")

H("4.2 Resultados y comparación del ajuste", 2)
pt = par[["NS b0", "NS b1", "NS b2", "NS a1", "SV b0", "SV b1", "SV b2", "SV b3", "SV a1", "SV a2",
          "RMSE NS (pb)", "RMSE SV (pb)"]].copy()
pt.columns = ["β₀", "β₁", "β₂", "α₁", "β₀ ", "β₁ ", "β₂ ", "β₃", "α₁ ", "α₂", "RMSE NS", "RMSE SV"]
pt.index.name = "Junio"
TAB(pt, "Parámetros de Nelson-Siegel (columnas 2–5) y Svensson (6–11), y RMSE en puntos base",
    fmt={c: (lambda v: pb(v, 2)) for c in pt.columns[:10]} | {"RMSE NS": lambda v: pb(v, 1), "RMSE SV": lambda v: pb(v, 1)},
    size=7.2, nota="β en %, α en años. RMSE = √(promedio de los errores al cuadrado), en puntos base.")
FIG("F16_ajustes_NS_SV.png", 16.5, "Curvas observadas (puntos), Nelson-Siegel (azul) y Svensson (rojo).")
P("**¿En qué fechas y en qué parte de la curva mejora Svensson?**")
BUL([
    f"**En todas las fechas**, porque NS es un caso particular de Svensson (β₃ = 0): el RMSE baja entre "
    f"{pb(par['Mejora RMSE (%)'].min())}% ({par['Mejora RMSE (%)'].idxmin()}) y {pb(par['Mejora RMSE (%)'].max())}% "
    f"({par['Mejora RMSE (%)'].idxmax()}). Las mayores mejoras son en 2018, 2025, 2026, 2017, 2024 y 2023.",
    "**En el extremo corto (1 a 6 meses)** en 2017, 2018, 2020, 2025 y 2026: una curvatura muy rápida que NS no puede "
    "seguir con el mismo α que usa para el tramo medio (en 2025 por recortes esperados y en 2026 por alzas esperadas).",
    "**En el tramo de 20 años desde 2021:** el bono a 20 años rinde más que el de 30 (3,38% vs. 3,14% en 2022; 4,06% vs. "
    "3,85% en 2023) por su menor demanda y liquidez desde su reintroducción en 2020. Esa joroba larga requiere el segundo "
    f"término. La peor fecha para ambos es 2022 (NS {pb(par.loc['2022', 'RMSE NS (pb)'], 1)} pb): la curva subía fuerte hasta "
    "1 año, era plana después y estaba a días de invertirse.",
])

H("4.3 Evolución de β₀, β₁ y β₂", 2)
FIG("F18_parametros_NS.png", 14.5, "Parámetros de Nelson-Siegel y sus contrapartes observadas.")
BUL([
    f"**β₀ (nivel):** cerca de 3% en 2017–2019, mínimo de {pb(par.loc['2020', 'NS b0'], 2)}% en 2020 (pandemia y compras de "
    f"bonos de la Fed) y luego sube hasta {pb(par.loc['2026', 'NS b0'], 2)}% en 2026. Sigue a la tasa a 30 años y refleja "
    "más inflación esperada y una mayor prima por plazo (déficit fiscal, más emisión, rebajas de calificación).",
    f"**β₁ (pendiente):** negativo (curva normal) en casi todos los años, con el valor más negativo en 2021 "
    f"({pb(par.loc['2021', 'NS b1'], 2)}); positivo en 2023 ({pb(par.loc['2023', 'NS b1'], 2)}) y 2024 "
    f"({pb(par.loc['2024', 'NS b1'], 2)}), los años de curva invertida. R(0) = β₀ + β₁ sigue a la tasa de la Fed.",
    f"**β₂ (curvatura):** casi 0 en 2017–2018 (curvas monótonas), negativo en 2019–2022 (valle), muy positivo en 2023 "
    f"({pb(par.loc['2023', 'NS b2'], 2)}, joroba en 6 meses en el peak de las alzas) y en su mínimo en 2025 "
    f"({pb(par.loc['2025', 'NS b2'], 2)}, curva en forma de \"bañera\").",
])

H("4.4 Evolución de la curva 2017–2026", 2)
FIG("F21_spreads_inversion.png", 15.5,
    "Arriba: tasas del Tesoro, tasa de fondos federales e inflación. Abajo: pendientes 10A − 3M y 10A − 2A "
    "(sombreado rojo: curva invertida; gris: recesión de 2020).")
P("El extremo corto de la curva lo fija la política de la Fed y el largo, las expectativas de inflación y crecimiento y "
  "la prima por plazo. Entre 2017 y 2026 la curva pasó por cinco etapas:")
P("**2017–2018: normalización.** Con pleno empleo, la Fed subió gradualmente la tasa (hasta 2,25–2,50% en dic-2018) y "
  "comenzó a reducir su balance, mientras la reforma tributaria ampliaba el déficit. La inflación bajo 2% y las tasas "
  "negativas en Europa y Japón contenían las tasas largas, así que la curva se aplanó: en junio de 2018 el diferencial "
  "10A − 2A era de solo 33 pb. En julio de 2018 comenzó la guerra comercial con China.")
P("**2019: primera inversión.** La escalada arancelaria y la desaceleración global hundieron las tasas largas. En junio "
  "la curva tenía forma de U (2,18% a 1 mes, 1,71% a 3 años) y 10A − 3M era −12 pb: el mercado esperaba recortes, y la "
  "Fed recortó tres veces entre julio y octubre.")
P("**2020–2021: pandemia y reapertura.** Con el COVID-19 la Fed llevó la tasa a 0–0,25% y compró bonos sin límite; "
  "hubo una recesión entre febrero y abril de 2020. En junio de 2020 todo el tramo hasta 3 años estaba bajo 0,2%. En 2021, "
  "las vacunas, el estímulo fiscal y una inflación que superó 5% subieron las tasas largas con las cortas aún en cero: "
  "fue la curva más empinada de la muestra (10A − 3M = +140 pb).")
P("**2022–2024: inflación y la inversión más larga en 40 años.** La invasión de Ucrania llevó la inflación a 9,1% y la "
  "Fed subió la tasa de 0% a 5,25–5,50% (julio de 2023), con alzas de 75 pb. En junio de 2022 la curva subía fuerte hasta "
  "1 año y era plana después; se invirtió días más tarde. En junio de 2023 la inversión era máxima (10A − 3M = −162 pb), "
  "tras la quiebra de Silicon Valley Bank y la disputa por el techo de deuda. En 2024 la inflación bajó y la Fed recortó "
  "desde septiembre, pero en junio la curva seguía invertida (−112 pb).")
P("**2025–2026: aranceles, déficit y shock petrolero.** Los aranceles de abril de 2025, la pérdida de la nota AAA de "
  "EE.UU. (Moody's) y una ley fiscal que amplió el déficit subieron la prima por plazo. En junio de 2025 la curva tenía "
  "forma de bañera: corto invertido (se esperaban recortes, que llegaron en sep–dic 2025) y largo empinado. En 2026, la "
  "guerra entre EE.UU., Israel e Irán (desde el 28 de febrero) disparó el petróleo y la inflación llegó a 4,2% en mayo; "
  "Kevin Warsh asumió la presidencia de la Fed. En junio de 2026 la curva era normal y creciente, con el nivel más alto de "
  "la muestra y alzas ya descontadas en el tramo corto. La Fed subió la tasa el 16 de septiembre y el bono a 10 años "
  "superó 5% por primera vez desde 2007.")

H("4.5 Inversiones de la curva: qué anticipaban y si ocurrió", 2)
P("Entre las fechas de junio, la curva estaba invertida en **2019** (10A − 3M = −12 pb), **2023** (−162 pb), **2024** "
  "(−112 pb) y **2025** (−17 pb, solo en el tramo corto). Una inversión indica que el mercado espera tasas cortas futuras "
  "más bajas, típicamente porque la Fed recortará frente a una desaceleración; históricamente precedió a las recesiones "
  "de EE.UU. Los episodios en los datos diarios:")
tab_ep = pd.DataFrame([
    {"Episodio (10A − 3M)": "may–oct 2019", "Mínimo": "−52 pb", "Anticipaba": "Recortes y recesión por la guerra comercial",
     "¿Ocurrió?": "Recortes sí (75 pb). Recesión sí en 2020, pero causada por la pandemia"},
    {"Episodio (10A − 3M)": "ene–mar 2020", "Mínimo": "−20 pb", "Anticipaba": "Huida a la calidad y recortes de emergencia",
     "¿Ocurrió?": "Sí: tasa a cero y recesión"},
    {"Episodio (10A − 3M)": "oct-2022 a dic-2024 (10A − 2A: jul-2022 a sep-2024)", "Mínimo": "−189 pb",
     "Anticipaba": "Recesión por las alzas y recortes posteriores",
     "¿Ocurrió?": "Recortes sí (175 pb entre sep-2024 y dic-2025). Recesión no, al menos hasta oct-2026"},
    {"Episodio (10A − 3M)": "feb–sep 2025", "Mínimo": "−27 pb", "Anticipaba": "Recortes por el efecto de los aranceles",
     "¿Ocurrió?": "Recortes sí (75 pb). Recesión no"},
]).set_index("Episodio (10A − 3M)")
TAB(tab_ep, "Episodios de inversión 2017–2026 y su resultado", size=8, anchos=[4.0, 1.6, 4.8, 6.6])
P("La señal de 2022–2024 falló en anticipar una recesión porque la inversión reflejaba sobre todo la baja esperada de "
  "la inflación, la prima por plazo estaba deprimida por años de compras de bonos de la Fed, hogares y empresas habían "
  "fijado tasas bajas en 2020–2021 y el déficit fiscal sostuvo el crecimiento. En 2026 la pendiente es positiva por un "
  "\"empinamiento bajista\": suben más las tasas largas, por inflación y riesgo fiscal, y no por una expectativa de recesión.")

# =============================================================================
# 5. CONCLUSIONES
# =============================================================================
H("5. Conclusiones", 1)
BUL([
    "La diversificación de Markowitz reduce mucho el riesgo, y las covarianzas son su núcleo: ignorarlas subestima el "
    "riesgo y elimina la posibilidad de cubrirse.",
    "Las restricciones generan mini-fronteras dentro de la original; su costo es bajo cerca del GMV y alto en retornos altos.",
    "El portafolio de tangencia y su alfa de Jensen (78% anual, t = 5,6) reflejan el error de estimación de las medias y el "
    "uso de los mismos datos para construir y evaluar M, no ineficiencia del mercado.",
    "Nelson-Siegel describe bien la curva del Tesoro y sus parámetros siguen al nivel, la pendiente y la curvatura; "
    "Svensson mejora el extremo corto y el tramo de 20 años. Las inversiones anticiparon bien los recortes de la Fed, pero "
    "la de 2022–2024 no fue seguida por una recesión.",
])

H("Referencias", 1)
for r_ in [
    "Bodie, Z., Kane, A. y Marcus, A. (2017). *Investments*, 11.ª ed. McGraw-Hill.",
    "Bernales, A. (2026). *Finanzas I – ENFIN415, Sesión I*. Universidad de Chile.",
    "Michaud, R. (1989). The Markowitz optimization enigma: is 'optimized' optimal? *Financial Analysts Journal*, 45(1).",
    "Nelson, C. y Siegel, A. (1987). Parsimonious modeling of yield curves. *Journal of Business*, 60(4).",
    "Svensson, L. (1994). Estimating and interpreting forward interest rates: Sweden 1992–1994. NBER WP 4871.",
    "Datos: Federal Reserve Board, H.15 Selected Interest Rates; Yahoo Finance; U.S. Bureau of Labor Statistics (IPC).",
    "Hechos de 2026: Federal Reserve, comunicado FOMC del 16-sep-2026; BEA, PIB del 2.º trimestre de 2026; CNBC (15-sep-2026 "
    "y 10-jun-2026) y CNN (22-may-2026).",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(2.5)
    runs(p, r_, size=9)

# =============================================================================
# ANEXO
# =============================================================================
H("Anexo. Retorno esperado, volatilidad y beta de cada acción (anual, ago-2021 a jul-2026)", 1)
ta = est[["Sector", "Retorno esperado anual", "Volatilidad anual", "Beta vs S&P 500"]].copy()
ta["Sector"] = ta["Sector"].map(SECTOR_CORTO)
ta.columns = ["Sector", "μ anual", "σ anual", "β"]
mitad = (len(ta) + 1) // 2
izq, der = ta.iloc[:mitad].reset_index(), ta.iloc[mitad:].reset_index()
lado = pd.concat([izq, der], axis=1)
lado.columns = ["Ticker", "Sector", "μ", "σ", "β", "Ticker ", "Sector ", "μ ", "σ ", "β "]
TAB(lado, "Estadísticas anuales de las 50 acciones (la matriz de covarianzas está en Resultados_Pregunta1A.xlsx)",
    fmt={c: pc for c in ["μ", "σ", "μ ", "σ "]} | {c: nu for c in ["β", "β "]}, size=7.4, indice=False,
    anchos=[1.2, 2.9, 1.3, 1.3, 1.0, 1.2, 2.9, 1.3, 1.3, 1.0])
P("**Archivos entregados:** carpeta *codigo* (scripts de Python 01 a 04 con los cálculos, comentados paso a paso), *datos* (datos "
  "descargados) y *resultados* (figuras y planillas Excel *Resultados_Pregunta1A/1B/2.xlsx*). Instrucciones en *Instrucciones_y_contenido.txt*.",
  size=9)

salida = BASE / "Informe_Tarea_ENFIN415.docx"
doc.save(salida)
print("Informe guardado en", salida)
