# =============================================================================
#  02_pregunta_1A.py  -  Pregunta 1A: frontera media-varianza con 50 acciones
#  Calcula los puntos 1 a 6 y guarda las figuras y Resultados_Pregunta1A.xlsx
# =============================================================================
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import (FIGURAS, LIMITE_CONCENTRACION, PESO_MIN_SECTORES,
                    SECTORES_RESTRICCION, TABLAS)
from utilidades import (COLOR_SECTOR, COLORES, PCT, FronteraAnalitica,
                        cargar_retornos, frontera_restringida, gmv_restringido,
                        guardar_fig, momentos_anuales, rango_factible, sectores)

sys.stdout.reconfigure(encoding="utf-8")

# -----------------------------------------------------------------------------
# 1) Retornos esperados, volatilidades y covarianzas en base anual
#    Retornos diarios continuos r = ln(Pt/Pt-1); se anualiza con 252 dias:
#    mu_anual = 252 mu_diaria, Omega_anual = 252 Omega_diaria.
# -----------------------------------------------------------------------------
r, rsp = cargar_retornos()
mu, sig, omega = momentos_anuales(r)
sec = sectores()
tick = list(mu.index)
n = len(tick)
T = len(r)
corr = r.corr()

# beta de cada accion contra el S&P 500 (solo descriptivo)
x = rsp["SP500"]
beta = r.apply(lambda c: np.cov(c, x)[0, 1] / x.var())

estad = pd.DataFrame({
    "Sector": sec,
    "Retorno esperado anual": mu,
    "Volatilidad anual": sig,
    "Beta vs S&P 500": beta,
    "Error est. de la media": sig / np.sqrt(T / 252),   # sigma / raiz(años de datos)
}).loc[tick]
estad.index.name = "Ticker"
estad = estad.sort_values(["Sector", "Retorno esperado anual"], ascending=[True, False])

# Resumen de correlaciones: promedio total, dentro del mismo sector, negativas
iu = np.triu_indices(n, 1)
cvals = corr.values[iu]
mismo = np.array([sec[tick[i]] == sec[tick[j]] for i, j in zip(*iu)])
k_max = cvals.argmax()
# Portafolio 1/N: que parte de su varianza viene de las covarianzas
w_eq = np.ones(n) / n
var_eq = w_eq @ omega.values @ w_eq
var_sin_cov = (w_eq ** 2 * np.diag(omega.values)).sum()
print(f"Datos: {T} retornos diarios, {r.index[0].date()} a {r.index[-1].date()}")
print(f"Correlacion promedio {cvals.mean():.2f} | mismo sector {cvals[mismo].mean():.2f} | "
      f"pares negativos {(cvals < 0).mean():.1%} | maxima {cvals.max():.2f} "
      f"({tick[iu[0][k_max]]}-{tick[iu[1][k_max]]})")
print(f"1/N: sigma {np.sqrt(var_eq):.1%} (sin covarianzas {np.sqrt(var_sin_cov):.1%}); "
      f"{1 - var_sin_cov / var_eq:.0%} de la varianza viene de covarianzas")

# -----------------------------------------------------------------------------
# 2) Frontera media-varianza con ventas cortas (solucion de clase)
#    min w'Ow  s.a.  w'mu = mu_bar, w'1 = 1  =>  w = O^-1 (l1*1 + l2*mu)
#    sigma^2(mu_bar) = (A mu_bar^2 - 2B mu_bar + C) / D
#    A = 1'O^-1 1, B = 1'O^-1 mu, C = mu'O^-1 mu, D = AC - B^2
#    (las formulas estan en utilidades.FronteraAnalitica)
# -----------------------------------------------------------------------------
F = FronteraAnalitica(mu.values, omega.values)
mus = np.linspace(-0.30, 1.00, 261)        # retornos objetivo
sig_libre = F.sigma(mus)
w_gmv = F.pesos_gmv()
eff = mus >= F.mu_gmv                       # rama eficiente: sobre el GMV
print(f"A={F.A:.2f} B={F.B:.2f} C={F.C:.2f} D={F.D:.2f}")
print(f"GMV: mu={F.mu_gmv:.1%} sigma={F.sigma_gmv:.1%} cortos={w_gmv[w_gmv < 0].sum():.0%}")

fig, ax = plt.subplots(figsize=(8.6, 6.2))
for s_, g in estad.groupby("Sector"):
    ax.scatter(g["Volatilidad anual"], g["Retorno esperado anual"], s=26,
               color=COLOR_SECTOR[s_], label=s_, zorder=3, edgecolor="white", lw=0.4)
