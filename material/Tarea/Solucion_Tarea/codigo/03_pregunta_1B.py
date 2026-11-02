# =============================================================================
#  03_pregunta_1B.py  -  PREGUNTA 1B: LMC, MODELO INDICE Y DESEMPENO
#   1. Linea de Mercado de Capitales y portafolio de tangencia M
#      (rf = tasa Treasury constant maturity a 1 anio, 31-jul-2026, Fed H.15)
#   2. Modelo indice  r_M,t - rf = alpha + beta (r_SP500,t - rf) + e_t
#      + test-t de alfa de Jensen, analisis del sesgo "in-sample"
#   3. Ratios de Sharpe y Treynor de M y del S&P 500
#   4. Asignacion optima x* = (E[R_M] - rf) / (c sigma_M^2), c = 2, 5, 10
# =============================================================================
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import (DATOS, DIAS_ANIO, FECHA_RF, FIGURAS, PESO_MIN_SECTORES,
                    RESULTADOS, SECTORES_RESTRICCION, TABLAS)

sys.stdout.reconfigure(encoding="utf-8")
from utilidades import (COLOR_SECTOR, COLORES, PCT, FronteraAnalitica,
                        cargar_retornos, guardar_fig, guardar_json,
                        momentos_anuales, sectores, tangencia_restringida)

rng = np.random.default_rng(2026)

# -----------------------------------------------------------------------------
# Tasa libre de riesgo
# -----------------------------------------------------------------------------
h15 = pd.read_csv(DATOS / "tasas_h15.csv", index_col=0, parse_dates=True)
y1 = h15.loc[FECHA_RF, "RIFLGFCY01_N.B"] / 100     # 1 anio, 31-jul-2026
# Las tasas H.15 de notas/bonos estan en base "bond-equivalent" (capitalizacion
# semestral).  Como los retornos de las acciones son continuos, se convierte:
rf = 2 * np.log(1 + y1 / 2)
rf_d = rf / DIAS_ANIO                              # tasa diaria (constante)
print(f"rf 1 anio (31-jul-2026): {y1:.4%} publicada -> {rf:.4%} continua")

# -----------------------------------------------------------------------------
# 1) LMC y portafolio de tangencia
# -----------------------------------------------------------------------------
r, rsp = cargar_retornos()
mu, sig, omega = momentos_anuales(r)
sec = sectores()
tick = list(mu.index)
F = FronteraAnalitica(mu.values, omega.values)
wM, muM, sM, SRM = F.tangencia(rf)
print(f"Tangencia M: mu={muM:.4f} sigma={sM:.4f} Sharpe={SRM:.4f} exp.bruta={np.abs(wM).sum():.2f}")

pesosM = pd.DataFrame({"Sector": sec.loc[tick], "Peso en M": wM,
                       "Retorno esperado": mu, "Volatilidad": sig}, index=tick)
pesosM = pesosM.sort_values("Peso en M", ascending=False)
pesosM.to_csv(TABLAS / "1B1_pesos_tangencia.csv")
peso_sector_M = pesosM.groupby("Sector")["Peso en M"].agg(
    neto="sum", largos=lambda s: s[s > 0].sum(), cortos=lambda s: s[s < 0].sum())

# Tangencias de las fronteras restringidas (para la discusion)
mask = sec.loc[tick].isin(SECTORES_RESTRICCION).values.astype(float)
tang_rest = {}
for k, kw, nom in [("limite", {"lim": 0.10}, "|w|≤10%"), ("sin_vc", {}, "Sin venta corta"),
                   ("sin_vc_sector", {"sector_mask": mask, "piso": PESO_MIN_SECTORES},
                    "Sin VC + Ener/Ind≥40%")]:
    w_, m_, s_, sr_ = tangencia_restringida(mu.values, omega.values, rf, k, **kw)
    tang_rest[k] = {"nombre": nom, "w": w_, "mu": m_, "sigma": s_, "sharpe": sr_,
                    "n_acciones": int((np.abs(w_) > 1e-3).sum())}
    print(f"Tangencia {nom}: mu={m_:.4f} sigma={s_:.4f} SR={sr_:.4f} n={tang_rest[k]['n_acciones']}")

