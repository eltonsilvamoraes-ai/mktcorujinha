# Teste — Frete Grátis nos Últimos 10 Dias de Julho

*Proposto por Elton, 20/07/2026*

## A ideia

Usar o valor hoje não gasto com emissão de NF-e para bancar frete grátis sem mínimo de compra nos últimos 10 dias de julho (21/07 a 31/07), reativando ao mesmo tempo a campanha de Meta Ads que foi pausada no sábado (18-19/07).

## Questão em aberto — falta um número

Para fechar a conta, falta o **valor mensal (ou nos 10 dias) economizado por não emitir NF-e**. Sem isso não dá para calcular quantos pedidos extras a promoção precisa gerar para se pagar.

**Nota à parte, sem alarme:** não emitir NF-e é uma exposição fiscal, não só uma economia de caixa. Se isso vier a ser obrigatório (ou já for e ainda não estiver sendo feito), essa "economia" deixa de ser recorrente. Vale confirmar com o contador antes de tratar como orçamento fixo para testes futuros.

## O que muda de fato com a promoção

O limiar atual de frete grátis é R$199. O combo do festival (3 peças, R$219,80) **já** passa desse valor — ou seja, a promoção de frete sem mínimo só muda a economia de quem compra **1 peça só** (R$106,60–109,90, abaixo do limiar atual).

## Custo real do frete — usar o número certo

- Custo médio nacional (todas as regiões): **R$8,74**
- Custo médio para SP + MG (as regiões da campanha reativada): **R$12–15**

Para modelar esse teste, usar R$12–15, não R$8,74 — é o custo real do público que a campanha vai atingir. Vale notar também: a própria planilha de Meta Ads usa **R$10,00** como frete de referência no cálculo de margem/ROAS de equilíbrio — abaixo do custo real dessa região, então o ROAS de equilíbrio calculado para SP/MG está um pouco otimista hoje.

## Onde essa mudança tem mais efeito (e onde não tem)

Segundo o funil completo (`metrics/registro-metricas.md`), o carrinho e o checkout já convertem bem (carrinho→venda ~20%, checkout iniciado→venda ~46%). O maior vazamento do funil está **antes** do carrinho (visualizar produto → adicionar ao carrinho, só 6,5% avançam). Frete grátis tende a atuar mais na ponta de carrinho/checkout — então é razoável esperar um efeito positivo, mas moderado, não a alavanca principal da conversão geral.

## Volume envolvido — risco financeiro é baixo

Em ~15 dias, apenas 24 pessoas iniciaram checkout e 13 fecharam pedido. Mesmo dobrando esse volume nos próximos 10 dias, o número de pedidos afetados pela mudança de frete é pequeno — o risco financeiro do teste em si é baixo, mesmo sem o número exato da economia de NF-e.

## Recomendação de desenho do teste

1. Rodar de 21/07 a 31/07 (10 dias, coincide com o fim do festival).
2. Reativar a campanha pausada tratando como um teste novo, não uma retomada — a mensagem de frete grátis sem mínimo muda a oferta, então vale não mexer de novo por pelo menos 4-7 dias (mesmo princípio já registrado em `ads-strategy/plano-meta-ads.md`).
3. Medir separadamente: conversão de quem compra 1 peça só vs. combo, frete como % da receita nesses 10 dias vs. o período anterior, e o de sempre (CPA, ROAS).
4. Registrar o resultado em `metrics/registro-metricas.md` ao final do período.
