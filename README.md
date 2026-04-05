# Ghost Automator Hub - Pro Plus Max

> Hub de automacao headless com Playwright + CustomTkinter.  
> **Modo PC por padrao. Modulos externos so ligam quando voce quiser.**

---

## Modos de operacao

| Modo | Quem usa | Como ligar |
|---|---|---|
| **Modo PC** | Padrao, sempre ativo | Nada a fazer |
| **Modo Avancado** | Telegram + API REST | `ATIVAR_MODO_AVANCADO=true` no `.env` |

No Modo PC o sistema e 100% local: so tu, o Chrome e o Playwright.
No Modo Avancado os modulos externos acordam conforme as flags no `.env`.

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

Edita so a linha obrigatoria:
```env
CHROME_USER_DATA=C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data
```

Substitui `SEU_USUARIO` pelo teu nome de usuario do Windows. Pronto.

---

## Rodar o Hub (Modo PC)

```bash
python automator_hub.py
```

A sidebar mostra o badge **MODO PC** em ciano.  
Telegram e API aparecem como `off` na sidebar.

---

## Scripts disponiveis

### Geracao unica (via Hub ou terminal)
```bash
python automacoes/flow_hub.py "Um samurai ciborgue em neon Tokyo, 4k"
```

### Batch (fila de prompts)
```bash
python automacoes/flow_batch.py prompts.txt
```

### Swarm (N imagens em paralelo)
```bash
python automacoes/flow_swarm.py prompts.txt --workers 3
```

---

## Ativar Modo Avancado

Edita o `.env`:
```env
ATIVAR_MODO_AVANCADO=true
ATIVAR_TELEGRAM=true
ATIVAR_API=true

TELEGRAM_BOT_TOKEN=token_do_botfather
TELEGRAM_CHAT_ID=teu_chat_id
```

O que muda no Hub:
- Badge da sidebar vira laranja **MODO AVANCADO ON**
- Nova aba **Modo Avancado** aparece com status dos modulos
- Botao **Iniciar API Server** aparece na sidebar
- Telegram e API aparecem como `ON` nos indicadores

Para subir a API manualmente:
```bash
python api_server.py
# Docs: http://localhost:8000/docs
```

---

## Estrutura

```
ghost-automator-hub/
|-- automator_hub.py         # Hub GUI (ponto de entrada principal)
|-- config.py                # Central de configuracao (le o .env)
|-- api_server.py            # API REST FastAPI (so usar se MODO_API=true)
|-- notificador_telegram.py  # Webhook Telegram (so usar se MODO_TELEGRAM=true)
|-- requirements.txt
|-- .env.example             # Template - copia para .env
|-- .gitignore
|-- prompts.txt
|-- automacoes/
|   |-- flow_hub.py          # Flow: geracao unica
|   |-- flow_batch.py        # Flow: fila de prompts
|   `-- flow_swarm.py        # Flow: paralelo com workers
`-- perfis/                  # Chrome sessions (nunca sobe pro GitHub)
```

---

## Seguranca

O `.gitignore` blinda:
- `perfis/` - Chrome User Data
- `.env` - tokens e senhas
- `geracoes_flow/` - imagens geradas
- `__pycache__/` e `.pyc`

---

*Feito com Playwright + CustomTkinter + FastAPI.*  
*Zero mouse sequestrado. Zero janela pulando na tela. Criado para farmar aura 24/7.*
