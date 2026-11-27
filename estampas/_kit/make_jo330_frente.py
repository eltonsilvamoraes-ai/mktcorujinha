"""Frente — "Que ele Cresça" + "Jo 3:30" (mesmo lettering da arte das costas).

Recorta da arte original só os componentes da linha "Que ele / Cresça"
(sem "e eu Diminua") e coloca "Jo 3:30" embaixo com a mesma fonte/textura
usada nas costas (Lobster + textura tirada da própria arte).

uso: python3 make_jo330_frente.py <saida.png>
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

import make_jo330 as jo

KEEP_MAX_TOP = 800        # componentes que começam acima disso = "Que ele Cresça"
UP = 2


def build(out, verse_size=95, gap=35):
    src = np.array(Image.open(jo.SRC).convert("RGB"))
    ink = src.max(2) > 60
    lab, n = nd.label(ink, np.ones((3, 3)))
    keep = np.zeros(n + 1, bool)
    for i, s in enumerate(nd.find_objects(lab), 1):
        if s[0].start < KEEP_MAX_TOP and s[0].stop < 870:
            keep[i] = True
    m = keep[lab]
    m = nd.binary_dilation(m, iterations=2) & ink | m
    ys, xs = np.where(m)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    bg = np.array([11, 22, 34], np.uint8)
    pad = 60
    H = (y1 - y0) + gap + verse_size * 2 + pad * 2
    Wd = (x1 - x0) + pad * 2
    canvas = np.zeros((H, Wd, 3), np.uint8); canvas[:] = bg
    crop = src[y0:y1, x0:x1].copy(); crop[~m[y0:y1, x0:x1]] = bg
    canvas[pad:pad + (y1 - y0), pad:pad + (x1 - x0)] = crop
    alpha = np.zeros((H, Wd), np.float32)
    alpha[pad:pad + (y1 - y0), pad:pad + (x1 - x0)] = m[y0:y1, x0:x1]
    # versículo
    im = Image.fromarray(canvas)
    big = im.resize((Wd * UP, H * UP), Image.LANCZOS)
    a = np.asarray(big).astype(float)
    patch = jo.texture_patch(src)
    patch = np.asarray(Image.fromarray(patch).resize((patch.shape[1] * UP, patch.shape[0] * UP), Image.LANCZOS)).astype(float)
    tile = np.concatenate([patch, patch[:, ::-1]], 1); tile = np.concatenate([tile, tile[::-1]], 0)
    tex = np.tile(tile, ((H * UP) // tile.shape[0] + 1, (Wd * UP) // tile.shape[1] + 1, 1))[:H * UP, :Wd * UP]
    vm = jo.text_mask("Jo 3:30", verse_size * UP, Wd * UP, H * UP, Wd * UP / 2,
                      (pad + (y1 - y0) + gap) * UP, -6)
    if vm.shape != a.shape[:2]:
        vm = np.asarray(Image.fromarray((vm * 255).astype(np.uint8)).resize((a.shape[1], a.shape[0]))) / 255
    a = a * (1 - vm[..., None]) + tex * vm[..., None]
    out_rgb = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    out_rgb.save(out)
    # versão com fundo transparente (para mockup)
    al = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((Wd * UP, H * UP), Image.LANCZOS)) / 255
    al = np.maximum(al, vm)
    rgba = np.dstack([np.asarray(out_rgb), (al * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(out.replace(".png", "_transp.png"))


if __name__ == "__main__":
    build(sys.argv[1])
