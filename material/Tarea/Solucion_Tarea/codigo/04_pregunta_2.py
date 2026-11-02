# =============================================================================
#  04_pregunta_2.py  -  PREGUNTA 2: MODELOS DE ESTRUCTURA DE TASAS
#   Fed H.15, Treasury Constant Maturities (1M ... 30A), ultimo dia transado
#   de junio de 2017 a 2026.  Ajuste de Nelson-Siegel (1987) y Svensson (1994)
#   con busqueda del OPTIMO GLOBAL, comparacion por RMSE, evolucion de
#   beta0, beta1, beta2 y analisis de inversiones de la curva.
#
#   Nelson-Siegel (notacion de clase, Sesion I lamina 82):
#     R(t) = b0 + b1*[(1-e^{-t/a1}) a1/t] + b2*[(1-e^{-t/a1}) a1/t - e^{-t/a1}]
#   Svensson (lamina 83): agrega  b3*[(1-e^{-t/a2}) a2/t - e^{-t/a2}]
#   Convencion: dias transados / dias transados => t en anios (1M = 1/12).
# =============================================================================
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, lsq_linear, minimize

from config import (ANIOS_CURVA, DATOS, ETIQUETAS_PLAZO, FIGURAS, PLAZOS_H15,
                    RESULTADOS, TABLAS)

sys.stdout.reconfigure(encoding="utf-8")
from utilidades import guardar_fig, guardar_json

rng = np.random.default_rng(1987)
# Region admisible (restricciones economicas estandar, ver informe):
#   b0 >= 0 (tasa de largo plazo R(inf) = b0 no negativa)
#   b0 + b1 >= 0 (tasa instantanea R(0) = b0 + b1 no negativa)
#   0.1 <= a1 <= 10 anios ; 0.1 <= a2 <= 30 anios, a2 distinto de a1 (Svensson;
#   si a1 = a2 los dos terminos de curvatura son colineales)
A1_MIN, A1_MAX = 0.10, 10.0
A2_MAX = 30.0

# -----------------------------------------------------------------------------
# Datos: curva del ultimo dia transado de junio de cada anio
# -----------------------------------------------------------------------------
h15 = pd.read_csv(DATOS / "tasas_h15.csv", index_col=0, parse_dates=True)
h15 = h15[list(PLAZOS_H15)]
h15.columns = ETIQUETAS_PLAZO
plazos = np.array(list(PLAZOS_H15.values()))

fechas = []
for a in ANIOS_CURVA:
    junio = h15.loc[f"{a}-06"].dropna(how="all")
    fechas.append(junio.index[-1])                 # ultimo dia transado de junio
curvas = h15.loc[fechas]
assert not curvas.isna().any().any(), "faltan plazos en alguna fecha"
curvas.index = curvas.index.date
curvas.to_csv(TABLAS / "2_curvas_observadas_junio.csv")
print(curvas.to_string())


# -----------------------------------------------------------------------------
# Modelos
# -----------------------------------------------------------------------------
def cargas(t, a):
    x = t / a
    f1 = (1 - np.exp(-x)) / x
    return f1, f1 - np.exp(-x)


def ns(t, b, a1):
    f1, f2 = cargas(t, a1)
    return b[0] + b[1] * f1 + b[2] * f2


def sv(t, b, a1, a2):
    f1, f2 = cargas(t, a1)
    _, f3 = cargas(t, a2)
    return b[0] + b[1] * f1 + b[2] * f2 + b[3] * f3


def diseno(a1, a2=None):
    """Matriz de diseno re-parametrizada: R = b0 (1 - f1) + g f1 + b2 f2 (+ b3 f3),
    con g = b0 + b1 = R(0).  Asi las dos restricciones (b0>=0, b0+b1>=0) son
    simples cotas sobre (b0, g)."""
    f1, f2 = cargas(plazos, a1)
    cols = [1 - f1, f1, f2]
    if a2 is not None:
        cols.append(cargas(plazos, a2)[1])
    return np.column_stack(cols)


