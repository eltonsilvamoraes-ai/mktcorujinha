"""Frente — "Entregue o seu caminho ao Senhor, confie nele e o mais ele fará."

Quadro 8 x 8 cm a 300 dpi, sem logo (pedido do cliente). Disposição aprovada
(v3), 3 linhas todas com a MESMA LARGURA (bloco justificado pela tinta):
    Entregue  O SEU CAMINHO
    ao Senhor, CONFIE NELE
    E O MAIS ELE FARÁ.
Vermelho só em "Entregue" e "ao Senhor," (letra de mão); resto em letra de
forma off-white.

uso: python3 make_frente_entregue.py <saida.svg> [fonte_mao] [fonte_forma] [tracking]
     (padrão: Yellowtail-Regular + Anton-Regular, a v3)
"""
import sys

from corujinha_art import OFFWHITE, RED, Font, Text, cm, document

W = H = round(cm(8))   # 945 px
ART_W = cm(7.4)        # largura comum de todas as linhas

LINES = [
    [("Entregue", "s", RED), ("O SEU CAMINHO", "a", OFFWHITE)],
    [("ao Senhor,", "s", RED), ("CONFIE NELE", "a", OFFWHITE)],
    [("E O MAIS ELE FARÁ.", "a", OFFWHITE)],
]
GAP_RATIO = 0.16       # espaço entre a letra de mão e a de forma (x corpo)
LEAD = 0.72            # espaço entre linhas (x altura de versal da menor linha)
_REF = None


def cap_h(font, ch="H"):
    b = font.ink(ch, 1000)
    return (b[3] - b[1]) / 1000


def script_ratio(script, block):
    """Mantém a relação da v3 (Yellowtail 1,40 x Anton) entre o "E" da
    letra de mão e a versal da letra de forma, para qualquer par de fontes."""
    global _REF
    if _REF is None:
        y, a = Font("Yellowtail-Regular"), Font("Anton-Regular")
        _REF = 1.40 * cap_h(y, "E") / cap_h(a)
    return _REF * cap_h(block) / cap_h(script, "E")


def build(out, script_name="Yellowtail-Regular", block_name="Anton-Regular",
          track=-10):
    script, block = Font(script_name), Font(block_name)
    ratio = script_ratio(script, block)
    cap = cap_h(block)

    def make_line(parts, size):
        items = []
        for txt, kind, color in parts:
            if kind == "s":
                items.append(Text(script, txt, size * ratio, color))
            else:
                items.append(Text(block, txt, size, color, tracking=float(track)))
        gap = size * GAP_RATIO
        return items, sum(t.w for t in items) + gap * (len(items) - 1), gap

    sizes = [100 * ART_W / make_line(p, 100)[1] for p in LINES]
    lead = LEAD * min(sizes) * cap
    total = sum(s * cap for s in sizes) + lead * (len(LINES) - 1)
    y = (H - total) / 2
    x0 = (W - ART_W) / 2

    body = []
    for parts, s in zip(LINES, sizes):
        items, _, gap = make_line(parts, s)
        baseline = y + s * cap
        x = x0
        for t in items:
            t.place(left=x)
            t.dy = baseline
            x += t.w + gap
            body.append(t.svg())
        y = baseline + lead

    open(out, "w").write(document("\n".join(body), W, H))


if __name__ == "__main__":
    build(*sys.argv[1:])
