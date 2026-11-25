"""O CÉU NÃO ESQUECE OS SEUS — prévias de cor (frente + costas) em mockup.

Gera, para cada cor de camiseta, a arte das costas (v6, proporcional) e a da
frente (só o lettering, sem o raminho), com as cores ajustadas:
  - clara (off-white): cores originais; branco = sem tinta (tecido aparece);
  - escura (preta / marrom): azul-marinho do TEXTO vira creme; na ILUSTRAÇÃO
    o branco de dentro do desenho recebe tinta clara (senão o pardal ficaria
    "transparente" e o tecido escuro apareceria no peito, nas pétalas etc.).
São prévias raster (rápidas); a produção é vetorizada depois da aprovação.

uso: python3 make_ceu_mockups.py <pasta_saida>
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as nd

import make_ceu_dtf as dtf
from vetorizar_cores import PALETTE, separate

TEES = {  # nome: (cor do tecido, escura?, modo no escuro)
    "offwhite": ("#EDE6D6", False, "base"),
    "preta_A-base-clara": ("#151515", True, "base"),
    "preta_B-negativo": ("#151515", True, "negativo"),
    "marrom_A-base-clara": ("#5A3F2E", True, "base"),
    "marrom_B-negativo": ("#5A3F2E", True, "negativo"),
}
CREAM_TXT = "#EFE8D8"     # texto claro nas camisetas escuras (off-white da marca)
BASE_INK = "#F3EEE4"      # tinta clara por baixo do desenho nas escuras
FRONT_W_CM = 10.0         # largura do texto na frente (peito)
UP = 2                    # upscale da prévia


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def prepared():
    """Imagem fonte com as flores ajustadas (v6) + máscaras ilustração/texto/ramo."""
    a = np.array(Image.open(dtf.SRC).convert("RGB"))
    tm, bm = dtf.split(a)
    cls = separate(Image.fromarray(a))
    yy, xx = np.ogrid[:a.shape[0], :a.shape[1]]
    for cx, cy, r in dtf.MUTE:
        circ = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
        a[circ & (cls["vermelho"] | cls["laranja"])] = (0x4D, 0x61, 0x73)
    # texto = componentes de baixo que começam acima do ramo; ramo = o resto
    lab, n = nd.label(bm, structure=np.ones((3, 3)))
    txt = np.zeros(n + 1, bool)
    frase = np.zeros(n + 1, bool)   # só as palavras (frente): sem ramo nem flor
    for i, sl in enumerate(nd.find_objects(lab), 1):
        if sl[0].start < dtf.GARLAND_TOP - 10:
            txt[i] = True
            if sl[0].stop <= dtf.GARLAND_TOP + 45:
                frase[i] = True
    # "— MT 6:26 —" no topo também é texto (no escuro vira creme)
    lab2, n2 = nd.label(tm, structure=np.ones((3, 3)))
    head = np.zeros(n2 + 1, bool)
    for i, sl in enumerate(nd.find_objects(lab2), 1):
        if sl[0].stop <= 90:
            head[i] = True
    yy2 = np.arange(a.shape[0])[:, None]
    hm = (head[lab2] | (yy2 < 88)) & tm
    return a, tm & ~hm, (txt[lab] & bm) | hm, (~txt[lab]) & bm, frase[lab] & bm


def colorize(a, regions, dark, mode="base"):
    """RGBA com a paleta de tinta; regions = {nome: máscara} da imagem."""
    up = Image.fromarray(a).resize((a.shape[1] * UP, a.shape[0] * UP), Image.LANCZOS)
    cls = separate(up)
    R = {k: np.array(Image.fromarray(v).resize(up.size, Image.NEAREST)) for k, v in regions.items()}
    h, w = cls["branco"].shape
    out = np.zeros((h, w, 4), np.uint8)
    for name, (ink, _) in PALETTE.items():
        if ink is None:
            continue
        m = cls[name]
        col = hex2rgb(ink)
        out[m] = (*col, 255)
        if dark and name == "marinho":
            for r in (("texto", "ramo", "ilustracao") if mode == "negativo" else ("texto", "ramo")):
                if r in R:
                    out[m & R[r]] = (*hex2rgb(CREAM_TXT), 255)
    # só o que pertence a alguma região entra
    allr = np.zeros((h, w), bool)
    for v in R.values():
        allr |= v
    if dark and mode == "negativo" and "ilustracao" in R:
        # negativo: o creme do pardal/pétalas some (vira tecido), as linhas ficam creme
        out[R["ilustracao"] & cls["creme"]] = 0
    if dark and mode == "base" and "ilustracao" in R:
        ink = R["ilustracao"]
        sil = nd.binary_closing(ink, structure=np.ones((3, 3)), iterations=2 * UP)
        sil = nd.binary_fill_holes(sil)
        base = sil & cls["branco"]
        out[base] = (*hex2rgb(BASE_INK), 255)
        allr |= sil
    out[~allr] = 0
    img = Image.fromarray(out, "RGBA")
    return img.crop(img.getbbox())


def tee(color, w=900, back=False):
    """Silhueta simples de camiseta oversized (desenho próprio)."""
    h = int(w * 0.90)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = w / 100
    body = [(21, 7), (38, 3), (62, 3), (79, 7), (99, 25), (89, 37), (80, 31), (80, 86),
            (20, 86), (20, 31), (11, 37), (1, 25)]
    d.polygon([(x * s, y * s) for x, y in body], fill=color)
    neck = 6 if not back else 3
    d.ellipse([38 * s, -neck * s, 62 * s, neck * s * 1.4], fill=(0, 0, 0, 0))
    shade = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse([38 * s - 6, -neck * s - 6, 62 * s + 6, neck * s * 1.4 + 6],
                                   outline=(0, 0, 0, 60), width=int(1.2 * s))
    im.alpha_composite(shade)
    return im, s  # s = px por "unidade"; corpo = 58 unidades ≈ 62 cm (oversized G)


def mockup(art, color, cm_w, top_cm, back):
    t, s = tee(color, back=back)
    px_cm = 60 * s / 62
    aw = int(cm_w * px_cm)
    ah = int(art.height * aw / art.width)
    a = art.resize((aw, ah), Image.LANCZOS)
    t.alpha_composite(a, (int(t.width / 2 - aw / 2), int(top_cm * px_cm + 4 * s)))
    return t


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    a, ilu, txt, ramo, frase = prepared()
    tiles = []
    for name, (color, dark, mode) in TEES.items():
        back = colorize(a, {"ilustracao": ilu, "texto": txt, "ramo": ramo}, dark, mode)
        front = colorize(a, {"texto": frase}, dark)
        back.save(os.path.join(outdir, f"costas_{name}.png"))
        front.save(os.path.join(outdir, f"frente_{name}.png"))
        mf = mockup(front, color, FRONT_W_CM, 10, back=False)
        mb = mockup(back, color, 23.2, 8, back=True)
        tiles.append((name, mf, mb))
    W = tiles[0][1].width
    H = tiles[0][1].height
    sheet = Image.new("RGB", (W * 2 + 60, (H + 30) * len(tiles) + 30), "#D9D9D9")
    for i, (name, mf, mb) in enumerate(tiles):
        y = 30 + i * (H + 30)
        sheet.paste(mf, (20, y), mf)
        sheet.paste(mb, (W + 40, y), mb)
    sheet.save(os.path.join(outdir, "mockups_frente_costas.png"))
    for name, mf, mb in tiles:
        pair = Image.new("RGB", (W * 2 + 60, H + 40), "#D9D9D9")
        pair.paste(mf, (20, 20), mf)
        pair.paste(mb, (W + 40, 20), mb)
        pair.save(os.path.join(outdir, f"mockup_{name}.png"))


if __name__ == "__main__":
    main(sys.argv[1])
