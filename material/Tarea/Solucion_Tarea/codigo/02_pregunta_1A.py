# =============================================================================
#  02_pregunta_1A.py  -  PREGUNTA 1A: FRONTERA MEDIA-VARIANZA (50 acciones)
#   1. Retornos esperados, volatilidades y covarianzas en base anual
#   2. Frontera media-varianza (ventas cortas permitidas, solucion de clase)
#   3. Frontera "ingenua" (solo la diagonal de Omega) y su volatilidad real
#   4. Frontera con limite de concentracion  -0.10 <= w_i <= 0.10
#   5. Frontera sin venta corta  w_i >= 0
#   6. Sin venta corta + (Energy + Industrials) >= 40%
# =============================================================================
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import (FIGURAS, LIMITE_CONCENTRACION, PESO_MIN_SECTORES,
                    RESULTADOS, SECTORES_RESTRICCION, TABLAS)
sys.stdout.reconfigure(encoding="utf-8")
from utilidades import (COLOR_SECTOR, COLORES, PCT, FronteraAnalitica,
                        cargar_retornos, frontera_restringida, gmv_restringido,
                        guardar_fig, guardar_json, momentos_anuales,
                        rango_factible, sectores)

# -----------------------------------------------------------------------------
# 1) Momentos anuales
# -----------------------------------------------------------------------------
r, rsp = cargar_retornos()
mu, sig, omega = momentos_anuales(r)
sec = sectores()
tick = list(mu.index)
n = len(tick)
T = len(r)
corr = r.corr()

# beta individual respecto del S&P 500 (dato descriptivo para la discusion)
x = rsp["SP500"]
beta = r.apply(lambda c: np.cov(c, x)[0, 1] / x.var())

tabla1 = pd.DataFrame({
    "Sector": sec,
    "Retorno esperado anual": mu,
    "Volatilidad anual": sig,
    "Retorno/Volatilidad": mu / sig,
    "Beta vs S&P 500": beta,
    "Error est. de la media": sig / np.sqrt(T / 252),
}).loc[tick]
tabla1.index.name = "Ticker"
tabla1 = tabla1.sort_values(["Sector", "Retorno esperado anual"], ascending=[True, False])
tabla1.to_csv(TABLAS / "1A1_estadisticas_acciones.csv")
omega.to_csv(TABLAS / "1A1_matriz_covarianzas_anual.csv")
corr.to_csv(TABLAS / "1A1_matriz_correlaciones.csv")

# Correlaciones promedio dentro y entre sectores
iu = np.triu_indices(n, 1)
cvals = corr.values[iu]
mismo = np.array([sec[tick[i]] == sec[tick[j]] for i, j in zip(*iu)])
corr_stats = {
    "corr_promedio": cvals.mean(), "corr_min": cvals.min(), "corr_max": cvals.max(),
    "corr_mismo_sector": cvals[mismo].mean(), "corr_distinto_sector": cvals[~mismo].mean(),
    "pct_corr_negativas": (cvals < 0).mean(),
    "par_corr_max": [tick[iu[0][cvals.argmax()]], tick[iu[1][cvals.argmax()]]],
    "par_corr_min": [tick[iu[0][cvals.argmin()]], tick[iu[1][cvals.argmin()]]],
}
# Proporcion de la varianza de un portafolio 1/N que proviene de covarianzas
w_eq = np.ones(n) / n
var_eq = w_eq @ omega.values @ w_eq
var_diag_eq = (w_eq ** 2 * np.diag(omega.values)).sum()
corr_stats.update({"sigma_1N": np.sqrt(var_eq), "sigma_1N_sin_cov": np.sqrt(var_diag_eq),
                   "mu_1N": w_eq @ mu.values, "share_var_cov_1N": 1 - var_diag_eq / var_eq,
                   "T_dias": T, "inicio": str(r.index[0].date()), "fin": str(r.index[-1].date())})

