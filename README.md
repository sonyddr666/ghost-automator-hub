# Ghost Automator Hub - Pro Plus Max

> Hub de comando centralizado para automacoes headless com Playwright.  
> Interface multi-tab Dark Mode + API REST + Webhook Telegram + Swarm Mode.
>
> **Isso nao e apenas um script. E um colapso estetico de produtividade.**

---

## Arquitetura

```
[Ghost1 CMD Portal / Telegram / qualquer front-end]
              |
              v  POST /gerar {"prompt": "..."}
     api_server.py (FastAPI localhost:8000)
              |
              v  dispara headless
     Playwright + Chrome User Data
              |
              v  PNG gerado
     geracoes_flow/imagem.png
              |
              v  notifica
     notificador_telegram.py  -->  teu celular
```

---

## Modulos

| Arquivo | Funcao |
|---|---|
| `automator_hub.py` | Hub GUI multi-tab (CustomTkinter) |
| `api_server.py` | API REST FastAPI (localhost:8000) |
| `notificador_telegram.py` | Webhook: envia PNG pro Telegram |
| `automacoes/flow_hub.py` | Script Flow modo unico |
| `automacoes/flow_batch.py` | Script Flow modo batch (fila) |
| `automacoes/flow_swarm.py` | Script Flow modo enxame (paralelo) |

---

## Instalacao

```bash
git clone https://github.com/sonyddr666/ghost-automator-hub.git
cd ghost-automator-hub

pip install -r requirements.txt
playwright install chromium
```

---

## Configuracao

```bash
cp .env.example .env
```

Edita o `.env`:
```env
CHROME_USER_DATA=C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data
TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
TELEGRAM_CHAT_ID=SEU_CHAT_ID_AQUI
```

---

## Como usar

### Modo Hub (GUI)
```bash
python automator_hub.py
```

### Modo API (servidor local)
```bash
python api_server.py
# Docs: http://localhost:8000/docs
```

Exemplo de chamada:
```bash
curl -X POST http://localhost:8000/gerar \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"Um samurai ciborgue em neon Tokyo, 4k\"}"
```

Resposta:
```json
{
  "id": "a3f9c1b2",
  "status": "na_fila",
  "mensagem": "Poltergeist invocado. Geracao iniciada em background.",
  "prompt": "Um samurai ciborgue em neon Tokyo, 4k",
  "criado_em": "2026-04-05T02:00:00"
}
```

Checar status:
```bash
curl http://localhost:8000/status/a3f9c1b2
```

### Modo Batch
```bash
python automacoes/flow_batch.py prompts.txt
```

### Modo Swarm (N imagens em paralelo)
```bash
python automacoes/flow_swarm.py prompts.txt --workers 3
```

---

## Configurar Bot Telegram

1. Abre o Telegram e fala com `@BotFather`
2. Manda `/newbot`, segue as instrucoes, copia o token
3. Fala com `@userinfobot` pra pegar teu `chat_id`
4. Cola os dois no `.env`
5. Quando uma imagem for gerada, ela chega direto no teu celular

---

## Estrutura

```
ghost-automator-hub/
|-- automator_hub.py         # Hub GUI multi-tab
|-- api_server.py            # API REST (FastAPI)
|-- notificador_telegram.py  # Webhook Telegram
|-- requirements.txt         # Dependencias
|-- .env.example             # Template de configuracao
|-- .gitignore               # Manto da invisibilidade
|-- prompts.txt              # Prompts de exemplo
|-- automacoes/
|   |-- flow_hub.py          # Flow modo unico
|   |-- flow_batch.py        # Flow modo batch
|   `-- flow_swarm.py        # Flow modo enxame (paralelo)
`-- perfis/                  # Chrome sessions (NUNCA sobe pro GitHub)
```

---

## Seguranca

O `.gitignore` blinda:
- `perfis/` - Chrome User Data (cookies, login Google)
- `.env` - tokens e senhas
- `geracoes_flow/` - imagens geradas localmente
- `__pycache__/` e arquivos `.pyc`

---

*Feito com Playwright + CustomTkinter + FastAPI. Zero mouse sequestrado. Zero janela pulando na tela.*  
*Criado para farmar aura 24/7.*
