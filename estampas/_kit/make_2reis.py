"""NÃO TEMAS — 2 Reis 6:15-17 — prévia v2 (camiseta preta).

Diagramação da referência 1: título enorme em itálico extra-largo e pesado
no topo (Archivo Expanded Black Italic, a mais próxima do lettering da ref.),
o monte sobe por trás da base das letras e os riscos de fogo passam por cima;
cavalos na base. Sem arco e sem estrela (pedido do cliente).
Embaixo, um bloco de texto diagramado ("lockup") com
"ALÉM DO QUE SE VÊ" + "2 REIS 6:16".

uso: python3 make_2reis.py <lockup> <saida.svg> [fonte_cursiva]
  (com fonte_cursiva: título "Não temas" caligráfico, inclinado, com textura gasta)
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


SCRIPT_COLOR = "#ECE29A"   # amarelo-palha (como o "Brand Studios" da ref.)


def distressed(svg_inner, w, h, seed=7):
    """Renderiza um trecho vetorial e aplica textura gasta (prévia raster)."""
    from corujinha_art import render
    import tempfile, os
    rng = np.random.default_rng(seed)
    with tempfile.TemporaryDirectory() as t:
        p = os.path.join(t, "t.png")
        render(document(svg_inner, w, h), p, width=w)
        im = np.array(Image.open(p).convert("RGBA"))
    # salpicos + riscos verticais finos (desgaste de serigrafia vintage)
    noise = rng.random((h // 3 + 1, w // 3 + 1))
    noise = np.array(Image.fromarray((noise * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)) / 255
    keep = noise > 0.18
    for _ in range(int(w * 0.04)):
        x = rng.integers(0, w); y0 = rng.integers(0, h); L = rng.integers(h // 20, h // 4)
        keep[y0:y0 + L, x:x + rng.integers(1, 3)] = False
    im[..., 3] = (im[..., 3] * keep).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def build(lock, out, script=None):
    if script is None:
        f = Font("ArchivoExpanded-900i")
        title = Text(f, TITLE, 1000, WHITE, tracking=-25, skew=SKEW)
        title = Text(f, TITLE, 1000 * TITLE_W / title.w, WHITE, tracking=-25, skew=SKEW)
        title.place(cx=W / 2, top=T_TOP)
        tb = title.box()
        title_svg = title.svg()
    else:
        f = Font(script)
        tw = cm(24.5)
        title = Text(f, "Não temas", 1000, SCRIPT_COLOR)
        title = Text(f, "Não temas", 1000 * tw / title.w, SCRIPT_COLOR)
        title.place(cx=W / 2, top=cm(2.2))
        tb0 = title.box()
        stroke = title.size * 0.014          # engrossa os traços finos
        rot = -6
        cx, cy = (tb0[0] + tb0[2]) / 2, (tb0[1] + tb0[3]) / 2
        inner = (f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">'
                 + title.svg(stroke=stroke) + "</g>")
        tex = distressed(inner, W, H)
        bb = tex.getbbox()
        tb = (bb[0], bb[1], bb[2], bb[3])
        # base "visual" do título = 80% da altura (floreios descem abaixo)
        tb = (tb[0], tb[1], tb[2], tb[1] + (tb[3] - tb[1]) * 0.80)
        title_svg = f'<image x="0" y="0" width="{W}" height="{H}" href="{png_uri(tex)}"/>'

    ilu = Image.open(ILUS).convert("RGB")
    # a ilustração encolhe se preciso para o rodapé caber no quadro (36 cm)
    lum0 = np.asarray(ilu).max(axis=2)
    rmax = np.where((lum0 > 40).any(axis=1))[0].max() / ilu.height
    foot = cm(0.6) + cm(2.6 if lock == "B" else 1.9) + cm(0.6)
    ih_max = (H - foot - tb[3]) / (rmax - BASE_ROW)
    iw = round(min(ILU_W, ih_max * ilu.width / ilu.height))
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
    body.append(title_svg)
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
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)


# ---------------------------------------------------------------- v4
# Título cursivo ENTRELAÇADO com a montanha (ref. "Social Club"): 2 linhas
# em diagonal grande, passando POR TRÁS do pico central e na frente do resto.
# Rodapé no estilo da ref.: versículo pequeno centralizado + frase em
# vermelho bold itálico. "2 REIS / 6:16" pequeno ao lado do título (como
# o "EST 2025") e a corujinha no lugar do ®.

SHIFT_UP = 0.8             # sobe título + ilustração (cm) para o rodapé caber
FOOT_W = cm(12.0)          # largura do versículo no rodapé
ILU4_W = 26.5              # largura da ilustração (cm) na v4+


def build_v4(out, color="#ECE29A", script="MonsieurLaDoulaise"):
    from corujinha_art import logo_svg
    ilu = Image.open(ILUS).convert("RGB")
    iw = round(cm(ILU4_W))
    ih = round(ilu.height * iw / ilu.width)
    ix, iy = (W - iw) // 2, round(cm(0.4 - SHIFT_UP))
    a = np.asarray(ilu.resize((iw, ih), Image.LANCZOS)).astype(int)
    alpha = np.clip((a.max(axis=2) - 22) * 5, 0, 255).astype(np.uint8)
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")

    # pico central (fica NA FRENTE do título)
    yy, xx = np.mgrid[0:ih, 0:iw]
    px, py = 0.50 * iw, 0.19 * ih            # topo do pico
    # só a ponta do pico (azul + fogo) passa na frente, entre "Não" e "temas"
    peak = (yy > py) & (yy < 0.29 * ih) & (np.abs(xx - px) < (yy - py) * 0.75 + 6)
    front = Image.fromarray(np.dstack([a.astype(np.uint8), np.where(peak, alpha, 0).astype(np.uint8)]), "RGBA")

    # título: "Não" / "temas" em diagonal
    f = Font(script)
    s1 = Text(f, "Não", cm(7.0), color)
    s2 = Text(f, "temas", cm(7.0), color)
    gap = cm(2.1)                              # vão onde aparece o pico
    total = s1.w + gap + s2.w
    x0 = (W - total) / 2 - cm(0.4)
    s1.place(left=x0, top=cm(2.0 - SHIFT_UP))
    s2.place(left=x0 + s1.w + gap, top=s1.box()[3] - cm(3.0))
    stroke = s1.size * 0.012
    b1, b2 = s1.box(), s2.box()
    rcx, rcy = (b1[0] + b2[2]) / 2, (b1[1] + b2[3]) / 2
    inner = (f'<g transform="rotate(-8 {rcx:.1f} {rcy:.1f})">'
             + s1.svg(stroke=stroke) + s2.svg(stroke=stroke) + "</g>")
    tex = distressed(inner, W, H, seed=11)

    body = [f'<rect width="{W}" height="{H}" fill="#0B0B0B"/>']   # só na prévia
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(rgba)}"/>')
    body.append(f'<image x="0" y="0" width="{W}" height="{H}" href="{png_uri(tex)}"/>')
    body.append(f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="{png_uri(front)}"/>')

    # "2 REIS / 6:16" pequeno à esquerda (como o EST 2025) + corujinha (como o ®)
    tb = tex.getbbox()
    ex = Font("Archivo-900i")
    # (sem logo e sem referência no topo: pedido do cliente — logo entra depois)

    # rodapé (estilo ref.)
    rows = np.where((alpha > 40).any(axis=1))[0]
    y = iy + rows.max() + cm(0.9)          # um pouco mais de respiro dos cavalos
    m8 = Font("Montserrat-800")
    lines = ("NÃO TEMAS, PORQUE MAIS SÃO",
             "OS QUE ESTÃO CONOSCO DO QUE",
             "OS QUE ESTÃO COM ELES")
    widest = max(Text(m8, ln, 100, CREAM, tracking=30).w for ln in lines)
    fs = 100 * FOOT_W / widest                 # linha mais larga = FOOT_W
    k = fs / cm(0.5)
    for ln in lines:
        t = Text(m8, ln, fs, CREAM, tracking=30).place(cx=W / 2, top=y)
        body.append(t.svg()); y = t.box()[3] + cm(0.2) * k
    ref = Text(Font("Montserrat-800"), "2 REIS 6:15-17", cm(0.42) * k, CREAM, tracking=150)
    ref.place(cx=W / 2, top=y + cm(0.3) * k)
    body.append(ref.svg())
    red = ref
    open(out, "w").write(document("\n".join(body), W, H))
    print(f"v4: arte até {red.box()[3]/300*2.54:.1f} cm")
