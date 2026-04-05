# Ghost Automator Hub - Pro Plus Max

Hub de comando centralizado para automacoes headless com Playwright.
Interface multi-tab em Dark Mode (CustomTkinter).

## Funcionalidades

- **Aba Executar** - seleciona um script `.py` da pasta `automacoes/`, digita o prompt e roda no background
- **Aba Perfis e Configs** - mapeamento do Chrome User Data (local, nunca sobe pro repo)
- **Aba Gravador (Codegen)** - abre o Playwright Codegen em qualquer site e gera o script automaticamente
- **Aba Terminal de Aura** - console integrado com logs em tempo real estilo hacker

## Instalacao

```bash
pip install -r requirements.txt
playwright install chromium
```

## Como usar

```bash
python automator_hub.py
```

## Estrutura

```
ghost_automator_hub/
├── automator_hub.py            # Hub central com GUI multi-tab
├── requirements.txt
├── .gitignore
├── README.md
├── prompts.txt                 # Prompts de exemplo para o modo batch
├── automacoes/
│   ├── flow_hub.py             # Script para o Google Flow (GUI)
│   └── flow_batch.py          # Script batch: le prompts.txt e gera uma imagem por linha
└── perfis/                    # NUNCA sobe pro GitHub (bloqueado no .gitignore)
```

## Scripts disponiveis

### `flow_hub.py` (via Hub ou direto)
```bash
python automacoes/flow_hub.py "Um samurai gato em neon Tokyo, 4k"
```

### `flow_batch.py` (gera N imagens de uma vez)
```bash
python automacoes/flow_batch.py prompts.txt
```

## Antes de rodar

Em `automacoes/flow_hub.py` e `automacoes/flow_batch.py`, ajusta a linha:

```python
CAMINHO_PERFIL = r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
```

Substitui `SEU_USUARIO` pelo teu nome de usuario do Windows.

---

Feito com Playwright + CustomTkinter. Zero mouse sequestrado. Zero janela pulando na tela.
