# Pesquisa de Produtos Campeões — Mercado Livre (projeto paralelo)

Projeto separado do e-commerce da Corujinha. Objetivo: encontrar **produtos campeões de venda** no Mercado Livre que valha a pena revender, aplicando filtros de oportunidade (muitas vendas + poucos concorrentes + em catálogo).

## Categoria alvo (confirmada)

- **MLB263532 = "Ferramentas"** (Mercado Livre **Brasil**)
- 11.003.786 itens, 9 subcategorias:
  - MLB2528 Acessórios para Ferramentas
  - MLB189210 Caixas e Organizadores
  - MLB2526 Ferramentas Elétricas
  - MLB439064 Ferramentas Industriais
  - MLB2527 Ferramentas Manuais
  - MLB437789 Ferramentas Pneumáticas
  - MLB269932 Ferramentas para Jardim
  - MLB5550 Medições e Instrumentação
  - MLB5236 Outros

> Correção feita: o código original passado (MLA1500) era da **Argentina** e da categoria "Construção". O alvo real é Ferramentas Brasil (MLB263532). Como a categoria é enorme, a pesquisa fina rende mais se rodada **por subcategoria** (ex.: só Ferramentas Elétricas) do que na categoria-mãe inteira.

## Parâmetros de pesquisa (diretrizes do cliente)

- Número de vendas: **+1000** (campeões de venda)
- Em catálogo: **sim** (item precisa estar em catálogo)
- Poucos concorrentes: **sim** (poucos vendedores no mesmo anúncio de catálogo)
- Categoria: Ferramentas (MLB263532)

## Campos a coletar (por produto)

Nome · Preço de venda · Tipo de anúncio (Premium/Clássico) · Marca · Categoria · Nome do vendedor · Fulfillment (sim/não) · Flex (sim/não) · Maior preço no catálogo · Menor preço no catálogo · Nº de concorrentes

## Situação técnica

A API pública do Mercado Livre foi fechada — busca, mais vendidos (highlights) e catálogo **exigem token de autenticação**. O site público bloqueia scraping com muro anti-robô. Só metadados de categoria são públicos. Diagnóstico completo e testes em `diagnostico-acesso.md`.

**RESOLVIDO (22/07):** token gerado via Client Credentials. Coleta feita pelo endpoint oficial `/highlights` (ranking de mais vendidos). Resultado em `campeoes-ferramentas-ml.xlsx` — 109 campeões em catálogo, 64 com ≤5 concorrentes.

## Arquivos

- `README.md` — este arquivo
- `diagnostico-acesso.md` — o que foi testado e por que precisa de token
- `mapeamento-campos-api.md` — de qual endpoint da API vem cada coluna
- `como-gerar-token-ml.md` — passo a passo para gerar o token de acesso
- `template-produtos.csv` — planilha com os cabeçalhos prontos

## Construção (22/07) — árvore completa

Varredura da árvore inteira de Construção (MLB1500): **313 sub-subcategorias**, **1.119 produtos campeões em catálogo**, **604 com ≤5 concorrentes**.

- `campeoes-construcao-ml.xlsx` — dataset completo (abas: Leia-me, Todos os campeões, Oportunidades ≤5 conc.)
- Google Sheets no Drive do Elton: "Construção — Top Oportunidades ML (Corujinha)" — 89 melhores (≤2 concorrentes e top-3 do nicho)

**Método:** endpoint `/highlights` (mais vendidos) rodado em cada folha da árvore. A busca aberta (`/search`) segue bloqueada mesmo com token — não é possível listar "todos os anúncios com +1000 vendas"; o ranking de mais vendidos é a fonte oficial de campeões, e a coluna de concorrentes é o filtro de oportunidade.
