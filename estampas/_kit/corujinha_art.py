"""Base do pipeline de estampas — A Marca da Corujinha.

Converte texto em contornos vetoriais (fontTools + uharfbuzz), mede a
tinta real das letras, posiciona o logo da coruja e renderiza PNG
(cairosvg). Tudo em pixels do quadro final (300 dpi por padrão).
"""
from __future__ import annotations

import os
import re

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

KIT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(KIT, "fonts")

OFFWHITE = "#EFE8D8"
RED = "#C83438"
DPI = 300


def cm(v: float, dpi: int = DPI) -> float:
    """Centímetros -> pixels."""
    return v / 2.54 * dpi


class Font:
    def __init__(self, name: str):
        path = os.path.join(FONTS, name + ".ttf")
        self.tt = TTFont(path)
        self.upm = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))

    def _shape(self, text: str):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def layout(self, text: str, size: float, tracking: float = 0.0,
               x: float = 0.0, y: float = 0.0, skew_deg: float = 0.0):
        """Retorna (path_d, ink_bbox) com a linha de base em (x, y).

        tracking em milésimos do corpo (como no Illustrator).
        """
        import math
        s = size / self.upm
        track = tracking / 1000 * size
        pen = SVGPathPen(self.glyphs)
        bpen = BoundsPen(self.glyphs)
        infos, poss = self._shape(text)
        cx = 0.0
        sk = math.tan(math.radians(skew_deg))
        for i, p in zip(infos, poss):
            gname = self.order[i.codepoint]
            gx = x + (cx + p.x_offset) * s
            gy = y - p.y_offset * s
            # fonte: y para cima -> SVG: y para baixo
            m = (s, 0, sk * s, -s, gx, gy)  # skew = falso itálico
            self.glyphs[gname].draw(TransformPen(pen, m))
            self.glyphs[gname].draw(TransformPen(bpen, m))
            cx += p.x_advance + track / s
        return pen.getCommands(), bpen.bounds  # bounds = (x0, y0, x1, y1)

    def ink(self, text, size, tracking=0.0):
        return self.layout(text, size, tracking)[1]

    def fit_width(self, text, width, tracking=0.0):
        """Corpo que faz a TINTA da linha ter exatamente `width`."""
        b = self.ink(text, 1000, tracking)
        return 1000 * width / (b[2] - b[0])

    def fit_tracking(self, text, size, width, lo=-200, hi=2000):
        """Tracking que faz a tinta da linha ter exatamente `width`."""
        for _ in range(40):
            mid = (lo + hi) / 2
            b = self.ink(text, size, mid)
            if b[2] - b[0] < width:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


class Text:
    """Trecho de texto posicionado; place() alinha pela tinta."""

    def __init__(self, font: Font, text: str, size: float, color: str,
                 tracking: float = 0.0, rotate: float = 0.0, skew: float = 0.0):
        self.font, self.text, self.size = font, text, size
        self.color, self.tracking, self.rotate, self.skew = color, tracking, rotate, skew
        d, b = font.layout(text, size, tracking, skew_deg=skew)
        self.ink = b
        self.dx = self.dy = 0.0

    @property
    def w(self):
        return self.ink[2] - self.ink[0]

    @property
    def h(self):
        return self.ink[3] - self.ink[1]

    def place(self, left=None, top=None, cx=None, cy=None, baseline=None):
        if left is not None:
            self.dx = left - self.ink[0]
        if cx is not None:
            self.dx = cx - (self.ink[0] + self.ink[2]) / 2
        if top is not None:
            self.dy = top - self.ink[1]
        if cy is not None:
            self.dy = cy - (self.ink[1] + self.ink[3]) / 2
        if baseline is not None:
            self.dy = baseline
        return self

    def box(self):
        x0, y0, x1, y1 = self.ink
        return (x0 + self.dx, y0 + self.dy, x1 + self.dx, y1 + self.dy)

    def svg(self, stroke: float = 0.0):
        d, _ = self.font.layout(self.text, self.size, self.tracking,
                                self.dx, self.dy, self.skew)
        extra = ""
        if stroke:
            extra = (f' stroke="{self.color}" stroke-width="{stroke:.2f}"'
                     ' stroke-linejoin="round"')
        tr = ""
        if self.rotate:
            b = self.box()
            tr = (f' transform="rotate({self.rotate} {(b[0]+b[2])/2:.2f} '
                  f'{(b[1]+b[3])/2:.2f})"')
        return f'<path fill="{self.color}"{extra}{tr} d="{d}"/>'


_LOGO = None


def logo_svg(cx: float, cy: float, width: float, color: str = OFFWHITE):
    """Logo da coruja centralizado em (cx, cy) com a largura dada."""
    global _LOGO
    if _LOGO is None:
        src = open(os.path.join(KIT, "logo_coruja.svg")).read()
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
        d = re.search(r' d="([^"]+)"', src).group(1)
        _LOGO = (vb, d)
    (vx, vy, vw, vh), d = _LOGO
    s = width / vw
    x = cx - width / 2 - vx * s
    y = cy - vh * s / 2 - vy * s
    return (f'<path fill="{color}" fill-rule="evenodd" '
            f'transform="translate({x:.2f} {y:.2f}) scale({s:.5f})" d="{d}"/>'), vh * s


def document(body: str, w_px: int, h_px: int, dpi: int = DPI):
    wmm = w_px / dpi * 25.4
    hmm = h_px / dpi * 25.4
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{wmm:.1f}mm" '
            f'height="{hmm:.1f}mm" viewBox="0 0 {w_px} {h_px}">\n{body}\n</svg>\n')


def render(svg: str, png: str, width: int | None = None, bg: str | None = None,
           dpi: int = DPI):
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png, output_width=width,
                     background_color=bg, dpi=dpi)


def preview_crop(png_in: str, png_out: str, pad: int = 40, bg=(17, 17, 17)):
    """Recorta a prévia na área da arte (para enviar ao cliente)."""
    from PIL import Image
    im = Image.open(png_in).convert("RGB")
    mask = im.convert("L").point(lambda v: 255 if v > max(bg) + 25 else 0)
    x0, y0, x1, y1 = mask.getbbox()
    im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad),
             min(im.height, y1 + pad))).save(png_out)
