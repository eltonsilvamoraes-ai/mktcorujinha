# Landing Page — Corujinha Merch

Página de entrada do motor MERCH: produtos personalizados para igrejas, congressos, ministérios, artistas, criadores e empresas. Foco inicial em camisetas. CTA único: WhatsApp com mensagem pronta.

- `index.html` — página-fonte (busca as fotos em `imagens/`)
- `corujinha-merch.html` — versão única para baixar/abrir, com as fotos embutidas. Gerada por `python3 merch/build.py` (rodar sempre que mudar o `index.html` ou as fotos).
- Página completa (direção visual "Fogo": Brasa, Barro, Osso, Breu; Bricolage Grotesque + Hanken Grotesk).
- `imagens/logo-coruja.png` — logo original. `imagens/logo-coruja.svg` — versão vetorial (cor via `currentColor`).
- Publicada como Artifact: https://claude.ai/artifact/SnAmudHYM7eZjvBL3g8PMb

## Ordem das seções (fundo)
1. Topo — "Sua mensagem merece ser vestida." + botões "Contar meu projeto" e "O que produzimos" (Brasa)
2. Faixa de perfis correndo (Breu)
3. Para quem carrega uma mensagem (Osso)
4. O que produzimos — ícones: camisetas, moletons, bonés, jaquetas, ecobags (Brasa)
5. Da ideia à entrega — 5 etapas + Produção / Criação de desenhos (Osso)
6. A camiseta que a gente faz — modelagem, gola, estampa, costura, tecido (Breu)
7. Por que a Corujinha — "Onde muitos enxergavam apenas roupas..." + Marca / Indústria / Merch (Brasa)
8. Perguntas frequentes (Osso)
9. Fechamento com WhatsApp (Brasa)

A seção "Projetos já realizados" foi retirada (sem fotos de trabalhos para terceiros por enquanto).

## A confirmar / pendente
- Fotos reais para todos os espaços marcados "Foto: ..." (enviar como arquivo anexo).
- Número de WhatsApp do comercial (usei 55 12 3933-9065, o mesmo da landing da fábrica).
- Técnicas de estampa usadas (silk, DTF, etc.) e gramatura da malha, para detalhar a seção da camiseta.
- Quantidade mínima e prazo médio, se quiserem cravar na seção de perguntas.

## Como trocar as fotos
Coloque a foto na pasta `imagens/`, ao lado do HTML, com o nome exato abaixo (`.jpg`, `.jpeg`, `.png` ou `.webp`). A página encontra sozinha; sem o arquivo, aparece o espaço com a coruja.

| Arquivo | Onde aparece |
|---|---|
| `fundo-topo` | Fundo da área vermelha do topo (fica coberto por um véu Brasa para o texto continuar legível) |
| `hero` | Foto grande do topo |
| `modelagem` | Pessoa vestindo, corpo inteiro |
| `gola`, `estampa`, `costura` | Detalhes da camiseta |

Para ajustar o enquadramento de uma foto, acrescente `data-pos="center top"` (ou `"50% 30%"`) no elemento que tem o `data-img` correspondente.
