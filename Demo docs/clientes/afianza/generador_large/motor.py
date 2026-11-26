"""Motor de maquetación de los documentos de demo «_large» (reportlab)."""
import io, random, re
from pathlib import Path
from PIL import Image as PI, ImageDraw, ImageFilter, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

BASE = Path(__file__).resolve().parent.parent
W, H = A4
PIE = "Documento ficticio para demostración. Sin valor legal."

# ---------- fuentes (las de macOS si existen; si no, las estándar de PDF) ----------
SUP = Path("/System/Library/Fonts/Supplemental")
FAM = {"Times": ("Times New Roman", "Times-Roman", "Times-Bold", "Times-Italic"),
       "Arial": ("Arial", "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"),
       "Georgia": ("Georgia", "Times-Roman", "Times-Bold", "Times-Italic")}
F = {}
for k, (f, r, b, i) in FAM.items():
    try:
        for s, n in (("", "R"), (" Bold", "B"), (" Italic", "I")):
            pdfmetrics.registerFont(TTFont(f"{k}{n}", str(SUP / f"{f}{s}.ttf")))
        F[k] = (f"{k}R", f"{k}B", f"{k}I")
    except Exception:
        F[k] = (r, b, i)
try:
    pdfmetrics.registerFont(TTFont("Mano", str(SUP / "Bradley Hand Bold.ttf"))); MANO = "Mano"
except Exception:
    MANO = F["Times"][2]


# ---------- utilidades ----------
def eur(x, d=2):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


MES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def iban(seed):
    """IBAN con dígitos de control no válidos a propósito y entidad inexistente."""
    r = random.Random(seed)
    return "ES00 9999 " + " ".join(f"{r.randint(0, 9999):04d}" for _ in range(4))


def cif(letra, seed):
    """NIF de empresa con dígito de control incorrecto a propósito."""
    r = random.Random(seed); n = [r.randint(0, 9) for _ in range(7)]
    s = sum(n[1::2]) + sum(sum(divmod(2 * d, 10)) for d in n[0::2])
    return f"{letra}{''.join(map(str, n))}{((10 - s % 10) % 10 + 3) % 10}"


def dni(seed):
    """DNI con letra incorrecta a propósito."""
    n = random.Random(seed).randint(10000000, 79999999)
    return f"{n}{'TRWAGMYFPDXBNJZSQVHLCKE'[(n + 7) % 23]}"


class Firma(Flowable):
    def __init__(self, seed, w=110, h=38):
        super().__init__(); self.seed, self.width, self.height = seed, w, h

    def draw(self):
        trazo(self.canv, self.seed, 0, 0, self.width, self.height)


def trazo(c, seed, x, y, w, h):
    r = random.Random(str(seed)); c.saveState()
    c.setStrokeColor(colors.HexColor(r.choice(["#1b2f7a", "#111a3a", "#23408f"]))); c.setLineWidth(r.uniform(.8, 1.3)); c.setLineCap(1)
    p = c.beginPath(); n = r.randint(5, 8); px, py = x + w * .05, y + h * .45; p.moveTo(px, py)
    for k in range(n):
        nx = x + w * (.08 + .8 * (k + 1) / n); ny = y + h * r.uniform(.2, .8)
        p.curveTo(px + w * .1, y + h * r.uniform(-.1, 1.2), nx - w * .16, y + h * r.uniform(-.1, 1.2), nx, ny); px, py = nx, ny
    p.curveTo(x + w, y + h * .1, x + w * .4, y - h * .05, x + w * .12, y + h * .12); c.drawPath(p); c.restoreState()


class Sello(Flowable):
    def __init__(self, l1, l2, col="#2b4c9b"):
        super().__init__(); self.l1, self.l2, self.col, self.width, self.height = l1, l2, col, 150, 50

    def draw(self):
        c = self.canv; c.saveState(); c.translate(10, 8); c.rotate(-4); col = colors.HexColor(self.col)
        c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(1.4); c.roundRect(0, 0, 132, 36, 4)
        c.setLineWidth(.5); c.roundRect(3, 3, 126, 30, 3); c.setFont(F["Arial"][1], 7.5); c.drawCentredString(66, 20, self.l1)
        c.setFont(F["Arial"][0], 6.5); c.drawCentredString(66, 10, self.l2); c.restoreState()


