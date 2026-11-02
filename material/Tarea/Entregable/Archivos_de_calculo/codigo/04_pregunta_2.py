# =============================================================================
#  04_pregunta_2.py  -  Pregunta 2: Nelson-Siegel y Svensson
#  Ajusta ambos modelos a la curva del Tesoro (Fed H.15) del ultimo dia
#  transado de junio de 2017 a 2026, compara el RMSE, grafica beta0, beta1 y
#  beta2 y busca los periodos de curva invertida.  Guarda las figuras F16, F18,
#  F21 y Resultados_Pregunta2.xlsx
#
#  Nelson-Siegel (notacion de clase):
#     R(t) = b0 + b1*[(1-e^{-t/a1}) a1/t] + b2*[(1-e^{-t/a1}) a1/t - e^{-t/a1}]
#  Svensson agrega:  b3*[(1-e^{-t/a2}) a2/t - e^{-t/a2}]
#  Plazo t en años (dias transados / dias transados: 1 mes = 1/12)
# =============================================================================
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, lsq_linear, minimize

from config import ANIOS_CURVA, DATOS, ETIQUETAS_PLAZO, FIGURAS, PLAZOS_H15, TABLAS
from utilidades import guardar_fig

sys.stdout.reconfigure(encoding="utf-8")
rng = np.random.default_rng(1987)       # semilla fija para los puntos iniciales aleatorios

# Restricciones para que los parametros tengan sentido economico:
#   b0 >= 0 (tasa de largo plazo no negativa), b0 + b1 >= 0 (tasa corta no negativa),
#   0.1 <= a1 <= 10 años y 0.1 <= a2 <= 30 años
A1_MIN, A1_MAX = 0.10, 10.0
A2_MAX = 30.0

# -----------------------------------------------------------------------------
# Datos: curva del ultimo dia transado de junio de cada año
# -----------------------------------------------------------------------------
h15 = pd.read_csv(DATOS / "tasas_h15.csv", index_col=0, parse_dates=True)
h15 = h15[list(PLAZOS_H15)]
h15.columns = ETIQUETAS_PLAZO
plazos = np.array(list(PLAZOS_H15.values()))

fechas = [h15.loc[f"{a}-06"].dropna(how="all").index[-1] for a in ANIOS_CURVA]
curvas = h15.loc[fechas]
curvas.index = curvas.index.date
print(curvas.to_string())


# -----------------------------------------------------------------------------
# Modelos
# -----------------------------------------------------------------------------
def cargas(t, a):
    """Las dos 'cargas' del modelo: pendiente f1 y curvatura f2."""
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
    """Matriz de regresion escrita como R = b0 (1 - f1) + g f1 + b2 f2 (+ b3 f3),
    con g = b0 + b1 = R(0); asi las restricciones b0 >= 0 y g >= 0 son cotas simples."""
    f1, f2 = cargas(plazos, a1)
    cols = [1 - f1, f1, f2]
    if a2 is not None:
        cols.append(cargas(plazos, a2)[1])
    return np.column_stack(cols)


def mco_restringido(X, y):
    """Dados los alfas el modelo es lineal en los betas: minimos cuadrados
    (con las cotas b0 >= 0, g >= 0 si la solucion libre no las cumple)."""
    p, *_ = np.linalg.lstsq(X, y, rcond=None)
    if p[0] < 0 or p[1] < 0:
        lb = np.r_[0.0, 0.0, np.full(X.shape[1] - 2, -np.inf)]
        p = lsq_linear(X, y, bounds=(lb, np.inf), method="bvls").x
    e = y - X @ p
    b = p.copy()
    b[1] = p[1] - p[0]                       # b1 = g - b0
    return b, float(e @ e)


# -----------------------------------------------------------------------------
# Busqueda del optimo global (la funcion de error tiene minimos locales):
#  1) para cada alfa los betas salen por minimos cuadrados (exacto)
#  2) se prueba una grilla fina de alfas (NS) o de pares (a1, a2) (Svensson)
#  3) se refina con Nelder-Mead desde los 5 mejores puntos de la grilla
#  4) se verifica con cientos de optimizaciones desde puntos iniciales al azar
# -----------------------------------------------------------------------------
GRID = np.exp(np.linspace(np.log(A1_MIN), np.log(A1_MAX), 800))
GRID1_SV = np.exp(np.linspace(np.log(A1_MIN), np.log(A1_MAX), 130))
GRID2_SV = np.exp(np.linspace(np.log(A1_MIN), np.log(A2_MAX), 170))
L1, H1, H2 = np.log(A1_MIN), np.log(A1_MAX), np.log(A2_MAX)


def sse_ns_a(a1, y):
    return mco_restringido(diseno(a1), y)[1]


