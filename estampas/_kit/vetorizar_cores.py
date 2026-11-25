"""Vetoriza uma arte raster por separação de cores (uma camada por tinta).

Cada pixel vai para a tinta mais próxima da paleta (em Lab); cada tinta é
traçada com o potrace nativo (apt install potrace) e vira um <path> próprio, pronto para serigrafia.
O branco é tratado como "sem tinta" (camiseta branca).

uso: python3 vetorizar_cores.py <entrada> <saida.svg> [altura_cm] [largura_quadro_cm] [altura_quadro_cm]
"""
import re
import sys

import numpy as np
from PIL import Image, ImageFilter

from corujinha_art import cm, document

# paleta medida na arte (k-means) — nome: (cor da tinta, amostra na imagem)
PALETTE = {
    "branco": (None, "#FDFCFC"),
    "marinho": ("#0B2540", "#092239"),
    "vermelho": ("#CE2A1F", "#CE190D"),
    "creme": ("#EEDFD2", "#ECDCD2"),
    "azul": ("#84A5BB", "#84A5BB"),
    "laranja": ("#E1745C", "#E1745C"),
}
# tons intermediários que aparecem na imagem e vão para a tinta mais escura
EXTRA = {"marinho": ["#4D6173", "#4C1916"]}
ORDER = ["creme", "azul", "laranja", "vermelho", "marinho"]  # de baixo p/ cima
UPSCALE = 3


def hex2rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def to_lab(rgb):
    from skimage.color import rgb2lab
    return rgb2lab(rgb.reshape(-1, 1, 3) / 255.0).reshape(-1, 3)


def separate(img):
    names, samples = [], []
    for n, (_, s) in PALETTE.items():
        names.append(n); samples.append(hex2rgb(s))
        for e in EXTRA.get(n, []):
            names.append(n); samples.append(hex2rgb(e))
    a = np.asarray(img, dtype=float)
    h, w, _ = a.shape
    lab = to_lab(a.reshape(-1, 3))
    ref = to_lab(np.array(samples, dtype=float))
    d = ((lab[:, None, :] - ref[None, :, :]) ** 2).sum(-1)
    idx = d.argmin(1).reshape(h, w)
    return {n: np.isin(idx, [i for i, m in enumerate(names) if m == n])
            for n in PALETTE}


def trace(mask, s, ox, oy):
    """Traça a máscara com o potrace nativo e devolve um <g> posicionado."""
    import re, subprocess, tempfile, os
    with tempfile.TemporaryDirectory() as t:
        pbm = os.path.join(t, "m.pbm")
        Image.fromarray(~mask).convert("1").save(pbm)  # PBM: preto (0) = tinta
        out = subprocess.run(["potrace", pbm, "-b", "svg", "-r", "72", "-t", "6",
                              "-a", "1", "-O", "0.25", "--flat", "-o", "-"],
                             capture_output=True, text=True, check=True).stdout
    g = re.search(r"<g transform=\"([^\"]+)\"[^>]*>(.*)</g>", out, re.S)
    return g.group(1), g.group(2)


def build(src, out, h_cm=30.0, fw_cm=27.0, fh_cm=32.0):
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * UPSCALE, im.height * UPSCALE), Image.LANCZOS)
    im = im.filter(ImageFilter.MedianFilter(3))
    masks = separate(im)
    W, H = round(cm(fw_cm)), round(cm(fh_cm))
    ah = cm(h_cm)
    s = ah / im.height
    aw = im.width * s
    ox, oy = (W - aw) / 2, (H - ah) / 2
    body = []
    for n in ORDER:
        ink = PALETTE[n][0]
        tr, inner = trace(masks[n], s, ox, oy)
        inner = re.sub(r'fill="[^"]*"', "", inner)
        body.append(f'<g id="{n}" fill="{ink}" transform="translate({ox:.2f} {oy:.2f}) '
                    f'scale({s:.6f})"><g transform="{tr}">{inner}</g></g>')
    open(out, "w").write(document("\n".join(body), W, H))


if __name__ == "__main__":
    args = sys.argv[1:3] + [float(v) for v in sys.argv[3:]]
    build(*args)
