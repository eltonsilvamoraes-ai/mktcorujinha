# Auditoria do Site — A Marca da Corujinha

*Última atualização: 22/08/2026*

## Avaliação visual — 22/08/2026 (home ao vivo, via screenshots)

Contexto: avaliação feita já com a Plataforma de Marca (Fase 0) como régua. O festival acabou; a home hoje roda a promo "Liquida de Inverno" + combo "Compre 03 Pague 02" (agora permanente).

### Forças confirmadas
- **Hero on-brand:** abre com uma estampa de mensagem ("Era tanto azeite, que faltaram as vasilhas") + CTA — lidera com propósito, não com desconto. ✅
- **Fotografia boa:** on-model, com fotos de costas mostrando as estampas (Espírito Santo, Milagres, Vasilhas, olho/fogo). Ativo forte.
- **Estampas distintas e fortes** — a alma da marca aparece no produto.
- Cards padronizados, prova social dupla (Google + Depoimentos), FAQ, frete R$199 consistente, lazy-load de imagens ativo.

### O gap real: o "chrome" do site é genérico (não o conteúdo)
1. **Paleta briga:** produtos são quentes (marrom/vinho/off-white), mas o site usa **botão verde** + **selo vermelho** padrão Nuvemshop. CTA deveria estar na cor da marca.
2. **"LIQUIDA DE INVERNO - 25% OFF"** como 1ª seção, em vermelho — "liquida" está na lista de palavras a evitar. Único ponto que destoa do premium. → ver `copy-topo-home.md`.
3. **Tipografia não sistematizada** — banner tem fonte com personalidade; resto é a default da plataforma. Sem voz tipográfica. Resolve na Fase 1 do branding.
4. **Dois blocos de avaliação** (Google + Depoimentos) — redundante, unificar.
5. **Falta faixa de manifesto** entre hero e grid (o propósito só aparece no rodapé).

### Veredito
Site num "7": funcional, bom conteúdo, casca genérica que segura o posicionamento premium. O salto pro "9" é **aplicar a identidade visual** (paleta + tipografia + CTA na cor da marca + tom sem "liquida") — é a Fase 3 do projeto de branding, e depende de fechar a Fase 1 (escolher direção Vigília ou Fogo).

### Ganhos rápidos entregues (não dependem da identidade)
- `site-audit/copy-topo-home.md` — copy da faixa de manifesto + renomeação das seções no tom da marca.

---

*Auditoria técnica anterior: 20/07/2026*

## Situação de partida (diagnóstico inicial)

- Conversão do site: **0,28%** (saudável para e-commerce: 1–2%)
- Ticket médio: ~R$168
- Margem de contribuição: ~65% no combo
- **Gargalo nº 1: conversão** — não é preço, não é margem

## Resolvido ✅

| Problema encontrado | Ação tomada |
|---|---|
| Produtos aparecendo como "esgotado" | Removidos/corrigidos da vitrine |
| Variações (tamanho) poluindo o card | Escondidas na vitrine — fluxo agora é Comprar → produto → escolhe tamanho |
| Botão de WhatsApp competindo com "Comprar" | Tornado discreto; Comprar é o CTA dominante |
| Frete grátis com dois valores (R$249 e R$299 fantasma dos Correios) | Unificado em R$249 |
| Promoções em código ("3POR247") | Reescritas por extenso |
| Falta de prova social | Avaliações do Google publicadas |
| Selo de festival em produtos fora da promoção | Selo restrito às oversized |
| Botão flutuante de app antigo | Removido |
| Checkout não testado | Testado ponta a ponta (3ª peça zera, Pix aparece, pedido completa) |
| Faixa de ícones da home desalinhada | Confirmado por screenshot: 4 colunas simétricas |
| Apóstrofo em "Festival de Oversized's" | Confirmado corrigido, testado na home e na coleção ESTAMPADA |
| Selo "0% OFF" aparecendo fora de promoção | Confirmado ausente em 24+ produtos testados |
| Tabela de medidas ausente na página de produto | Confirmada presente (em texto) em pelo menos um produto — checar cobertura nos demais |

## Pendente — refino

- [~] Padronizar tabela de medidas em texto em todos os produtos oversized — **em andamento** (Elton confirmou 20/07, é a maior alavanca de conversão disponível agora, ver funil em `metrics/registro-metricas.md`)
- [x] Recuperação de carrinho abandonado — **já ativa**. 2 das 13 vendas do período vieram de recuperação manual via WhatsApp após carrinho abandonado — processo funciona na prática, vale manter mesmo com automação rodando
- [x] Regra da peça grátis na Nuvemshop — **confirmada ativa** (menor valor, restrita a oversized, não acumulável)
- [~] Automatizar pedido de avaliação por produto no pós-venda — **ferramenta já existe**, Elton vai reforçar cobertura manualmente
- [x] Frete grátis em R$199 — **confirmado: decisão consciente**, não é resíduo de configuração antiga

## Hipóteses a investigar

- Conversão de público **não-local** (fora de Jacareí-SP) ainda não foi provada — o público quente atual tende a fechar na loja física, não no site.
- Distribuição (alcance) pode ser o fator limitante mais do que o próprio site, já que "a casa está pronta" segundo os aprendizados registrados.

## Auditoria ao vivo — 20/07/2026

Acesso liberado. Auditoria feita via HTML real da home e da página de produto "Oversized Only Jesus - Preto" (curl, já que a ferramenta de fetch de página renderizada não conseguiu completar a navegação neste ambiente — sem confirmação visual via screenshot ainda).

