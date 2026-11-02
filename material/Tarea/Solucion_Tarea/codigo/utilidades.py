# =============================================================================
#  utilidades.py : funciones compartidas (carga de datos, fronteras, graficos)
# =============================================================================
import json

import cvxpy as cp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

from config import ACCIONES, DATOS, DIAS_ANIO, FECHA_FIN, TICKERS

matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# Estilo de graficos (uniforme en todo el informe)
# ---------------------------------------------------------------------------
COLORES = {
    "frontera": "#1f3b73",      # azul oscuro: frontera sin restricciones (P2)
    "ingenua_real": "#c0392b",  # rojo: frontera ingenua, volatilidad real
    "ingenua_perc": "#e67e22",  # naranjo: frontera ingenua, volatilidad "percibida"
    "limite10": "#16a085",      # verde azulado: |w|<=10%
    "sin_vc": "#8e44ad",        # morado: sin venta corta
    "sector": "#b7950b",        # dorado: sin venta corta + Energy/Industrials>=40%
    "lmc": "#2c3e50",
    "sp500": "#d35400",
    "gris": "#7f8c8d",
}
COLOR_SECTOR = {
    "Energy": "#8c564b", "Industrials": "#7f7f7f", "Financials": "#1f77b4",
    "Health Care": "#2ca02c", "Information Technology": "#d62728",
    "Utilities": "#bcbd22", "Communication Services": "#9467bd",
    "Consumer Discretionary": "#ff7f0e", "Consumer Staples": "#17becf",
    "Materials": "#e377c2", "Real Estate": "#393b79",
}
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 200, "font.size": 10,
    "axes.titlesize": 11.5, "axes.titleweight": "bold", "axes.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "legend.fontsize": 8.5,
    "legend.frameon": False, "font.family": "DejaVu Sans",
})
PCT = FuncFormatter(lambda x, _: f"{x:.0%}")
PCT1 = FuncFormatter(lambda x, _: f"{x:.1%}")


def guardar_fig(fig, ruta):
    fig.tight_layout()
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
def cargar_retornos(hasta=FECHA_FIN):
    """Retornos diarios con capitalizacion continua r_t = ln(P_t / P_{t-1})
    (la tasa de retorno preferida en clase, Sesion I, lamina 10)."""
    precios = pd.read_csv(DATOS / "precios_acciones.csv", index_col=0,
                          parse_dates=True)[TICKERS]
    sp = pd.read_csv(DATOS / "precios_sp500.csv", index_col=0, parse_dates=True)
    r = np.log(precios).diff().dropna()
    rsp = np.log(sp).diff().dropna()
    r, rsp = r.loc[:hasta], rsp.loc[:hasta]
    return r, rsp


def momentos_anuales(r):
    """Media, volatilidad y matriz de covarianzas en base ANUAL.
    Con retornos continuos i.i.d.: mu_anual = 252*mu_diario,
    Var_anual = 252*Var_diaria (=> sigma_anual = sqrt(252)*sigma_diaria)."""
    mu = r.mean() * DIAS_ANIO
    omega = r.cov() * DIAS_ANIO
    sigma = np.sqrt(np.diag(omega))
    return mu, pd.Series(sigma, index=r.columns), omega


def sectores():
    return pd.Series(ACCIONES)


# ---------------------------------------------------------------------------
# Frontera media-varianza SIN restricciones (solucion analitica de clase)
#   min_w  w' Omega w   s.a.  w' mu = mu_bar ,  w' 1 = 1
#   Lagrangiano => w* = Omega^{-1} (lambda1 * 1 + lambda2 * mu)
#   Con A = 1'O^-1 1, B = 1'O^-1 mu, C = mu'O^-1 mu, D = AC - B^2:
#   sigma^2(mu_bar) = (A mu_bar^2 - 2 B mu_bar + C) / D
# ---------------------------------------------------------------------------
class FronteraAnalitica:
    def __init__(self, mu, omega):
        self.mu = np.asarray(mu, float)
        self.omega = np.asarray(omega, float)
        self.inv = np.linalg.inv(self.omega)
        uno = np.ones_like(self.mu)
        self.A = uno @ self.inv @ uno
        self.B = uno @ self.inv @ self.mu
        self.C = self.mu @ self.inv @ self.mu
        self.D = self.A * self.C - self.B ** 2
        self.uno = uno

    def pesos(self, mu_bar):
        lam1 = (self.C - self.B * mu_bar) / self.D
        lam2 = (self.A * mu_bar - self.B) / self.D
        return self.inv @ (lam1 * self.uno + lam2 * self.mu)

    def sigma(self, mu_bar):
        mu_bar = np.asarray(mu_bar, float)
        return np.sqrt((self.A * mu_bar ** 2 - 2 * self.B * mu_bar + self.C) / self.D)

    @property
    def mu_gmv(self):          # portafolio de minima varianza global
        return self.B / self.A

    @property
    def sigma_gmv(self):
        return np.sqrt(1 / self.A)

    def pesos_gmv(self):
        return self.inv @ self.uno / self.A

    def tangencia(self, rf):
        """Portafolio de tangencia M: maximiza Sharpe.
        w_M = O^{-1}(mu - rf 1) / 1'O^{-1}(mu - rf 1)."""
        z = self.inv @ (self.mu - rf * self.uno)
        w = z / z.sum()
        m = w @ self.mu
        s = np.sqrt(w @ self.omega @ w)
        return w, m, s, (m - rf) / s


