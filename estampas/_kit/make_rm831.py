"""ROMANOS 8:31 — "Se Deus é por nós, quem será contra nós?"

Converte a arte colorida do cliente em estampa de 1 COR com aspecto de
impressão envelhecida (vintage):
  - cobertura de tinta = quanto o pixel "se afasta do branco" (min RGB);
  - tons médios viram grão (dither estocástico), áreas fortes ficam chapadas;
  - desgaste: falhas e riscos aleatórios tiram tinta (cara de estampa gasta);
  - o branco da arte (cruz, águia, neve) fica SEM tinta = cor da camiseta.
O degradê cinza das bordas da imagem original é descartado.

uso: python3 make_rm831.py <cor_tinta> <cor_camiseta> <saida.png> [transp.png]
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

SRC = "../romanos-8-31/referencias/arte_cliente.webp"
UP = 3
TOP, BOTTOM = 120, 965        # faixa útil da arte (fora disso é a vinheta cinza)


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.uint8)


def ink_mask(seed=7, wear=1.0):
    """wear: 1.0 = desgaste da v1 | 0.4 = leve | 0.15 = mínimo"""
    src = Image.open(SRC).convert("RGBA")
    im = Image.new("RGBA", src.size, "white"); im.alpha_composite(src)   # fundo transparente -> branco
    im = im.convert("RGB")
    w, h = im.size
    big = im.resize((w * UP, h * UP), Image.LANCZOS)
    a = np.asarray(big).astype(float)
    c = (255 - a.min(axis=2)) / 255.0            # 0 = branco, 1 = cor forte
    c = np.clip((c - 0.06) / 0.48, 0, 1)   # texto bege mais firme
    rows = np.arange(h * UP)[:, None]
    c[((rows < TOP * UP) | (rows > BOTTOM * UP))[:, 0]] = 0
    # cinzas neutros fracos da névoa/vinheta não viram tinta
    sat = (a.max(axis=2) - a.min(axis=2)) / 255.0
    c[(sat < 0.08) & (c < 0.35)] *= 0.4
    rng = np.random.default_rng(seed)
    grain = rng.random(c.shape)
    grain = np.asarray(Image.fromarray((grain * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), float) / 255
    grain = (grain - grain.min()) / (grain.max() - grain.min())
    ink = (c > 0.55) | (c > grain * 0.55 + 0.08)
    # desgaste vintage: manchas grandes suaves + riscos finos
    blot = rng.random((h // 6, w // 6))
    blot = np.asarray(Image.fromarray((blot * 255).astype(np.uint8)).resize((w * UP, h * UP), Image.BICUBIC), float) / 255
    ink &= ~((blot > 1 - 0.20 * wear) & (grain > 0.55))
    for _ in range(int(900 * wear)):
        x = rng.integers(0, w * UP); y = rng.integers(0, h * UP)
        L = rng.integers(8, 60); ang = rng.normal(0, 0.25)
        xs = (x + np.arange(L) * np.sin(ang)).astype(int).clip(0, w * UP - 1)
        ys = (y + np.arange(L) * np.cos(ang)).astype(int).clip(0, h * UP - 1)
        ink[ys, xs] = False
    ink = nd.binary_opening(ink, iterations=1) | (ink & (c > 0.7))
    return ink


def build(ink_hex, tee_hex, out, transp=None, wear=1.0):
    m = ink_mask(wear=float(wear))
    H, W = m.shape
    img = np.zeros((H, W, 3), np.uint8); img[:] = hexrgb(tee_hex)
    img[m] = hexrgb(ink_hex)
    Image.fromarray(img).save(out)
    if transp:
        rgba = np.zeros((H, W, 4), np.uint8); rgba[m] = (*hexrgb(ink_hex), 255)
        Image.fromarray(rgba, "RGBA").save(transp)


if __name__ == "__main__":
    build(*sys.argv[1:])
