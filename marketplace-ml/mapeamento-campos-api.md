# Mapeamento — Campo da Planilha → Endpoint da API

Como cada coluna pedida será preenchida, uma vez que exista um `access_token`.

## Fluxo de coleta

1. **`GET /highlights/MLB/category/MLB263532`** (ou por subcategoria, ex. MLB2526)
   → devolve o ranking dos mais vendidos: lista de `id` (item) ou `catalog_product_id`, na ordem de vendas. Estes são os campeões.
2. Para cada item campeão, **`GET /items/{item_id}`** → nome, preço, categoria, tipo de anúncio, marca, vendedor, envio.
3. Para cada produto de catálogo, **`GET /products/{catalog_product_id}`** → preço mín/máx do catálogo e nº de concorrentes (vendedores disputando o mesmo anúncio).
4. Para o nome do vendedor, **`GET /users/{seller_id}`**.

## Tabela de mapeamento

| Coluna da planilha | Fonte | Campo / regra |
|---|---|---|
| Nome Produto | `/items/{id}` | `title` |
| Preço Venda | `/items/{id}` | `price` |
| Tipo Anúncio | `/items/{id}` | `listing_type_id`: `gold_pro`→Premium, `gold_special`→Clássico |
| Marca | `/items/{id}` | `attributes[]` onde `id="BRAND"` → `value_name` |
| Categoria | `/items/{id}` | `category_id` (traduzido via `/categories/{id}`) |
| Nome Vendedor | `/users/{seller_id}` | `nickname` |
| Fulfillment (sim/não) | `/items/{id}` | `shipping.logistic_type == "fulfillment"` → Sim |
| Flex (sim/não) | `/items/{id}` | `shipping.logistic_type == "self_service"` → Sim |
| Está em catálogo | `/items/{id}` | `catalog_listing == true` e existe `catalog_product_id` |
| Maior Preço Catálogo | `/products/{catalog_id}` | maior preço entre as ofertas (`buy_box_winner` + `/products/{id}/items`) |
| Menor Preço Catálogo | `/products/{catalog_id}` | menor preço entre as ofertas |
| Nº de Concorrentes | `/products/{catalog_id}` | contagem de vendedores ofertando o mesmo produto de catálogo |

## Filtros aplicados no final (na planilha)

- Em catálogo = Sim (descartar itens sem `catalog_product_id`)
- Poucos concorrentes = manter os com nº de vendedores baixo (definir corte, ex. ≤ 5)
- Campeões de venda = vêm do ranking de highlights (já ordenados por venda)

## Observação sobre limites da API

- O `access_token` expira em ~6 horas → a coleta precisa rodar dentro desse prazo após gerar o token.
- Há limite de requisições (rate limit). Para categorias grandes, coletar por subcategoria e em lotes evita bloqueio.
