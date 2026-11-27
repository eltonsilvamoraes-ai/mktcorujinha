"""QUE ELE CRESÇA E EU DIMINUA — inserir "Jo 3:30" no mesmo estilo do lettering.

A arte base é a imagem gerada no ChatGPT (lettering feito à mão, não é fonte).
O versículo usa a fonte livre mais próxima (Lobster: script grosso inclinado)
e recebe a MESMA textura das letras da arte: um recorte do miolo de uma letra
grande é usado como textura (pincel seco / riscos), então o acabamento casa.

uso: python3 make_jo330.py <opcao> <saida.png>
  A = centralizado embaixo do floreio final
  B = no topo, acima de "Que ele"
  C = embaixo, à direita, alinhado ao fim do floreio
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

from corujinha_art import Font, Text, document, render

SRC = "../jo-3-30/referencias/arte_chatgpt_que-ele-cresca.png"
UP = 2
FONT = "Lobster-Regular"


def texture_patch(a):
    lum = a.max(axis=2)
    letters = nd.binary_closing(lum > 120, np.ones((3, 3)), iterations=4)
    dist = nd.distance_transform_edt(letters)
    y, x = np.unravel_index(dist.argmax(), dist.shape)
    r = int(dist.max() * 0.65)
    return a[y - r:y + r, x - r:x + r]


def text_mask(txt, size, w, h, cx, top, rot):
    f = Font(FONT)
    t = Text(f, txt, size, "#FFFFFF").place(cx=cx, top=top)
    b = t.box()
    inner = (f'<g transform="rotate({rot} {(b[0]+b[2])/2:.1f} {(b[1]+b[3])/2:.1f})">'
             + t.svg(stroke=size * 0.035) + "</g>")
    import tempfile, os
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.png")
        render(document(inner, w, h), p, width=w)
        return np.asarray(Image.open(p).convert("RGBA"))[..., 3] / 255


def build(opt, out):
    src = Image.open(SRC).convert("RGB")
    W, H = src.width * UP, src.height * UP
    base = np.asarray(src.resize((W, H), Image.LANCZOS)).astype(float)
    patch = texture_patch(np.asarray(src))
    patch = np.asarray(Image.fromarray(patch).resize((patch.shape[1] * UP, patch.shape[0] * UP), Image.LANCZOS)).astype(float)
    # textura em mosaico espelhado (sem emendas)
    tile = np.concatenate([patch, patch[:, ::-1]], axis=1)
    tile = np.concatenate([tile, tile[::-1]], axis=0)
    reps = (H // tile.shape[0] + 1, W // tile.shape[1] + 1, 1)
    tex = np.tile(tile, reps)[:H, :W]

    size, rot = {"A": (115, -6), "B": (130, -6), "C": (130, -6)}[opt]
    size *= UP
    pos = {"A": (W * 0.50, 1305 * UP), "B": (W * 0.50, 150 * UP), "C": (W * 0.66, 1290 * UP)}[opt]
    m = text_mask("Jo 3:30", size, W, H, pos[0], pos[1], rot)
    bg = np.array([11, 22, 34], float)
    out_img = base * (1 - m[..., None]) + (bg * (1 - m[..., None]) * 0 + tex * m[..., None])
    Image.fromarray(np.clip(out_img, 0, 255).astype(np.uint8)).save(out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
