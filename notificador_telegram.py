#!/usr/bin/env python3
"""
notificador_telegram.py
Webhook de Retorno Termico

Quando uma imagem eh gerada, esse modulo dispara o PNG direto
no teu Telegram pessoal ou grupo privado.

Config necessaria (coloca no .env ou muda as constantes abaixo):
  TELEGRAM_BOT_TOKEN  - token do bot (via @BotFather)
  TELEGRAM_CHAT_ID    - teu chat_id pessoal (via @userinfobot)

Instalar: pip install python-telegram-bot
"""

import os
from pathlib import Path

try:
    import telegram
    TELEGRAM_DISPONIVEL = True
except ImportError:
    TELEGRAM_DISPONIVEL = False

# Pega do .env ou substitui direto aqui
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_AQUI")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID",   "SEU_CHAT_ID_AQUI")


async def enviar_imagem(caminho: str, prompt: str = ""):
    if not TELEGRAM_DISPONIVEL:
        print("[Telegram] python-telegram-bot nao instalado. Pulando notificacao.")
        return

    if TELEGRAM_BOT_TOKEN == "SEU_TOKEN_AQUI":
        print("[Telegram] Configure TELEGRAM_BOT_TOKEN no .env ou no arquivo.")
        return

    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        caption = f"Imagem gerada com sucesso!\nPrompt: {prompt[:200]}" if prompt else "Imagem gerada!"

        with open(caminho, "rb") as foto:
            await bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=foto,
                caption=caption
            )
        print(f"[Telegram] PNG enviado: {caminho}")
    except Exception as e:
        print(f"[Telegram] Erro ao enviar: {e}")


async def enviar_texto(mensagem: str):
    if not TELEGRAM_DISPONIVEL:
        return
    if TELEGRAM_BOT_TOKEN == "SEU_TOKEN_AQUI":
        return
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem)
    except Exception as e:
        print(f"[Telegram] Erro ao enviar texto: {e}")


# Teste rapido: python notificador_telegram.py caminho/da/imagem.png
if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 2:
        print("Uso: python notificador_telegram.py imagem.png")
        sys.exit(1)

    asyncio.run(enviar_imagem(sys.argv[1], "Teste manual do notificador"))
