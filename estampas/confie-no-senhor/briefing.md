# Estampa "CONFIE NO SENHOR" — status: APROVADA (v3, opção 2)

Estampa de costas para camiseta preta oversized. Recriação de uma referência ("TRUST YOUR DENTIST", com "always" em cursiva vermelha atravessando o texto e a assinatura "✦ DENTORALL ✦" embaixo), trocando as palavras.

## Especificação final

| Elemento | Definição |
|---|---|
| Texto principal | 2 linhas com a **mesma largura** (bloco justificado): `CONFIE` / `NO SENHOR` |
| Fonte principal | Anton, caixa alta, entrelinha curta (44 px entre linhas), tracking levemente negativo |
| Cursiva | "Jesus Saves" em Yellowtail, vermelho `#C83438`, inclinada −9° subindo para a direita, 82% da largura do bloco, atravessando a emenda entre as linhas, sem contorno |
| Assinatura | "SL 37:05" em Montserrat 500, bem espaçada, com uma corujinha (logo) de cada lado no lugar das ✦ — cada coruja ≈ 1,4 cm de largura |
| Cores | Texto e logos off-white `#EFE8D8`; cursiva `#C83438`; camiseta preta |
| Quadro | 27 × 32 cm, 300 dpi (3189 × 3780 px); arte ≈ 24,5 × 16,5 cm centralizada |
| Posição na peça | Topo da arte 8–10 cm abaixo da gola |

## Arquivos entregues

- `ConfieNoSenhor_final.png` — fundo transparente, 300 dpi  *(PENDENTE: subir nesta pasta)*
- `ConfieNoSenhor_final.svg` — 270 × 320 mm, texto em curvas, abre no Illustrator sem as fontes ✅
- `previa_v3_aprovada.png` — prévia da v3 renderizada sobre preto ✅

## Histórico das decisões

1. **v1** — três linhas (CONFIE / N O / SENHOR), com N à esquerda, O à direita e a cursiva passando pelo vão. Testadas três cursivas: Mrs Saint Delafield, Yellowtail e Allura. Mrs Saint Delafield e Allura ganharam contorno da mesma cor (11 e 9 px) porque os traços finos sumiriam na estampa.
2. **v2** — texto em duas linhas (CONFIE / NO SENHOR), logo pequeno embaixo da assinatura.
3. **v3** — as estrelas viraram corujinhas ao lado do versículo; o logo de baixo saiu. Escolhida a **opção 2 (Yellowtail)**.

## Pontos de atenção

- **Serigrafia:** avaliar aumentar as corujinhas — com ~1,4 cm as escamas podem fechar na tela.

## v4 — versículo mais grosso (entregue)

- "SL 37:05" refeito em **Montserrat 600** (antes 500), mesma altura, largura e posição; corujas intactas.
- `ConfieNoSenhor_costas_final_v4.svg` (270 × 320 mm, curvas) + `ConfieNoSenhor_costas_final_v4.png` (transparente, 300 dpi).
- Alternativa mais grossa: `ConfieNoSenhor_costas_final_v4_versiculo700.svg` (Montserrat 700).
- Gerar de novo: `python3 _kit/make_costas_versiculo.py <500|600|700> <saida.svg>` (rodar dentro de `_kit/`).
