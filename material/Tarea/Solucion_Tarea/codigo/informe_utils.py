# =============================================================================
#  informe_utils.py
#  Partes comunes de los generadores de informe (05 y 06): carga de los
#  resultados guardados por 02-04, formatos numericos en espaniol y funciones
#  para escribir el documento Word (parrafos, tablas, figuras, pie de pagina).
#  Cada script que lo importa crea su propio documento (variable `doc`).
# =============================================================================
import json
import re
import sys

import numpy as np
import pandas as pd
from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from config import BASE, FIGURAS, RESULTADOS, TABLAS

sys.stdout.reconfigure(encoding="utf-8")

AZUL = RGBColor(0x13, 0x28, 0x4B)
DORADO = "C9A227"

# -----------------------------------------------------------------------------
# Resultados
# -----------------------------------------------------------------------------
A = json.load(open(RESULTADOS / "p1a_resultados.json", encoding="utf-8"))
B = json.load(open(RESULTADOS / "p1b_resultados.json", encoding="utf-8"))
C = json.load(open(RESULTADOS / "p2_resultados.json", encoding="utf-8"))
est = pd.read_csv(TABLAS / "1A1_estadisticas_acciones.csv", index_col=0)
res_front = pd.read_csv(TABLAS / "1A_resumen_fronteras.csv")
ing = pd.read_csv(TABLAS / "1A3_comparacion_ingenua.csv")
gmvw = pd.read_csv(TABLAS / "1A_pesos_gmv.csv", index_col=0)
pesosM = pd.read_csv(TABLAS / "1B1_pesos_tangencia.csv", index_col=0)
desemp = pd.read_csv(TABLAS / "1B3_sharpe_treynor.csv", index_col=0)
acc_st = pd.read_csv(TABLAS / "1B3_sharpe_treynor_acciones.csv", index_col=0)
asig = pd.read_csv(TABLAS / "1B4_asignacion_optima.csv")
curvas = pd.read_csv(TABLAS / "2_curvas_observadas_junio.csv", index_col=0)
par = pd.read_csv(TABLAS / "2_parametros_NS_SV.csv", index_col=0)
sinr = pd.read_csv(TABLAS / "2_NS_sin_restricciones_robustez.csv", index_col=0)
junv = pd.read_csv(TABLAS / "2_inversion_fechas_junio.csv", index_col=0)


# -----------------------------------------------------------------------------
# Formatos numericos en espaniol (coma decimal)
# -----------------------------------------------------------------------------
def pc(x, d=1):
    return f"{100 * x:.{d}f}%".replace(".", ",")


def nu(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pb(x, d=0):
    return f"{x:.{d}f}".replace(".", ",")


def miles(n):
    return f"{int(n):,}".replace(",", ".")


# Cifras derivadas usadas en el texto
Fa, Fb, Fd = A["A"], A["B"], A["D"]
s_sp = B["sp500"]["sigma"]
mu_frontera_en_sp = (Fb + np.sqrt(Fd * (Fa * s_sp ** 2 - 1))) / Fa
corr = A["corr"]
mi = B["modelo_indice"]
sim = B["simulacion_H0"]
fm = B["fuera_muestra"]
M = B["M"]
rf = B["rf"]
tang = B["tangencias_restringidas"]
fr = A["fronteras"]
gl = A["gmv_libre"]
gi = A["gmv_ingenua"]
inv = C["inversiones"]
anios = [str(pd.Timestamp(f).year) for f in par.index]
par.index = anios
corr_b1 = np.corrcoef(par["NS b1"], (curvas["3M"] - curvas["10A"]).values)[0, 1]
corr_b0 = np.corrcoef(par["NS b0"], curvas["30A"].values)[0, 1]
ff_r0 = None
mejora = C["mejora_media_por_plazo_pb"]
n_inv_rank = len(B["acciones_ranking_distinto"])
t_teorico = mi["ratio_informacion"] * np.sqrt(mi["T"] / 252)


def sig_en(nombre_col, fila):
    return res_front.loc[fila, nombre_col]


# -----------------------------------------------------------------------------
# Utilidades de documento
# -----------------------------------------------------------------------------
doc = Document()
sec0 = doc.sections[0]
sec0.page_height, sec0.page_width = Cm(27.94), Cm(21.59)   # tamanio carta
for m_ in ("left_margin", "right_margin"):
    setattr(sec0, m_, Cm(2.2))
sec0.top_margin, sec0.bottom_margin = Cm(2.0), Cm(2.0)

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.line_spacing = 1.12
for nivel, tam in [(1, 15), (2, 12.5), (3, 11)]:
    h = doc.styles[f"Heading {nivel}"]
    h.font.name = "Calibri"
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    h.font.size = Pt(tam)
    h.font.bold = True
    h.font.color.rgb = AZUL
    h.paragraph_format.space_before = Pt(12 if nivel == 1 else 9)
    h.paragraph_format.space_after = Pt(5)
    h.paragraph_format.keep_with_next = True

CONT = {"fig": 0, "tab": 0}


def runs(p, texto, size=None, color=None):
    """Texto con marcas simples: **negrita** y *cursiva*."""
    texto = re.sub(r"(?<![A-Za-z])([xw])\*", r"\1∗", texto)   # x*, w* -> asterisco matematico (no toca "xlsx*")
    partes = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", texto)
    for t in partes:
        if not t:
            continue
        if t.startswith("**"):
            r = p.add_run(t[2:-2]); r.bold = True
        elif t.startswith("*"):
            r = p.add_run(t[1:-1]); r.italic = True
        else:
            r = p.add_run(t)
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
    return p


def P(texto, just=True, size=None, sangria=False, despues=None):
    p = doc.add_paragraph()
    if just:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if sangria:
        p.paragraph_format.left_indent = Cm(0.6)
    if despues is not None:
        p.paragraph_format.space_after = Pt(despues)
    t_ = texto.strip()
    if t_.endswith(":") or (t_.startswith("**") and t_.endswith("**") and len(t_) < 140):
        p.paragraph_format.keep_with_next = True      # no dejar la introduccion sola al pie
    return runs(p, texto, size)


def BUL(items, size=None, estilo="List Bullet"):
    for it in items:
        p = doc.add_paragraph(style=estilo)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(2.5)
        runs(p, it, size)


def H(texto, nivel=1):
    return doc.add_heading(texto, level=nivel)


def EQ(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(texto)
    r.italic = True
    r.font.name = "Cambria Math"
    r.font.size = Pt(11)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    return p


def FIG(nombre, ancho_cm, leyenda):
    CONT["fig"] += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIGURAS / nombre), width=Cm(ancho_cm))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs(c, f"**Figura {CONT['fig']}.** {leyenda}", size=8.8, color=RGBColor(0x40, 0x40, 0x40))
    return CONT["fig"]