def mco_restringido(X, y):
    """Dado(s) a, el modelo es LINEAL en los parametros => minimos cuadrados
    exactos (con cotas b0>=0, g>=0 via BVLS si la solucion libre las viola)."""
    p, *_ = np.linalg.lstsq(X, y, rcond=None)
    if p[0] < 0 or p[1] < 0:
        lb = np.r_[0.0, 0.0, np.full(X.shape[1] - 2, -np.inf)]
        p = lsq_linear(X, y, bounds=(lb, np.inf), method="bvls").x
    e = y - X @ p
    b = p.copy()
    b[1] = p[1] - p[0]                       # volver a b1 = g - b0
    return b, float(e @ e)


# -----------------------------------------------------------------------------
# Estimacion GLOBAL
#  Paso 1: dados los parametros no lineales (a1, a2) el problema es lineal en
#          los beta => se resuelven exactamente ("beta concentrados").
#  Paso 2: busqueda exhaustiva en una grilla fina (logaritmica) de a1 (NS) o
#          de (a1, a2) (Svensson) dentro de la region admisible.
#  Paso 3: refinamiento local (Nelder-Mead) desde los 5 mejores puntos.
#  Paso 4: verificacion: cientos de optimizaciones locales de TODOS los
#          parametros desde puntos iniciales aleatorios; ninguna debe superar
#          al optimo encontrado.
# -----------------------------------------------------------------------------
GRID = np.exp(np.linspace(np.log(A1_MIN), np.log(A1_MAX), 800))
GRID1_SV = np.exp(np.linspace(np.log(A1_MIN), np.log(A1_MAX), 130))
GRID2_SV = np.exp(np.linspace(np.log(A1_MIN), np.log(A2_MAX), 170))
L1, H1, H2 = np.log(A1_MIN), np.log(A1_MAX), np.log(A2_MAX)


def sse_ns_a(a1, y):
    return mco_restringido(diseno(a1), y)[1]


def sse_sv_a(a1, a2, y):
    if abs(np.log(a2 / a1)) < 0.05:          # evita colinealidad exacta
        return np.inf
    return mco_restringido(diseno(a1, a2), y)[1]


def ajustar_ns(y):
    sse_grid = np.array([sse_ns_a(a, y) for a in GRID])
    best = (np.inf, None)
    for a0 in GRID[np.argsort(sse_grid)[:5]]:
        res = minimize(lambda la: sse_ns_a(np.exp(np.clip(la[0], L1, H1)), y), [np.log(a0)],
                       method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14})
        if res.fun < best[0]:
            best = (res.fun, float(np.exp(np.clip(res.x[0], L1, H1))))
    a1 = best[1]
    b, sse = mco_restringido(diseno(a1), y)
    return {"b": b, "a1": a1, "sse": sse, "sse_grid": sse_grid}


def ajustar_sv(y):
    pts = sorted(((sse_sv_a(a1, a2, y), a1, a2) for a1 in GRID1_SV for a2 in GRID2_SV),
                 key=lambda z: z[0])
    best = (np.inf, None, None)
    for _, a1, a2 in pts[:5]:
        f = lambda la: sse_sv_a(np.exp(np.clip(la[0], L1, H1)), np.exp(np.clip(la[1], L1, H2)), y)
        res = minimize(f, [np.log(a1), np.log(a2)], method="Nelder-Mead",
                       options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 4000})
        if res.fun < best[0]:
            best = (res.fun, float(np.exp(np.clip(res.x[0], L1, H1))),
                    float(np.exp(np.clip(res.x[1], L1, H2))))
    _, a1, a2 = best
    b, sse = mco_restringido(diseno(a1, a2), y)
    return {"b": b, "a1": a1, "a2": a2, "sse": sse}