def sse_sv_a(a1, a2, y):
    if abs(np.log(a2 / a1)) < 0.05:          # a1 = a2 haria colineales las dos curvaturas
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
    b, sse = mco_restringido(diseno(best[1]), y)
    return {"b": b, "a1": best[1], "sse": sse}


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
    """Optimiza todos los parametros a la vez desde puntos iniciales al azar y
    devuelve el error final de cada intento (para verificar el optimo global)."""
    if modelo == "ns":
        lb, ub = [0, 0, -30, A1_MIN], [20, 20, 30, A1_MAX]
        fr = lambda p: diseno(p[3]) @ p[:3] - y
        p0f = lambda: [rng.uniform(0, 6), rng.uniform(0, 6), rng.uniform(-10, 10),
                       np.exp(rng.uniform(L1, H1))]
    else:
        lb, ub = [0, 0, -40, -40, A1_MIN, A1_MIN], [20, 20, 40, 40, A1_MAX, A2_MAX]
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


res_ns, res_sv, filas = {}, {}, []
for fch, y in curvas.iterrows():
    y = y.values.astype(float)
    rn, rs = ajustar_ns(y), ajustar_sv(y)
    mi_ns, mi_sv = multi_inicio(y, "ns"), multi_inicio(y, "sv", 200)
    res_ns[fch], res_sv[fch] = rn, rs
    n = len(y)
    filas.append({
        "Fecha": fch,
        "NS b0": rn["b"][0], "NS b1": rn["b"][1], "NS b2": rn["b"][2], "NS a1": rn["a1"],
        "SV b0": rs["b"][0], "SV b1": rs["b"][1], "SV b2": rs["b"][2], "SV b3": rs["b"][3],
        "SV a1": rs["a1"], "SV a2": rs["a2"],
        "RMSE NS (pb)": 100 * np.sqrt(rn["sse"] / n), "RMSE SV (pb)": 100 * np.sqrt(rs["sse"] / n),
        # verificacion: ningun inicio aleatorio debe lograr un error menor
        "Optimo global NS": mi_ns.min() >= rn["sse"] - 1e-8,
        "Optimo global SV": mi_sv.min() >= rs["sse"] - 1e-8,
        "% inicios al optimo NS": 100 * np.mean(mi_ns <= rn["sse"] * 1.001 + 1e-10),
        "% inicios al optimo SV": 100 * np.mean(mi_sv <= rs["sse"] * 1.001 + 1e-10),
    })
param = pd.DataFrame(filas).set_index("Fecha")
param["Mejora RMSE (%)"] = 100 * (1 - param["RMSE SV (pb)"] / param["RMSE NS (pb)"])
print(param[["NS b0", "NS b1", "NS b2", "NS a1", "RMSE NS (pb)", "RMSE SV (pb)", "Mejora RMSE (%)",
             "Optimo global NS", "Optimo global SV"]].round(3).to_string())
print(f"Inicios aleatorios que llegan al optimo: NS {param['% inicios al optimo NS'].mean():.0f}%, "
      f"Svensson {param['% inicios al optimo SV'].mean():.0f}%")

# ¿Que pasa sin las restricciones? (NS con betas libres y a1 entre 0.05 y 30)
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

# ¿En que plazos mejora Svensson?  |error NS| - |error SV| en puntos base
err_ns = pd.DataFrame({f: 100 * (curvas.loc[f].values - ns(plazos, res_ns[f]["b"], res_ns[f]["a1"]))
                       for f in curvas.index}, index=ETIQUETAS_PLAZO).T
err_sv = pd.DataFrame({f: 100 * (curvas.loc[f].values - sv(plazos, res_sv[f]["b"], res_sv[f]["a1"], res_sv[f]["a2"]))
                       for f in curvas.index}, index=ETIQUETAS_PLAZO).T
mejora_plazo = err_ns.abs() - err_sv.abs()
print("Mejora promedio por plazo (pb):", mejora_plazo.mean().round(1).to_dict())

# -----------------------------------------------------------------------------
# Figura: curvas observadas y ajustadas
# -----------------------------------------------------------------------------
tt = np.linspace(1 / 52, 30, 400)
fig, axes = plt.subplots(2, 5, figsize=(15, 6.4), sharex=True)
for ax, f in zip(axes.ravel(), curvas.index):
    ax.scatter(plazos, curvas.loc[f].values, color="k", s=16, zorder=5, label="Observado (H.15)")
    ax.plot(tt, ns(tt, res_ns[f]["b"], res_ns[f]["a1"]), color="#1f3b73", lw=1.8, label="Nelson-Siegel")
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

