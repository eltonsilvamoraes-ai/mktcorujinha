"""Frente — "Entregue o seu caminho ao Senhor, confie nele e o mais ele fará."

Quadro 8 x 8 cm a 300 dpi. Diagramação em 3 linhas como o cliente mandou:
    Entregue o seu caminho
    ao Senhor, confie nele
    e o mais ele fará.
Trechos em vermelho (cursiva Yellowtail): "Entregue" e "ao Senhor,".
Resto em Anton caixa alta off-white (mesma família das costas).
Assinatura "SL 37:5" em Montserrat com corujinhas nas pontas (ecoa as costas).

uso: python3 make_frente_entregue.py <opcao> <saida.svg>
  opcao 1 = linhas centralizadas, mesmo corpo
  opcao 2 = bloco justificado (todas as linhas com a mesma largura, como nas costas)
  opcao 3 = centralizado, coruja grande em cima, sem assinatura
"""
import sys

from corujinha_art import (OFFWHITE, RED, Font, Text, cm, document, logo_svg)

ANTON = Font("Anton-Regular")
SCRIPT = Font("Yellowtail-Regular")
MONT = Font("Montserrat-600")

W = H = round(cm(8))           # 945 px
ART_W = cm(7.4)                # largura útil da arte

LINES = [
    [("Entregue", "s"), ("O SEU CAMINHO", "a")],
    [("ao Senhor,", "s"), ("CONFIE NELE", "a")],
    [("E O MAIS ELE FARÁ.", "a")],
]
SCRIPT_RATIO = 1.45   # corpo da cursiva em relação ao Anton
GAP_RATIO = 0.20      # espaço entre cursiva e Anton (x corpo Anton)
TRACK_A = -10         # tracking levemente negativo, como nas costas


def make_line(parts, a_size):
    items = []
    for txt, kind in parts:
        if kind == "s":
            items.append(Text(SCRIPT, txt, a_size * SCRIPT_RATIO, RED, skew=0))
        else:
            items.append(Text(ANTON, txt, a_size, OFFWHITE, tracking=TRACK_A))
    gap = a_size * GAP_RATIO
    width = sum(t.w for t in items) + gap * (len(items) - 1)
    return items, width, gap


def lay_line(items, gap, cx, width, baseline):
    x = cx - width / 2
    for t in items:
        t.place(left=x)
        t.dy = baseline
        x += t.w + gap
    return items


def build(opt: int, out: str):
    body = []
    cx = W / 2
    cap = 0.735  # altura de versal do Anton por corpo (medida abaixo)
    b = ANTON.ink("H", 1000)
    cap = (b[3] - b[1]) / 1000

    # corpo do Anton por linha
    if opt == 2:
        sizes = []
        for parts in LINES:
            _, w1, _ = make_line(parts, 100)
            sizes.append(100 * ART_W / w1)
    else:
        widest = max(make_line(p, 100)[1] for p in LINES)
        s = 100 * ART_W / widest
        sizes = [s] * len(LINES)

    lead = 0.62  # espaço entre linhas (x altura de versal): folga para as hastes da cursiva
    total = sum(s * cap for s in sizes) + lead * sizes[0] * cap * (len(LINES) - 1)

    sig_h = 0
    if opt in (1, 2):
        sig_h = cm(0.75) + cm(0.45)   # espaço + altura da assinatura
    top_logo = cm(2.1) if opt == 3 else 0
    logo_gap = cm(0.6) if opt == 3 else 0
    block = top_logo + logo_gap + total + sig_h
    y = (H - block) / 2

    if opt == 3:
        d, lh = logo_svg(cx, y + top_logo / 2, top_logo * 1313 / 951)
        body.append(d)
        y += top_logo + logo_gap

    for parts, s in zip(LINES, sizes):
        items, width, gap = make_line(parts, s)
        baseline = y + s * cap
        for t in lay_line(items, gap, cx, width, baseline):
            body.append(t.svg())
        y = baseline + lead * sizes[0] * cap

    if opt in (1, 2):
        y = y - lead * sizes[0] * cap + cm(0.75)
        sig_cap = cm(0.30)
        mb = MONT.ink("SL 37:5", 1000)
        msize = 1000 * sig_cap / (mb[3] - mb[1])
        sig = Text(MONT, "SL 37:5", msize, OFFWHITE, tracking=320)
        sig.place(cx=cx, top=y)
        body.append(sig.svg())
        owl_w = cm(0.9)
        sb = sig.box()
        cy = (sb[1] + sb[3]) / 2
        for ox in (sb[0] - cm(0.25) - owl_w / 2, sb[2] + cm(0.25) + owl_w / 2):
            body.append(logo_svg(ox, cy, owl_w)[0])

    open(out, "w").write(document("\n".join(body), W, H))


if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2])
