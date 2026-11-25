"""NÃO TEMAS — 2 Reis 6:15-17 — prévia (camiseta preta).

Diagramação da referência 1 (3 faixas): título enorme itálico pesado no
topo com arco terminando numa chama; monte em fogo no meio; cavalos de fogo
na base. O fogo do monte passa POR CIMA da base das letras (camadas
encaixadas). Linha pequena embaixo: "ALÉM DO QUE SE VÊ · 2 REIS 6:16".
A ilustração é raster (gerada no Figma) nesta fase; o texto já é vetor.

uso: python3 make_2reis.py <opcao> <saida.svg>
  1 = Archivo Black Italic   2 = Barlow Black Italic
  3 = Saira Black Italic     4 = Russo One (inclinada 12°)
"""
import base64
import io
import sys

import numpy as np
from PIL import Image

from corujinha_art import Font, Text, cm, document

ILUS = "../2-reis-6/ilustracao/cavalos_fogo_v1_figma.png"
W, H = round(cm(28)), round(cm(36))
WHITE, CREAM = "#FFFFFF", "#E9E2CF"
FONTS = {1: ("Archivo-900i", 0), 2: ("Barlow-900i", 0), 3: ("Saira-900i", 0),
         4: ("RussoOne-Regular", 12)}
TITLE = "NÃO TEMAS"
TITLE_W = cm(25.5)


def png_uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def flame(cx, cy, h, color):
    """Chama estilizada de 3 línguas (vetor próprio), base em (cx, cy)."""
    s = h / 100
    p = lambda x, y: f"{cx + x * s:.1f} {cy - y * s:.1f}"
    d = (f"M{p(0, 0)} "
         f"C{p(-26, 0)} {p(-36, 22)} {p(-30, 44)} "          # bojo esquerdo
         f"C{p(-27, 54)} {p(-30, 62)} {p(-36, 72)} "         # língua esquerda
         f"C{p(-20, 66)} {p(-14, 56)} {p(-12, 50)} "
         f"C{p(-10, 70)} {p(-2, 84)} {p(2, 100)} "           # língua central (alta)
         f"C{p(8, 84)} {p(16, 74)} {p(14, 58)} "
         f"C{p(20, 64)} {p(26, 68)} {p(30, 76)} "            # língua direita
         f"C{p(36, 54)} {p(32, 0)} {p(0, 0)} Z "
         f"M{p(2, 12)} C{p(-12, 12)} {p(-14, 28)} {p(-6, 40)} "  # miolo vazado
         f"C{p(-4, 34)} {p(2, 30)} {p(4, 24)} C{p(8, 30)} {p(12, 26)} {p(12, 20)} "
         f"C{p(12, 14)} {p(8, 12)} {p(2, 12)} Z")
    return f'<path fill="{color}" fill-rule="evenodd" d="{d}"/>'


def build(opt, out):
    fname, skew = FONTS[opt]
    f = Font(fname)
    b = f.ink(TITLE, 1000)
    size = 1000 * TITLE_W / (b[2] - b[0])
    title = Text(f, TITLE, size, WHITE, tracking=-15, skew=skew)
    size *= TITLE_W / title.w
    title = Text(f, TITLE, size, WHITE, tracking=-15, skew=skew)
    t_top = cm(4.3)
    title.place(cx=W / 2, top=t_top)
    tb = title.box()

    # ilustração: 25,5 cm de largura; os picos do fogo sobem até o meio do título
    ilu = Image.open(ILUS).convert("RGB")
    iw = round(cm(24.5))
    ih = round(ilu.height * iw / ilu.width)
    ix = (W - iw) // 2
    # crista do monte (~17% da imagem) encosta na base do título: os picos e
    # o fogo sobem por trás/por cima das letras, como na referência
    iy = round(tb[3] - ih * 0.20)
    ilu_r = ilu.resize((iw, ih), Image.LANCZOS)
    a = np.asarray(ilu_r).astype(int)
    # fundo preto -> transparente (é o tecido)
    lum = a.max(axis=2)
    alpha = np.clip((lum - 18) * 6, 0, 255).astype(np.uint8)
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    # fogo (laranja/amarelo saturado) volta POR CIMA do título
    r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    fire = (r > 170) & (r - bl > 90) & (g > 60)
    fire_a = np.where(fire, alpha, 0).astype(np.uint8)
    fire_rgba = Image.fromarray(np.dstack([a.astype(np.uint8), fire_a]), "RGBA")

    body = [f'<rect width="{W}" height="{H}" fill="#0B0B0B"/>']  # só na prévia
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(rgba)}"/>')
    body.append(title.svg())
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(fire_rgba)}"/>')

    # arco fino por cima do título terminando numa chama (como o arco+estrela da ref.)
    ax0, ay0 = tb[0] + (tb[2] - tb[0]) * 0.08, tb[1] - cm(0.35)
    ax1, ay1 = tb[2] - cm(2.2), tb[1] - cm(1.5)
    body.append(
        f'<path fill="{WHITE}" d="M{ax0:.1f} {ay0:.1f} '
        f'Q{(ax0 + ax1) / 2:.1f} {ay1 - cm(0.9):.1f} {ax1:.1f} {ay1:.1f} '
        f'L{ax1 + cm(0.1):.1f} {ay1 + cm(0.32):.1f} '
        f'Q{(ax0 + ax1) / 2:.1f} {ay1 - cm(0.45):.1f} {ax0:.1f} {ay0:.1f} Z"/>')
    body.append(flame(ax1 + cm(0.95), ay1 + cm(0.7), cm(2.6), WHITE))

    # linha pequena embaixo
    mont = Font("Montserrat-600")
    line = Text(mont, "ALÉM DO QUE SE VÊ  ·  2 REIS 6:16", cm(0.62), CREAM, tracking=260)
    line.place(cx=W / 2, top=iy + ih + cm(0.2))
    body.append(line.svg())
    open(out, "w").write(document("\n".join(body), W, H))
    lb = line.box()
    print(f"opção {opt}: título {(tb[2]-tb[0])/300*2.54:.1f} cm; arte até {lb[3]/300*2.54:.1f} cm")


if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2])