def multi_inicio(y, modelo, n_inicios=300):
    """Optimizacion local 'ingenua' de TODOS los parametros a la vez (como haria
    un optimizador estandar) desde n puntos iniciales aleatorios.  Devuelve la
    SSE final de cada intento: sirve para (i) verificar que nadie supera nuestro
    optimo y (ii) mostrar que existen minimos locales."""
    if modelo == "ns":
        lb = [0, 0, -30, A1_MIN]
        ub = [20, 20, 30, A1_MAX]
        fr = lambda p: diseno(p[3]) @ p[:3] - y
        p0f = lambda: [rng.uniform(0, 6), rng.uniform(0, 6), rng.uniform(-10, 10),
                       np.exp(rng.uniform(L1, H1))]
    else:
        lb = [0, 0, -40, -40, A1_MIN, A1_MIN]
        ub = [20, 20, 40, 40, A1_MAX, A2_MAX]
        fr = lambda p: diseno(p[4], p[5]) @ p[:4] - y
        p0f = lambda: [rng.uniform(0, 6), rng.uniform(0, 6), rng.uniform(-10, 10),
                       rng.uniform(-10, 10), np.exp(rng.uniform(L1, H1)), np.exp(rng.uniform(L1, H2))]
    finales = []
    for _ in range(n_inicios):
        try:
            r_ = least_squares(fr, p0f(), bounds=(lb, ub), method="trf", xtol=1e-12,
                               ftol=1e-12, max_nfev=3000)
            finales.append(2 * r_.cost)
        except Exception:  # noqa: BLE001
            continue
    return np.array(finales)


res_ns, res_sv, filas, verif = {}, {}, [], {}
for fch, y in curvas.iterrows():
    y = y.values.astype(float)
    rn = ajustar_ns(y)
    rs = ajustar_sv(y)
    mi_ns = multi_inicio(y, "ns")
    mi_sv = multi_inicio(y, "sv", 200)
    res_ns[fch], res_sv[fch] = rn, rs
    verif[str(fch)] = {
        "ns_min_multi": float(mi_ns.min()), "ns_pct_global": float(np.mean(mi_ns <= rn["sse"] * 1.001 + 1e-10)),
        "sv_min_multi": float(mi_sv.min()), "sv_pct_global": float(np.mean(mi_sv <= rs["sse"] * 1.001 + 1e-10)),
        "ns_sse": rn["sse"], "sv_sse": rs["sse"]}
    n = len(y)
    fila = {"Fecha": fch,
            "NS b0": rn["b"][0], "NS b1": rn["b"][1], "NS b2": rn["b"][2], "NS a1": rn["a1"],
            "SV b0": rs["b"][0], "SV b1": rs["b"][1], "SV b2": rs["b"][2], "SV b3": rs["b"][3],
            "SV a1": rs["a1"], "SV a2": rs["a2"],
            "RMSE NS (pb)": 100 * np.sqrt(rn["sse"] / n), "RMSE SV (pb)": 100 * np.sqrt(rs["sse"] / n),
            "RMSE ajust. NS (pb)": 100 * np.sqrt(rn["sse"] / (n - 4)),
            "RMSE ajust. SV (pb)": 100 * np.sqrt(rs["sse"] / (n - 6)),
            "SSE NS": rn["sse"], "SSE SV": rs["sse"],
            "% inicios al optimo NS": 100 * verif[str(fch)]["ns_pct_global"],
            "% inicios al optimo SV": 100 * verif[str(fch)]["sv_pct_global"]}
    # Criterio de informacion (penaliza parametros): BIC = n ln(SSE/n) + k ln(n)
    fila["BIC NS"] = n * np.log(rn["sse"] / n) + 4 * np.log(n)
    fila["BIC SV"] = n * np.log(rs["sse"] / n) + 6 * np.log(n)
    filas.append(fila)
    print(f"{fch}: NS rmse={fila['RMSE NS (pb)']:.2f}pb (multi-inicio min {100*np.sqrt(mi_ns.min()/n):.2f}, "
          f"{fila['% inicios al optimo NS']:.0f}% llegan) | SV rmse={fila['RMSE SV (pb)']:.2f}pb "
          f"(multi-inicio min {100*np.sqrt(mi_sv.min()/n):.2f}, {fila['% inicios al optimo SV']:.0f}% llegan)")
param = pd.DataFrame(filas).set_index("Fecha")
param["Mejora RMSE (%)"] = 100 * (1 - param["RMSE SV (pb)"] / param["RMSE NS (pb)"])
param["Global OK NS"] = [verif[str(f)]["ns_min_multi"] >= verif[str(f)]["ns_sse"] - 1e-8 for f in param.index]
param["Global OK SV"] = [verif[str(f)]["sv_min_multi"] >= verif[str(f)]["sv_sse"] - 1e-8 for f in param.index]
param.to_csv(TABLAS / "2_parametros_NS_SV.csv")

