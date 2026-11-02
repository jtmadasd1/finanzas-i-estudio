# =============================================================================
#  03_pregunta_1B.py  -  Pregunta 1B: LMC, modelo indice y desempeno
#  Calcula los puntos 1 a 4 y guarda la figura F09 y Resultados_Pregunta1B.xlsx
# =============================================================================
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import DATOS, DIAS_ANIO, FECHA_RF, FIGURAS, TABLAS
from utilidades import (COLORES, PCT, FronteraAnalitica, cargar_retornos,
                        guardar_fig, momentos_anuales, sectores,
                        tangencia_restringida)

sys.stdout.reconfigure(encoding="utf-8")
rng = np.random.default_rng(2026)      # semilla fija para la simulacion del punto 2

# -----------------------------------------------------------------------------
# Tasa libre de riesgo: Treasury constant maturity a 1 año del 31-jul-2026.
# El H.15 la publica en base "equivalente a bono" (capitalizacion semestral);
# como los retornos de las acciones son continuos, se convierte:
#     rf = 2 * ln(1 + y/2)
# -----------------------------------------------------------------------------
h15 = pd.read_csv(DATOS / "tasas_h15.csv", index_col=0, parse_dates=True)
y1 = h15.loc[FECHA_RF, "RIFLGFCY01_N.B"] / 100
rf = 2 * np.log(1 + y1 / 2)
rf_d = rf / DIAS_ANIO                   # tasa diaria para la regresion
print(f"rf publicada {y1:.2%} -> continua {rf:.3%}")

# -----------------------------------------------------------------------------
# 1) LMC y portafolio de tangencia M (maximo Sharpe con ventas cortas)
#    w_M = O^-1 (mu - rf 1) / 1'O^-1 (mu - rf 1)
#    LMC: E[Rp] = rf + Sharpe_M * sigma_p
# -----------------------------------------------------------------------------
r, rsp = cargar_retornos()
mu, sig, omega = momentos_anuales(r)
sec = sectores()
tick = list(mu.index)
F = FronteraAnalitica(mu.values, omega.values)
wM, muM, sM, SRM = F.tangencia(rf)
print(f"M: mu={muM:.1%} sigma={sM:.1%} Sharpe={SRM:.2f} | largos {wM[wM > 0].sum():.0%}, "
      f"cortos {wM[wM < 0].sum():.0%}, exposicion bruta {np.abs(wM).sum():.1f}x")

pesosM = pd.DataFrame({"Sector": sec.loc[tick], "Peso en M": wM,
                       "Retorno esperado": mu, "Volatilidad": sig}, index=tick)
pesosM = pesosM.sort_values("Peso en M", ascending=False)

# Maximo Sharpe con restricciones (para comparar en la figura)
tang_lim = tangencia_restringida(mu.values, omega.values, rf, "limite", lim=0.10)
tang_lo = tangencia_restringida(mu.values, omega.values, rf, "sin_vc")
print(f"Maximo Sharpe con |w|<=10%: {tang_lim[3]:.2f} | sin venta corta: {tang_lo[3]:.2f}")

# S&P 500 en la misma ventana
mu_sp = rsp["SP500"].mean() * DIAS_ANIO
s_sp = rsp["SP500"].std() * np.sqrt(DIAS_ANIO)

