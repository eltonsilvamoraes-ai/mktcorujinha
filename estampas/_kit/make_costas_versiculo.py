"""Costas CONFIE NO SENHOR: refaz só o versículo com peso maior.

Mantém altura, largura total e posição do "SL 37:05" aprovado; só troca o
peso da Montserrat (500 -> 600/700). Corujas e resto da arte intactos.

uso: python3 make_costas_versiculo.py <peso> <saida.svg>
"""
import re
import sys

from corujinha_art import Font, OFFWHITE

SRC = "../confie-no-senhor/ConfieNoSenhor_final.svg"
# tinta do versículo na v3 aprovada (coordenadas do grupo)
X0, Y0, X1, Y1 = 1274.6, 1853.4, 1914.4, 1919.2


def build(weight: int, out: str):
    svg = open(SRC).read()
    f = Font(f"Montserrat-{weight}")
    b = f.ink("SL 37:05", 1000)
    size = 1000 * (Y1 - Y0) / (b[3] - b[1])
    tr = f.fit_tracking("SL 37:05", size, X1 - X0)
    _, ink = f.layout("SL 37:05", size, tr)
    d, _ = f.layout("SL 37:05", size, tr, X0 - ink[0], Y1 - ink[3])
    paths = list(re.finditer(r'<path fill="#EFE8D8" d="[^"]+"/>', svg))
    verse = paths[2]  # 3º path off-white sem transform = versículo
    new = f'<path fill="{OFFWHITE}" d="{d}"/>'
    open(out, "w").write(svg[:verse.start()] + new + svg[verse.end():])


if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2])