# Robustez: NS SIN restricciones (a1 en [0.05, 30], betas libres)
sin_rest = []
for fch, y in curvas.iterrows():
    y = y.values.astype(float)
    best = None
    for a in np.exp(np.linspace(np.log(0.05), np.log(30), 1500)):
        f1, f2 = cargas(plazos, a)
        X = np.column_stack([np.ones_like(plazos), f1, f2])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b
        if best is None or e @ e < best[0]:
            best = (float(e @ e), a, b)
    sin_rest.append({"Fecha": fch, "a1": best[1], "b0": best[2][0], "b1": best[2][1], "b2": best[2][2],
                     "R(0)=b0+b1": best[2][0] + best[2][1], "RMSE (pb)": 100 * np.sqrt(best[0] / len(y))})
sin_rest = pd.DataFrame(sin_rest).set_index("Fecha")
sin_rest.to_csv(TABLAS / "2_NS_sin_restricciones_robustez.csv")
print(sin_rest.round(3).to_string())

demo = {"pct_min_ns": float(param["% inicios al optimo NS"].min()),
        "fecha_min_ns": str(param["% inicios al optimo NS"].idxmin()),
        "pct_min_sv": float(param["% inicios al optimo SV"].min()),
        "fecha_min_sv": str(param["% inicios al optimo SV"].idxmin()),
        "pct_medio_ns": float(param["% inicios al optimo NS"].mean()),
        "pct_medio_sv": float(param["% inicios al optimo SV"].mean())}
print("Multi-inicio:", demo)

# Residuos por plazo (pb)
resid_ns = pd.DataFrame({f: 100 * (curvas.loc[f].values - ns(plazos, res_ns[f]["b"], res_ns[f]["a1"]))
                         for f in curvas.index}, index=ETIQUETAS_PLAZO).T
resid_sv = pd.DataFrame({f: 100 * (curvas.loc[f].values - sv(plazos, res_sv[f]["b"], res_sv[f]["a1"], res_sv[f]["a2"]))
                         for f in curvas.index}, index=ETIQUETAS_PLAZO).T
resid_ns.to_csv(TABLAS / "2_residuos_NS_pb.csv")
resid_sv.to_csv(TABLAS / "2_residuos_SV_pb.csv")
mejora_plazo = (resid_ns.abs() - resid_sv.abs())          # >0 => Svensson mejora en ese plazo

# -----------------------------------------------------------------------------
# Figuras
# -----------------------------------------------------------------------------
tt = np.linspace(1 / 52, 30, 400)
fig, axes = plt.subplots(2, 5, figsize=(15, 6.4), sharex=True)
for ax, f in zip(axes.ravel(), curvas.index):
    y = curvas.loc[f].values
    ax.scatter(plazos, y, color="k", s=16, zorder=5, label="Observado (H.15)")
    ax.plot(tt, ns(tt, res_ns[f]["b"], res_ns[f]["a1"]), color="#1f3b73", lw=1.8,
            label="Nelson-Siegel")
    ax.plot(tt, sv(tt, res_sv[f]["b"], res_sv[f]["a1"], res_sv[f]["a2"]), color="#c0392b",
            lw=1.4, ls="--", label="Svensson")
    p = param.loc[f]
    ax.set_title(f"{pd.Timestamp(f):%d-%m-%Y}", fontsize=10)
    ax.text(0.97, 0.05, f"RMSE NS {p['RMSE NS (pb)']:.1f} pb\nRMSE SV {p['RMSE SV (pb)']:.1f} pb",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5,
            bbox=dict(boxstyle="round", fc="white", ec="0.8"))
    ax.set_xticks([0, 5, 10, 20, 30])
for ax in axes[1]:
    ax.set_xlabel("Plazo (años)")
for ax in axes[:, 0]:
    ax.set_ylabel("Tasa (%)")
axes[0, 0].legend(fontsize=7, loc="upper left")
fig.suptitle("P2 – Ajuste Nelson-Siegel y Svensson: último día transado de junio, 2017–2026",
             fontweight="bold")
guardar_fig(fig, FIGURAS / "F16_ajustes_NS_SV.png")