# Rendimiento del S&P 500 en la misma ventana
mu_sp = rsp["SP500"].mean() * DIAS_ANIO
s_sp = rsp["SP500"].std() * np.sqrt(DIAS_ANIO)
mu_sptr = rsp["SP500_TR"].mean() * DIAS_ANIO

# Figura LMC
mus = np.linspace(-0.3, 1.2, 301)
sig_f = F.sigma(mus)
eff = mus >= F.mu_gmv
fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.plot(sig_f[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Frontera eficiente (P1A.2)")
ax.plot(sig_f[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
xs = np.linspace(0, 0.6, 50)
ax.plot(xs, rf + SRM * xs, color=COLORES["lmc"], lw=1.6,
        label=f"LMC: E[R] = {rf:.2%} + {SRM:.2f}·σ")
ax.scatter([sM], [muM], s=90, marker="*", color="#c0392b", zorder=6,
           label=f"Tangencia M (σ={sM:.1%}, μ={muM:.1%}, Sharpe={SRM:.2f})")
ax.scatter([0], [rf], s=40, color="k", zorder=6, label=f"Activo libre de riesgo rf={rf:.2%}")
ax.scatter([s_sp], [mu_sp], s=60, marker="s", color=COLORES["sp500"], zorder=6,
           label=f"S&P 500 (σ={s_sp:.1%}, μ={mu_sp:.1%})")
ax.plot(xs, rf + (mu_sp - rf) / s_sp * xs, color=COLORES["sp500"], lw=1, ls=":",
        label=f"Línea de transformación con el S&P 500 (Sharpe={(mu_sp - rf) / s_sp:.2f})")
ax.scatter(sig, mu, s=12, color=COLORES["gris"], alpha=0.55, label="Acciones individuales")
for k, mk in [("sin_vc", "^"), ("limite", "v")]:
    t_ = tang_rest[k]
    ax.scatter([t_["sigma"]], [t_["mu"]], marker=mk, s=55, zorder=6,
               color=COLORES["sin_vc"] if k == "sin_vc" else COLORES["limite10"],
               label=f"Máx. Sharpe {t_['nombre']} (Sharpe={t_['sharpe']:.2f})")
ax.set_xlim(0, 0.6); ax.set_ylim(-0.1, 1.2)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("P1B.1 – Línea de Mercado de Capitales y portafolio de tangencia M")
ax.legend(loc="upper left", fontsize=7.3)
guardar_fig(fig, FIGURAS / "F09_LMC_tangencia.png")

# Figura: pesos de M
fig, ax = plt.subplots(figsize=(11, 4.3))
pm = pesosM["Peso en M"]
ax.bar(range(len(pm)), pm.values, color=[COLOR_SECTOR[s_] for s_ in pesosM["Sector"]])
ax.set_xticks(range(len(pm))); ax.set_xticklabels(pm.index, rotation=90, fontsize=7)
ax.yaxis.set_major_formatter(PCT); ax.axhline(0, color="k", lw=0.6)
ax.set_ylabel("Peso en M")
ax.set_title(f"Pesos del portafolio de tangencia M (largos: {pm[pm > 0].sum():.0%}, "
             f"cortos: {pm[pm < 0].sum():.0%}, exposición bruta: {pm.abs().sum():.1f}x)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=s_) for s_, c in COLOR_SECTOR.items()],
          ncol=4, fontsize=7, loc="upper right")
guardar_fig(fig, FIGURAS / "F10_pesos_tangencia.png")

# -----------------------------------------------------------------------------
# 2) Modelo indice para M:  r_M,t - rf = alpha + beta (r_SP,t - rf) + e_t
# -----------------------------------------------------------------------------
rM = r.values @ wM                                   # retorno diario de M
exM = rM - rf_d
exSP = rsp["SP500"].values - rf_d
X = sm.add_constant(exSP)
ols = sm.OLS(exM, X).fit()
hac = sm.OLS(exM, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
ols_tr = sm.OLS(exM, sm.add_constant(rsp["SP500_TR"].values - rf_d)).fit()
T = len(exM)
alfa_d, beta_M = ols.params
modelo_indice = {
    "alfa_diario": alfa_d, "alfa_anual": alfa_d * DIAS_ANIO, "beta": beta_M,
    "ee_alfa": ols.bse[0], "t_alfa": ols.tvalues[0], "p_alfa": ols.pvalues[0],
    "ee_beta": ols.bse[1], "t_beta": ols.tvalues[1],
    "t_beta_igual_1": (beta_M - 1) / ols.bse[1],
    "t_alfa_HAC": hac.tvalues[0], "p_alfa_HAC": hac.pvalues[0],
    "R2": ols.rsquared, "sigma_e_anual": np.sqrt(ols.mse_resid * DIAS_ANIO),
    "T": T, "gl": int(ols.df_resid),
    "alfa_anual_SPTR": ols_tr.params[0] * DIAS_ANIO, "t_alfa_SPTR": ols_tr.tvalues[0],
    "beta_SPTR": ols_tr.params[1],
}
modelo_indice["ratio_informacion"] = modelo_indice["alfa_anual"] / modelo_indice["sigma_e_anual"]
modelo_indice["IR_teorico"] = np.sqrt(max(SRM ** 2 - ((mu_sp - rf) / s_sp) ** 2, 0))
print(ols.summary())

fig, ax = plt.subplots(figsize=(7.6, 5.4))
ax.scatter(exSP, exM, s=6, alpha=0.35, color=COLORES["frontera"])
xx = np.linspace(exSP.min(), exSP.max(), 10)
ax.plot(xx, alfa_d + beta_M * xx, color="#c0392b", lw=2,
        label=f"α = {alfa_d:.5f} diario ({alfa_d * DIAS_ANIO:.1%} anual, t = {ols.tvalues[0]:.2f})\n"
              f"β = {beta_M:.3f} (t = {ols.tvalues[1]:.2f}),  R² = {ols.rsquared:.3f}")
ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Exceso de retorno diario del S&P 500"); ax.set_ylabel("Exceso de retorno diario de M")
ax.set_title("P1B.2 – Modelo índice del portafolio de tangencia (ago-2021 a jul-2026)")
ax.legend(loc="upper left", fontsize=8.5)
guardar_fig(fig, FIGURAS / "F11_modelo_indice.png")

# ---- 2b) Sesgo por usar los mismos datos: simulacion bajo H0 (alfa = 0) ----
# Se simulan 5 anios de retornos con la MISMA matriz de covarianzas observada,
# pero con medias "CAPM puras": mu_i = rf + beta_i (mu_SP - rf)  (todos los
# alfas verdaderos = 0).  En cada simulacion se repite exactamente nuestro
# procedimiento: estimar M con esos datos y testear su alfa con esos datos.
R_all = np.column_stack([r.values, rsp["SP500"].values])
cov_d = np.cov(R_all, rowvar=False)
beta_i = cov_d[:-1, -1] / cov_d[-1, -1]
mu_sp_d = rsp["SP500"].mean()
mu_h0 = np.append(rf_d + beta_i * (mu_sp_d - rf_d), mu_sp_d)
L = np.linalg.cholesky(cov_d)
N_SIM = 1000
t_sim, sr_sim, alfa_sim = [], [], []
for _ in range(N_SIM):
    Z = rng.standard_normal((T, R_all.shape[1])) @ L.T + mu_h0
    Rs, sps = Z[:, :-1], Z[:, -1]
    m_ = Rs.mean(0) * DIAS_ANIO
    O_ = np.cov(Rs, rowvar=False) * DIAS_ANIO
    w_ = np.linalg.solve(O_, m_ - rf)
    w_ = w_ / w_.sum()
    rp = Rs @ w_
    sr_sim.append((rp.mean() * DIAS_ANIO - rf) / (rp.std(ddof=1) * np.sqrt(DIAS_ANIO)))
    fit = sm.OLS(rp - rf_d, sm.add_constant(sps - rf_d)).fit()
    t_sim.append(fit.tvalues[0]); alfa_sim.append(fit.params[0] * DIAS_ANIO)
t_sim, sr_sim, alfa_sim = map(np.array, (t_sim, sr_sim, alfa_sim))
# Nota: si la suma de pesos cambia de signo el "portafolio" puede invertirse;
# se usa |Sharpe| como en la literatura para la distribucion del maximo Sharpe.
sim_h0 = {
    "N_sim": N_SIM, "t_alfa_media": float(np.mean(np.abs(t_sim))),
    "t_alfa_p05": float(np.percentile(np.abs(t_sim), 5)),
    "t_alfa_p95": float(np.percentile(np.abs(t_sim), 95)),
    "pct_t_mayor_196": float(np.mean(np.abs(t_sim) > 1.96)),
    "sharpe_media": float(np.mean(np.abs(sr_sim))),
    "sharpe_p95": float(np.percentile(np.abs(sr_sim), 95)),
    "pct_sharpe_mayor_obs": float(np.mean(np.abs(sr_sim) >= SRM)),
    "pct_t_mayor_obs": float(np.mean(np.abs(t_sim) >= abs(ols.tvalues[0]))),
    "sharpe_esperado_teorico": float(np.sqrt(((mu_sp - rf) / s_sp) ** 2 + 50 * DIAS_ANIO / T)),
}
print("Simulacion H0:", sim_h0)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].hist(np.abs(t_sim), bins=40, color=COLORES["gris"], alpha=0.85)
axes[0].axvline(abs(ols.tvalues[0]), color="#c0392b", lw=2, label=f"t(α) observado = {ols.tvalues[0]:.2f}")
axes[0].axvline(1.96, color="k", ls="--", lw=1, label="Valor crítico 5% (1,96)")
axes[0].set_xlabel("|t(α)| del portafolio de tangencia estimado"); axes[0].set_ylabel("Frecuencia")
axes[0].set_title("t de Jensen bajo H0 (α verdadero = 0)")
axes[0].legend(fontsize=8)
axes[1].hist(np.abs(sr_sim), bins=40, color=COLORES["gris"], alpha=0.85)
axes[1].axvline(SRM, color="#c0392b", lw=2, label=f"Sharpe observado de M = {SRM:.2f}")
axes[1].axvline((mu_sp - rf) / s_sp, color=COLORES["sp500"], lw=1.5, ls=":",
                label=f"Sharpe S&P 500 = {(mu_sp - rf) / s_sp:.2f}")
axes[1].set_xlabel("Sharpe in-sample del portafolio de tangencia"); axes[1].set_ylabel("Frecuencia")
axes[1].set_title("Sharpe in-sample bajo H0 (α verdadero = 0)")
axes[1].legend(fontsize=8)
fig.suptitle(f"Simulación de Monte Carlo ({N_SIM} muestras de 5 años, medias CAPM y Ω observada)",
             fontweight="bold")
guardar_fig(fig, FIGURAS / "F12_simulacion_H0.png")

# ---- 2c) Prueba fuera de muestra: estimar con ago-21/jul-25, evaluar ago-25/jul-26 ----
corte = "2025-07-31"
y1_c = h15.loc[corte, "RIFLGFCY01_N.B"] / 100
rf_c = 2 * np.log(1 + y1_c / 2)
r_in, r_out = r.loc[:corte], r.loc[corte:].iloc[1:]
sp_out = rsp.loc[r_out.index, "SP500"].values
mu_in, _, om_in = momentos_anuales(r_in)
F_in = FronteraAnalitica(mu_in.values, om_in.values)
w_in, mu_in_M, s_in_M, sr_in_M = F_in.tangencia(rf_c)
w_in_lo, mu_in_lo, s_in_lo, sr_in_lo = tangencia_restringida(mu_in.values, om_in.values, rf_c, "sin_vc")
w_eq = np.ones(len(tick)) / len(tick)


def ret_portafolio(r_log, w):
    """Retorno log EXACTO de un portafolio (rebalanceo diario): se agregan los
    retornos simples, R_p = sum w_i (e^{r_i} - 1), y luego r_p = ln(1 + R_p).
    Para la evaluacion fuera de muestra se usa esta version exacta porque M
    tiene mucho apalancamiento y la aproximacion sum w_i r_i deja de ser buena."""
    Rp = np.expm1(r_log) @ w
    return np.log1p(np.maximum(Rp, -0.999999))


def desempeno(rp, sp, rf_anual):
    rfd = rf_anual / DIAS_ANIO
    fit = sm.OLS(rp - rfd, sm.add_constant(sp - rfd)).fit()
    m = rp.mean() * DIAS_ANIO
    s = rp.std(ddof=1) * np.sqrt(DIAS_ANIO)
    return {"mu": m, "sigma": s, "sharpe": (m - rf_anual) / s, "beta": fit.params[1],
            "treynor": (m - rf_anual) / fit.params[1], "alfa_anual": fit.params[0] * DIAS_ANIO,
            "t_alfa": fit.tvalues[0], "R2": fit.rsquared,
            "retorno_acumulado": float(np.exp(rp.sum()) - 1)}


fuera_muestra = {
    "corte": corte, "rf_entrenamiento": rf_c, "n_dias_prueba": len(r_out),
    "M_in_sample_sharpe_prometido": sr_in_M, "M_LO_in_sample_sharpe_prometido": sr_in_lo,
    "M (sin restricciones)": desempeno(ret_portafolio(r_out.values, w_in), sp_out, rf_c),
    "M sin venta corta": desempeno(ret_portafolio(r_out.values, w_in_lo), sp_out, rf_c),
    "1/N": desempeno(ret_portafolio(r_out.values, w_eq), sp_out, rf_c),
    "S&P 500": desempeno(sp_out, sp_out, rf_c),
    "exp_bruta_M_in": float(np.abs(w_in).sum()),
}
print("Fuera de muestra:", {k: (v if not isinstance(v, dict) else {a: round(b, 3) for a, b in v.items()})
                            for k, v in fuera_muestra.items()})

fig, ax = plt.subplots(figsize=(8.6, 4.6))
fechas = r_out.index.insert(0, pd.Timestamp(corte))
for nom, rp_, col in [("M estimado con ago-21/jul-25 (sin restricciones)", ret_portafolio(r_out.values, w_in), "#c0392b"),
                      ("M sin venta corta estimado con ago-21/jul-25", ret_portafolio(r_out.values, w_in_lo), COLORES["sin_vc"]),
                      ("1/N (50 acciones)", ret_portafolio(r_out.values, w_eq), COLORES["gris"]),
                      ("S&P 500", sp_out, COLORES["sp500"])]:
    ax.plot(fechas, np.exp(np.concatenate([[0], np.cumsum(rp_)])), label=nom, color=col, lw=1.6)
ax.axhline(1, color="k", lw=0.5)
ax.set_ylabel("Valor de $1 invertido el 31-jul-2025")
ax.set_title("Prueba fuera de muestra (ago-2025 a jul-2026)")
ax.legend(fontsize=8)
guardar_fig(fig, FIGURAS / "F13_fuera_de_muestra.png")

# -----------------------------------------------------------------------------
# 3) Sharpe y Treynor
# -----------------------------------------------------------------------------
def medidas(rp, nombre):
    fit = sm.OLS(rp - rf_d, sm.add_constant(rsp["SP500"].values - rf_d)).fit()
    m = rp.mean() * DIAS_ANIO
    s = rp.std(ddof=1) * np.sqrt(DIAS_ANIO)
    b = fit.params[1]
    return {"Portafolio": nombre, "μ anual": m, "σ anual": s, "β": b, "R²": fit.rsquared,
            "Sharpe": (m - rf) / s, "Treynor": (m - rf) / b,
            "α Jensen anual": fit.params[0] * DIAS_ANIO, "t(α)": fit.tvalues[0]}


w_gmv = F.pesos_gmv()
w_lo = tang_rest["sin_vc"]["w"]
tabla_desemp = pd.DataFrame([
    medidas(rM, "Tangencia M (sin restricciones)"),
    medidas(rsp["SP500"].values, "S&P 500 (índice de precios)"),
    medidas(rsp["SP500_TR"].values, "S&P 500 Total Return"),
    medidas(r.values @ w_lo, "Máx. Sharpe sin venta corta"),
    medidas(r.values @ w_gmv, "Mínima varianza global"),
    medidas(r.values @ w_eq, "1/N (50 acciones)"),
]).set_index("Portafolio")
tabla_desemp.to_csv(TABLAS / "1B3_sharpe_treynor.csv")
print(tabla_desemp.round(4).to_string())

# Sharpe y Treynor de cada accion: ¿cuantas invierten el ranking frente al S&P?
ind = pd.DataFrame([medidas(r[t_].values, t_) for t_ in tick]).set_index("Portafolio")
ind["Sector"] = sec.loc[tick].values
sh_sp, tr_sp = tabla_desemp.loc["S&P 500 (índice de precios)", ["Sharpe", "Treynor"]]
ind["Sharpe>SP"] = ind["Sharpe"] > sh_sp
ind["Treynor>SP"] = ind["Treynor"] > tr_sp
ind["Ranking distinto"] = ind["Sharpe>SP"] != ind["Treynor>SP"]
ind.to_csv(TABLAS / "1B3_sharpe_treynor_acciones.csv")
invierten = ind[ind["Ranking distinto"]].sort_values("R²")

fig, ax = plt.subplots(figsize=(8.0, 5.6))
for s_, g in ind.groupby("Sector"):
    ax.scatter(g["Sharpe"], g["Treynor"], s=28, color=COLOR_SECTOR[s_], label=s_, edgecolor="white", lw=0.4)
for t_, rw in ind.iterrows():
    if rw["Ranking distinto"] or t_ in ("NVDA", "LLY", "AVGO", "CAT"):
        ax.annotate(t_, (rw["Sharpe"], rw["Treynor"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.axvline(sh_sp, color=COLORES["sp500"], ls="--", lw=1.2, label=f"Sharpe S&P 500 = {sh_sp:.2f}")
ax.axhline(tr_sp, color=COLORES["sp500"], ls=":", lw=1.2, label=f"Treynor S&P 500 = {tr_sp:.1%}")
ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Ratio de Sharpe (riesgo total)"); ax.set_ylabel("Ratio de Treynor (riesgo sistemático)")
ax.set_title("P1B.3 – Sharpe vs. Treynor de las 50 acciones frente al S&P 500")
ax.set_ylim(-0.3, 0.75)
ax.legend(fontsize=6.8, ncol=2, loc="upper left")
guardar_fig(fig, FIGURAS / "F14_sharpe_vs_treynor.png")

# -----------------------------------------------------------------------------
# 4) Asignacion optima entre M y rf:  x* = (E[R_M] - rf) / (c * sigma_M^2)
# -----------------------------------------------------------------------------
asign = []
for c in (2, 5, 10):
    x = (muM - rf) / (c * sM ** 2)
    Ec = rf + x * (muM - rf)
    sc = x * sM
    asign.append({"c": c, "x* (en M)": x, "1 - x* (en rf)": 1 - x,
                  "Posición": "Pide prestado (borrowing)" if x > 1 else "Presta (lending)",
                  "E[R_C]": Ec, "σ_C": sc, "Utilidad U = E - c/2 σ²": Ec - c / 2 * sc ** 2,
                  "x* con máx. Sharpe sin VC": (tang_rest["sin_vc"]["mu"] - rf) / (c * tang_rest["sin_vc"]["sigma"] ** 2),
                  "x* con S&P 500": (mu_sp - rf) / (c * s_sp ** 2)})
asign_df = pd.DataFrame(asign)
asign_df.to_csv(TABLAS / "1B4_asignacion_optima.csv", index=False)
print(asign_df.round(4).to_string())

fig, ax = plt.subplots(figsize=(8.6, 6.0))
xs = np.linspace(0, 1.45, 100)
ax.plot(xs, rf + SRM * xs, color=COLORES["lmc"], lw=2, label="LMC")
ax.plot(sig_f[eff], mus[eff], color=COLORES["frontera"], lw=1.4, alpha=0.6, label="Frontera eficiente")
cols = {2: "#c0392b", 5: "#e67e22", 10: "#16a085"}
for a in asign:
    c = a["c"]
    U = a["Utilidad U = E - c/2 σ²"]
    ax.plot(xs, U + c / 2 * xs ** 2, color=cols[c], lw=1.2, ls="--")
    ax.scatter([a["σ_C"]], [a["E[R_C]"]], color=cols[c], s=60, zorder=6,
               label=f"c = {c}: x* = {a['x* (en M)']:.2f} → {a['Posición'].split(' (')[0].lower()} "
                     f"{abs(1 - a['x* (en M)']):.0%} a rf")
ax.scatter([sM], [muM], s=110, marker="*", color="k", zorder=7, label="M (x = 1)")
ax.scatter([0], [rf], s=35, color="k", zorder=7)
ax.axvspan(0, sM, color="#16a085", alpha=0.05)
ax.axvspan(sM, 1.45, color="#c0392b", alpha=0.05)
ax.text(sM / 2, 3.2, "Lending\n(x* < 1)", ha="center", fontsize=9, color="#16a085")
ax.text((sM + 1.45) / 2, 3.2, "Borrowing\n(x* > 1, apalancado)", ha="center", fontsize=9, color="#c0392b")
ax.set_xlim(0, 1.45); ax.set_ylim(-0.05, 3.6)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual")
ax.set_title("P1B.4 – Asignación óptima en la LMC y curvas de indiferencia U = E[R] − (c/2)σ²")
ax.legend(loc="center right", fontsize=7.8)
guardar_fig(fig, FIGURAS / "F15_asignacion_optima.png")

# -----------------------------------------------------------------------------
# Guardar
# -----------------------------------------------------------------------------
guardar_json({
    "y1_publicada": y1, "rf": rf, "rf_diaria": rf_d,
    "M": {"mu": muM, "sigma": sM, "sharpe": SRM, "exp_bruta": float(np.abs(wM).sum()),
          "largos": float(wM[wM > 0].sum()), "cortos": float(wM[wM < 0].sum()),
          "top_largos": pesosM["Peso en M"].head(8).to_dict(),
          "top_cortos": pesosM["Peso en M"].tail(8).to_dict()},
    "peso_sector_M": peso_sector_M.to_dict(orient="index"),
    "tangencias_restringidas": {k: {a: b for a, b in v.items() if a != "w"} for k, v in tang_rest.items()},
    "pesos_tangencia_sin_vc": {t_: float(w_) for t_, w_ in zip(tick, tang_rest["sin_vc"]["w"]) if w_ > 1e-3},
    "sp500": {"mu": mu_sp, "sigma": s_sp, "sharpe": (mu_sp - rf) / s_sp, "mu_TR": mu_sptr},
    "modelo_indice": modelo_indice, "simulacion_H0": sim_h0, "fuera_muestra": fuera_muestra,
    "desempeno": tabla_desemp.to_dict(orient="index"),
    "acciones_ranking_distinto": invierten[["Sharpe", "Treynor", "β", "R²"]].to_dict(orient="index"),
    "asignacion": asign,
}, RESULTADOS / "p1b_resultados.json")

with pd.ExcelWriter(TABLAS / "Resultados_Pregunta1B.xlsx") as xw:
    pd.DataFrame({"rf publicada (1A, 31-jul-2026)": [y1], "rf continua": [rf]}).to_excel(xw, sheet_name="rf", index=False)
    pesosM.to_excel(xw, sheet_name="Pesos_M")
    peso_sector_M.to_excel(xw, sheet_name="Pesos_M_sector")
    pd.DataFrame({k: v["w"] for k, v in tang_rest.items()}, index=tick).to_excel(xw, sheet_name="Tangencias_restringidas")
    pd.DataFrame([modelo_indice]).T.rename(columns={0: "valor"}).to_excel(xw, sheet_name="Modelo_indice")
    pd.DataFrame({"Fecha": r.index, "r_M": rM, "r_SP500": rsp["SP500"].values,
                  "exceso_M": exM, "exceso_SP": exSP}).to_excel(xw, sheet_name="Series_regresion", index=False)
    tabla_desemp.to_excel(xw, sheet_name="Sharpe_Treynor")
    ind.to_excel(xw, sheet_name="Sharpe_Treynor_acciones")
    asign_df.to_excel(xw, sheet_name="Asignacion_optima", index=False)
    pd.DataFrame({k: v for k, v in fuera_muestra.items() if isinstance(v, dict)}).to_excel(xw, sheet_name="Fuera_de_muestra")
    pd.DataFrame([sim_h0]).T.to_excel(xw, sheet_name="Simulacion_H0")
print("Listo.")
