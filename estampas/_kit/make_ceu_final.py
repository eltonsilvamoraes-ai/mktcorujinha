"""O CÉU NÃO ESQUECE OS SEUS (Mt 6:26) — arquivos finais vetorizados (DTF).

COSTAS: arte v6 (pássaro e texto na proporção original), quadro 28 x 36 cm,
        arte ~23,2 x 36 cm centralizada.
FRENTE: só a frase "O CÉU NÃO / ESQUECE / OS SEUS", 10 cm de largura.

Cores em CAMADAS SEPARADAS para o cliente trocar depois: um <g> por
parte (ilustracao / texto / ramo) x cor, com id legível no Illustrator/Corel,
ex.: "texto__marinho_0B2540". Cores originais (camiseta clara).

uso: python3 make_ceu_final.py <pasta_saida>
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

from corujinha_art import cm, document, render
from make_ceu_mockups import prepared
from vetorizar_cores import ORDER, PALETTE, re, separate, trace

INTERNAL = 3          # traça a frente em 3x e reduz (curvas mais lisas)
# cores permitidas por parte (o resto é borda suavizada/textura e vai para a
# cor permitida mais próxima; "branco" = sem tinta)
ALLOWED = {
    "ilustracao": ["branco", "marinho", "vermelho", "creme", "azul", "laranja"],
    "texto": ["branco", "marinho", "vermelho"],
    "ramo": ["branco", "marinho", "vermelho", "creme", "azul"],
}


def separate_in(canvas, allowed):
    """Como vetorizar_cores.separate, mas só com as cores permitidas."""
    from vetorizar_cores import EXTRA, hex2rgb, to_lab
    names, samples = [], []
    for n in allowed:
        names.append(n); samples.append(hex2rgb(PALETTE[n][1]))
        for e in EXTRA.get(n, []):
            names.append(n); samples.append(hex2rgb(e))
    arr = np.asarray(canvas, dtype=float)
    h, w, _ = arr.shape
    lab = to_lab(arr.reshape(-1, 3))
    ref = to_lab(np.array(samples, dtype=float))
    idx = ((lab[:, None, :] - ref[None, :, :]) ** 2).sum(-1).argmin(1).reshape(h, w)
    return {n: np.isin(idx, [i for i, m in enumerate(names) if m == n]) for n in allowed}


def layered(canvas, labels, names, scale=1.0):
    """Um <g> por região x cor. labels: int por pixel (0 = nada)."""
    # pixel de tinta fora de qualquer região (borda/antialias) -> região mais próxima
    idx = nd.distance_transform_edt(labels == 0, return_distances=False, return_indices=True)
    lab = labels[idx[0], idx[1]]
    out = []
    for ri, rname in enumerate(names, 1):
        groups = []
        sel = lab == ri
        ys, xs = np.where(sel)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        cls = separate_in(canvas.crop((x0, y0, x1, y1)), ALLOWED[rname])
        for n in ORDER:
            if n not in cls:
                continue
            m = np.zeros(sel.shape, bool)
            m[y0:y1, x0:x1] = cls[n] & sel[y0:y1, x0:x1]
            if m.sum() < 20:
                continue
            ink = PALETTE[n][0]
            tr, inner = trace(m, 1, 0, 0)
            inner = re.sub(r'fill="[^"]*"', "", inner)
            gid = f"{rname}__{n}_{ink[1:]}"
            groups.append(f'  <g id="{gid}" fill="{ink}"><g transform="{tr}">{inner}</g></g>')
        tf = f' transform="scale({scale:.6f})"' if scale != 1 else ""
        out.append(f'<g id="{rname.upper()}"{tf}>\n' + "\n".join(groups) + "\n</g>")
    return "\n".join(out)


def place(a, regions, box, size_px, frame_px):
    """Recorta box, escala para size_px e centraliza no quadro; devolve canvas+labels."""
    x0, y0, x1, y1 = box
    keep = np.zeros(a.shape[:2], bool)
    for m in regions:
        keep |= m
    # tudo que não pertence às partes pedidas vira branco (sem tinta); uma
    # folga de 2 px preserva a borda suavizada das letras
    keep = nd.binary_dilation(keep, iterations=2)
    a = a.copy()
    a[~keep] = 255
    im = Image.fromarray(a[y0:y1, x0:x1])
    aw, ah = size_px
    W, H = frame_px
    ox, oy = (W - aw) // 2, (H - ah) // 2
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(im.resize((aw, ah), Image.LANCZOS), (ox, oy))
    lab = np.zeros((y1 - y0, x1 - x0), np.uint8)
    for i, m in enumerate(regions, 1):
        lab[m[y0:y1, x0:x1]] = i
    L = np.zeros((H, W), np.uint8)
    L[oy:oy + ah, ox:ox + aw] = np.array(Image.fromarray(lab).resize((aw, ah), Image.NEAREST))
    # ink que caiu fora das regiões (ex.: branco do source) fica 0; tinta clara
    return canvas, L


def bbox(mask):
    ys, xs = np.where(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    a, ilu, txt, ramo, frase = prepared()
    # partes para edição: texto = frase + "MT 6:26"; ramo = raminho de baixo inteiro
    rows = np.arange(a.shape[0])[:, None]
    baixo = (txt | ramo) & (rows >= 880)
    ramo = baixo & ~frase
    txt = (txt | ramo) & ~ramo

    # ---------- COSTAS 28 x 36 ----------
    allm = ilu | txt | ramo
    box = bbox(allm)
    W, H = round(cm(28)), round(cm(36))
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(W / bw, H / bh)
    canvas, L = place(a, [ilu, txt, ramo], box, (round(bw * s), round(bh * s)), (W, H))
    body = layered(canvas, L, ["ilustracao", "texto", "ramo"])
    svg = document(body, W, H)
    open(os.path.join(outdir, "MT6-26_COSTAS.svg"), "w").write(svg)
    render(svg, os.path.join(outdir, "MT6-26_COSTAS.png"), width=W)
    print(f"costas: arte {bw*s/300*2.54:.1f} x {bh*s/300*2.54:.1f} cm no quadro 28 x 36")

    # ---------- FRENTE 10 cm ----------
    box = bbox(frase)
    bw, bh = box[2] - box[0], box[3] - box[1]
    fw = round(cm(10))
    fh = round(bh * fw / bw)
    k = INTERNAL
    canvas, L = place(a, [frase], box, (fw * k, fh * k), (fw * k, fh * k))
    body = layered(canvas, L, ["texto"], scale=1 / k)
    svg = document(body, fw, fh)
    open(os.path.join(outdir, "MT6-26_FRENTE.svg"), "w").write(svg)
    render(svg, os.path.join(outdir, "MT6-26_FRENTE.png"), width=fw)
    print(f"frente: {fw/300*2.54:.1f} x {fh/300*2.54:.1f} cm")


if __name__ == "__main__":
    main(sys.argv[1])