# Evolucion de las curvas (NS) en un solo grafico
fig, ax = plt.subplots(figsize=(9, 5.6))
cmap = plt.get_cmap("viridis")
for k, f in enumerate(curvas.index):
    col = cmap(k / (len(curvas) - 1))
    ax.plot(tt, sv(tt, res_sv[f]["b"], res_sv[f]["a1"], res_sv[f]["a2"]), color=col, lw=2,
            label=f"{pd.Timestamp(f):%b-%Y}")
    ax.scatter(plazos, curvas.loc[f].values, color=col, s=12)
ax.set_xlabel("Plazo (años)"); ax.set_ylabel("Tasa (%)")
ax.set_title("Curva de tasas del Tesoro de EE.UU. a fines de junio (ajuste Svensson)")
ax.legend(ncol=2, fontsize=8, loc="lower right")
guardar_fig(fig, FIGURAS / "F17_evolucion_curvas.png")

# Parametros NS en el tiempo vs. medidas empiricas
c = curvas
nivel_emp = c["10A"]
pend_emp = c["3M"] - c["10A"]                          # comparable con b1 (= corto - largo)
curv_emp = 2 * c["2A"] - c["3M"] - c["10A"]            # "mariposa"
anios = [pd.Timestamp(f).year for f in curvas.index]
fig, axes = plt.subplots(2, 2, figsize=(11, 7.2))
ax = axes[0, 0]
ax.plot(anios, param["NS b0"], "o-", color="#1f3b73", lw=2, label="β0 (Nelson-Siegel)")
ax.plot(anios, nivel_emp.values, "s--", color="0.5", label="Tasa 10 años (observada)")
ax.plot(anios, c["30A"].values, "^:", color="0.7", label="Tasa 30 años (observada)")
ax.set_title("Nivel: β0 = tasa de largo plazo R(∞)"); ax.set_ylabel("%"); ax.legend(fontsize=8)
ax = axes[0, 1]
ax.plot(anios, param["NS b1"], "o-", color="#c0392b", lw=2, label="β1 (Nelson-Siegel)")
ax.plot(anios, pend_emp.values, "s--", color="0.5", label="3M − 10A (observado)")
ax.axhline(0, color="k", lw=0.8)
ax.set_title("Pendiente: β1 = R(0) − R(∞)  (β1 > 0 ⇒ curva invertida)"); ax.legend(fontsize=8)
ax = axes[1, 0]
ax.plot(anios, param["NS b2"], "o-", color="#16a085", lw=2, label="β2 (Nelson-Siegel)")
ax.plot(anios, curv_emp.values, "s--", color="0.5", label="2·2A − 3M − 10A (observado)")
ax.axhline(0, color="k", lw=0.8)
ax.set_title("Curvatura: β2 (> 0 joroba, < 0 valle)"); ax.set_ylabel("%"); ax.legend(fontsize=8)
ax = axes[1, 1]
ax.plot(anios, param["NS b0"] + param["NS b1"], "o-", color="#8e44ad", lw=2, label="β0 + β1 = R(0) (tasa instantánea)")
ff = pd.read_csv(DATOS / "fed_funds_h15_semanal.csv", index_col=0, parse_dates=True)["FedFunds_efectiva"]
ff_jun = [ff.loc[:pd.Timestamp(f)].iloc[-1] for f in curvas.index]
ax.plot(anios, ff_jun, "s--", color="0.5", label="Fondos federales efectiva (H.15)")
ax2 = ax.twinx()
ax2.plot(anios, param["NS a1"], "d:", color="#e67e22", label="α1 (eje der., años)")
ax2.set_ylabel("α1 (años)", color="#e67e22"); ax2.grid(False)
ax.set_title("Tasa corta implícita R(0) y parámetro de decaimiento α1"); ax.set_ylabel("%")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
for a_ in axes.ravel():
    a_.set_xticks(anios); a_.tick_params(axis="x", labelsize=8)
fig.suptitle("Evolución de los parámetros de Nelson-Siegel (fines de junio, 2017–2026)", fontweight="bold")
guardar_fig(fig, FIGURAS / "F18_parametros_NS.png")

