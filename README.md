# Projeto — Otimização de E-commerce da Corujinha

Central de trabalho para melhorar a plataforma de e-commerce (Nuvemshop) d'**A Marca da Corujinha**, entender métricas de Meta Ads, desenvolver estratégias de campanha e criar rotina de acompanhamento dos números do negócio.

Este repositório **não é o código do site** — a loja roda na Nuvemshop, uma plataforma fechada sem acesso a repositório. Este projeto é o espaço de análise, estratégia e rotina que orienta as decisões sobre o site, os anúncios e o crescimento do canal digital.

## Estrutura

- **`CLAUDE.md`** — guia de marca (missão, tom de voz, público, posicionamento). Consultar antes de escrever qualquer conteúdo.
- **`site-audit/`** — auditorias da loja (home, página de produto, checkout): o que está bom, o que trava a conversão.
- **`ads-strategy/`** — estratégia de campanhas de Meta Ads (funil, públicos, criativos, verba).
- **`metrics/`** — histórico de números: conversão, CPA, ROAS, visitas, vendas. A régua da transição físico→digital.
- **`financeiro/`** — benchmarks de margem e referências financeiras do setor.
- **`checklists/`** — rotinas recorrentes (semanal, mensal, pré-campanha) para não deixar nada passar.
- **`market-research/`** — benchmarks de mercado, concorrentes, referências do nicho de streetwear cristão/moda gospel.

## Objetivo maior

Fortalecer as vendas do site para viabilizar a transição da empresa do físico para o digital. O gargalo identificado não é preço nem margem — é **conversão**. Este projeto existe para medir, entender e melhorar esse número de forma contínua.

**Prazo:** a loja física será entregue em até **5 meses** (a partir de 20/07/2026 → por volta de dezembro/2026). Esse é o mesmo prazo para escalar a operação online — aprender, otimizar, testar e acompanhar os números — de forma que o digital sustente o negócio quando o físico encerrar.

## Acesso à web

Acesso ao domínio `amarcadacorujinha.com.br` liberado em 20/07/2026. Funciona buscar o HTML real da loja (via curl) para auditar estrutura, preços, textos e badges. A ferramenta de fetch com renderização (WebFetch) e a automação de navegador (Playwright/Chromium) não conseguem completar a navegação neste ambiente — então auditorias visuais (como o site realmente aparece na tela) ainda dependem de screenshots enviados pelo usuário.