def _sombrear(celda, color_hex):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def TAB(df, titulo, fmt=None, size=8.3, indice=True, anchos=None, nota=None, resaltar=None):
    """Inserta una tabla con encabezado azul.  fmt: dict columna -> funcion."""
    CONT["tab"] += 1
    t = doc.add_paragraph()
    t.paragraph_format.keep_with_next = True
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs(t, f"**Tabla {CONT['tab']}.** {titulo}", size=9, color=AZUL)
    fmt = fmt or {}
    cols = ([df.index.name or ""] if indice else []) + list(df.columns)
    tb = doc.add_table(rows=1, cols=len(cols))
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, c in enumerate(cols):
        cell = tb.rows[0].cells[j]
        cell.text = ""
        r = cell.paragraphs[0].add_run(str(c))
        r.bold = True; r.font.size = Pt(size); r.font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        _sombrear(cell, "13284B")
    trPr = tb.rows[0]._tr.get_or_add_trPr()          # repetir encabezado si la tabla se corta
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
    for k, (idx, fila) in enumerate(df.iterrows()):
        celdas = tb.add_row().cells
        vals = ([idx] if indice else []) + [fila[c] for c in df.columns]
        for j, (c, v) in enumerate(zip(cols, vals)):
            if j >= (1 if indice else 0) and c in fmt:
                txt = fmt[c](v) if not (isinstance(v, float) and np.isnan(v)) else "–"
            elif isinstance(v, (float, np.floating)):
                txt = "–" if np.isnan(v) else nu(v, 3)
            else:
                txt = str(v)
            celdas[j].text = ""
            pp = celdas[j].paragraphs[0]
            rr = pp.add_run(txt)
            rr.font.size = Pt(size)
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 or not indice else WD_ALIGN_PARAGRAPH.LEFT
            if k % 2 == 1:
                _sombrear(celdas[j], "EEF2F8")
            if resaltar is not None and resaltar(idx, fila):
                _sombrear(celdas[j], "FCF3CF")
    if anchos:
        for fila in tb.rows:
            for j, w in enumerate(anchos):
                fila.cells[j].width = Cm(w)
    if nota:
        n = doc.add_paragraph()
        runs(n, nota, size=8, color=RGBColor(0x55, 0x55, 0x55))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return CONT["tab"]


def SALTO():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def pie_de_pagina():
    pie = sec0.footer.paragraphs[0]
    pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pie.add_run("Finanzas I (ENFIN415) · Tarea 2026 · página ")
    r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    for tipo, texto in (("begin", None), (None, "PAGE"), ("end", None)):
        run = pie.add_run()
        run.font.size = Pt(8)
        if tipo:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tipo); run._r.append(el)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = texto
            run._r.append(el)


pie_de_pagina()


def FIG2(nombres, ancho_cm, leyenda):
    """Dos figuras lado a lado con una sola leyenda (paneles a y b)."""
    CONT["fig"] += 1
    tb = doc.add_table(rows=1, cols=2)
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for celda, nombre in zip(tb.rows[0].cells, nombres):
        pp = celda.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.add_run().add_picture(str(FIGURAS / nombre), width=Cm(ancho_cm))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs(c, f"**Figura {CONT['fig']}.** {leyenda}", size=8.8, color=RGBColor(0x40, 0x40, 0x40))
    return CONT["fig"]