# RMSE por fecha y residuos por plazo
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1, 1.25]})
ax = axes[0]
xx = np.arange(len(anios))
ax.bar(xx - 0.2, param["RMSE NS (pb)"], 0.4, color="#1f3b73", label="Nelson-Siegel")
ax.bar(xx + 0.2, param["RMSE SV (pb)"], 0.4, color="#c0392b", label="Svensson")
ax.set_xticks(xx); ax.set_xticklabels(anios, fontsize=8)
ax.set_ylabel("RMSE (puntos base)"); ax.set_title("Error de ajuste por fecha"); ax.legend()
ax = axes[1]
im = ax.imshow(mejora_plazo.values, cmap="RdBu", vmin=-8, vmax=8, aspect="auto")
ax.set_xticks(range(len(ETIQUETAS_PLAZO))); ax.set_xticklabels(ETIQUETAS_PLAZO)
ax.set_yticks(range(len(anios))); ax.set_yticklabels(anios)
for i in range(mejora_plazo.shape[0]):
    for j in range(mejora_plazo.shape[1]):
        ax.text(j, i, f"{mejora_plazo.values[i, j]:.1f}", ha="center", va="center", fontsize=6.5)
ax.grid(False)
fig.colorbar(im, ax=ax, label="|error NS| − |error SV| (pb)")
ax.set_title("¿Dónde mejora Svensson? (azul = SV ajusta mejor)")
guardar_fig(fig, FIGURAS / "F19_rmse_residuos.png")

# Funcion objetivo de NS vs a1 (multiples minimos locales)
fig, ax = plt.subplots(figsize=(8.4, 4.4))
for k, f in enumerate(curvas.index):
    ax.plot(GRID, res_ns[f]["sse_grid"], color=cmap(k / (len(curvas) - 1)), lw=1.3,
            label=f"{pd.Timestamp(f).year}")
    ax.scatter([res_ns[f]["a1"]], [res_ns[f]["sse"]], color=cmap(k / (len(curvas) - 1)), s=25, zorder=5)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("α1 (años, escala log)"); ax.set_ylabel("SSE mínima dado α1 (β por MCO)")
ax.set_title("Nelson-Siegel: SSE mínima para cada α1 (punto = óptimo global)")
ax.legend(ncol=5, fontsize=7.5)
guardar_fig(fig, FIGURAS / "F20_funcion_objetivo_NS.png")

# -----------------------------------------------------------------------------
# Inversiones de la curva (datos diarios 2017 - ultimo dato disponible)
# -----------------------------------------------------------------------------
d = h15.loc["2017-01-01":, ["3M", "2A", "10A", "30A"]].dropna()
d["10A-3M"] = d["10A"] - d["3M"]
d["10A-2A"] = d["10A"] - d["2A"]


def episodios(s, min_dias=5, gap=20):
    """Tramos con spread < 0; se unen tramos separados por < gap dias habiles."""
    neg = (s < 0).values
    idx = s.index
    eps, i = [], 0
    while i < len(neg):
        if neg[i]:
            j = i
            while j + 1 < len(neg) and (neg[j + 1] or (neg[j + 1:j + 1 + gap].any())):
                j += 1
            seg = s.iloc[i:j + 1]
            if (seg < 0).sum() >= min_dias:
                eps.append({"inicio": idx[i].date(), "fin": idx[j].date(),
                            "dias_habiles_invertida": int((seg < 0).sum()),
                            "meses": round((idx[j] - idx[i]).days / 30.44, 1),
                            "spread_minimo_pb": round(100 * seg.min(), 0),
                            "fecha_minimo": seg.idxmin().date()})
            i = j + 1
        else:
            i += 1
    return eps


inv = {"10A-3M": episodios(d["10A-3M"]), "10A-2A": episodios(d["10A-2A"])}
for k, v in inv.items():
    print(k, pd.DataFrame(v).to_string())

junio_inv = pd.DataFrame({
    "10A-3M (pb)": 100 * (curvas["10A"] - curvas["3M"]),
    "10A-2A (pb)": 100 * (curvas["10A"] - curvas["2A"]),
    "Max(corto) - 10A (pb)": 100 * (curvas[["1M", "3M", "6M", "1A"]].max(axis=1) - curvas["10A"]),
    "Plazo con tasa mínima": curvas.idxmin(axis=1),
    "Plazo con tasa máxima": curvas.idxmax(axis=1),
})
junio_inv["¿Invertida (10A<3M)?"] = junio_inv["10A-3M (pb)"] < 0
junio_inv.to_csv(TABLAS / "2_inversion_fechas_junio.csv")
print(junio_inv.to_string())

