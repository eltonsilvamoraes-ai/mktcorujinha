# Estampas — A Marca da Corujinha

Pasta de criação de estampas (arte de camiseta) da marca.

## Regras de trabalho (sempre)

1. **Prévia antes de produção.** Fechar a arte só com prévias: imagens individuais e grandes, uma por opção, recortadas na área da arte. O PNG e o SVG de produção só são gerados depois da aprovação.
2. **Sempre o logo da coruja** (cabeça de coruja estilizada) nas estampas da marca — exceto quando o cliente dispensar (ex.: frente "Entregue o seu caminho", sem logo).
3. Paleta padrão em camiseta preta: off-white `#EFE8D8` (texto e logo), vermelho `#C83438` (cursiva/destaque).
4. **Entrega sempre dentro de uma pasta** com o nome da estampa (ex.: `entregas/Salmos 37-05/`), enviada também como `.zip`. Usar hífen no lugar de ":" no nome (o ":" é proibido em nomes de pasta no Windows e no Mac).
5. Quadro de produção: 27 × 32 cm a 300 dpi (3189 × 3780 px), PNG com fundo transparente + SVG 270 × 320 mm com texto em curvas.

## Estrutura

```
estampas/
├── README.md                ← este arquivo
├── _kit/                    ← pipeline reutilizável (scripts, logo, fontes)
│   ├── make_art.py          ← funções base (Font, star)        [PENDENTE: subir]
│   ├── make_art3.py         ← layout final; build(..., final=True) [PENDENTE: subir]
│   ├── logo_coruja.svg      ← logo vetorizado (preto, evenodd, viewBox 1313×951) ✅
│   ├── vetorizar_logo.py    ← PNG → SVG (potracer, upscale 3×, máscara invertida + borda 20 px) ✅
│   ├── logo-original/       ← PNG/JPG originais do logo + prévia off-white na camiseta preta ✅
│   └── fonts/               ← Anton, Yellowtail, Montserrat… (via npm @fontsource)
└── confie-no-senhor/        ← briefing e arquivos finais de cada estampa
```

## Pipeline (resumo)

- **Fontes:** pacotes npm `@fontsource/anton`, `yellowtail`, `montserrat`, `allura`, `mrs-saint-delafield` (mesmos arquivos do Google Fonts).
- **Python:** `fontTools` extrai os contornos das letras em vetor; `uharfbuzz` aplica o kerning.
- **Largura das linhas** ajustada pela tinta real das letras (não pelo avanço), para as bordas do bloco justificado alinharem exatamente.
- **Render PNG:** `rsvg-convert` (ou `cairosvg` como alternativa).
- **Logo:** vetorizado do PNG com `potracer`. Atenção: no potracer a máscara sai invertida — traçar a área branca (g >= 128) com borda de 20 px em volta.
- **Nova estampa:** copiar `make_art3.py`, trocar os textos, gerar prévia → aprovar → `final=True`.
