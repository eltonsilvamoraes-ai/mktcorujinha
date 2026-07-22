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

### Topo
- **Orçamento:** R$80/dia (subiu de ~R$44/dia médio do ciclo anterior)
- **Criativo:** 1 vídeo só — o que mais performou (concentra o sinal do algoritmo, escolha correta)
- **Objetivo declarado:** confirmar qual evento de otimização está selecionado (ver alerta abaixo)

### Fundo (novo — antes estava zerado)
- **Público:** remarketing da campanha de Topo
- **Criativo:** 3–5 vídeos de produtos mais vendidos, apresentando as oversized (em vez de só o vídeo "Compre 3 Pague 2")
- **Motivação:** os dados pediam isso — no ciclo anterior 100% das vendas vieram de Topo e Fundo estava zerado

### Alertas e recomendações para este ciclo

1. **R$80/dia provavelmente NÃO tira do modo de aprendizado sozinho** se a otimização for por **Compra**. A regra do Meta é ~50 eventos de otimização/semana por conjunto. Com CPA ~R$50, R$80/dia ≈ 11 compras/semana — bem abaixo de 50. Se o evento de otimização for AddToCart (66 em 15 dias ≈ 4,4/dia), fica mais perto de sair do aprendizado. **Confirmar qual evento está otimizando.**
2. **Pausar + reativar + mudar orçamento ~60% reinicia a fase de aprendizado** pelas regras do Meta — os primeiros dias não serão estáveis. Não é motivo pra não fazer, só pra não tirar conclusão cedo.
3. **Frequência do Topo:** com orçamento maior e público frio pequeno, a frequência sobe rápido. Vigiar no Gerenciador; acima de ~3-4 é fadiga chegando. Ter 1 variação de backup pronta.
4. **Fundo — considerar catálogo dinâmico:** se a Nuvemshop estiver integrada ao Meta Commerce Manager, anúncio dinâmico de catálogo (cada pessoa vê o produto que viu no site) tende a bater criativo fixo, e ataca direto a maior perda do funil (93,5% veem produto e não põem no carrinho).
5. **Fundo — público amplo:** não restringir só a quem viu o vídeo do Topo; incluir quem visitou site / viu produto / add-to-cart nos últimos 30 dias. O público de remarketing ainda é pequeno (~1.000 views de produto, 66 carrinhos).
6. **5 vídeos em público pequeno diluem o sinal:** deixar rodar a 1ª semana, depois cortar pros 2-3 melhores. Não interromper antes disso.

## Pendências

- [ ] Confirmar instalação e disparo do Pixel (responsável: Aline)
- [ ] Confirmar qual evento de otimização a campanha de Topo está usando (Compra vs. AddToCart) — muda a leitura do "sair do aprendizado"
- [ ] Verificar se a Nuvemshop está integrada ao Meta Commerce Manager (habilita catálogo dinâmico no Fundo)
- [ ] Ao fim do ciclo (31/07): registrar resultado em `metrics/registro-metricas.md`, comparar Topo vs. Fundo agora que Fundo existe
- [ ] Construir uma "skill" calibrada de Meta Ads com os aprendizados de cada ciclo
