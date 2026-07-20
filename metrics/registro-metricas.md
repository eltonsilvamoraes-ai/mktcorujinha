# Registro de Métricas — A Marca da Corujinha

A régua da transição físico→digital: **conversão, CPA e ROAS**. A meta de julho/2026 não é faturar alto — é sair do mês com esses três números limpos.

## Glossário rápido

- **Conversão** = pedidos ÷ visitas. Saudável para e-commerce: 1–2%. Baseline atual: 0,28%.
- **CPA** (Custo por Aquisição) = verba investida em ads ÷ número de vendas geradas por ads.
- **ROAS** (Retorno sobre Investimento em Ads) = receita gerada por ads ÷ verba investida em ads.

## Baseline

- Visitas/dia (antes do festival): ~47
- Conversão histórica: 0,28%
- Ticket médio: ~R$168

## Log diário — Festival de Oversized (até 31/07)

| Data | Visitas | Visualizaram produto | Carrinhos | Vendas (site) | Vendas (loja física) | Observações |
|---|---|---|---|---|---|---|
| 20/07 (dia 1) | 291 | 158 (54%) | 10 (5 testes + 1 real + demais?) | 0 | 3 kits (+ 1 cliente do carrinho, fecha na loja) | ~6x o baseline; amostra pequena, 0 vendas no site é esperado nesse volume (≈0,8 venda projetada pela taxa histórica) |

> Atualizar esta tabela diariamente durante o festival. Não é preciso reagir a cada dia — o objetivo é olhar a tendência ao final do mês.

## Log de campanhas Meta Ads

Fonte: planilha "Painel de Desempenho — Meta Ads" (Google Sheets) + PDF de análise, período 06/07 a 20/07/2026.

### Resumo do período (15 dias corridos, 13 pedidos)

| Indicador | Topo de Funil | Fundo de Funil | Total |
|---|---|---|---|
| Investimento | R$653,94 | R$0,00 | R$653,94 |
| Receita | R$2.765,51 | R$0,00 | R$2.765,51 |
| Pedidos | 13 | 0 | 13 |
| Ticket médio | R$212,73 | — | R$212,73 |
| Margem de contribuição (antes de ads) | 63,5% | — | 63,5% |
| CPA | R$50,30 | — | R$50,30 |
| ROAS | 4,23x | 0,00x | 4,23x |
| ROAS de equilíbrio | 1,57x | — | 1,57x |
| Meta de ROAS | 5,00x | 5,00x | 5,00x |
| Lucro após ads | R$1.102,13 | R$0,00 | R$1.102,13 |
| Margem líquida (após ads, antes de custo fixo) | 39,9% | — | 39,9% |

**Leitura:** campanha está lucrativa (ROAS 4,23x contra um equilíbrio de 1,57x) e a margem líquida pós-ads (39,9%) está bem acima do benchmark internacional de moda DTC (ver `financeiro/benchmark-margem.md`). Ainda não bateu a meta de ROAS de 5,00x, mas está perto.

### Evolução diária

| Data | Investimento | Pedidos | Receita | ROAS | ROAS equilíbrio |
|---|---|---|---|---|---|
| 06/07 | R$14,61 | 0 | R$0,00 | 0,00x | — |
| 07/07 | R$40,69 | 3 | R$756,50 | 18,59x | 1,61x |
| 08/07 | R$43,05 | 1 | R$114,60 | 2,66x | 1,23x |
| 09/07 | R$58,91 | 0 | R$0,00 | 0,00x | — |
| 10/07 | R$55,05 | 0 | R$0,00 | 0,00x | — |
| 11/07 | R$49,63 | 2 | R$492,21 | 9,92x | 1,65x |
| 12/07 | R$50,56 | 0 | R$0,00 | 0,00x | — |
| 13/07 | R$49,50 | 1 | R$85,50 | 1,73x | 2,33x |
| 14/07 | R$58,96 | 2 | R$380,79 | 6,46x | 1,59x |
| 15/07 | R$94,61 | 1 | R$239,80 | 2,53x | 1,40x |
| 16/07 | R$57,20 | 2 | R$460,31 | 8,05x | 1,51x |
| 17/07 | R$50,41 | 0 | R$0,00 | 0,00x | — |
| 18/07 | R$30,76 | 0 | R$0,00 | 0,00x | — |
| 19/07 | R$0,00 | 0 | R$0,00 | 0,00x | — |
| 20/07 | R$0,00 | 1 | R$235,80 | — | 1,67x |

### Achados importantes

1. **Todos os 13 pedidos vieram de campanhas "Topo".** A coluna "Fundo de Funil" está zerada — ainda não existe campanha ativa de retargeting/Vendas rodando separadamente. Isso quer dizer duas coisas possíveis: (a) o "Topo" está, na prática, também levando gente direto à compra (bom sinal — a oferta é forte o bastante pra converter sem precisar de segundo toque), e (b) ainda não foi testado o que uma campanha de Fundo dedicada (remarketing, objetivo Vendas) faria em cima do público que já foi gerado. Recomendação: com ~15 dias de tráfego acumulado, já existe base para ligar uma campanha de Fundo.
2. **6 de 15 dias tiveram zero pedidos** apesar de verba ativa — comportamento típico de "feast or famine" com volume baixo, não é sinal de campanha quebrada. Amostra ainda pequena para tirar conclusões por dia; olhar a tendência acumulada.
3. **ROAS varia de 0x a 18,59x dia a dia** — reforça o aprendizado já registrado: não mexer na campanha com poucos dias de dado.
4. Margem de contribuição de referência da própria planilha (63,2%) bate com a realizada (63,5%) — a precificação está calibrada.

## Leituras acumuladas

- Público quente atual é muito **local** (Jacareí-SP e região) — tende a fechar na loja física mesmo vendo a oferta no site.
- O site só será provado de fato pelo público **não-local**, que cresce com mais alcance (daí a importância dos vídeos de topo de funil).
- A campanha de Meta Ads, isoladamente, já está lucrativa e dentro (na verdade acima) dos benchmarks do setor — o gargalo segue sendo a conversão do site em si, não a aquisição paga.