# ---------------------------------------------------------------------------
# Frontera media-varianza CON restricciones (programacion cuadratica, cvxpy)
# ---------------------------------------------------------------------------
def _restricciones(w, tipo, sector_mask=None, lim=0.10, piso=0.40):
    cons = []
    if tipo == "limite":
        cons += [w <= lim, w >= -lim]
    elif tipo == "sin_vc":
        cons += [w >= 0]
    elif tipo == "sin_vc_sector":
        cons += [w >= 0, sector_mask @ w >= piso]
    elif tipo != "libre":
        raise ValueError(tipo)
    return cons


def rango_factible(mu, tipo, **kw):
    """Retorno minimo y maximo alcanzable bajo las restricciones (PL)."""
    n = len(mu)
    w = cp.Variable(n)
    base = [cp.sum(w) == 1] + _restricciones(w, tipo, **kw)
    lo = cp.Problem(cp.Minimize(mu @ w), base)
    lo.solve(solver=cp.CLARABEL)
    hi = cp.Problem(cp.Maximize(mu @ w), base)
    hi.solve(solver=cp.CLARABEL)
    return lo.value, hi.value


def frontera_restringida(mu, omega, tipo, mus, **kw):
    """Para cada retorno objetivo mu_bar resuelve
       min w'Omega w  s.a.  w'1 = 1, w'mu = mu_bar, + restricciones."""
    mu = np.asarray(mu, float)
    omega = np.asarray(omega, float)
    n = len(mu)
    w = cp.Variable(n)
    mu_bar = cp.Parameter()
    cons = [cp.sum(w) == 1, mu @ w == mu_bar] + _restricciones(w, tipo, **kw)
    prob = cp.Problem(cp.Minimize(cp.quad_form(w, cp.psd_wrap(omega))), cons)
    sig, pesos = [], []
    for m in mus:
        mu_bar.value = float(m)
        prob.solve(solver=cp.CLARABEL)
        if w.value is None or prob.status not in ("optimal", "optimal_inaccurate"):
            sig.append(np.nan)
            pesos.append(np.full(n, np.nan))
            continue
        ww = np.asarray(w.value).ravel()
        sig.append(np.sqrt(max(ww @ omega @ ww, 0)))
        pesos.append(ww)
    return np.array(sig), np.array(pesos)


def gmv_restringido(mu, omega, tipo, **kw):
    n = len(mu)
    w = cp.Variable(n)
    cons = [cp.sum(w) == 1] + _restricciones(w, tipo, **kw)
    cp.Problem(cp.Minimize(cp.quad_form(w, cp.psd_wrap(np.asarray(omega)))),
               cons).solve(solver=cp.CLARABEL)
    ww = np.asarray(w.value).ravel()
    return ww


def tangencia_restringida(mu, omega, rf, tipo, **kw):
    """Maximo Sharpe con restricciones lineales (homogeneas en w).
    Truco estandar: con y = w/k, min y'Oy s.a. (mu-rf)'y = 1 y las
    restricciones escaladas por k = 1'y >= 0."""
    mu = np.asarray(mu, float)
    omega = np.asarray(omega, float)
    n = len(mu)
    y = cp.Variable(n)
    k = cp.Variable(nonneg=True)
    cons = [(mu - rf) @ y == 1, cp.sum(y) == k]
    if tipo == "limite":
        lim = kw.get("lim", 0.10)
        cons += [y <= lim * k, y >= -lim * k]
    elif tipo == "sin_vc":
        cons += [y >= 0]
    elif tipo == "sin_vc_sector":
        cons += [y >= 0, kw["sector_mask"] @ y >= kw.get("piso", 0.40) * k]
    cp.Problem(cp.Minimize(cp.quad_form(y, cp.psd_wrap(omega))),
               cons).solve(solver=cp.CLARABEL)
    w = np.asarray(y.value).ravel() / k.value
    m = w @ mu
    s = np.sqrt(w @ omega @ w)
    return w, m, s, (m - rf) / s


def guardar_json(obj, ruta):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=conv)


def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)
