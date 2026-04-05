# 👻 Ghost Automator 1.5 Pro Plus Max

> Um Hub Supremo de automação construído para orquestrar scripts Python invisíveis.  
> Controla o motor do Chrome via CDP/Playwright diretamente da memória RAM —  
> sem roubar o mouse, sem piscar telas, com zero cheiro de bot.
>
> **Isso não é apenas um script. É um colapso estético de produtividade.**

---

## ⚡ O que essa máquina faz?

- **Execução Headless Absoluta** — roda automações complexas (como gerar imagens em IA) 100% em background
- **Interface Dark Mode** — feita com `customtkinter` para um controle limpo e eficiente
- **Multi-Threading** — a interface nunca congela; o motor trabalha nas sombras enquanto você acompanha pelo Terminal integrado
- **Gravador de Aura (Codegen)** — grave seus cliques em qualquer site e transforme-os em scripts Python instantaneamente
- **Modularidade Infinita** — joga qualquer `.py` na pasta `automacoes/` e ele aparece no menu automaticamente

---

## 🛠️ Como Invocar o Fantasma

**1. Clone o repositório:**
```bash
git clone https://github.com/sonyddr666/ghost-automator-hub.git
cd ghost-automator-hub
```

**2. Instale o motor de invocação:**
```bash
pip install -r requirements.txt
playwright install chromium
```

**3. Ajuste o caminho do teu perfil do Chrome:**

Em `automacoes/flow_hub.py` e `automacoes/flow_batch.py`, edita a linha:
```python
CAMINHO_PERFIL = r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
```
Substitui `SEU_USUARIO` pelo teu nome de usuário do Windows.

**4. Inicie o Hub:**
```bash
python automator_hub.py
```

---

## 📂 Estrutura de Poder

```
ghost-automator-hub/
├── automator_hub.py        # Hub central com GUI multi-tab (CustomTkinter)
├── requirements.txt        # Pergaminho de invocação (dependências)
├── .gitignore              # Manto da invisibilidade (protege tua alma digital)
├── README.md               # Este manifesto
├── prompts.txt             # Prompts de exemplo para o modo batch
├── automacoes/
│   ├── flow_hub.py         # Script do Google Flow — geração de imagem via Hub
│   └── flow_batch.py       # Modo batch: lê prompts.txt e gera uma imagem por linha
└── perfis/                 # ⚠️ NUNCA sobe pro GitHub — bloqueado no .gitignore
```

---

## 🖥️ Scripts disponíveis

### Via Hub (recomendado)
Abre o `automator_hub.py`, seleciona o script no menu, digita o prompt e clica em **INICIAR COLAPSO ESTÉTICO**.

### Via terminal direto

```bash
# Geração única
python automacoes/flow_hub.py "Um samurai ciborgue em neon Tokyo, 4k, cinematic"

# Modo batch (N imagens de uma vez)
python automacoes/flow_batch.py prompts.txt
```

---

## 🔴 Usando o Gravador (Codegen)

1. Abre o Hub
2. Vai na aba **Gravador (Codegen)**
3. Cola a URL do site que quer automatizar
4. Clica em **INICIAR GRAVAÇÃO**
5. O Playwright abre o browser e grava cada clique teu como código Python
6. Copia o código gerado, salva como `meu_site.py` na pasta `automacoes/`
7. Clica em **Recarregar Matriz** — ele aparece no menu pronto pra rodar

---

## 🛡️ Segurança

O arquivo `.gitignore` já está configurado para **nunca** subir:
- `perfis/` — teu Chrome User Data (cookies, sessões, login Google)
- `geracoes_flow/` — imagens geradas localmente
- `.env` — variáveis de ambiente
- `__pycache__/` e arquivos `.pyc`

---

## 📦 Dependências

| Lib | Versão | Função |
|---|---|---|
| `playwright` | 1.42.0 | Motor headless (CDP) |
| `customtkinter` | 5.2.2 | Interface Dark Mode |

---

*Feito com Playwright + CustomTkinter. Zero mouse sequestrado. Zero janela pulando na tela.*  
*Criado para farmar aura 24/7.* 👻