class Cab(Flowable):
    """Cabecera de color para facturas, pólizas y fichas."""
    def __init__(self, st, titulo, sub, w):
        super().__init__(); self.st, self.t, self.s, self.width, self.height = st, titulo, sub, w, 46

    def draw(self):
        c = self.canv; col = colors.HexColor(self.st["color"])
        c.setFillColor(col); c.rect(0, 0, self.width, 40, stroke=0, fill=1); c.setFillColor(colors.white)
        c.setFont(self.st["f"][1], 15); c.drawString(12, 17, self.t); c.setFont(self.st["f"][0], 8); c.drawString(12, 6, self.s)


def logo(c, st, x, y, s=20):
    col = colors.HexColor(st["color"]); c.saveState(); c.setFillColor(col); c.setStrokeColor(col); k = st.get("logo", "hex")
    if k == "hex":
        import math
        p = c.beginPath()
        for i in range(6):
            a = math.pi / 6 + i * math.pi / 3; q = (x + s / 2 + s / 2 * math.cos(a), y + s / 2 + s / 2 * math.sin(a))
            (p.moveTo if i == 0 else p.lineTo)(*q)
        p.close(); c.drawPath(p, fill=1, stroke=0)
    elif k == "bar":
        for i, h in enumerate((.5, .8, 1)): c.rect(x + i * s * .36, y, s * .26, s * h, fill=1, stroke=0)
    elif k == "circ":
        c.circle(x + s / 2, y + s / 2, s / 2, fill=1, stroke=0); c.setFillColor(colors.white); c.circle(x + s * .62, y + s * .6, s * .24, fill=1, stroke=0)
    elif k == "esc":
        c.setLineWidth(1.6); c.rect(x, y + s * .25, s * .8, s * .75, fill=0); c.line(x, y + s * .25, x + s * .4, y); c.line(x + s * .8, y + s * .25, x + s * .4, y)
    else:
        c.rect(x, y, s, s, fill=0); c.line(x, y, x + s, y + s); c.line(x, y + s / 2, x + s / 2, y + s)
    c.setFillColor(col); c.setFont(st["f"][1], 10.5); c.drawString(x + s + 7, y + s * .5, st["marca"]); c.setFont(st["f"][0], 6.8); c.setFillColor(colors.HexColor("#666666"))
    c.drawString(x + s + 7, y + s * .5 - 9, st.get("lema", "")); c.restoreState()


class NumCanvas(Canvas):
    st = {}
    def __init__(self, *a, **k): super().__init__(*a, **k); self._p = []
    def showPage(self): self._p.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._p)
        for i, d in enumerate(self._p, 1):
            self.__dict__.update(d); self.pie(i, n); Canvas.showPage(self)
        Canvas.save(self)

    def pie(self, i, n):
        st = self.st; self.setFont(st["f"][0], 7); self.setFillColor(colors.HexColor("#777777"))
        self.drawString(62, 30, st.get("ref", "")); self.drawRightString(W - 62, 30, f"Página {i} de {n}")
        self.setFont(st["f"][0], 5.8); self.drawCentredString(W / 2, 18, PIE)


def estilos(st):
    r, b, it = st["f"]; s = st.get("size", 10.2); c = colors.HexColor(st["color"]); L = st.get("lead", 1.42)
    return {"p": PS("p", fontName=r, fontSize=s, leading=s * L, alignment=TA_JUSTIFY, spaceAfter=s * .55),
            "t": PS("t", fontName=b, fontSize=s + 5.5, leading=s + 10, alignment=TA_CENTER, spaceBefore=12, spaceAfter=12, textColor=c),
            "h2": PS("h2", fontName=b, fontSize=s + 1, leading=s + 5, spaceBefore=s, spaceAfter=s * .5, textColor=c, keepWithNext=1),
            "h3": PS("h3", fontName=b, fontSize=s, leading=s + 4, spaceBefore=4, spaceAfter=3, keepWithNext=1),
            "c": PS("c", fontName=r, fontSize=s, leading=s * L, alignment=TA_CENTER, spaceAfter=6),
            "i": PS("i", fontName=it, fontSize=s - 1, leading=(s - 1) * 1.35, alignment=TA_JUSTIFY, spaceAfter=6, textColor=colors.HexColor("#444444")),
            "b": PS("b", fontName=r, fontSize=s, leading=s * L, leftIndent=16, bulletIndent=4, alignment=TA_JUSTIFY, spaceAfter=s * .35),
            "d": PS("d", fontName=r, fontSize=s - 1.3, leading=(s - 1.3) * 1.28),
            "dr": PS("dr", fontName=r, fontSize=s - 1.3, leading=(s - 1.3) * 1.28, alignment=TA_RIGHT),
            "dh": PS("dh", fontName=b, fontSize=s - 1.3, leading=(s - 1.3) * 1.28, textColor=colors.white),
            "dbr": PS("dbr", fontName=b, fontSize=s - 1.3, leading=(s - 1.3) * 1.28, alignment=TA_RIGHT),
            "db": PS("db", fontName=b, fontSize=s - 1.3, leading=(s - 1.3) * 1.28)}


