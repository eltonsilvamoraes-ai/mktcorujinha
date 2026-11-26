"""Frente NÃO TEMAS — só o texto, como na MT 6:26 (mesma cursiva das costas,
amarelo-palha com textura gasta; vermelho na off-white).

uso: python3 make_2reis_frente.py <opcao> <cor> <saida.svg>
  opcao 1 = uma linha, leve subida (-8°), 10 cm de largura
  opcao 2 = duas linhas escalonadas ("Não" / "temas"), como nas costas, 9 cm
"""
import sys

from corujinha_art import Font, Text, cm, document
from make_2reis import distressed, png_uri

SCRIPT = "MonsieurLaDoulaise"


def build(opt, color, out):
    f = Font(SCRIPT)
    W = round(cm(12)); H = round(cm(8))
    if opt == 1:
        t = Text(f, "Não Temas", 1000, color)
        t = Text(f, "Não Temas", 1000 * cm(9.6) / t.w, color)
        t.place(cx=W / 2, cy=H / 2)
        parts = [t]
    else:
        s1 = Text(f, "Não", cm(3.2), color)
        s2 = Text(f, "Temas", cm(3.2), color)
        gap = cm(0.5)
        tot = s1.w + gap + s2.w
        sc = cm(8.6) / tot
        s1 = Text(f, "Não", cm(3.2) * sc, color); s2 = Text(f, "Temas", cm(3.2) * sc, color)
        x0 = (W - (s1.w + gap * sc + s2.w)) / 2
        s1.place(left=x0, top=cm(1.6))
        s2.place(left=x0 + s1.w + gap * sc, top=s1.box()[3] - s1.h * 0.42)
        parts = [s1, s2]
    stroke = parts[0].size * 0.012
    bx = [p.box() for p in parts]
    cx = (min(b[0] for b in bx) + max(b[2] for b in bx)) / 2
    cy = (min(b[1] for b in bx) + max(b[3] for b in bx)) / 2
    inner = f'<g transform="rotate(-8 {cx:.1f} {cy:.1f})">' + "".join(p.svg(stroke=stroke) for p in parts) + "</g>"
    tex = distressed(inner, W, H, seed=5)
    bb = tex.getbbox()
    tex = tex.crop(bb)
    w, h = tex.size
    svg = document(f'<image x="0" y="0" width="{w}" height="{h}" href="{png_uri(tex)}"/>', w, h)
    open(out, "w").write(svg)
    print(f"frente opção {opt}: {w/300*2.54:.1f} x {h/300*2.54:.1f} cm")
    return tex


if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2], sys.argv[3])
