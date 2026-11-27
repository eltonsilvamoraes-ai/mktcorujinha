"""ROMANOS 8:31 v2 — paisagem estilizada (estilo badge "Pine & Peak").

Textos tirados da arte do cliente (arco "SE DEUS É POR NÓS", cursiva
"Quem será contra nós?", linha "ROMANOS 8:31"); a paisagem do meio é a nova
ilustração gerada no Figma (sol + montanha + pinheiros + lago + cruz + águia),
em 2 tintas. Leve desgaste vintage.

uso: python3 make_rm831_v2.py <versao> <saida.png>
  off   = camiseta off-white: paisagem/arco marinho, sol + cursiva telha
  preta = camiseta preta: paisagem/arco creme, sol + cursiva telha
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

SRC = "../romanos-8-31/referencias/arte_cliente.webp"
ILU = "../romanos-8-31/ilustracao/paisagem_v1_figma.png"
UP = 3
SUN_CY, SUN_R = 485, 284       # círculo do sol na arte original (px)
SCRIPT_TOP = 578               # topo do "Quem será" (px)

V = {
    "off": dict(tee=(237, 230, 214), main=(31, 42, 68), accent=(194, 72, 47)),
    "preta": dict(tee=(20, 20, 20), main=(236, 228, 210), accent=(196, 98, 72)),
}


def text_masks():
    src = Image.open(SRC).convert("RGBA")
    big = src.resize((src.width * UP, src.height * UP), Image.LANCZOS)
    raw = np.asarray(big).astype(int)
    r, g, b, al = raw[..., 0], raw[..., 1], raw[..., 2], raw[..., 3]
    H, W = al.shape
    yy, xx = np.mgrid[0:H, 0:W]
    # ARCO: texto semitransparente na arte -> cor pura + alpha
    beige_a = (r > 150) & (r - b > 35) & (r - b < 120) & (g > 120) & (al > 40)
    cx = 372 * UP
    outside = (xx - cx) ** 2 + (yy - SUN_CY * UP) ** 2 > ((SUN_R + 8) * UP) ** 2
    arc = beige_a & outside & (yy < 330 * UP)
    # CURSIVA + REFERÊNCIA: sobre branco (como na v1)
    wb = Image.new("RGBA", big.size, "white"); wb.alpha_composite(big)
    a = np.asarray(wb.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    beige = (r > 165) & (r - b > 40) & (r - b < 115) & (g > 135)
    band = beige & (yy > SCRIPT_TOP * UP) & (yy < 945 * UP)
    lab, n = nd.label(band, np.ones((3, 3)))
    script = np.zeros_like(band)
    for i, sl in enumerate(nd.find_objects(lab), 1):
        if sl[0].stop <= 615 * UP:          # névoa/neve só existe no topo da faixa
            continue
        # restos de pinheiros/neve entre "Quem" e "será" (topo alto, peça pequena)
        area = (lab[sl] == i).sum()
        if sl[0].start < 650 * UP and 300 * UP < sl[1].start < 600 * UP and area < 1500 * UP * UP:
            continue
        script[sl] |= lab[sl] == i
    for m in (arc,):
        lab, n = nd.label(m, np.ones((3, 3)))
        sz = nd.sum(m, lab, range(1, n + 1))
        m &= np.isin(lab, np.where(sz > 30 * UP)[0] + 1)
    return arc, script, (H, W)


def build(ver, out):
    c = V[ver]
    arc, script, (H, W) = text_masks()
    ilu = np.asarray(Image.open(ILU).convert("RGB")).astype(int)
    r, g, b = ilu[..., 0], ilu[..., 1], ilu[..., 2]
    red = (r > 150) & (r - b > 90) & (g < 150)
    navy = (ilu.max(axis=2) < 140) & ~red
    # coloca a paisagem no lugar da original (largura ~ do sol original + pinheiros)
    tw = int(690 * UP)
    th = int(ilu.shape[0] * tw / ilu.shape[1])
    def rs(m):
        return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((tw, th), Image.LANCZOS)) > 127
    red, navy = rs(red), rs(navy)
    lab, n = nd.label(navy | red, np.ones((3, 3)))
    sz = nd.sum(navy | red, lab, range(1, n + 1))
    small = np.isin(lab, np.where(sz < 60 * UP * UP)[0] + 1)
    # remove só manchas soltas grandes demais p/ ser pássaro e longe do centro (folha perdida)
    ys, xs = np.mgrid[0:lab.shape[0], 0:lab.shape[1]]
    stray = small & (xs > 0.9 * lab.shape[1]) & (ys < 0.2 * lab.shape[0])
    navy &= ~stray; red &= ~stray
    ox = (W - tw) // 2
    oy = int(205 * UP) - int(th * 0.09)
    out_img = np.zeros((H, W, 3), np.uint8); out_img[:] = c["tee"]
    def put(m, col, x, y):
        h, w = m.shape
        ys, xs = slice(max(y, 0), min(y + h, H)), slice(max(x, 0), min(x + w, W))
        mm = m[ys.start - y:ys.stop - y, xs.start - x:xs.stop - x]
        reg = out_img[ys, xs]; reg[mm] = col
    put(red, c["accent"], ox, oy)
    put(navy, c["main"], ox, oy)
    # a cursiva começa logo abaixo do lago: desloca os textos de baixo
    lake_bottom = oy + int(np.where(navy.any(1))[0].max())
    st = np.where(script.any(1))[0].min()
    dy = lake_bottom + int(14 * UP) - st
    sc = np.zeros_like(script); 
    if dy >= 0: sc[dy:] = script[:H - dy]
    else: sc[:H + dy] = script[-dy:]
    out_img[arc] = c["main"]
    out_img[sc] = c["accent"]
    # desgaste leve
    rng = np.random.default_rng(4)
    ink = (out_img != np.array(c["tee"], np.uint8)).any(2)
    noise = rng.random((H, W))
    out_img[ink & (noise > 0.985)] = c["tee"]
    used = np.where(ink.any(1))[0]
    Image.fromarray(out_img[max(used.min() - 60, 0):used.max() + 60]).save(out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