# Figura: mapa de calor de correlaciones ordenado por sector
orden = tabla1.index.tolist()
fig, ax = plt.subplots(figsize=(9.2, 8))
im = ax.imshow(corr.loc[orden, orden].values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels(orden, rotation=90, fontsize=6.5); ax.set_yticklabels(orden, fontsize=6.5)
ax.grid(False)
lim = np.cumsum(tabla1["Sector"].value_counts(sort=False).reindex(tabla1["Sector"].unique()).values)
for b in lim[:-1]:
    ax.axhline(b - 0.5, color="k", lw=0.6); ax.axvline(b - 0.5, color="k", lw=0.6)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02, label="Correlación")
ax.set_title("Correlaciones de retornos diarios (ago-2021 a jul-2026), ordenadas por sector")
guardar_fig(fig, FIGURAS / "F01_correlaciones.png")

# -----------------------------------------------------------------------------
# 2) Frontera media-varianza sin restricciones (ventas cortas permitidas)
# -----------------------------------------------------------------------------
F = FronteraAnalitica(mu.values, omega.values)
mus = np.linspace(-0.30, 1.00, 261)
sig_libre = F.sigma(mus)
# Verificacion numerica: QP generico con cvxpy debe coincidir con la formula
sig_chk, _ = frontera_restringida(mu.values, omega.values, "libre", mus[::20])
err_max = np.nanmax(np.abs(sig_chk - sig_libre[::20]))
print(f"Chequeo formula analitica vs QP numerico: error max = {err_max:.2e}")

w_gmv = F.pesos_gmv()


def resumen_portafolio(w):
    w = np.asarray(w)
    return {"mu": float(w @ mu.values), "sigma": float(np.sqrt(w @ omega.values @ w)),
            "n_activos": int((np.abs(w) > 1e-3).sum()), "exposicion_bruta": float(np.abs(w).sum()),
            "suma_cortos": float(w[w < 0].sum()), "w_max": float(w.max()), "w_min": float(w.min()),
            "peso_energy_ind": float(w[sec.loc[tick].isin(SECTORES_RESTRICCION).values].sum())}


fig, ax = plt.subplots(figsize=(8.6, 6.2))
for s_, g in tabla1.groupby("Sector"):
    ax.scatter(g["Volatilidad anual"], g["Retorno esperado anual"], s=26,
               color=COLOR_SECTOR[s_], label=s_, zorder=3, edgecolor="white", lw=0.4)
for t_ in ["NVDA", "AVGO", "LLY", "CAT", "TSLA", "AMT", "PFE", "KO", "XOM", "SO"]:
    ax.annotate(t_, (sig[t_], mu[t_]), fontsize=7, xytext=(3, 3), textcoords="offset points")
eff = mus >= F.mu_gmv
ax.plot(sig_libre[eff], mus[eff], color=COLORES["frontera"], lw=2.2,
        label="Frontera eficiente (ventas cortas permitidas)")
ax.plot(sig_libre[~eff], mus[~eff], color=COLORES["frontera"], lw=1.4, ls="--",
        label="Rama ineficiente")
ax.scatter([F.sigma_gmv], [F.mu_gmv], marker="D", s=55, color="k", zorder=5,
           label=f"Mínima varianza global (σ={F.sigma_gmv:.1%}, μ={F.mu_gmv:.1%})")
ax.set_xlim(0, 0.65); ax.set_ylim(-0.30, 1.00)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("P1A.2 – Frontera media-varianza con 50 acciones del S&P 500")
ax.legend(loc="upper left", ncol=2, fontsize=7.2)
guardar_fig(fig, FIGURAS / "F02_frontera_mv.png")

