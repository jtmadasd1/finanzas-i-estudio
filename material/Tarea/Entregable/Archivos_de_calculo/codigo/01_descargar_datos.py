# =============================================================================
#  01_descargar_datos.py  -  Descarga de datos (se corre una sola vez)
#   1) Precios diarios de cierre de las 50 acciones y del S&P 500 (Yahoo Finance)
#   2) Fed H.15: Treasury Constant Maturities (diario) y fondos federales (semanal)
#   3) IPC de EE.UU. (BLS), solo para el grafico de contexto de la pregunta 2
#  Todo queda guardado en la carpeta /datos
# =============================================================================
import io
import json
import urllib.request

import pandas as pd
import yfinance as yf

from config import (ACCIONES, DATOS, FECHA_FIN, FECHA_INICIO_PRECIOS, INDICE,
                    TICKERS, URL_H15, URL_H15_FF)


def descargar_yahoo(tickers, inicio, fin):
    """Cierre ajustado por splits y dividendos (sin ajuste, los splits de NVDA,
    AMZN, GOOGL, NFLX, etc. aparecerian como caidas falsas de 67% a 95%)."""
    fin_excl = (pd.Timestamp(fin) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")   # 'end' es exclusivo
    data = yf.download(tickers, start=inicio, end=fin_excl, auto_adjust=True,
                       progress=False, threads=False)
    precios = data["Close"]
    if isinstance(precios, pd.Series):
        precios = precios.to_frame(tickers[0])
    precios = precios.reindex(columns=tickers)
    for t in precios.columns[precios.isna().all()]:      # reintento si alguna fallo
        for _ in range(3):
            d = yf.download(t, start=inicio, end=fin_excl, auto_adjust=True,
                            progress=False, threads=False)["Close"]
            if len(d.dropna()):
                precios[t] = d.squeeze()
                break
    return precios


def leer_h15(url):
    """Archivo CSV de la Fed: las primeras 5 filas son descripciones de las series."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=90).read().decode("utf-8")
    return raw, pd.read_csv(io.StringIO(raw), skiprows=5, index_col=0, parse_dates=True,
                            na_values=["ND", "NC", ""])


def descargar_ipc():
    """IPC (CPI-U) mensual del BLS e inflacion de 12 meses.  La API publica
    entrega como maximo 3 años por consulta, por eso se pide por tramos."""
    filas = []
    for a0 in range(2015, 2027, 3):
        cuerpo = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": str(a0),
                             "endyear": str(min(a0 + 2, 2026))}).encode()
        req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=cuerpo,
                                     headers={"Content-type": "application/json", "User-Agent": "Mozilla/5.0"})
        d = json.loads(urllib.request.urlopen(req, timeout=90).read().decode("utf-8"))
        for o in d["Results"]["series"][0]["data"]:
            # '-' = mes no publicado (oct-2025, cierre del gobierno federal)
            if o["period"].startswith("M") and o["period"] != "M13" and o["value"] != "-":
                filas.append({"Fecha": pd.Timestamp(int(o["year"]), int(o["period"][1:]), 1),
                              "IPC": float(o["value"])})
    ipc = pd.DataFrame(filas).drop_duplicates("Fecha").set_index("Fecha").sort_index().asfreq("MS")
    ipc["Inflacion_12m"] = ipc["IPC"].pct_change(12, fill_method=None) * 100
    ipc.to_csv(DATOS / "macro_bls.csv")
    print("IPC hasta", ipc.index[-1].date())


def main():
    # 1) Acciones y S&P 500
    precios = descargar_yahoo(TICKERS, FECHA_INICIO_PRECIOS, FECHA_FIN)
    print("Acciones:", len(precios), "dias,", precios.index[0].date(), "a", precios.index[-1].date(),
          "| datos faltantes:", int(precios.isna().sum().sum()))
    precios.to_csv(DATOS / "precios_acciones.csv", index_label="Fecha")
    pd.Series(ACCIONES, name="Sector").rename_axis("Ticker").to_csv(DATOS / "sectores.csv")
    sp = descargar_yahoo([INDICE], FECHA_INICIO_PRECIOS, FECHA_FIN)
    sp.columns = ["SP500"]
    sp.to_csv(DATOS / "precios_sp500.csv", index_label="Fecha")

    # 2) Fed H.15
    raw, h15 = leer_h15(URL_H15)
    (DATOS / "FRB_H15_TCM_original.csv").write_text(raw, encoding="utf-8")
    h15.index.name = "Fecha"
    h15.to_csv(DATOS / "tasas_h15.csv")
    print("H.15:", h15.index[0].date(), "a", h15.index[-1].date())
    _, ff = leer_h15(URL_H15_FF)
    ff.columns = ["FedFunds_efectiva", "Prime", "Tasa_descuento"]
    ff.loc["2015":].to_csv(DATOS / "fed_funds_h15_semanal.csv", index_label="Fecha")

    # 3) IPC (la API del BLS permite pocas consultas diarias; si falla se
    #    mantiene el archivo ya descargado)
    try:
        descargar_ipc()
    except Exception as e:  # noqa: BLE001
        print("Aviso: no se pudo actualizar el IPC (", e, "); se usa macro_bls.csv existente")


if __name__ == "__main__":
    main()
