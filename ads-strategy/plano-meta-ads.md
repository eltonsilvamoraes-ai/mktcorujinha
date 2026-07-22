# Estratégia de Meta Ads — A Marca da Corujinha

*Última atualização: 20/07/2026*

## Regra de ouro

O objetivo escolhido na campanha diz ao Meta **quem procurar**. Vender no site exige objetivo de **Vendas**, não engajamento — engajamento otimiza para quem clica/curte, não para quem compra.

## Pré-requisito (item zero)

Pixel instalado e disparando corretamente os eventos:
- PageView
- ViewContent
- AddToCart
- Purchase

Sem isso, qualquer otimização de campanha de Vendas fica cega.

## Estrutura de funil

### Topo → gera público de remarketing
- **Objetivo:** Engajamento / visualizações de vídeo (ou Reconhecimento)
- **Não manda tráfego direto para o site** — o papel é encher o público quente
- **Criativo:** vídeos descontraídos, linguagem espontânea (ver `CLAUDE.md` — estilo TikTok/Reels)

### Meio (opcional, para depois)
- **Objetivo:** Tráfego / Engajamento
- **Criativo:** Fogo nos Olhos (ou outro criativo validado)

### Fundo → converte no site
- **Objetivo:** Vendas / Compra
- **Público:** remarketing (quem já engajou/visitou)
- **Criativo:** vídeo explicativo da oferta + "Fogo nos Olhos" (campeão histórico, ~300k views, já validado no WhatsApp — agora testado no site)

## Verba e ritmo

- Começar pequeno: **R$20–30/dia**
- Estrutura simples: só topo + fundo
- Deixar rodar **4–7 dias sem mexer** antes de otimizar — dar tempo pro algoritmo aprender

## Princípios

1. Não superconstruir campanha com verba pequena — estrutura simples aprende mais rápido que estrutura complexa
2. Medir antes de escalar — tráfego pago só rende sobre um site que já converte
3. Criativo de fundo deve reaproveitar o que já converteu em outro canal (ex.: WhatsApp) antes de criar do zero

## Ciclo atual — reativação em 21/07/2026 (últimos 10 dias do festival)

Estrutura final confirmada pelo Elton (21/07):

### Topo — aquisição (público frio)
- **Objetivo:** Iniciar Checkout (InitiateCheckout)
- **Orçamento:** R$50/dia (testou R$80, voltou pra R$50)
- **Criativo:** 1 vídeo só — o que mais performou

### Fundo — conversão (remarketing quente)
- **Objetivo:** Compra
- **Criativo:** catálogo dinâmico do Meta, integrado só com as **oversized estampadas** (coerente: é a categoria da oferta "Compre 3 Pague 2")
- **Público:** visitou site 30d + iniciou/adicionou carrinho 14d + interagiu no Instagram 30d

### Leitura desta estrutura

- **Objetivos bem escolhidos:** Topo em Iniciar Checkout (mais eventos que Compra → aprende mais rápido com orçamento pequeno) e Fundo em Compra (público já quente, pode pedir o evento mais fundo). Correto.
- **Catálogo dinâmico só estampada** ataca direto a maior perda do funil (ver produto → carrinho, 93,5% de perda): cada pessoa revê o produto que olhou. Alinhado à oferta.

### Expectativa de "aprendizado" — estado normal é "limitado"

- **Topo:** ~1,6 checkouts/dia no histórico recente vs. ~7/dia (50/semana) necessários pra sair do aprendizado. Vai ficar em **"aprendizado limitado"** — normal pro volume, NÃO desligar por isso.
- **Fundo:** remarketing de público pequeno fica em "aprendizado limitado" quase sempre — esperado e OK, remarketing funciona mesmo assim porque o público é quente.
- Sair do aprendizado de verdade depende de **volume/alcance** (crescer o Topo), não de mexer em configuração.

### Ação recomendada em aberto — exclusão de público

Como as DUAS campanhas agora mandam pro site (Topo=checkout, Fundo=compra), elas podem competir pela mesma pessoa e encarecer ambas:
1. **No Topo, excluir o público do Fundo** (site 30d / carrinho 14d / IG 30d) → Topo foca em frio puro, Fundo colhe o quente sem concorrência.
2. **Nas duas, excluir quem já comprou** (30-60d) → não gastar verba de aquisição com cliente atual.

### Outras notas

- **Reativar + mudar orçamento reinicia o aprendizado** pelas regras do Meta — primeiros dias instáveis, não concluir cedo.
- **Frequência do Topo:** público frio é pequeno; vigiar frequência, acima de ~3-4 é fadiga. Ter 1 vídeo de backup.

## Pendências

- [ ] Confirmar instalação e disparo do Pixel (responsável: Aline)
- [ ] **Aplicar exclusões de público** (Fundo fora do Topo; compradores fora das duas) — evita concorrência interna
- [ ] Ao fim do ciclo (31/07): registrar resultado em `metrics/registro-metricas.md`, comparar Topo vs. Fundo agora que Fundo existe
- [ ] Construir uma "skill" calibrada de Meta Ads com os aprendizados de cada ciclo
