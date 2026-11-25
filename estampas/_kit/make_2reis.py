"""NÃO TEMAS — 2 Reis 6:15-17 — prévia v2 (camiseta preta).

Diagramação da referência 1: título enorme em itálico extra-largo e pesado
no topo (Archivo Expanded Black Italic, a mais próxima do lettering da ref.),
o monte sobe por trás da base das letras e os riscos de fogo passam por cima;
cavalos na base. Sem arco e sem estrela (pedido do cliente).
Embaixo, um bloco de texto diagramado ("lockup") com
"ALÉM DO QUE SE VÊ" + "2 REIS 6:16".

uso: python3 make_2reis.py <lockup> <saida.svg>
  lockup A = centralizado em 2 níveis com filetes
  lockup B = bloco à esquerda + referência à direita, separados por fio vertical
"""
import base64
import io
import sys

import numpy as np
from PIL import Image

from corujinha_art import Font, Text, cm, document

ILUS = "../2-reis-6/ilustracao/cavalos_fogo_v2a_figma.png"
W, H = round(cm(28)), round(cm(36))
WHITE, CREAM, GOLD, RED = "#FFFFFF", "#E9E2CF", "#E3A83B", "#B4483C"
TITLE = "NÃO TEMAS"
TITLE_W = cm(26.0)
T_TOP = cm(3.0)
ILU_W = cm(27.0)
SKEW = 7                  # inclinação extra além do itálico da fonte (como na ref.)
BASE_ROW = 300 / 1280     # linha da imagem que encosta na base do título


def png_uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def rule(x0, x1, y, w, color):
    return (f'<rect x="{x0:.1f}" y="{y - w / 2:.1f}" width="{x1 - x0:.1f}" '
            f'height="{w:.1f}" fill="{color}"/>')


def lockup_A(cx, top):
    """ALÉM DO QUE SE VÊ (itálico largo) / —— 2 REIS 6:16 —— (espaçado)."""
    ex = Font("ArchivoExpanded-900i")
    m = Font("Montserrat-600")
    l1 = Text(ex, "ALÉM DO QUE SE VÊ", cm(1.05), CREAM, tracking=40).place(cx=cx, top=top)
    b1 = l1.box()
    l2 = Text(m, "2 REIS 6:16", cm(0.42), GOLD, tracking=600).place(cx=cx, top=b1[3] + cm(0.45))
    b2 = l2.box()
    y = (b2[1] + b2[3]) / 2
    gap = cm(0.5)
    parts = [l1.svg(), l2.svg(),
             rule(b1[0], b2[0] - gap, y, cm(0.06), CREAM),
             rule(b2[2] + gap, b1[2], y, cm(0.06), CREAM)]
    return parts, b2[3]


def lockup_B(cx, top, width):
    """Bloco: ALÉM DO / QUE SE VÊ (itálico largo, 2 linhas) | fio | 2 REIS
    6:16 + microtexto do versículo, alinhado como uma etiqueta."""
    ex = Font("ArchivoExpanded-900i")
    m6 = Font("Montserrat-600")
    m5 = Font("Montserrat-500")
    x0 = cx - width / 2
    a1 = Text(ex, "ALÉM DO", cm(1.15), CREAM, tracking=20).place(left=x0, top=top)
    a2 = Text(ex, "QUE SE VÊ", cm(1.15), CREAM, tracking=20)
    a2.place(left=x0, top=a1.box()[3] + cm(0.28))
    bl = max(a1.box()[2], a2.box()[2])
    bottom = a2.box()[3]
    vx = bl + cm(0.75)
    rx = vx + cm(0.75)
    r1 = Text(m6, "2 REIS 6:16", cm(0.5), GOLD, tracking=420).place(left=rx, top=top + cm(0.05))
    micro = ["NÃO TEMAS, PORQUE MAIS SÃO", "OS QUE ESTÃO CONOSCO DO QUE", "OS QUE ESTÃO COM ELES."]
    parts = [a1.svg(), a2.svg(), r1.svg(),
             rule(vx - cm(0.03), vx + cm(0.03), 0, 0, CREAM)]
    parts[-1] = (f'<rect x="{vx - cm(0.03):.1f}" y="{top:.1f}" width="{cm(0.06):.1f}" '
                 f'height="{bottom - top:.1f}" fill="{CREAM}"/>')
    y = r1.box()[3] + cm(0.42)
    for ln in micro:
        t = Text(m5, ln, cm(0.3), CREAM, tracking=160).place(left=rx, top=y)
        parts.append(t.svg())
        y = t.box()[3] + cm(0.2)
    # centraliza o bloco inteiro
    right = max(r1.box()[2], max(Text(m5, ln, cm(0.3), CREAM, tracking=160).w for ln in micro) + rx)
    shift = cx - (x0 + right) / 2
    return [f'<g transform="translate({shift:.1f} 0)">' + "".join(parts) + "</g>"], max(bottom, y)


def build(lock, out):
    f = Font("ArchivoExpanded-900i")
    title = Text(f, TITLE, 1000, WHITE, tracking=-25, skew=SKEW)
    title = Text(f, TITLE, 1000 * TITLE_W / title.w, WHITE, tracking=-25, skew=SKEW)
    title.place(cx=W / 2, top=T_TOP)
    tb = title.box()

    ilu = Image.open(ILUS).convert("RGB")
    iw = round(ILU_W)
    ih = round(ilu.height * iw / ilu.width)
    ix = (W - iw) // 2
    iy = round(tb[3] - ih * BASE_ROW)
    a = np.asarray(ilu.resize((iw, ih), Image.LANCZOS)).astype(int)
    alpha = np.clip((a.max(axis=2) - 22) * 5, 0, 255).astype(np.uint8)
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    fire = (r > 170) & (g > 100) & (r - b > 90)
    fire_rgba = Image.fromarray(np.dstack([a.astype(np.uint8), np.where(fire, alpha, 0).astype(np.uint8)]), "RGBA")

    body = [f'<rect width="{W}" height="{H}" fill="#0B0B0B"/>']   # só na prévia
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(rgba)}"/>')
    body.append(title.svg())
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(fire_rgba)}"/>')

    # fim real da tinta da ilustração (poeira)
    rows = np.where((alpha > 40).any(axis=1))[0]
    ink_bottom = iy + rows.max()
    top = ink_bottom + cm(0.6)
    if lock == "A":
        parts, end = lockup_A(W / 2, top)
    else:
        parts, end = lockup_B(W / 2, top, cm(20))
    body += parts
    open(out, "w").write(document("\n".join(body), W, H))
    print(f"lockup {lock}: título {(tb[2]-tb[0])/300*2.54:.1f} x {(tb[3]-tb[1])/300*2.54:.1f} cm; "
          f"arte de {tb[1]/300*2.54:.1f} até {end/300*2.54:.1f} cm")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
