#!/usr/bin/env python3
"""
config.py
Central de configuracao do Ghost Automator Hub.

Todos os modulos importam daqui.
Para ativar modos avancados, edita o .env (nao o codigo).
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv opcional

# ==========================================
# MODO PC (sempre ativo, nucleo do sistema)
# ==========================================
CHROME_USER_DATA = os.getenv(
    "CHROME_USER_DATA",
    r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
)

PASTA_AUTOMACOES = Path("automacoes")
PASTA_GERACOES   = Path("geracoes_flow")
PASTA_PERFIS     = Path("perfis")

for pasta in [PASTA_AUTOMACOES, PASTA_GERACOES, PASTA_PERFIS]:
    pasta.mkdir(exist_ok=True)

# ==========================================
# MODO AVANCADO (desligado por padrao)
# So acorda se ATIVAR_MODO_AVANCADO=true no .env
# ==========================================
MODO_AVANCADO = os.getenv("ATIVAR_MODO_AVANCADO", "false").lower() == "true"

# Sub-flags (so importam se MODO_AVANCADO=true)
MODO_TELEGRAM  = MODO_AVANCADO and os.getenv("ATIVAR_TELEGRAM",  "false").lower() == "true"
MODO_API       = MODO_AVANCADO and os.getenv("ATIVAR_API",       "false").lower() == "true"

# Credenciais Telegram (so usadas se MODO_TELEGRAM=true)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID",   "")

# Porta da API (so usada se MODO_API=true)
API_PORT = int(os.getenv("API_PORT", "8000"))
