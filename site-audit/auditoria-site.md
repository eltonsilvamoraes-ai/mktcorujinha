# Auditoria do Site — A Marca da Corujinha

*Última atualização: 20/07/2026*

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

## Pendente — refino

- [x] Alinhar texto da faixa de ícones da home — **confirmado resolvido por screenshot** (20/07): 4 colunas simétricas, ícone + título + subtítulo bem distribuídos
- [x] Corrigir apóstrofo em "Festival de Oversized's" — **não aparece no hero principal** (banner mostra "FESTIVAL DE OVERSIZED" limpo). Não confirmado em páginas de coleção do festival ainda
- [x] Esconder selo "0% OFF" em produtos fora da promoção — **confirmado resolvido**, inclusive visualmente (moletons e blusas sem selo)
- [ ] Tabela de medidas visível na página de produto — **parcialmente resolvido**, ver auditoria ao vivo
- [ ] Ativar recuperação de carrinho abandonado (baixa urgência — volume ainda baixo)
- [ ] Configurar regra na Nuvemshop: peça grátis = sempre a de menor valor, restrita a oversized, não acumula com outras promoções

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

### Achado novo — frete grátis está em R$199, não R$249

Tanto a home quanto a página de produto mostram **"Frete Grátis pra Todo Brasil para compras acima de R$199"** — não R$249, que era o valor documentado como "unificado" antes do festival. Pode ser proposital (com o combo do festival custando R$219,80, um limiar de R$199 é mais fácil de bater e ainda estimula quem compra só 1 peça a completar frete grátis) — mas como diverge do que está registrado, vale **confirmar com quem mexeu na configuração** se foi decisão consciente para o período do festival ou se ficou um valor antigo.

### Achado novo — tabela de medidas existe, mas está escondida

A tabela de medidas **existe** (é a 5ª foto do carrossel de imagens do produto, arquivo "tabela-medidas-oversized..."), mas:
- Não tem destaque — é só mais uma foto no carrossel, fácil de não ver.
- A FAQ menciona "recomendamos conferir nossa tabela de medidas" mas o texto não é um link/botão que leva direto até ela.

Recomendação: transformar em uma seção própria (aba "Tamanhos" ou botão "Ver tabela de medidas" perto do seletor de tamanho) em vez de depender da pessoa rolar o carrossel de fotos até o fim.

### Confirmado por screenshot (20/07) — topo da home completo

- Faixa de ícones (Frete Grátis / 3x Sem Juros / Compre 3 Pague 2 / Primeira Troca Grátis) bem alinhada, 4 colunas simétricas ✅
- Banner hero do festival: "FESTIVAL DE OVERSIZED", "VÁLIDO ATÉ 31/07", "COMPRE 03 PEÇAS E PAGUE 02! A TERCEIRA PEÇA É GRÁTIS", CTA "COMPRAR >", assinado com "'Revesti-vos de Cristo' — Romanos 13:14" ✅ mensagem clara, identidade forte, verso-âncora presente
- Nenhum "0% OFF" ou "Esgotado" visível em nenhum card de produto, incluindo os fora da promoção (moletons, blusas, cropped) ✅
- Frete grátis R$199 confirmado visualmente na faixa de ícones e no ticker do topo — reforça o achado do código

### Achado novo — avaliação por produto é rara

Nos cards de produto da seção "TOP 05 - OVERSIZED MAIS VENDIDAS", apenas 1 dos 4 produtos visíveis mostra estrelas de avaliação (com contagem baixa, ex. "(1)"). Os outros 3 não mostram nada — sinal de que a maioria dos produtos ainda não acumulou avaliação própria vinculada ao SKU, mesmo a loja tendo boas avaliações agregadas no Google. Quem rola a vitrine rápido não vê prova social na maioria dos cards.

**Recomendação:** pedir avaliação por produto no pós-venda (e-mail ou WhatsApp automático X dias após a entrega) para popular esse selo direto na vitrine — é mais forte que só ter os depoimentos do Google numa seção separada, porque aparece no momento exato da decisão (olhando o card do produto).

### Ainda não verificado

- Apóstrofo em "Oversized's" — não aparece no hero nem na home; pode estar em página de coleção específica do festival ainda não vista.
- Página de produto completa via screenshot (a tabela de medidas, especificamente onde ela aparece no carrossel).
- Carrinho e checkout renderizados.

## Próxima auditoria ao vivo

Pendente: rodar o mesmo processo pra página de carrinho e para páginas de coleção do festival (onde pode estar o typo do apóstrofo). Velocidade de carregamento mobile ainda não medida.