for t_ in ["NVDA", "AVGO", "LLY", "CAT", "TSLA", "AMT", "PFE", "KO", "XOM", "SO"]:
    ax.annotate(t_, (sig[t_], mu[t_]), fontsize=7, xytext=(3, 3), textcoords="offset points")
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
# 3) Frontera "ingenua": mismos calculos pero con la diagonal de Omega
#    (sigma_ij = 0).  Despues se mide la volatilidad REAL de esos pesos con
#    la Omega completa y la volatilidad PERCIBIDA con la diagonal.
# -----------------------------------------------------------------------------
Fd = FronteraAnalitica(mu.values, np.diag(np.diag(omega.values)))
W_ing = np.array([Fd.pesos(m) for m in mus])
sig_ing_perc = Fd.sigma(mus)
sig_ing_real = np.sqrt(np.einsum("ij,jk,ik->i", W_ing, omega.values, W_ing))
effd = mus >= Fd.mu_gmv
w_dg = Fd.pesos_gmv()

fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.plot(sig_libre[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Frontera MV con Ω completa (P2)")
ax.plot(sig_libre[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
ax.plot(sig_ing_real[effd], mus[effd], color=COLORES["ingenua_real"], lw=2.2,
        label="Frontera ingenua: volatilidad REAL (pesos diag., σ con Ω completa)")
ax.plot(sig_ing_real[~effd], mus[~effd], color=COLORES["ingenua_real"], lw=1.2, ls="--")
ax.plot(sig_ing_perc[effd], mus[effd], color=COLORES["ingenua_perc"], lw=2,
        label="Frontera ingenua: volatilidad PERCIBIDA (σ con diag(Ω))")
ax.plot(sig_ing_perc[~effd], mus[~effd], color=COLORES["ingenua_perc"], lw=1.2, ls="--")
ax.scatter(sig, mu, s=10, color=COLORES["gris"], alpha=0.6, label="Acciones individuales")
ax.scatter([Fd.sigma_gmv], [Fd.mu_gmv], marker="D", s=40, color=COLORES["ingenua_perc"], zorder=5)
ax.scatter([np.sqrt(w_dg @ omega.values @ w_dg)], [Fd.mu_gmv], marker="D", s=40,
           color=COLORES["ingenua_real"], zorder=5)
ax.scatter([F.sigma_gmv], [F.mu_gmv], marker="D", s=40, color=COLORES["frontera"], zorder=5)
ax.set_xlim(0, 0.65); ax.set_ylim(-0.30, 1.00)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("P1A.3 – Frontera completa vs. frontera “ingenua” (σij = 0)")
ax.legend(loc="lower right", fontsize=7.6)
guardar_fig(fig, FIGURAS / "F03_frontera_ingenua.png")

# Comparacion en algunos retornos objetivo (GMV, 20%, 30%, 50%)
ingenua = pd.DataFrame([{
    "mu_objetivo": m,
    "sigma_frontera_completa": float(F.sigma(m)),
    "sigma_ingenua_real": float(np.sqrt(Fd.pesos(m) @ omega.values @ Fd.pesos(m))),
    "sigma_ingenua_percibida": float(Fd.sigma(m)),
    "exposicion_bruta_completa": float(np.abs(F.pesos(m)).sum()),   # suma de |w|
} for m in [F.mu_gmv, 0.20, 0.30, 0.50]])
print(f"GMV ingenuo: sigma percibida {Fd.sigma_gmv:.1%} vs real {np.sqrt(w_dg @ omega.values @ w_dg):.1%}")

# -----------------------------------------------------------------------------
# 4), 5), 6) Fronteras con restricciones: no hay formula, se resuelve el mismo
#    problema con programacion cuadratica para cada retorno objetivo.
#    4) -0.10 <= w_i <= 0.10   5) w_i >= 0   6) w_i >= 0 y Energy+Industrials >= 40%
# -----------------------------------------------------------------------------
mask = sec.loc[tick].isin(SECTORES_RESTRICCION).values.astype(float)
casos = {
    "limite": dict(kw={"lim": LIMITE_CONCENTRACION}, nombre="−10% ≤ wᵢ ≤ 10%", color=COLORES["limite10"]),
    "sin_vc": dict(kw={}, nombre="Sin venta corta (wᵢ ≥ 0)", color=COLORES["sin_vc"]),
    "sin_vc_sector": dict(kw={"sector_mask": mask, "piso": PESO_MIN_SECTORES},
                          nombre="Sin venta corta + Energy/Industrials ≥ 40%", color=COLORES["sector"]),
}
fronteras = {}
for k, c in casos.items():
    lo, hi = rango_factible(mu.values, k, **c["kw"])          # retornos minimo y maximo posibles
    grid = np.linspace(lo + 1e-4, hi - 1e-4, 181)
    s_, W_ = frontera_restringida(mu.values, omega.values, k, grid, **c["kw"])
    wg = gmv_restringido(mu.values, omega.values, k, **c["kw"])
    e = grid >= wg @ mu.values
    n_acc = [int((np.abs(w_) > 1e-3).sum()) for w_ in W_[e]]   # acciones con peso > 0,1%
    fronteras[k] = {"mus": grid, "sig": s_, "W": W_, "rango": (lo, hi), "w_gmv": wg,
                    "n_acc": (min(n_acc), max(n_acc))}
    print(f"{k}: retornos posibles [{lo:.1%}, {hi:.1%}] | GMV sigma {np.sqrt(wg @ omega.values @ wg):.2%} "
          f"| acciones en la frontera eficiente: {min(n_acc)} a {max(n_acc)}")

# Figura con todas las fronteras
fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.plot(sig_libre[eff], mus[eff], color=COLORES["frontera"], lw=2.2, label="Sin restricciones (P2)")
ax.plot(sig_libre[~eff], mus[~eff], color=COLORES["frontera"], lw=1.2, ls="--")
for k, c in casos.items():
    f = fronteras[k]
    mg = f["w_gmv"] @ mu.values
    e = f["mus"] >= mg
    ax.plot(f["sig"][e], f["mus"][e], color=c["color"], lw=2.2, label=c["nombre"])
    ax.plot(f["sig"][~e], f["mus"][~e], color=c["color"], lw=1.2, ls="--")
    ax.scatter([np.sqrt(f["w_gmv"] @ omega.values @ f["w_gmv"])], [mg], marker="D", s=35, color=c["color"], zorder=5)
ax.scatter([F.sigma_gmv], [F.mu_gmv], marker="D", s=35, color=COLORES["frontera"], zorder=5)
ax.scatter(sig, mu, s=12, color=COLORES["gris"], alpha=0.55, label="Acciones individuales")
ax.plot(sig_ing_real[effd], mus[effd], color=COLORES["ingenua_real"], lw=1.6, ls="-.",
        label="Ingenua (volatilidad real)")
ax.set_xlim(0.08, 0.55); ax.set_ylim(0.0, 0.60)
ax.xaxis.set_major_formatter(PCT); ax.yaxis.set_major_formatter(PCT)
ax.set_xlabel("Volatilidad anual (σ)"); ax.set_ylabel("Retorno esperado anual (μ)")
ax.set_title("Resumen – Todas las fronteras eficientes")
ax.legend(loc="upper left", fontsize=7.6)
guardar_fig(fig, FIGURAS / "F07_resumen_fronteras.png")


def sigma_en(k, m):
    """Volatilidad minima para el retorno objetivo m en la frontera k."""
    if k == "libre":
        return float(F.sigma(m))
    lo, hi = fronteras[k]["rango"]
    if m < lo or m > hi:
        return np.nan
    return float(frontera_restringida(mu.values, omega.values, k, [m], **casos[k]["kw"])[0][0])


resumen = []
for k, nom in [("libre", "Sin restricciones (P2)")] + [(k, c["nombre"]) for k, c in casos.items()]:
    wg = w_gmv if k == "libre" else fronteras[k]["w_gmv"]
    resumen.append({
        "Frontera": nom,
        "Retorno máximo factible": np.inf if k == "libre" else fronteras[k]["rango"][1],
        "GMV μ": wg @ mu.values, "GMV σ": np.sqrt(wg @ omega.values @ wg),
        "σ para μ̄=20%": sigma_en(k, 0.20), "σ para μ̄=30%": sigma_en(k, 0.30), "σ para μ̄=40%": sigma_en(k, 0.40),
    })
resumen = pd.DataFrame(resumen)
print(resumen.round(4).to_string())

pesos_gmv = pd.DataFrame({"Sector": sec.loc[tick], "GMV sin restricciones": w_gmv,
                          "GMV |w|<=10%": fronteras["limite"]["w_gmv"],
                          "GMV sin venta corta": fronteras["sin_vc"]["w_gmv"],
                          "GMV sin VC + sector": fronteras["sin_vc_sector"]["w_gmv"]}, index=tick)

# -----------------------------------------------------------------------------
# Guardar todo en Excel
# -----------------------------------------------------------------------------
with pd.ExcelWriter(TABLAS / "Resultados_Pregunta1A.xlsx") as xw:
    estad.to_excel(xw, sheet_name="1_Estadisticas")
    omega.to_excel(xw, sheet_name="1_Covarianzas_anual")
    corr.to_excel(xw, sheet_name="1_Correlaciones")
    pd.DataFrame({"mu_objetivo": mus, "sigma_frontera": sig_libre, "sigma_ingenua_real": sig_ing_real,
                  "sigma_ingenua_percibida": sig_ing_perc}).to_excel(xw, sheet_name="2_3_Fronteras", index=False)
    ingenua.to_excel(xw, sheet_name="3_Ingenua_vs_completa", index=False)
    for k, hoja in [("limite", "4_Frontera_limite10"), ("sin_vc", "5_Frontera_sin_vc"),
                    ("sin_vc_sector", "6_Frontera_sector")]:
        f = fronteras[k]
        pd.DataFrame(f["W"], columns=tick).assign(mu_objetivo=f["mus"], sigma=f["sig"]).set_index(
            ["mu_objetivo", "sigma"]).to_excel(xw, sheet_name=hoja)
    resumen.to_excel(xw, sheet_name="Resumen_fronteras", index=False)
    pesos_gmv.to_excel(xw, sheet_name="Pesos_GMV")
print("Listo: Resultados_Pregunta1A.xlsx y figuras F02, F03, F07")
