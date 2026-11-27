"""QUE ELE CRESÇA E EU DIMINUA (Jo 3:30) — opção no estilo da ref. "Stay Cool":
lettering anos 70, letras gordas e arredondadas, palavras ENCAIXADAS umas nas
outras (cada palavra tem um contorno da cor do fundo que "corta" a de trás),
bloco compacto e textura de giz/lápis tirada da própria referência.

uso: python3 make_jo330_groovy.py <fonte> <saida.png>
"""
import os
import sys
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage as nd

from corujinha_art import Font, Text, document, render
from make_jo330 import texture_patch

REF = "../jo-3-30/referencias/ref_stay-cool.jpg"
W, H = 2048, 3072
BG = (11, 22, 34)
# (texto, escala, deslocamento x em fração da largura do bloco)
LINES = [("Que ele", 0.70, -0.06), ("Cresça", 1.0, 0.0), ("e eu", 0.60, 0.12),
         ("Diminua", 1.0, 0.0)]
VERSE = ("Jo 3:30", 0.24)
BLOCK_W = 1700
OVERLAP = 0.10     # quanto cada linha sobe sobre a anterior (x altura de versal)
GAP = 0.055        # espessura do corte entre palavras (x corpo)


def mask(t, extra=0.0):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.png")
        render(document(t.svg(stroke=extra) if extra else t.svg(), W, H), p, width=W)
        return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 110


def build(font, out, rot=-5):
    f = Font(font)
    cap = (lambda b: b[3] - b[1])(f.ink("H", 1000)) / 1000
    big = max(Text(f, t, 1000 * s, "#FFF").w for t, s, _ in LINES[:4] if s == 1.0)
    base = 1000 * BLOCK_W / big
    y = 0.0
    words = []
    prev = None
    for t, s_, dx in LINES:
        size = base * s_
        tx = Text(f, t, size, "#FFF")
        tx.place(cx=W / 2 + dx * BLOCK_W, top=0)
        if prev is not None:
            # topo das versais desta linha encosta na linha de base da anterior,
            # menos OVERLAP (encaixe)
            capt = tx.dy + (tx.ink[1] if False else 0)
            pb = prev.dy                      # linha de base anterior
            tx.dy = pb + size * cap * (1 - OVERLAP)
        else:
            tx.dy = size * cap
        words.append(tx)
        prev = tx
    vt, vs = VERSE
    v = Text(f, vt, base * vs, "#FFF").place(cx=W / 2)
    bottom = max(w.box()[3] for w in words)
    v.place(cx=W / 2, top=bottom + base * vs * 0.45)
    words.append(v)
    # centraliza verticalmente
    top = min(w.box()[1] for w in words); bot = max(w.box()[3] for w in words)
    shift = (H - (bot - top)) / 2 - top
    for w in words:
        w.dy += shift
    letters = np.zeros((H, W), bool)
    for w in words:
        fill = mask(w)
        cut = mask(w, extra=w.size * GAP * 2)
        letters &= ~cut
        letters |= fill
    img = Image.fromarray((letters * 255).astype(np.uint8)).rotate(rot, resample=Image.BICUBIC, center=(W / 2, H / 2))
    letters = np.asarray(img) > 127
    ref = np.asarray(Image.open(REF).convert("RGB"))
    patch = texture_patch(ref)
    patch = np.asarray(Image.fromarray(patch).resize((patch.shape[1] * 3, patch.shape[0] * 3), Image.LANCZOS))
    tile = np.concatenate([patch, patch[:, ::-1]], 1); tile = np.concatenate([tile, tile[::-1]], 0)
    tex = np.tile(tile, (H // tile.shape[0] + 1, W // tile.shape[1] + 1, 1))[:H, :W]
    outimg = np.zeros((H, W, 3), np.uint8); outimg[:] = BG
    outimg[letters] = tex[letters]
    Image.fromarray(outimg).save(out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
