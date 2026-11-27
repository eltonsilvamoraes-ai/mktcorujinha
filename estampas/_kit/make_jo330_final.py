"""JO 3:30 — arquivos finais VAZADOS (1 cor) para DTF.

Vazado: só as letras viram tinta; os riscos escuros da textura de giz e o
fundo ficam sem tinta (aparece o tecido). Uma camada só, fácil de trocar a cor.
COSTAS: arte completa + "Jo 3:30" (opção A reduzida), 28 cm de largura.
FRENTE: "Que ele Cresça", 8 cm de largura.

uso: python3 make_jo330_final.py <pasta_saida> [cor_tinta]
"""
import os
import sys

import numpy as np
from PIL import Image

from corujinha_art import cm, document, render
from vetorizar_cores import re, trace

PREV = "../jo-3-30/previas/"


def vector(png, width_cm, ink, gid, out_base, frame=None):
    a = np.asarray(Image.open(png).convert("RGB")).astype(float)
    lum = a.mean(axis=2)
    m = lum > 128
    ys, xs = np.where(m)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    m = m[y0:y1, x0:x1]
    up = 2
    mi = Image.fromarray((m * 255).astype(np.uint8)).resize((m.shape[1] * up, m.shape[0] * up), Image.LANCZOS)
    m = np.asarray(mi) > 127
    W = round(cm(width_cm))
    s = W / m.shape[1]
    H = round(m.shape[0] * s)
    tr, inner = trace(m, 1, 0, 0)
    inner = re.sub(r'fill="[^"]*"', "", inner)
    FW, FH = (W, H) if frame is None else (round(cm(frame[0])), round(cm(frame[1])))
    ox, oy = (FW - W) / 2, (FH - H) / 2
    body = (f'<g id="{gid.upper()}"><g id="{gid}_{ink[1:]}" fill="{ink}" '
            f'transform="translate({ox:.2f} {oy:.2f}) scale({s:.6f})"><g transform="{tr}">{inner}</g></g></g>')
    svg = document(body, FW, FH)
    open(out_base + ".svg", "w").write(svg)
    render(svg, out_base + ".png", width=FW)
    print(os.path.basename(out_base), f"{W/300*2.54:.1f} x {H/300*2.54:.1f} cm")
    return svg


def main(outdir, ink="#F2EEE3"):
    os.makedirs(outdir, exist_ok=True)
    vector(PREV + "jo330_opcaoA_v2.png", 28, ink, "costas", os.path.join(outdir, "JO3-30_COSTAS"), frame=(28, 36))
    vector(PREV + "frente_que-ele-cresca_v2.png", 8, ink, "frente", os.path.join(outdir, "JO3-30_FRENTE"))


if __name__ == "__main__":
    main(*sys.argv[1:])
