"""NÃO TEMAS — teste em "cromia" (separação simulada) com retícula.

O PRETO VIRA TINTA: a ilustração é separada em tintas (preto, azul, vermelho,
laranja, dourado, creme, branco) e cada tinta é reticulada com PONTO ELÍPTICO
a 45°, lineatura 40 lpi — como uma separação de cromia/processo simulado.
Assim a arte funciona sobre qualquer cor de tecido (as sombras são pontos
pretos impressos, não o tecido).

uso: python3 make_2reis_reticula.py <saida_ilustracao.png> [dpi]
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

import make_2reis as m
from vetorizar_cores import to_lab

LPI, ANGLE, ELLIPSE = 40, 45, 0.70     # lineatura, ângulo, achatamento do ponto
INKS = [  # nome, cor da tinta, amostra na imagem (ordem = ordem de impressão)
    ("preto", "#121212", "#0A0A0A"),
    ("azul", "#5B8FC2", "#5B8FC2"),
    ("vermelho", "#B4483C", "#B4483C"),
    ("laranja", "#E0722C", "#E0722C"),
    ("dourado", "#E8B53E", "#E8B53E"),
    ("creme", "#DCCBA3", "#DCCBA3"),
    ("branco", "#F4EFE4", "#F4EFE4"),
]
TEMP = 700.0       # suavidade da separação (maior = transições mais suaves)


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def threshold_map(h, w, cell):
    """Matriz de limiar de ponto elíptico, rotacionada (valores 0..1 uniformes)."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    t = np.deg2rad(ANGLE)
    u = (x * np.cos(t) + y * np.sin(t)) / cell
    v = (-x * np.sin(t) + y * np.cos(t)) / cell
    fu, fv = u - np.floor(u) - 0.5, v - np.floor(v) - 0.5
    d = np.sqrt(fu ** 2 + (fv / ELLIPSE) ** 2)
    # equaliza: transforma distância em "área coberta" (0..1 uniforme)
    s = np.sort(d[: min(h, 400), : min(w, 400)].ravel())
    return (np.searchsorted(s, d) / s.size).astype(np.float32)


def separate_soft(img):
    a = np.asarray(img, float)
    lab = to_lab(a.reshape(-1, 3))
    ref = to_lab(np.array([rgb(s) for _, _, s in INKS]))
    d2 = ((lab[:, None, :] - ref[None]) ** 2).sum(-1)
    w = np.exp(-(d2 - d2.min(1, keepdims=True)) / TEMP)
    w /= w.sum(1, keepdims=True)
    return w.reshape(a.shape[0], a.shape[1], len(INKS)).astype(np.float32)


def build(out, dpi=450):
    ilu = Image.open(m.ILUS).convert("RGB")
    iw = round(m.ILU4_W / 2.54 * dpi)
    ih = round(ilu.height * iw / ilu.width)
    # separação numa resolução média (suaviza o pontilhado do original em tom)
    mid = ilu.resize((iw // 3, ih // 3), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.2))
    cov = separate_soft(mid)
    # silhueta: o preto do FUNDO não é tinta (só o preto dentro do desenho)
    lum = np.asarray(mid).max(axis=2)
    sil = nd.binary_fill_holes(nd.binary_closing(lum > 40, np.ones((3, 3)), iterations=5))
    soft = np.asarray(Image.fromarray((sil * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)), float) / 255
    cov[..., 0] *= soft
    cell = dpi / LPI
    thr = threshold_map(ih, iw, cell)
    outimg = np.zeros((ih, iw, 4), np.uint8)
    for k, (name, ink, _) in enumerate(INKS):
        c = np.asarray(Image.fromarray((cov[..., k] * 255).astype(np.uint8)).resize((iw, ih), Image.BILINEAR), np.float32) / 255
        dots = c > thr
        outimg[dots] = (*rgb(ink).astype(np.uint8), 255)
        print(name, f"{dots.mean()*100:.1f}% de cobertura")
    Image.fromarray(outimg, "RGBA").save(out)


if __name__ == "__main__":
    build(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 450)
