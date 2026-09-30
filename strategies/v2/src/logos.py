"""Genera los logos v2 de Strategies como SVG vectoriales.
Las letras salen de Archivo Expanded SemiBold (OFL). Las dos S son dibujo propio:
dos elipses apiladas con trazo uniforme y un nodo en el arranque de la primera."""
import math, json, pathlib, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = pathlib.Path(__file__).parent
FONT = str(HERE / "Archivo-Expanded-SemiBold.ttf")
T = 138            # grosor del trazo de la S (≈ 0,9 del asta de la I)
TRACK = 60         # tracking entre letras (unidades de 1000)
GAP = 70           # aire extra entre la S inicial y la T para el nodo
A0, NODE_A = -55, 0  # terminal de arranque y posición del nodo (grados)
SX0, SX1, STOP, SBOT = 59, 796, -699, 12  # caja de la S (misma que la S de Archivo)

def s_geom(x, a0=A0):
    x0, x1 = x + SX0, x + SX1
    cx = (x0 + x1) / 2; rx = (x1 - x0 - T) / 2
    yt, yb = STOP + T / 2, SBOT - T / 2; ry = (yb - yt) / 4
    c1, c2, ym = yt + ry, yb - ry, (yt + yb) / 2
    P = lambda c, a: (cx + rx * math.cos(math.radians(a)), c + ry * math.sin(math.radians(a)))
    s, e = P(c1, a0), P(c2, 180 + a0 if a0 != A0 else 125)
    d = (f"M{s[0]:.1f} {s[1]:.1f} A{rx:.1f} {ry:.1f} 0 0 0 {cx-rx:.1f} {c1:.1f} "
         f"A{rx:.1f} {ry:.1f} 0 0 0 {cx:.1f} {ym:.1f} A{rx:.1f} {ry:.1f} 0 0 1 {cx+rx:.1f} {c2:.1f} "
         f"A{rx:.1f} {ry:.1f} 0 0 1 {e[0]:.1f} {e[1]:.1f}")
    return d, P(c1, NODE_A)

def shape(text):
    font = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, {"kern": True})
    x, out = 0, []
    for inf, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((text[inf.cluster], x + pos.x_offset)); x += pos.x_advance + TRACK
    return out, x - TRACK

def glyph(f, ch, dx):
    gs = f.getGlyphSet(); pen = SVGPathPen(gs)
    gs[f.getBestCmap()[ord(ch)]].draw(TransformPen(pen, (1, 0, 0, -1, dx, 0)))
    return pen.getCommands()

def wordmark(text="STRATEGIES", custom=True, node=True):
    """Devuelve (viewBox, cuerpo) con currentColor para la tinta y var(--node) para el nodo."""
    f = TTFont(FONT); gl, width = shape(text)
    parts, dots = [], []
    for i, (ch, x) in enumerate(gl):
        if custom and i > 0: x += GAP
        if custom and ch == "S":
            d, n = s_geom(x)
            parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{T}"/>')
            if i == 0 and node:
                dots.append(f'<circle cx="{n[0]:.1f}" cy="{n[1]:.1f}" r="{T/2}" style="fill:var(--node,#EE8A22)"/>')
        else:
            parts.append(f'<path d="{glyph(f, ch, x)}" fill="currentColor"/>')
    w = width + (GAP if custom else 0)
    top = -905 if "É" in text else -699
    return f"0 {top} {w:.0f} {12-top}", "".join(parts + dots)

def isotype():
    d, n = s_geom(0)
    return (f"{SX0} {STOP} {SX1-SX0} {SBOT-STOP}",
            f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{T}"/>'
            f'<circle cx="{n[0]:.1f}" cy="{n[1]:.1f}" r="{T/2}" style="fill:var(--node,#EE8A22)"/>')

def segmented():
    d, _ = s_geom(0)
    return (f"{SX0} {STOP} {SX1-SX0} {SBOT-STOP}",
            f'<path d="{d}" pathLength="600" stroke-dasharray="90 12" fill="none" stroke="currentColor" stroke-width="{T}"/>')

def seal():
    return ("8 8 84 84", '<path fill="currentColor" d="M40 10 H82 A8 8 0 0 1 90 18 V31 H51 A6 6 0 0 0 51 43 H90 V60 '
            'A30 30 0 0 1 60 90 H18 A8 8 0 0 1 10 82 V69 H49 A6 6 0 0 0 49 57 H10 V40 A30 30 0 0 1 40 10Z"/>')

ASSETS = {
    "wm": wordmark(), "wm-acento": wordmark("STRATÉGIES"), "wm-plano": wordmark(custom=False),
    "iso": isotype(), "iso-seg": segmented(), "iso-sello": seal(),
}

def svg_file(vb, body, ink="#111315", bg=None):
    x, y, w, h = map(float, vb.split())
    if bg:  # el negativo lleva su área de protección: la mitad de la altura de la S
        m = h * .5; x, y, w, h = x - m, y - m, w + 2 * m, h + 2 * m
        vb = f"{x:.0f} {y:.0f} {w:.0f} {h:.0f}"
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" style="color:{ink}">{rect}{body}</svg>\n'

if __name__ == "__main__":
    out = HERE.parent / "logo"
    for name, (vb, body) in ASSETS.items():
        (out / f"{name}.svg").write_text(svg_file(vb, body))
        (out / f"{name}-negativo.svg").write_text(svg_file(vb, body, "#F3F3F0", "#111315"))
    (HERE / "assets.json").write_text(json.dumps(ASSETS))
    print({k: v[0] for k, v in ASSETS.items()})
