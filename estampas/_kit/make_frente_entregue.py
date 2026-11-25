"""Frente — "Entregue o seu caminho ao Senhor, confie nele e o mais ele fará."

Quadro 8 x 8 cm a 300 dpi. Diagramação do cliente, 3 linhas, todas com a
MESMA LARGURA (bloco justificado pela tinta real das letras):
    ENTREGUE o seu caminho
    ao Senhor, CONFIE NELE
    E O mais ELE FARÁ.
Letra de forma = Anton caixa alta; letra de mão = Yellowtail.
Frente SEM logo (pedido do cliente, v2).

uso: python3 make_frente_entregue.py <opcao> <saida.svg>
  1 = vermelho só em ENTREGUE e "ao Senhor,"
  2 = igual à 1 + "SL 37:5" pequeno embaixo
  3 = vermelho em todas as palavras de destaque (ENTREGUE, caminho, ao Senhor, mais)
"""
import sys

from corujinha_art import OFFWHITE, RED, Font, Text, cm, document

ANTON = Font("Anton-Regular")
SCRIPT = Font("Yellowtail-Regular")
MONT = Font("Montserrat-600")

W = H = round(cm(8))   # 945 px
ART_W = cm(7.4)        # largura comum de todas as linhas

SCRIPT_RATIO = 1.40    # corpo da letra de mão em relação ao Anton
GAP_RATIO = 0.16       # espaço entre palavras de fontes diferentes (x corpo Anton)
TRACK_A = -10          # tracking levemente negativo, como nas costas
LEAD = 0.55            # espaço entre linhas (x altura de versal da menor linha)


def lines(opt):
    hl = RED if opt == 3 else OFFWHITE   # cor das letras de mão "neutras"
    return [
        [("ENTREGUE", "a", RED), ("O SEU", "a", OFFWHITE), ("caminho", "s", hl)],
        [("ao Senhor,", "s", RED), ("CONFIE NELE", "a", OFFWHITE)],
        [("E O", "a", OFFWHITE), ("mais", "s", hl), ("ELE FARÁ.", "a", OFFWHITE)],
    ]


def make_line(parts, a_size):
    items = []
    for txt, kind, color in parts:
        if kind == "s":
            items.append(Text(SCRIPT, txt, a_size * SCRIPT_RATIO, color))
        else:
            items.append(Text(ANTON, txt, a_size, color, tracking=TRACK_A))
    gap = a_size * GAP_RATIO
    width = sum(t.w for t in items) + gap * (len(items) - 1)
    return items, width, gap


def build(opt: int, out: str):
    b = ANTON.ink("H", 1000)
    cap = (b[3] - b[1]) / 1000
    L = lines(opt)
    sizes = [100 * ART_W / make_line(p, 100)[1] for p in L]
    lead = LEAD * min(sizes) * cap
    total = sum(s * cap for s in sizes) + lead * (len(L) - 1)
    sig_gap, sig_cap = cm(0.6), cm(0.30)
    if opt == 2:
        total += sig_gap + sig_cap
    y = (H - total) / 2
    x0 = (W - ART_W) / 2

    body = []
    for parts, s in zip(L, sizes):
        items, _, gap = make_line(parts, s)
        baseline = y + s * cap
        x = x0
        for t in items:
            t.place(left=x)
            t.dy = baseline
            x += t.w + gap
            body.append(t.svg())
        y = baseline + lead

    if opt == 2:
        y = y - lead + sig_gap
        mb = MONT.ink("SL 37:5", 1000)
        msize = 1000 * sig_cap / (mb[3] - mb[1])
        sig = Text(MONT, "SL 37:5", msize, OFFWHITE, tracking=320)
        sig.place(cx=W / 2, top=y)
        body.append(sig.svg())

    open(out, "w").write(document("\n".join(body), W, H))


if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2])
