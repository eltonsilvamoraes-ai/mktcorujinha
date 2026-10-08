# Landing Page — Corujinha Merch

Página de entrada do motor MERCH: produtos personalizados para igrejas, congressos, ministérios, artistas, criadores e empresas. Foco inicial em camisetas. CTA único: WhatsApp com mensagem pronta.

- `index.html` — página completa e autocontida (direção visual "Fogo": Brasa, Barro, Osso, Breu; Bricolage Grotesque + Hanken Grotesk).
- `imagens/logo-coruja.png` — logo original. `imagens/logo-coruja.svg` — versão vetorial (cor via `currentColor`).
- Publicada como Artifact: https://claude.ai/artifact/SnAmudHYM7eZjvBL3g8PMb

## Ordem das seções (fundo)
1. Topo — "Sua mensagem merece ser vestida." + botões "Contar meu projeto" e "Projetos já realizados" (Brasa)
2. Faixa de perfis correndo (Breu)
3. Para quem carrega uma mensagem (Osso)
4. O que produzimos — camisetas (destaque), moletons, bonés, jaquetas, ecobags (Brasa)
5. Projetos já realizados (Breu)
6. Da ideia à entrega — 5 etapas + Produção / Criação de desenhos (Osso)
7. A camiseta que a gente faz — modelagem, gola, estampa, costura, tecido (Breu)
8. Por que a Corujinha — "Onde muitos enxergavam apenas roupas..." + Marca / Indústria / Merch (Brasa)
9. Perguntas frequentes (Osso)
10. Fechamento com WhatsApp (Brasa)

Espaços de foto em "O que produzimos": `camiseta` (destaque, 1200 x 1500, assunto centralizado — no celular vira quadrada) e `moletom`, `bone`, `jaqueta`, `ecobag` (800 x 1000, vertical 4:5).

## A confirmar / pendente
- Fotos reais para todos os espaços marcados "Foto: ..." (enviar como arquivo anexo).
- Projetos já realizados: nome, tipo e quantidade de peças de cada um + foto.
- Número de WhatsApp do comercial (usei 55 12 3933-9065, o mesmo da landing da fábrica).
- Técnicas de estampa usadas (silk, DTF, etc.) e gramatura da malha, para detalhar a seção da camiseta.
- Quantidade mínima e prazo médio, se quiserem cravar na seção de perguntas.

## Como trocar as fotos
Coloque a foto na pasta `imagens/`, ao lado do HTML, com o nome exato abaixo (`.jpg`, `.jpeg`, `.png` ou `.webp`). A página encontra sozinha; sem o arquivo, aparece o espaço com a coruja.

| Arquivo | Onde aparece |
|---|---|
| `fundo-topo` | Fundo da área vermelha do topo (fica coberto por um véu Brasa para o texto continuar legível) |
| `hero` | Foto grande do topo |
| `selo` | Fotinho do cartão "Produção própria" |
| `modelagem` | Pessoa vestindo, corpo inteiro |
| `gola`, `estampa`, `costura` | Detalhes da camiseta |
| `projeto-1` … `projeto-5` | Projetos já realizados |
| `camiseta` | O que produzimos: card grande (destaque) |
| `moletom`, `bone`, `jaqueta`, `ecobag` | O que produzimos |

Para ajustar o enquadramento de uma foto, acrescente `data-pos="center top"` (ou `"50% 30%"`) no elemento que tem o `data-img` correspondente.