# -----------------------------------------------------------------------------
# Figura: evolucion de beta0 (nivel), beta1 (pendiente) y beta2 (curvatura)
# comparados con sus equivalentes observados
# -----------------------------------------------------------------------------
c = curvas
anios = [pd.Timestamp(f).year for f in curvas.index]
ff = pd.read_csv(DATOS / "fed_funds_h15_semanal.csv", index_col=0, parse_dates=True)["FedFunds_efectiva"]
fig, axes = plt.subplots(2, 2, figsize=(11, 7.2))
ax = axes[0, 0]
ax.plot(anios, param["NS b0"], "o-", color="#1f3b73", lw=2, label="β0 (Nelson-Siegel)")
ax.plot(anios, c["10A"].values, "s--", color="0.5", label="Tasa 10 años (observada)")
ax.plot(anios, c["30A"].values, "^:", color="0.7", label="Tasa 30 años (observada)")
ax.set_title("Nivel: β0 = tasa de largo plazo R(∞)"); ax.set_ylabel("%"); ax.legend(fontsize=8)
ax = axes[0, 1]
ax.plot(anios, param["NS b1"], "o-", color="#c0392b", lw=2, label="β1 (Nelson-Siegel)")
ax.plot(anios, (c["3M"] - c["10A"]).values, "s--", color="0.5", label="3M − 10A (observado)")
ax.axhline(0, color="k", lw=0.8)
ax.set_title("Pendiente: β1 = R(0) − R(∞)  (β1 > 0 ⇒ curva invertida)"); ax.legend(fontsize=8)
ax = axes[1, 0]
ax.plot(anios, param["NS b2"], "o-", color="#16a085", lw=2, label="β2 (Nelson-Siegel)")
ax.plot(anios, (2 * c["2A"] - c["3M"] - c["10A"]).values, "s--", color="0.5", label="2·2A − 3M − 10A (observado)")
ax.axhline(0, color="k", lw=0.8)
ax.set_title("Curvatura: β2 (> 0 joroba, < 0 valle)"); ax.set_ylabel("%"); ax.legend(fontsize=8)
ax = axes[1, 1]
ax.plot(anios, param["NS b0"] + param["NS b1"], "o-", color="#8e44ad", lw=2, label="β0 + β1 = R(0) (tasa instantánea)")
ax.plot(anios, [ff.loc[:pd.Timestamp(f)].iloc[-1] for f in curvas.index], "s--", color="0.5",
        label="Fondos federales efectiva (H.15)")
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

# -----------------------------------------------------------------------------
# Curva invertida: con datos diarios se buscan los tramos en que la tasa a
# 10 años fue menor que la de 3 meses (o que la de 2 años)
# -----------------------------------------------------------------------------
d = h15.loc["2017-01-01":, ["3M", "2A", "10A", "30A"]].dropna()
d["10A-3M"] = d["10A"] - d["3M"]
d["10A-2A"] = d["10A"] - d["2A"]


def episodios(s, min_dias=5, gap=20):
    """Tramos con spread < 0 (se unen tramos separados por menos de 20 dias habiles)."""
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
                            "dias_invertida": int((seg < 0).sum()),
                            "spread_minimo_pb": round(100 * seg.min(), 0),
                            "fecha_minimo": seg.idxmin().date()})
            i = j + 1
        else:
            i += 1
    return eps


inv = {"10A-3M": episodios(d["10A-3M"]), "10A-2A": episodios(d["10A-2A"])}
for k, v in inv.items():
    print(k, pd.DataFrame(v).to_string(), sep="\n")

junio_inv = pd.DataFrame({
    "10A-3M (pb)": 100 * (curvas["10A"] - curvas["3M"]),
    "10A-2A (pb)": 100 * (curvas["10A"] - curvas["2A"]),
    "Plazo con tasa minima": curvas.idxmin(axis=1),
    "Plazo con tasa maxima": curvas.idxmax(axis=1),
})
junio_inv["Invertida (10A < 3M)"] = junio_inv["10A-3M (pb)"] < 0
print(junio_inv.to_string())

# Figura: tasas, politica monetaria, inflacion y pendientes de la curva
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
# Guardar en Excel
# -----------------------------------------------------------------------------
with pd.ExcelWriter(TABLAS / "Resultados_Pregunta2.xlsx") as xw:
    curvas.to_excel(xw, sheet_name="Curvas_observadas")
    param.to_excel(xw, sheet_name="Parametros_y_RMSE")
    mejora_plazo.to_excel(xw, sheet_name="Mejora_SV_por_plazo_pb")
    sin_rest.to_excel(xw, sheet_name="NS_sin_restricciones")
    junio_inv.to_excel(xw, sheet_name="Inversion_en_junio")
    for k, v in inv.items():
        pd.DataFrame(v).to_excel(xw, sheet_name=f"Episodios_{k}", index=False)
    d.to_excel(xw, sheet_name="Tasas_diarias_y_spreads")
print("Listo: Resultados_Pregunta2.xlsx y figuras F16, F18, F21")