### Confirmado resolvido

- **"Esgotado"** e **"0% OFF"** e o preço "de" riscado: o código já vem com `display:none` embutido no servidor — só aparecem quando a condição é real (produto realmente esgotado / com desconto real). Não há bug ativo aqui, apesar do HTML bruto conter o texto (é assim que a Nuvemshop renderiza por padrão).
- **Prova social**: avaliações do Google aparecem tanto na home quanto na página de produto, com nomes reais e depoimentos completos ✅
- **FAQ da página de produto**: cobre propósito da marca, modelagem oversized, envio, trocas (7 dias), pagamento, atacado e produção para igrejas/eventos — bem alinhado ao tom de voz do `CLAUDE.md` ✅
- **Rodapé institucional**: "A Primeira Marca Cristã Convertida do Brasil" + "Onde muitos enxergavam apenas roupas, Deus nos mostrou propósito." + endereço da fábrica em Jacareí-SP ✅
- **Fluxo de compra**: Comprar → escolher tamanho → adicionar ao carrinho, sem fricção extra ✅

### Frete grátis em R$199 (não R$249) — confirmado intencional

Elton confirmou (20/07) que a mudança de R$249 para R$199 foi decisão consciente para o período do festival, não um valor antigo esquecido. Ver `financeiro/teste-frete-gratis-julho.md` para o próximo teste envolvendo frete.

### Tabela de medidas — atualização (screenshot de "Oversized Tudo ou Nada - Preto")

Neste produto a tabela de medidas aparece como **texto de verdade dentro da descrição** ("TABELA DE MEDIDAS (ALTURA X LARGURA)" com cm exatos por tamanho: P 76×58, M 78×60, G 80×62, GG 82×64, G1 84×66) — muito melhor do que a versão só-em-imagem que eu tinha visto antes no produto "Only Jesus" (lá, a tabela existe só como a 5ª foto do carrossel, sem texto).

**Isso sugere inconsistência entre produtos**, não um problema resolvido de forma sistemática: alguns cadastros de produto têm a tabela em texto na descrição, outros só têm a imagem no carrossel (mais fácil de passar batido). Recomendação: padronizar — todo produto oversized deveria ter a tabela em texto na descrição, copiando o padrão do "Tudo ou Nada" pros demais.

### Confirmado por screenshot (20/07) — topo da home completo

- Faixa de ícones (Frete Grátis / 3x Sem Juros / Compre 3 Pague 2 / Primeira Troca Grátis) bem alinhada, 4 colunas simétricas ✅
- Banner hero do festival: "FESTIVAL DE OVERSIZED", "VÁLIDO ATÉ 31/07", "COMPRE 03 PEÇAS E PAGUE 02! A TERCEIRA PEÇA É GRÁTIS", CTA "COMPRAR >", assinado com "'Revesti-vos de Cristo' — Romanos 13:14" ✅ mensagem clara, identidade forte, verso-âncora presente
- Nenhum "0% OFF" ou "Esgotado" visível em nenhum card de produto, incluindo os fora da promoção (moletons, blusas, cropped) ✅
- Frete grátis R$199 confirmado visualmente na faixa de ícones e no ticker do topo — reforça o achado do código

### Achado confirmado com mais dados — avaliação por produto é inconsistente

Vendo a página de coleção "ESTAMPADA" inteira (24 produtos de uma vez), o padrão se confirma em escala: parte dos cards mostra estrelas com contagem (ex. "★★★★★ (6)", "★★★★☆ (7)", "★★★☆☆ (3)"), mas boa parte não mostra nenhuma avaliação. A loja tem um widget de avaliação nativo por produto funcionando de verdade (visto na página de "Oversized Tudo ou Nada" — 4,8 de média, 4 avaliações, com nome, selo de "comprador verificado" e texto), só falta cobertura em mais SKUs.

**Recomendação:** automatizar pedido de avaliação por produto no pós-venda (e-mail/WhatsApp X dias após entrega) — o selo aparece direto no card da vitrine, no momento exato da decisão, o que pesa mais do que os depoimentos do Google isolados numa seção à parte.

### Pontos fortes confirmados na página de produto ("Oversized Tudo ou Nada - Preto")

- **Caixa explicativa do combo** logo abaixo do preço: "Compre 3 e pague 2! Válido para este produto e todos da categoria: Oversized Cristã → ESTAMPADA. Nesta promoção você pode combinar este produto com outros da mesma categoria." — resolve de cara a dúvida mais comum de quem nunca viu a oferta (será que esse produto entra na promoção?) ✅
- **Opções de entrega detalhadas**: 3 transportadoras com prazo e preço + opção de retirar na loja física em Jacareí-SP com horário de funcionamento — bom para o público local, reduz fricção pra quem prefere retirar ✅
- **Widget de perguntas e respostas** existe mas está vazio ("Este produto ainda não tem perguntas") — não é problema, só espaço não utilizado ainda.

### Ainda não verificado

- Carrinho e checkout renderizados (já testados manualmente antes, mas não visualmente nesta rodada de auditoria).
- Velocidade de carregamento mobile.
- Se a tabela de medidas em texto está presente em todos os produtos oversized ou só em alguns.

## Próxima auditoria ao vivo

Pendente: página de carrinho, velocidade mobile, e uma checagem rápida se a tabela de medidas em texto está em todos os produtos ou só em parte deles.
