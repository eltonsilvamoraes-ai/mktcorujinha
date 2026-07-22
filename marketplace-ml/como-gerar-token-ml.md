# Como gerar o token de acesso da API do Mercado Livre

O token é o que me permite puxar os dados automaticamente. Vale para pesquisa pontual (expira em ~6h — gera, me passa, eu rodo na hora).

## Passo a passo

1. **Entrar em** https://developers.mercadolivre.com.br → logar com a conta ML de vocês.
2. **Criar uma aplicação** ("Minhas aplicações" → "Criar nova aplicação").
   - Nome: qualquer (ex.: "Pesquisa Corujinha").
   - Marcar o escopo/permissão de **leitura (read)**.
   - **Redirect URI:** pode usar `https://httpbin.org/get` (serve só pra receber o código).
3. Anotar o **App ID** (client_id) e a **Secret Key** (client_secret) gerados.
4. **Autorizar** — abrir no navegador (trocando SEU_APP_ID e a mesma redirect URI):
   ```
   https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=SEU_APP_ID&redirect_uri=https://httpbin.org/get
   ```
   Depois de logar e autorizar, o navegador vai para a redirect URI com um `?code=TG-xxxxxxxx` na URL. **Copiar esse código** (`TG-...`).
5. **Trocar o código pelo token** — rodar (ou me pedir pra montar) esta chamada:
   ```
   curl -X POST https://api.mercadolibre.com/oauth/token \
     -d grant_type=authorization_code \
     -d client_id=SEU_APP_ID \
     -d client_secret=SUA_SECRET \
     -d code=TG-xxxxxxxx \
     -d redirect_uri=https://httpbin.org/get
   ```
   A resposta traz `access_token` (o que eu preciso) e `refresh_token`.

## O que me passar

Só o **`access_token`** (começa com `APP_USR-...`). Com ele eu rodo a coleta inteira e monto a planilha.

## Segurança

- O `access_token` é uma credencial ligada à conta de vocês. Trate como senha.
- Expira sozinho em ~6h — depois disso fica inofensivo.
- **Não vou salvá-lo no repositório** — uso só durante a sessão pra fazer as chamadas.
- Se quiser, revogue a aplicação depois da pesquisa (Minhas aplicações → remover).