mus = np.linspace(-0.3, 1.2, 301)
sig_f = F.sigma(mus)
eff = mus >= F.mu_gmv
fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.plot(sig_f[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Frontera eficiente (P1A.2)")
ax.plot(sig_f[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
xs = np.linspace(0, 0.6, 50)
ax.plot(xs, rf + SRM * xs, color=COLORES["lmc"], lw=1.6, label=f"LMC: E[R] = {rf:.2%} + {SRM:.2f}·σ")
ax.scatter([sM], [muM], s=90, marker="*", color="#c0392b", zorder=6,
           label=f"Tangencia M (σ={sM:.1%}, μ={muM:.1%}, Sharpe={SRM:.2f})")
ax.scatter([0], [rf], s=40, color="k", zorder=6, label=f"Activo libre de riesgo rf={rf:.2%}")
ax.scatter([s_sp], [mu_sp], s=60, marker="s", color=COLORES["sp500"], zorder=6,
           label=f"S&P 500 (σ={s_sp:.1%}, μ={mu_sp:.1%})")
ax.plot(xs, rf + (mu_sp - rf) / s_sp * xs, color=COLORES["sp500"], lw=1, ls=":",
        label=f"Línea de transformación con el S&P 500 (Sharpe={(mu_sp - rf) / s_sp:.2f})")
ax.scatter(sig, mu, s=12, color=COLORES["gris"], alpha=0.55, label="Acciones individuales")
ax.scatter([tang_lo[2]], [tang_lo[1]], marker="^", s=55, zorder=6, color=COLORES["sin_vc"],
           label=f"Máx. Sharpe Sin venta corta (Sharpe={tang_lo[3]:.2f})")
ax.scatter([tang_lim[2]], [tang_lim[1]], marker="v", s=55, zorder=6, color=COLORES["limite10"],
           label=f"Máx. Sharpe |w|≤10% (Sharpe={tang_lim[3]:.2f})")
ax.set_xlim(0, 0.6); ax.set_ylim(-0.1, 1.2)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("P1B.1 – Línea de Mercado de Capitales y portafolio de tangencia M")
ax.legend(loc="upper left", fontsize=7.3)
guardar_fig(fig, FIGURAS / "F09_LMC_tangencia.png")

# -----------------------------------------------------------------------------
# 2) Modelo indice de M con datos diarios (MCO) y test-t de alfa = 0:
#    r_M,t - rf = alfa + beta (r_SP500,t - rf) + e_t
# -----------------------------------------------------------------------------
rM = r.values @ wM                      # retorno diario de M
exM = rM - rf_d
exSP = rsp["SP500"].values - rf_d
ols = sm.OLS(exM, sm.add_constant(exSP)).fit()
alfa_d, beta_M = ols.params
print(ols.summary())
print(f"alfa = {alfa_d:.5f} diario ({alfa_d * DIAS_ANIO:.1%} anual), t = {ols.tvalues[0]:.2f} "
      f"(valor critico 1,96) -> {'se rechaza' if abs(ols.tvalues[0]) > 1.96 else 'no se rechaza'} alfa = 0")
modelo_indice = pd.DataFrame({
    "Estimacion": [alfa_d, alfa_d * DIAS_ANIO, beta_M],
    "Error estandar": [ols.bse[0], ols.bse[0] * DIAS_ANIO, ols.bse[1]],
    "t": [ols.tvalues[0], ols.tvalues[0], ols.tvalues[1]],
    "valor p": [ols.pvalues[0], ols.pvalues[0], ols.pvalues[1]],
}, index=["alfa diario", "alfa anual (x252)", "beta"])
modelo_indice.loc["R2", "Estimacion"] = ols.rsquared

# 2b) ¿Que pasa por usar los mismos datos para construir y evaluar M?
#     Simulamos 1.000 muestras de 5 años con la misma matriz de covarianzas
#     pero con todos los alfas verdaderos = 0 (medias segun CAPM), y en cada
#     una repetimos el procedimiento: armar M con esos datos y testear su alfa.
R_all = np.column_stack([r.values, rsp["SP500"].values])
cov_d = np.cov(R_all, rowvar=False)
beta_i = cov_d[:-1, -1] / cov_d[-1, -1]
mu_sp_d = rsp["SP500"].mean()
mu_h0 = np.append(rf_d + beta_i * (mu_sp_d - rf_d), mu_sp_d)
L = np.linalg.cholesky(cov_d)
T = len(exM)
t_sim = []
for _ in range(1000):
    Z = rng.standard_normal((T, R_all.shape[1])) @ L.T + mu_h0
    Rs, sps = Z[:, :-1], Z[:, -1]
    w_ = np.linalg.solve(np.cov(Rs, rowvar=False) * DIAS_ANIO, Rs.mean(0) * DIAS_ANIO - rf)
    w_ = w_ / w_.sum()
    t_sim.append(sm.OLS(Rs @ w_ - rf_d, sm.add_constant(sps - rf_d)).fit().tvalues[0])
t_sim = np.abs(np.array(t_sim))
print(f"Simulacion con alfa verdadero = 0: t promedio {t_sim.mean():.2f}, "
      f"{(t_sim > 1.96).mean():.0%} de los casos 'rechaza' alfa = 0")

# 2c) Fuera de muestra: armar M con datos hasta jul-2025 y ver como le fue
#     entre ago-2025 y jul-2026 (sin volver a optimizar)
corte = "2025-07-31"
rf_c = 2 * np.log(1 + h15.loc[corte, "RIFLGFCY01_N.B"] / 100 / 2)
r_in, r_out = r.loc[:corte], r.loc[corte:].iloc[1:]
mu_in, _, om_in = momentos_anuales(r_in)
w_in, _, _, sr_prometido = FronteraAnalitica(mu_in.values, om_in.values).tangencia(rf_c)
# retorno diario exacto del portafolio: se suman retornos simples y se vuelve a log
r_out_M = np.log1p(np.maximum(np.expm1(r_out.values) @ w_in, -0.999999))
ret_acum = np.exp(r_out_M.sum()) - 1
print(f"Fuera de muestra: Sharpe prometido {sr_prometido:.2f}, retorno ago-25/jul-26 {ret_acum:.1%}")


# -----------------------------------------------------------------------------
# 3) Ratios de Sharpe y Treynor:  Sharpe = (E[R]-rf)/sigma ; Treynor = (E[R]-rf)/beta
# -----------------------------------------------------------------------------
def medidas(rp):
    b = sm.OLS(rp - rf_d, sm.add_constant(rsp["SP500"].values - rf_d)).fit().params[1]
    m = rp.mean() * DIAS_ANIO
    s = rp.std(ddof=1) * np.sqrt(DIAS_ANIO)
    return {"μ anual": m, "σ anual": s, "β": b, "Sharpe": (m - rf) / s, "Treynor": (m - rf) / b}


sharpe_treynor = pd.DataFrame({
    "Portafolio de tangencia M": medidas(rM),
    "S&P 500": medidas(rsp["SP500"].values),
    "JNJ (ejemplo de ranking distinto)": medidas(r["JNJ"].values),
}).T
print(sharpe_treynor.round(4).to_string())

# -----------------------------------------------------------------------------
# 4) Asignacion optima entre M y rf (max U = E - c/2 sigma^2):
#    x* = (E[R_M] - rf) / (c sigma_M^2);  x* > 1 pide prestado, x* < 1 presta
# -----------------------------------------------------------------------------
asignacion = []
for c in (2, 5, 10):
    x = (muM - rf) / (c * sM ** 2)
    asignacion.append({"c": c, "x* (en M)": x, "1 - x* (en rf)": 1 - x,
                       "Posicion": "Pide prestado (borrowing)" if x > 1 else "Presta (lending)",
                       "E[R_C]": rf + x * (muM - rf), "sigma_C": x * sM,
                       "x* si se usa el S&P 500": (mu_sp - rf) / (c * s_sp ** 2)})
asignacion = pd.DataFrame(asignacion)
print(asignacion.round(4).to_string())

# -----------------------------------------------------------------------------
# Guardar en Excel
# -----------------------------------------------------------------------------
with pd.ExcelWriter(TABLAS / "Resultados_Pregunta1B.xlsx") as xw:
    pd.DataFrame({"rf publicada (1 año, 31-jul-2026)": [y1], "rf continua": [rf]}).to_excel(
        xw, sheet_name="rf", index=False)
    pesosM.to_excel(xw, sheet_name="1_Pesos_M")
    pd.DataFrame({"M": [muM, sM, SRM], "Max Sharpe |w|<=10%": list(tang_lim[1:]),
                  "Max Sharpe sin venta corta": list(tang_lo[1:])},
                 index=["mu", "sigma", "Sharpe"]).to_excel(xw, sheet_name="1_Tangencias")
    modelo_indice.to_excel(xw, sheet_name="2_Modelo_indice")
    pd.DataFrame({"Fecha": r.index, "exceso_M": exM, "exceso_SP500": exSP}).to_excel(
        xw, sheet_name="2_Datos_regresion", index=False)
    pd.DataFrame({"valor": [t_sim.mean(), (t_sim > 1.96).mean(), sr_prometido, ret_acum]},
                 index=["t promedio simulado (alfa=0)", "% simulaciones que rechazan",
                        "Sharpe prometido M (datos hasta jul-2025)",
                        "Retorno real de M ago-2025 a jul-2026"]).to_excel(xw, sheet_name="2_Mismos_datos")
    sharpe_treynor.to_excel(xw, sheet_name="3_Sharpe_Treynor")
    asignacion.to_excel(xw, sheet_name="4_Asignacion_optima", index=False)
print("Listo: Resultados_Pregunta1B.xlsx y figura F09")
