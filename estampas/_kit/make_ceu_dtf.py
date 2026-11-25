"""O CÉU NÃO ESQUECE OS SEUS (Mt 6:26) — versão DTF, 28 cm x até 36 cm.

Parte da arte que o cliente gerou (referencia_cliente_chatgpt.webp):
1. separa a ilustração (topo) do bloco de texto (embaixo) por componentes
   conectados — não existe uma linha reta livre entre os dois;
2. reduz o bloco de texto (fator K) para caber em 36 cm de altura;
3. troca a florzinha central do ramo de baixo pela corujinha da marca;
4. vetoriza tudo por separação de cores (vetorizar_cores.py).

uso: python3 make_ceu_dtf.py <saida.svg> [largura_ilustracao_cm]
     (padrão 28: ilustração na largura toda; menor = sobra altura e o texto cresce)
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

from corujinha_art import cm, document, logo_svg
from vetorizar_cores import ORDER, PALETTE, re, separate, trace

SRC = "../o-ceu-nao-esquece/ilustracao/referencia_cliente_chatgpt.webp"
FW, FH = 28.0, 36.0            # quadro (cm): a arte ocupa a largura toda
SPLIT_Y = 900                  # componentes que começam abaixo disso = texto
FLOWER = (501, 1419, 68)       # florzinha central do ramo de baixo (x, y, raio)
OWL_W = 2.3                    # largura da corujinha (x raio da flor)
OVERLAP = 0.05                 # quanto o texto sobe sobre a ilustração (x altura do texto)
NAVY = PALETTE["marinho"][0]


def split(a):
    ink = np.asarray(Image.fromarray(a).convert("L")) < 235
    lab, n = nd.label(ink, structure=np.ones((3, 3)))
    bottom = np.zeros(n + 1, bool)
    for i, s in enumerate(nd.find_objects(lab), 1):
        c = (s[0].start + s[0].stop) / 2
        if s[0].start >= SPLIT_Y or (c >= 888 and s[0].stop - s[0].start < 40):
            bottom[i] = True           # (2ª regra: til do "NÃO" e respingos)
    return (~bottom[lab]) & ink, bottom[lab] & ink


def part(a, mask):
    o = np.full_like(a, 255)
    o[mask] = a[mask]
    ys, xs = np.where(mask)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    return Image.fromarray(o).crop(box), box


def build(out, top_w_cm=FW):
    a = np.array(Image.open(SRC).convert("RGB"))
    tm, bm = split(a)
    # tira a florzinha central de baixo (lugar da corujinha)
    fx, fy, fr = FLOWER
    yy, xx = np.ogrid[:a.shape[0], :a.shape[1]]
    # área limpa em volta da coruja (elipse do tamanho do logo + folga)
    rx, ry = OWL_W * fr / 2 * 1.12, OWL_W * fr / 2 * 951 / 1313 * 1.25
    hole = ((xx - fx) / rx) ** 2 + ((yy - fy) / ry) ** 2 <= 1
    bm &= ~hole
    # some com os pedacinhos de pétala/folha que sobraram em volta da coruja
    near = nd.binary_dilation(hole, iterations=25)
    lab, n = nd.label(bm, structure=np.ones((3, 3)))
    sizes = nd.sum(bm, lab, range(1, n + 1))
    for i, sl in enumerate(nd.find_objects(lab), 1):
        if sizes[i - 1] < 400 and near[sl].any() and (near[sl] & (lab[sl] == i)).any():
            bm[sl][lab[sl] == i] = False
    top, tb = part(a, tm)
    bot, bb = part(a, bm)

    W, H = round(cm(FW)), round(cm(FH))
    tw = round(cm(top_w_cm))
    st = tw / top.width
    th = round(top.height * st)
    k = (H - th) / (bot.height * st * (1 - OVERLAP))   # maior texto que cabe
    k = min(k, W / (bot.width * st))                     # e não passa de 28 cm
    sb = st * k
    bw, bh = round(bot.width * sb), round(bot.height * sb)
    by = th - round(bh * OVERLAP)
    # centro do bloco de texto alinhado como na arte original
    tx = (W - tw) // 2
    bcx = tx + ((bb[0] + bb[2]) / 2 - tb[0]) * st
    bx = round(min(max(bcx - bw / 2, 0), W - bw))
    total_h = by + bh
    oy = (H - total_h) // 2

    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(top.resize((tw, th), Image.LANCZOS), (tx, oy))
    b = bot.resize((bw, bh), Image.LANCZOS)
    bmask = Image.fromarray(np.asarray(b.convert("L")) < 245)
    canvas.paste(b, (bx, oy + by), bmask)

    masks = separate(canvas)
    body = []
    for n in ORDER:
        tr, inner = trace(masks[n], 1, 0, 0)
        inner = re.sub(r'fill="[^"]*"', "", inner)
        body.append(f'<g id="{n}" fill="{PALETTE[n][0]}"><g transform="{tr}">{inner}</g></g>')
    # corujinha no lugar da flor
    ocx = bx + (fx - bb[0]) * sb
    ocy = oy + by + (fy - bb[1]) * sb
    body.append(f'<g id="logo">{logo_svg(ocx, ocy, OWL_W * fr * sb, NAVY)[0]}</g>')
    open(out, "w").write(document("\n".join(body), W, H))
    print(f"K={k:.3f}  arte: {W/300*2.54:.1f} x {total_h/300*2.54:.1f} cm  "
          f"texto: {bw/300*2.54:.1f} cm de largura")


if __name__ == "__main__":
    build(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else FW)