# -----------------------------------------------------------------------------
# 3) Frontera "ingenua": pesos con Omega_D = diag(sigma_i^2)
# -----------------------------------------------------------------------------
omega_d = np.diag(np.diag(omega.values))
Fd = FronteraAnalitica(mu.values, omega_d)
W_ing = np.array([Fd.pesos(m) for m in mus])
sig_ing_perc = Fd.sigma(mus)                                   # lo que "cree" el inversionista
sig_ing_real = np.sqrt(np.einsum("ij,jk,ik->i", W_ing, omega.values, W_ing))  # con Omega completa

fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.plot(sig_libre[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Frontera MV con Ω completa (P2)")
ax.plot(sig_libre[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
effd = mus >= Fd.mu_gmv
ax.plot(sig_ing_real[effd], mus[effd], color=COLORES["ingenua_real"], lw=2.2,
        label="Frontera ingenua: volatilidad REAL (pesos diag., σ con Ω completa)")
ax.plot(sig_ing_real[~effd], mus[~effd], color=COLORES["ingenua_real"], lw=1.2, ls="--")
ax.plot(sig_ing_perc[effd], mus[effd], color=COLORES["ingenua_perc"], lw=2,
        label="Frontera ingenua: volatilidad PERCIBIDA (σ con diag(Ω))")
ax.plot(sig_ing_perc[~effd], mus[~effd], color=COLORES["ingenua_perc"], lw=1.2, ls="--")
ax.scatter(sig, mu, s=10, color=COLORES["gris"], alpha=0.6, label="Acciones individuales")
gi = np.argmin(np.abs(mus - Fd.mu_gmv))
ax.scatter([Fd.sigma_gmv], [Fd.mu_gmv], marker="D", s=40, color=COLORES["ingenua_perc"], zorder=5)
w_dg = Fd.pesos_gmv()
ax.scatter([np.sqrt(w_dg @ omega.values @ w_dg)], [Fd.mu_gmv], marker="D", s=40,
           color=COLORES["ingenua_real"], zorder=5)
ax.scatter([F.sigma_gmv], [F.mu_gmv], marker="D", s=40, color=COLORES["frontera"], zorder=5)
ax.set_xlim(0, 0.65); ax.set_ylim(-0.30, 1.00)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("P1A.3 – Frontera completa vs. frontera “ingenua” (σij = 0)")
ax.legend(loc="lower right", fontsize=7.6)
guardar_fig(fig, FIGURAS / "F03_frontera_ingenua.png")

ingenua_puntos = []
for m in [F.mu_gmv, 0.20, 0.30, 0.50]:
    w_n = Fd.pesos(m)
    ingenua_puntos.append({
        "mu_objetivo": m, "sigma_frontera_completa": float(F.sigma(m)),
        "sigma_ingenua_percibida": float(Fd.sigma(m)),
        "sigma_ingenua_real": float(np.sqrt(w_n @ omega.values @ w_n)),
        "exposicion_bruta_ingenua": float(np.abs(w_n).sum()),
        "exposicion_bruta_completa": float(np.abs(F.pesos(m)).sum()),
    })
ingenua_df = pd.DataFrame(ingenua_puntos)
ingenua_df.to_csv(TABLAS / "1A3_comparacion_ingenua.csv", index=False)
gmv_ing = {"mu": Fd.mu_gmv, "sigma_percibida": Fd.sigma_gmv,
           "sigma_real": float(np.sqrt(w_dg @ omega.values @ w_dg)),
           "w_max": float(w_dg.max()), "w_min": float(w_dg.min())}

# -----------------------------------------------------------------------------
# 4), 5), 6) Fronteras con restricciones (programacion cuadratica)
# -----------------------------------------------------------------------------
mask = sec.loc[tick].isin(SECTORES_RESTRICCION).values.astype(float)
casos = {
    "limite": dict(kw={"lim": LIMITE_CONCENTRACION}, nombre="−10% ≤ wᵢ ≤ 10%"),
    "sin_vc": dict(kw={}, nombre="Sin venta corta (wᵢ ≥ 0)"),
    "sin_vc_sector": dict(kw={"sector_mask": mask, "piso": PESO_MIN_SECTORES},
                          nombre="Sin venta corta + Energy/Industrials ≥ 40%"),
}
fronteras = {}
for k, c in casos.items():
    lo, hi = rango_factible(mu.values, k, **c["kw"])
    grid = np.linspace(lo + 1e-4, hi - 1e-4, 181)
    s_, W_ = frontera_restringida(mu.values, omega.values, k, grid, **c["kw"])
    wg = gmv_restringido(mu.values, omega.values, k, **c["kw"])
    fronteras[k] = {"mus": grid, "sig": s_, "W": W_, "rango": (lo, hi), "w_gmv": wg}
    print(f"{k}: retorno factible [{lo:.3f}, {hi:.3f}] | GMV mu={wg @ mu.values:.3f} "
          f"sigma={np.sqrt(wg @ omega.values @ wg):.4f}")


def plot_comparacion(ax, claves, zoom=True):
    ax.plot(sig_libre[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Sin restricciones (P2)")
    ax.plot(sig_libre[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
    for k in claves:
        f = fronteras[k]
        wg = f["w_gmv"]
        mg = wg @ mu.values
        e = f["mus"] >= mg
        col = {"limite": COLORES["limite10"], "sin_vc": COLORES["sin_vc"],
               "sin_vc_sector": COLORES["sector"]}[k]
        ax.plot(f["sig"][e], f["mus"][e], color=col, lw=2.2, label=casos[k]["nombre"])
        ax.plot(f["sig"][~e], f["mus"][~e], color=col, lw=1.2, ls="--")
        ax.scatter([np.sqrt(wg @ omega.values @ wg)], [mg], marker="D", s=35, color=col, zorder=5)
    ax.scatter([F.sigma_gmv], [F.mu_gmv], marker="D", s=35, color=COLORES["frontera"], zorder=5)
    ax.scatter(sig, mu, s=12, color=COLORES["gris"], alpha=0.55, label="Acciones individuales")
    ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")


# Figura P4
fig, ax = plt.subplots(figsize=(8.6, 6.0))
plot_comparacion(ax, ["limite"])
for t_ in ["NVDA", "AVGO", "LLY", "CAT", "PFE", "AMT"]:
    ax.annotate(t_, (sig[t_], mu[t_]), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_xlim(0, 0.65); ax.set_ylim(-0.30, 1.00)
ax.set_title("P1A.4 – Frontera con límite de concentración |wᵢ| ≤ 10%")
ax.legend(loc="upper left")
guardar_fig(fig, FIGURAS / "F04_frontera_limite10.png")

# Figura P5
fig, ax = plt.subplots(figsize=(8.6, 6.0))
plot_comparacion(ax, ["sin_vc"])
for t_ in ["NVDA", "AVGO", "LLY", "CAT", "XOM", "TSLA", "PFE", "AMT", "KO", "WMT"]:
    ax.annotate(t_, (sig[t_], mu[t_]), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_xlim(0, 0.65); ax.set_ylim(-0.30, 1.00)
ax.set_title("P1A.5 – Frontera sin venta corta (wᵢ ≥ 0)")
ax.legend(loc="upper left")
guardar_fig(fig, FIGURAS / "F05_frontera_sin_vc.png")

# Figura P6 (zoom)
fig, ax = plt.subplots(figsize=(8.6, 6.0))
plot_comparacion(ax, ["sin_vc", "sin_vc_sector"])
for t_ in ["NVDA", "AVGO", "LLY", "CAT", "XOM", "RTX", "WM", "LMT", "KO", "GS"]:
    ax.annotate(t_, (sig[t_], mu[t_]), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_xlim(0.08, 0.55); ax.set_ylim(0.0, 0.50)
ax.set_title("P1A.6 – Sin venta corta + (Energy + Industrials) ≥ 40%")
ax.legend(loc="upper left")
guardar_fig(fig, FIGURAS / "F06_frontera_sector.png")

# Figura resumen: todas las fronteras (zoom en la zona relevante)
fig, ax = plt.subplots(figsize=(8.6, 6.0))
plot_comparacion(ax, ["limite", "sin_vc", "sin_vc_sector"])
ax.plot(sig_ing_real[effd], mus[effd], color=COLORES["ingenua_real"], lw=1.6, ls="-.",
        label="Ingenua (volatilidad real)")
ax.set_xlim(0.08, 0.55); ax.set_ylim(0.0, 0.60)
ax.set_title("Resumen – Todas las fronteras eficientes")
ax.legend(loc="upper left", fontsize=7.6)
guardar_fig(fig, FIGURAS / "F07_resumen_fronteras.png")

# Composicion por sector a lo largo de las fronteras sin venta corta
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
orden_sec = list(COLOR_SECTOR.keys())
for ax, k in zip(axes, ["sin_vc", "sin_vc_sector"]):
    f = fronteras[k]
    mg = f["w_gmv"] @ mu.values
    e = (f["mus"] >= mg) & ~np.isnan(f["sig"])
    W = pd.DataFrame(np.clip(f["W"][e], 0, None), columns=tick)
    S = W.T.groupby(sec.loc[tick].values).sum().T.reindex(columns=orden_sec).fillna(0)
    ax.stackplot(f["mus"][e], S.T.values, colors=[COLOR_SECTOR[s_] for s_ in orden_sec],
                 labels=orden_sec, alpha=0.9)
    ax.set_xlim(f["mus"][e][0], f["mus"][e][-1]); ax.set_ylim(0, 1)
    ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
    ax.set_xlabel("Retorno esperado objetivo (μ̄)")
    ax.set_title(casos[k]["nombre"])
    if k == "sin_vc_sector":
        ax.axhline(0.4, color="k", lw=0.8, ls=":")
axes[0].set_ylabel("Peso en el portafolio eficiente")
axes[1].legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7.5)
fig.suptitle("Composición sectorial de los portafolios eficientes", fontweight="bold")
guardar_fig(fig, FIGURAS / "F08_composicion_sin_vc.png")

# Numero de acciones con peso > 0 a lo largo de la frontera sin venta corta
# (solo en la rama eficiente, contando pesos de al menos 0,1%)
n_act = {}
for k, f in fronteras.items():
    e = f["mus"] >= f["w_gmv"] @ mu.values
    n_act[k] = [int((np.abs(w_) > 1e-3).sum()) if not np.isnan(w_).any() else None
                for w_ in f["W"][e]]

# -----------------------------------------------------------------------------
# Tabla resumen comparativa
# -----------------------------------------------------------------------------
def sigma_en(k, m):
    if k == "libre":
        return float(F.sigma(m))
    f = fronteras[k]
    lo, hi = f["rango"]
    if m < lo or m > hi:
        return np.nan
    s_, _ = frontera_restringida(mu.values, omega.values, k, [m], **casos[k]["kw"])
    return float(s_[0])


resumen = []
for k, nom in [("libre", "Sin restricciones (P2)"), ("limite", casos["limite"]["nombre"]),
               ("sin_vc", casos["sin_vc"]["nombre"]), ("sin_vc_sector", casos["sin_vc_sector"]["nombre"])]:
    wg = w_gmv if k == "libre" else fronteras[k]["w_gmv"]
    rg = (-np.inf, np.inf) if k == "libre" else fronteras[k]["rango"]
    rp = resumen_portafolio(wg)
    resumen.append({"Frontera": nom, "Retorno mínimo factible": rg[0], "Retorno máximo factible": rg[1],
                    "GMV μ": rp["mu"], "GMV σ": rp["sigma"], "GMV n° acciones": rp["n_activos"],
                    "GMV exposición bruta": rp["exposicion_bruta"],
                    "σ para μ̄=15%": sigma_en(k, 0.15), "σ para μ̄=20%": sigma_en(k, 0.20),
                    "σ para μ̄=30%": sigma_en(k, 0.30), "σ para μ̄=40%": sigma_en(k, 0.40)})
resumen_df = pd.DataFrame(resumen)
resumen_df.to_csv(TABLAS / "1A_resumen_fronteras.csv", index=False)
print(resumen_df.round(4).to_string())

# Pesos del GMV de cada frontera
pesos_gmv = pd.DataFrame({"Sector": sec.loc[tick], "GMV sin restricciones": w_gmv,
                          "GMV |w|<=10%": fronteras["limite"]["w_gmv"],
                          "GMV sin venta corta": fronteras["sin_vc"]["w_gmv"],
                          "GMV sin VC + sector": fronteras["sin_vc_sector"]["w_gmv"]}, index=tick)
pesos_gmv.to_csv(TABLAS / "1A_pesos_gmv.csv")

# Acciones que participan en algun punto de la frontera eficiente sin venta corta
def acciones_usadas(k):
    f = fronteras[k]
    mg = f["w_gmv"] @ mu.values
    e = (f["mus"] >= mg) & ~np.isnan(f["sig"])
    W = f["W"][e]
    return sorted([tick[j] for j in range(n) if (W[:, j] > 1e-3).any()])


# -----------------------------------------------------------------------------
# Guardar resultados para la pregunta 1B y el informe
# -----------------------------------------------------------------------------
np.savez(RESULTADOS / "p1a_fronteras.npz", mus=mus, sig_libre=sig_libre,
         sig_ing_real=sig_ing_real, sig_ing_perc=sig_ing_perc,
         **{f"{k}_{c}": np.asarray(v) for k, f in fronteras.items()
            for c, v in f.items() if c in ("mus", "sig", "W", "w_gmv")})
guardar_json({
    "corr": corr_stats, "gmv_libre": resumen_portafolio(w_gmv),
    "gmv_ingenua": gmv_ing, "ingenua_puntos": ingenua_puntos,
    "fronteras": {k: {"rango": f["rango"], "gmv": resumen_portafolio(f["w_gmv"]),
                      "n_acciones_min": int(np.nanmin([v for v in n_act[k] if v is not None])),
                      "n_acciones_max": int(np.nanmax([v for v in n_act[k] if v is not None])),
                      "acciones_usadas_eficiente": acciones_usadas(k) if k != "limite" else None}
                  for k, f in fronteras.items()},
    "chequeo_analitico_vs_qp": err_max,
    "A": F.A, "B": F.B, "C": F.C, "D": F.D,
}, RESULTADOS / "p1a_resultados.json")

with pd.ExcelWriter(TABLAS / "Resultados_Pregunta1A.xlsx") as xw:
    tabla1.to_excel(xw, sheet_name="1A1_Estadisticas")
    omega.to_excel(xw, sheet_name="1A1_Covarianzas_anual")
    corr.to_excel(xw, sheet_name="1A1_Correlaciones")
    pd.DataFrame({"mu_objetivo": mus, "sigma_P2": sig_libre, "sigma_ingenua_real": sig_ing_real,
                  "sigma_ingenua_percibida": sig_ing_perc}).to_excel(xw, sheet_name="Frontera_P2_P3", index=False)
    for k in fronteras:
        pd.DataFrame(fronteras[k]["W"], columns=tick).assign(
            mu_objetivo=fronteras[k]["mus"], sigma=fronteras[k]["sig"]).set_index(
            ["mu_objetivo", "sigma"]).to_excel(xw, sheet_name=f"Frontera_{k}"[:31])
    resumen_df.to_excel(xw, sheet_name="Resumen", index=False)
    pesos_gmv.to_excel(xw, sheet_name="Pesos_GMV")
    ingenua_df.to_excel(xw, sheet_name="Ingenua_vs_completa", index=False)
print("Listo: figuras en", FIGURAS)