NUM = re.compile(r"^[-+]?[\d.]+(,\d+)?( ?(€|%))?$")


def tabla(rows, E, st, w, cols=None, cab=True, grid=True):
    n = len(rows[0]); cols = cols or [1] * n; tot = sum(cols); out = []
    for i, r in enumerate(rows):
        ult = i == len(rows) - 1 and str(r[0]).lower().startswith("total")
        out.append([Paragraph(str(x), E["dh"] if cab and i == 0 else E["dbr"] if ult and NUM.match(str(x).strip()) else E["db"] if ult else E["dr"] if NUM.match(str(x).strip()) else E["d"]) for x in r])
    ts = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if grid: ts += [("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#b8bcc4"))]
    if cab: ts += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(st["color"])), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f6f8")])]
    return Table(out, colWidths=[w * c / tot for c in cols], style=TableStyle(ts), repeatRows=1 if cab else 0, spaceAfter=9, spaceBefore=3)


def escaneo(lineas, seed=1, w=900, h=1270, ticket=False):
    """Imagen con aspecto de escaneo: sin capa de texto."""
    r = random.Random(seed); im = PI.new("L", (w, h), 244); d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype(str(SUP / "Courier New Bold.ttf"), 25 if not ticket else 30); fb = ImageFont.truetype(str(SUP / "Courier New Bold.ttf"), 32)
    except Exception:
        f = fb = ImageFont.load_default()
    y = 80
    for k, l in enumerate(lineas):
        d.text((70 + r.randint(-1, 1), y), l, fill=r.randint(25, 70), font=fb if k == 0 else f); y += 46 if k == 0 else 38
    px = im.load()
    for _ in range(w * h // 70):
        x, yy = r.randrange(w), r.randrange(h); px[x, yy] = max(0, px[x, yy] - r.randint(10, 60))
    im = im.rotate(r.uniform(-1.1, 1.1), fillcolor=225, expand=False).filter(ImageFilter.GaussianBlur(.7))
    b = io.BytesIO(); im.save(b, "JPEG", quality=62); b.seek(0); return b


def flujo(txt, st, w, scans=None):
    """Convierte el mini-marcado en elementos de página."""
    E = estilos(st); out = []; tb = []; opt = {}
    def cierra():
        nonlocal tb, opt
        if tb:
            out.append(tabla(tb, E, st, w, opt.get("cols"), not opt.get("nocab"), not opt.get("nogrid"))); tb = []; opt = {}
    for ln in txt.strip().split("\n"):
        l = ln.strip()
        if l.startswith("|"): tb.append([x.strip() for x in l.strip("|").split("|")]); continue
        cierra()
        if not l: continue
        if l.startswith("!cols "): opt["cols"] = [float(x) for x in l[6:].split(",")]
        elif l == "!nocab": opt["nocab"] = 1
        elif l == "!nogrid": opt["nogrid"] = 1
        elif l == "!page": out.append(PageBreak())
        elif l.startswith("!space"): out.append(Spacer(1, float(l.split()[1])))
        elif l == "!dos": out += [NextPageTemplate("dos"), PageBreak()]
        elif l == "!uno": out += [NextPageTemplate("uno"), PageBreak()]
        elif l.startswith("!cab "):
            a, _, b = l[5:].partition(";;"); out += [Cab(st, a, b, w), Spacer(1, 8)]
        elif l.startswith("!sello "):
            a, _, b = l[7:].partition(";;"); out.append(Sello(a, b, st.get("sello", "#2b4c9b")))
        elif l.startswith("!scan "):
            out.append(Image(scans[l[6:]], width=w * .92, height=w * .92 * 1.41))
        elif l.startswith("!firma "):
            cs = [c.split(";") for c in l[7:].split("||")]; k = len(cs)
            cel = [[Paragraph(c[0].strip(), E["db"]), Spacer(1, 4), Firma(c[1].strip()), Paragraph("Fdo.: " + c[1].strip(), E["d"]), Paragraph(c[2].strip() if len(c) > 2 else "", E["d"])] for c in cs]
            out.append(KeepTogether([Spacer(1, 12), Table([cel], colWidths=[w / k] * k, style=[("VALIGN", (0, 0), (-1, -1), "TOP")])]))
        elif l.startswith("!caja "):
            out.append(Table([[Paragraph(l[6:], E["p"])]], colWidths=[w], style=[("BOX", (0, 0), (-1, -1), .8, colors.HexColor(st["color"])), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f7f9"))], spaceAfter=8))
        elif l.startswith("!c "): out.append(Paragraph(l[3:], E["c"]))
        elif l.startswith("!i "): out.append(Paragraph(l[3:], E["i"]))
        elif l.startswith("!mano "): out.append(Paragraph(l[6:], PS("m", fontName=MANO, fontSize=13, leading=18, textColor=colors.HexColor("#1b2f7a"))))
        elif l.startswith("### "): out.append(Paragraph(l[4:], E["h3"]))
        elif l.startswith("## "): out.append(Paragraph(l[3:], E["h2"]))
        elif l.startswith("# "): out.append(Paragraph(l[2:], E["t"]))
        elif l.startswith("- "): out.append(Paragraph(l[2:], E["b"], bulletText="•"))
        else: out.append(Paragraph(l, E["p"]))
    cierra(); return out


def portada(st, titulo, sub, lineas):
    E = estilos(st); r, b, _ = st["f"]; c = colors.HexColor(st["color"])
    big = PS("big", fontName=b, fontSize=23, leading=29, textColor=c, alignment=TA_CENTER, spaceAfter=14); mid = PS("mid", fontName=r, fontSize=13, leading=19, alignment=TA_CENTER, spaceAfter=10)
    return [Spacer(1, 135), Paragraph(titulo, big), Paragraph(sub, mid), Spacer(1, 45)] + [Paragraph(x, mid) for x in lineas] + [PageBreak()]


def indice(txt, st):
    """Índice de apartados (sin páginas, como en muchos contratos)."""
    E = estilos(st); hs = [l[3:].strip() for l in txt.split("\n") if l.startswith("## ")]
    return [Paragraph("ÍNDICE", E["t"])] + [Paragraph(h, PS("x", parent=E["p"], spaceAfter=3)) for h in hs] + [PageBreak()]


def pdf(carpeta, nombre, st, txt, titulo, port=None, idx=False, rub=(), scans=None):
    ruta = BASE / carpeta; ruta.mkdir(exist_ok=True); st = dict(st); mx, top = 62, 78 if st.get("marca") else 56
    w = W - 2 * mx; st["ref"] = st.get("ref", "")
    cls = type("NC", (NumCanvas,), {"st": st})
    def fondo(c, d):
        if st.get("marca"): logo(c, st, mx, H - 58); c.setStrokeColor(colors.HexColor("#cccccc")); c.setLineWidth(.4); c.line(mx, H - 66, W - mx, H - 66)
        if rub and d.page > (1 if port else 0):
            for k, s in enumerate(rub): trazo(c, f"rub{s}", W - 50, H / 2 - 60 + 70 * k, 38, 20)
    doc = BaseDocTemplate(str(ruta / f"{nombre}.pdf"), pagesize=A4, title=titulo, author=st.get("marca", ""), creator="", invariant=1)
    g = 16; cw = (w - g) / 2
    fr = lambda x, ww: Frame(x, 52, ww, H - top - 56, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("uno", [fr(mx, w)], onPage=fondo), PageTemplate("dos", [fr(mx, cw), fr(mx + cw + g, cw)], onPage=fondo)])
    fl = list(port and portada(st, *port) or []) + (indice(txt, st) if idx else [])
    ps = txt.split("!dos")
    fl += flujo(ps[0], st, w, scans)
    for x in ps[1:]:
        a, _, b = x.partition("!uno")
        fl += [NextPageTemplate("dos"), PageBreak()] + flujo(a, {**st, "size": st.get("size2", 7.8), "lead": 1.25}, cw, scans)
        if b.strip(): fl += [NextPageTemplate("uno"), PageBreak()] + flujo(b, st, w, scans)
    doc.build(fl, canvasmaker=cls)


def est(marca, lema="", font="Times", color="#1f2937", logo="hex", **k):
    return dict(marca=marca, lema=lema, f=F[font], color=color, logo=logo, **k)
