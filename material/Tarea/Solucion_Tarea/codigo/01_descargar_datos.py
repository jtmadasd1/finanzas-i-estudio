# =============================================================================
#  01_descargar_datos.py
#  Descarga todos los datos usados en la tarea y los guarda en /datos:
#   (1) precios diarios de cierre (ajustados por splits y dividendos) de las
#       50 acciones, Yahoo Finance via yfinance;
#   (2) indice S&P 500 (^GSPC) y, para robustez, S&P 500 Total Return;
#   (3) Fed H.15 "Treasury Constant Maturities" (archivo oficial de la Fed).
#  Ejecutar una sola vez:  python 01_descargar_datos.py
# =============================================================================
import io
import json
import urllib.request

import pandas as pd
import yfinance as yf

from config import (ACCIONES, DATOS, FECHA_FIN, FECHA_INICIO_PRECIOS, INDICE,
                    INDICE_TR, TICKERS, URL_H15, URL_H15_FF)


def descargar_yahoo(tickers, inicio, fin):
    """Precios de cierre ajustados (auto_adjust=True ajusta splits y dividendos).

    Se usa el cierre AJUSTADO porque en la ventana hay varios splits (NVDA 10:1
    en 2024, AVGO 10:1 en 2024, AMZN 20:1 y GOOGL 20:1 en 2022, TSLA 3:1 en
    2022, WMT 3:1 en 2024, NFLX 10:1 en 2025): con el cierre sin ajustar esos
    dias aparecerian como caidas falsas de -67% a -95%.
    """
    # yfinance trata 'end' como exclusivo: se suma un dia
    fin_excl = (pd.Timestamp(fin) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    data = yf.download(tickers, start=inicio, end=fin_excl, auto_adjust=True,
                       progress=False, threads=False)
    precios = data["Close"]
    if isinstance(precios, pd.Series):
        precios = precios.to_frame(tickers[0])
    precios = precios.reindex(columns=tickers)
    # Reintento individual para cualquier serie que haya fallado
    for t in precios.columns[precios.isna().all()]:
        for _ in range(3):
            d = yf.download(t, start=inicio, end=fin_excl, auto_adjust=True,
                            progress=False, threads=False)["Close"]
            if len(d.dropna()):
                precios[t] = d.squeeze()
                break
    return precios


def main():
    # ---------------- (1) acciones ----------------
    precios = descargar_yahoo(TICKERS, FECHA_INICIO_PRECIOS, FECHA_FIN)
    faltantes = precios.isna().sum()
    print("Observaciones:", len(precios), "| desde", precios.index[0].date(),
          "hasta", precios.index[-1].date())
    print("Datos faltantes por accion (deberian ser 0):\n",
          faltantes[faltantes > 0] if faltantes.any() else "ninguno")
    precios.to_csv(DATOS / "precios_acciones.csv", index_label="Fecha")

    pd.Series(ACCIONES, name="Sector").rename_axis("Ticker").to_csv(
        DATOS / "sectores.csv")

    # ---------------- (2) S&P 500 ----------------
    sp = descargar_yahoo([INDICE, INDICE_TR], FECHA_INICIO_PRECIOS, FECHA_FIN)
    sp.columns = ["SP500", "SP500_TR"]
    sp.to_csv(DATOS / "precios_sp500.csv", index_label="Fecha")

    # ---------------- (3) Fed H.15 ----------------
    req = urllib.request.Request(URL_H15, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    (DATOS / "FRB_H15_TCM_original.csv").write_text(raw, encoding="utf-8")
    # Las primeras 5 filas son metadatos; la 6a tiene los codigos de serie
    h15 = pd.read_csv(io.StringIO(raw), skiprows=5, index_col=0,
                      parse_dates=True, na_values=["ND", "NC", ""])
    h15.index.name = "Fecha"
    h15.to_csv(DATOS / "tasas_h15.csv")
    print("H.15: ", h15.index[0].date(), "->", h15.index[-1].date(),
          "| series:", list(h15.columns))

    # ---------------- (4) Contexto macro (solo para la discusion de P2) -------
    # (a) Tasa de fondos federales efectiva y tasa de descuento: H.15 semanal
    req = urllib.request.Request(URL_H15_FF, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=90).read().decode("utf-8")
    ff = pd.read_csv(io.StringIO(raw), skiprows=5, index_col=0, parse_dates=True,
                     na_values=["ND", "NC", ""])
    ff.columns = ["FedFunds_efectiva", "Prime", "Tasa_descuento"]
    ff.loc["2015":].to_csv(DATOS / "fed_funds_h15_semanal.csv", index_label="Fecha")
    print("Fed funds hasta", ff.index[-1].date())
    # (b) IPC (CPI-U, todos los items, sin desestacionalizar) y desempleo: BLS
    #     (la API publica permite ~25 consultas diarias; si falla se conserva
    #     el archivo ya descargado)
    try:
        descargar_bls()
    except Exception as e:  # noqa: BLE001
        print("Aviso: no se pudo actualizar BLS (", e, ") -> se usa macro_bls.csv existente")


def descargar_bls():
    filas = []
    for serie, nombre in [("CUUR0000SA0", "IPC"), ("LNS14000000", "Desempleo")]:
        for a0 in range(2015, 2027, 3):
            # La API publica (v1) acepta el rango de anios solo via POST
            cuerpo = json.dumps({"seriesid": [serie], "startyear": str(a0),
                                 "endyear": str(min(a0 + 2, 2026))}).encode()
            req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/",
                                         data=cuerpo, headers={"Content-type": "application/json",
                                                               "User-Agent": "Mozilla/5.0"})
            d = json.loads(urllib.request.urlopen(req, timeout=90).read().decode("utf-8"))
            for o in d["Results"]["series"][0]["data"]:
                # '-' = dato no publicado (p.ej. oct-2025, cierre del gobierno federal)
                if o["period"].startswith("M") and o["period"] != "M13" and o["value"] != "-":
                    filas.append({"Fecha": pd.Timestamp(int(o["year"]), int(o["period"][1:]), 1),
                                  "serie": nombre, "valor": float(o["value"])})
    bls = pd.DataFrame(filas).pivot_table(index="Fecha", columns="serie", values="valor").sort_index()
    bls = bls.asfreq("MS")   # mantiene el mes faltante como NaN (alinea t vs t-12)
    bls["Inflacion_12m"] = bls["IPC"].pct_change(12, fill_method=None) * 100
    bls.to_csv(DATOS / "macro_bls.csv")
    print("BLS hasta", bls.index[-1].date())


if __name__ == "__main__":
    main()
