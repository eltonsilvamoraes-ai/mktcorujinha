# Diagnóstico de Acesso — API do Mercado Livre

*Testado em 21/07/2026*

## Resultado dos testes

| Endpoint | Objetivo | Resultado |
|---|---|---|
| `GET /categories/MLB263532` | Metadados da categoria | ✅ 200 (público) |
| `GET /categories/MLB1500` | Metadados (Construção BR) | ✅ 200 (público) |
| `GET /sites/MLB/search?...` | Buscar produtos | ❌ 403 forbidden |
| `GET /highlights/MLB/category/...` | Mais vendidos (ranking) | ❌ 401 unauthorized |
| `GET /products/search?...` | Produtos de catálogo | ❌ 403 PolicyAgent |
| `GET /trends/MLB/...` | Buscas em tendência | ❌ 403 PolicyAgent |
| Página web `lista.mercadolivre.com.br/...` | Scraping do site | ❌ redireciona p/ verificação anti-robô |

## Conclusão

Desde ~2023 o Mercado Livre restringiu a API pública. **Todo endpoint que retorna listagem de produto, ranking de vendas ou dados de catálogo exige um `access_token` de OAuth** (de uma aplicação registrada em developers.mercadolibre.com). Só metadados de categoria seguem públicos. O site público bloqueia acesso automatizado com muro anti-bot (DataDome/verificação de conta).

Portanto: **não há caminho anônimo.** Para coletar os dados é obrigatório um token. Ver `como-gerar-token-ml.md`.

## Observação sobre "+1000 vendas"

O ML deixou de expor a quantidade exata vendida por item na API. O filtro numérico "+1000 vendas" exato ficou inviável. **Substituto melhor:** o endpoint `/highlights/{site}/category/{cat}` retorna o *ranking* dos mais vendidos da categoria (posição 1, 2, 3...) — que identifica os campeões de venda de forma mais confiável que um número solto, e é exatamente o que o objetivo do projeto pede.