macro = pd.read_csv(DATOS / "macro_bls.csv", index_col=0, parse_dates=True)
fig, axes = plt.subplots(2, 1, figsize=(11, 7.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
ax = axes[0]
for col, c_ in [("3M", "#e67e22"), ("2A", "#16a085"), ("10A", "#1f3b73"), ("30A", "#8e44ad")]:
    ax.plot(d.index, d[col], color=c_, lw=1.2, label=f"Tesoro {col}")
ax.step(ff.loc["2017":].index, ff.loc["2017":], color="k", lw=1, where="post", label="Fondos federales efectiva")
ax.plot(macro.loc["2017":].index, macro.loc["2017":, "Inflacion_12m"], color="#c0392b", lw=1, ls=":",
        label="Inflación IPC 12 meses")
for f in curvas.index:
    ax.axvline(pd.Timestamp(f), color="0.6", lw=0.6, ls="--")
ax.set_ylabel("%"); ax.legend(ncol=3, fontsize=8, loc="upper left")
ax.set_title("Tasas del Tesoro, política monetaria e inflación (líneas verticales: fechas de ajuste)")
ax = axes[1]
ax.plot(d.index, 100 * d["10A-3M"], color="#c0392b", lw=1.2, label="10A − 3M")
ax.plot(d.index, 100 * d["10A-2A"], color="#1f3b73", lw=1.2, label="10A − 2A")
ax.axhline(0, color="k", lw=0.8)
for e in inv["10A-3M"]:
    ax.axvspan(pd.Timestamp(e["inicio"]), pd.Timestamp(e["fin"]), color="#c0392b", alpha=0.10)
ax.axvspan(pd.Timestamp("2020-02-01"), pd.Timestamp("2020-04-30"), color="0.3", alpha=0.25,
           label="Recesión NBER (feb–abr 2020)")
ax.set_ylabel("Spread (pb)"); ax.legend(fontsize=8, loc="lower left")
ax.set_title("Pendiente de la curva: episodios de inversión (sombreado rojo: 10A − 3M < 0)")
guardar_fig(fig, FIGURAS / "F21_spreads_inversion.png")

# -----------------------------------------------------------------------------
# Guardar
# -----------------------------------------------------------------------------
guardar_json({"fechas": [str(f) for f in curvas.index], "demo_minimos_locales": demo, "verificacion": verif,
              "inversiones": {k: [{a: str(b) if not isinstance(b, (int, float)) else b for a, b in e.items()}
                                  for e in v] for k, v in inv.items()},
              "mejora_media_por_plazo_pb": mejora_plazo.mean().to_dict(),
              "ultimo_dato_h15": str(h15.dropna().index[-1].date()),
              "curva_ultimo_dato": h15.dropna().iloc[-1].to_dict(),
              "curva_rf": h15.loc["2026-07-31"].to_dict()},
             RESULTADOS / "p2_resultados.json")
with pd.ExcelWriter(TABLAS / "Resultados_Pregunta2.xlsx") as xw:
    curvas.to_excel(xw, sheet_name="Curvas_observadas")
    param.to_excel(xw, sheet_name="Parametros_RMSE")
    resid_ns.to_excel(xw, sheet_name="Residuos_NS_pb")
    resid_sv.to_excel(xw, sheet_name="Residuos_SV_pb")
    junio_inv.to_excel(xw, sheet_name="Inversion_junio")
    for k, v in inv.items():
        pd.DataFrame(v).to_excel(xw, sheet_name=f"Episodios_{k}", index=False)
    d.to_excel(xw, sheet_name="Tasas_diarias_spreads")
print(param[["NS b0", "NS b1", "NS b2", "NS a1", "RMSE NS (pb)", "RMSE SV (pb)", "Mejora RMSE (%)",
             "Global OK NS", "Global OK SV"]].round(3).to_string())
print(param[["SV b0", "SV b1", "SV b2", "SV b3", "SV a1", "SV a2", "BIC NS", "BIC SV"]].round(3).to_string())
print(mejora_plazo.round(2).to_string())
