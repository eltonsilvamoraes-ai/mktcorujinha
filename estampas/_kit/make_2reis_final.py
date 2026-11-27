"""NÃO TEMAS (2 Reis 6:15-17) — arquivos finais vetorizados (DTF, chapado).

COSTAS (v9 aprovada) e FRENTE (só "Não temas", opção 2 = palavras separadas),
para camiseta PRETA e OFF-WHITE. Cores em camadas separadas (um <g> por parte
x cor, com id legível), como na MT 6:26:
  - ILUSTRACAO   (cores da gravura; na preta o preto NÃO é tinta = tecido)
  - TITULO       ("Não temas", 1 cor, textura gasta vetorizada)
  - PICO_FRENTE  (ponta do monte que passa por cima do título)
  - RODAPE       (versículo + referência)
Na off-white a ilustração ganha a camada "preto" (base preta granulada).

uso: python3 make_2reis_final.py <pasta_saida>
"""
import os
import sys

import numpy as np
from PIL import Image

import make_2reis as m
import make_2reis_frente as fr
from corujinha_art import document, render
from vetorizar_cores import re, to_lab, trace

INKS = [  # nome, cor da tinta (amostra = mesma cor)
    ("preto", "#0B0B0B"),
    ("marrom", "#4C3630"),
    ("cinza", "#6A675F"),
    ("azul", "#6A98B2"),
    ("vermelho", "#A84B3A"),
    ("dourado", "#E0A53C"),
    ("bege", "#C4AB86"),
    ("creme", "#E3D2B0"),
]
VERSIONS = {  # nome: (título, rodapé, tecido da prévia, base preta?)
    "PRETA": ("#ECE29A", m.CREAM, "#151515", False),
    "OFFWHITE": ("#C83438", "#1A1A1A", "#EDE6D6", True),
}


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def layers(rgba, ox, oy, part, include_black):
    a = np.asarray(rgba)
    on = a[..., 3] > 110
    lab = to_lab(a[..., :3].reshape(-1, 3).astype(float))
    ref = to_lab(np.array([rgb(c) for _, c in INKS], float))
    idx = ((lab[:, None] - ref[None]) ** 2).sum(-1).argmin(1).reshape(on.shape)
    out = []
    for k, (name, ink) in enumerate(INKS):
        if name == "preto" and not include_black:
            continue
        msk = on & (idx == k)
        if msk.sum() < 30:
            continue
        tr, inner = trace(msk, 1, 0, 0)
        inner = re.sub(r'fill="[^"]*"', "", inner)
        out.append(f'  <g id="{part}__{name}_{ink[1:]}" fill="{ink}" transform="translate({ox} {oy})">'
                   f'<g transform="{tr}">{inner}</g></g>')
    return out


def mono(mask_img, color, gid):
    msk = np.asarray(mask_img)[..., 3] > 128
    tr, inner = trace(msk, 1, 0, 0)
    inner = re.sub(r'fill="[^"]*"', "", inner)
    return f'  <g id="{gid}" fill="{color}"><g transform="{tr}">{inner}</g></g>'


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for ver, (tcol, fcol, tee, base) in VERSIONS.items():
        # ---------------- COSTAS ----------------
        m.build_v4("/dev/null", color=tcol, bg=None, base=base, text=fcol)
        L = m.LAST
        front_mask = np.asarray(L["front"])[..., 3] > 0
        back = np.array(L["rgba"]); back[front_mask, 3] = 0
        from scipy import ndimage as nd
        pico = np.array(L["rgba"]); pico[~nd.binary_dilation(front_mask, iterations=3), 3] = 0  # sobreposição: sem fresta
        body = ['<g id="ILUSTRACAO">'] + layers(Image.fromarray(back), L["ix"], L["iy"], "ilustracao", base) + ["</g>"]
        body += ['<g id="TITULO">', mono(L["tex"], tcol, f"titulo_{tcol[1:]}"), "</g>"]
        body += ['<g id="PICO_FRENTE">'] + layers(Image.fromarray(pico), L["ix"], L["iy"], "pico", base) + ["</g>"]
        foot = [re.sub(r'fill="[^"]*"', "", p, count=1) for p in L["footer"]]
        body += [f'<g id="RODAPE" fill="{fcol}">'] + foot + ["</g>"]
        svg = document("\n".join(body), m.W, m.H)
        name = f"2REIS6-15-17_COSTAS_{ver}"
        open(os.path.join(outdir, name + ".svg"), "w").write(svg)
        render(svg, os.path.join(outdir, name + ".png"), width=m.W)
        render(svg, os.path.join(outdir, f"_previa_{name}.png"), width=1100, bg=tee)

        # ---------------- FRENTE ----------------
        tex = fr.build(2, tcol, "/dev/null")
        svg = document(mono(tex, tcol, f"texto_{tcol[1:]}").replace("  <g id", '<g id', 1), tex.width, tex.height)
        svg = svg.replace('<g id="texto', '<g id="TEXTO"><g id="texto', 1).replace("</svg>", "</g>\n</svg>")
        name = f"2REIS6-15-17_FRENTE_{ver}"
        open(os.path.join(outdir, name + ".svg"), "w").write(svg)
        render(svg, os.path.join(outdir, name + ".png"), width=tex.width)
        render(svg, os.path.join(outdir, f"_previa_{name}.png"), width=tex.width, bg=tee)
        print(ver, "ok")


if __name__ == "__main__":
    main(sys.argv[1])
