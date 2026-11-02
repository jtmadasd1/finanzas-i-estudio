# =============================================================================
#  FINANZAS I (ENFIN415) - TAREA 2026 - Prof. Alejandro Bernales
#  config.py : parametros generales compartidos por todos los scripts
# =============================================================================
from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"
RESULTADOS = BASE / "resultados"
FIGURAS = RESULTADOS / "figuras"
TABLAS = RESULTADOS / "tablas"
for _p in (DATOS, RESULTADOS, FIGURAS, TABLAS):
    _p.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Ventana de estimacion (Pregunta 1): 5 anios de retornos diarios.
# Se usa el precio del 30-jul-2021 solo para calcular el primer retorno
# (2-ago-2021); el ultimo precio es el cierre del 31-jul-2026.
# ---------------------------------------------------------------------------
FECHA_INICIO_PRECIOS = "2021-07-30"
FECHA_FIN = "2026-07-31"
DIAS_ANIO = 252  # dias transados por anio (para anualizar)

# ---------------------------------------------------------------------------
# 50 acciones del S&P 500 y su sector GICS.
# Requisito: al menos DOS acciones de Energy, Financials, Health Care,
# Industrials, Information Technology y Utilities.  Se agregan los otros cinco
# sectores GICS para que el universo se parezca mas al indice completo.
# Todas pertenecieron al S&P 500 durante toda la ventana (evita sesgo de
# supervivencia "dentro de la muestra" y series incompletas).
# ---------------------------------------------------------------------------
ACCIONES = {
    # Energy (5)
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy", "EOG": "Energy", "SLB": "Energy",
    # Industrials (6)
    "CAT": "Industrials", "UNP": "Industrials", "LMT": "Industrials",
    "DE": "Industrials", "WM": "Industrials", "RTX": "Industrials",
    # Financials (6)
    "JPM": "Financials", "BAC": "Financials", "GS": "Financials",
    "BRK-B": "Financials", "V": "Financials", "AXP": "Financials",
    # Health Care (6)
    "JNJ": "Health Care", "UNH": "Health Care", "PFE": "Health Care",
    "MRK": "Health Care", "ABBV": "Health Care", "LLY": "Health Care",
    # Information Technology (6)
    "AAPL": "Information Technology", "MSFT": "Information Technology",
    "NVDA": "Information Technology", "AVGO": "Information Technology",
    "ORCL": "Information Technology", "CSCO": "Information Technology",
    # Utilities (5)
    "NEE": "Utilities", "DUK": "Utilities", "SO": "Utilities",
    "AEP": "Utilities", "SRE": "Utilities",
    # Communication Services (4)
    "GOOGL": "Communication Services", "META": "Communication Services",
    "NFLX": "Communication Services", "VZ": "Communication Services",
    # Consumer Discretionary (4)
    "AMZN": "Consumer Discretionary", "HD": "Consumer Discretionary",
    "MCD": "Consumer Discretionary", "TSLA": "Consumer Discretionary",
    # Consumer Staples (4)
    "PG": "Consumer Staples", "KO": "Consumer Staples",
    "PEP": "Consumer Staples", "WMT": "Consumer Staples",
    # Materials (2)
    "LIN": "Materials", "NEM": "Materials",
    # Real Estate (2)
    "PLD": "Real Estate", "AMT": "Real Estate",
}
TICKERS = list(ACCIONES.keys())
assert len(TICKERS) == 50

INDICE = "^GSPC"          # S&P 500 (indice de precios, el pedido en la tarea)
INDICE_TR = "^SP500TR"    # S&P 500 Total Return (solo para robustez)

# Sectores de la restriccion de la pregunta 1A.6
SECTORES_RESTRICCION = ("Energy", "Industrials")
PESO_MIN_SECTORES = 0.40
LIMITE_CONCENTRACION = 0.10   # pregunta 1A.4: -0.10 <= w_i <= 0.10

# ---------------------------------------------------------------------------
# Pregunta 2: estructura de tasas (Fed H.15, Treasury Constant Maturities)
# ---------------------------------------------------------------------------
URL_H15 = ("https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15"
           "&series=bf17364827e38702b42a58cf8eaa3f78&lastobs=&from=&to="
           "&filetype=csv&label=include&layout=seriescolumn&type=package")
# Paquete H.15 de promedios semanales (fondos federales, prime, descuento)
URL_H15_FF = ("https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15"
              "&series=8e83f7f17c5cea4d190d85ae6737639f&lastobs=&from=&to="
              "&filetype=csv&label=include&layout=seriescolumn&type=package")
# Plazo de cada serie en anios (convencion dias transados / dias transados:
# 1 mes = 1/12 anio, etc.)
PLAZOS_H15 = {
    "RIFLGFCM01_N.B": 1 / 12, "RIFLGFCM03_N.B": 3 / 12, "RIFLGFCM06_N.B": 6 / 12,
    "RIFLGFCY01_N.B": 1.0, "RIFLGFCY02_N.B": 2.0, "RIFLGFCY03_N.B": 3.0,
    "RIFLGFCY05_N.B": 5.0, "RIFLGFCY07_N.B": 7.0, "RIFLGFCY10_N.B": 10.0,
    "RIFLGFCY20_N.B": 20.0, "RIFLGFCY30_N.B": 30.0,
}
ETIQUETAS_PLAZO = ["1M", "3M", "6M", "1A", "2A", "3A", "5A", "7A", "10A", "20A", "30A"]
ANIOS_CURVA = list(range(2017, 2027))   # junio de 2017 ... junio de 2026
FECHA_RF = "2026-07-31"                 # tasa libre de riesgo (1 anio) para la LMC
