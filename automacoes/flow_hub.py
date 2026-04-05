#!/usr/bin/env python3
"""
flow_hub.py
Script de exemplo para o Ghost Automator 1.5 Pro Plus Max.
Recebe um prompt via sys.argv e usa o perfil real do Chrome para gerar imagem no Flow.

Uso:
    python flow_hub.py "Um samurai gato em neon Tokyo, 4k, cinematic"
"""

import sys
import asyncio
import os
from playwright.async_api import async_playwright

# Ajusta esse caminho pro teu usuario do Windows
CAMINHO_PERFIL = r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"

PASTA_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "geracoes_flow")
os.makedirs(PASTA_OUTPUT, exist_ok=True)


async def main():
    if len(sys.argv) < 2:
        print("Uso: python flow_hub.py \"Um samurai gato em neon Tokyo\"")
        return

    prompt = " ".join(sys.argv[1:])
    print(f"Prompt recebido: {prompt}")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=CAMINHO_PERFIL,
            headless=True,
            args=["--headless=new", "--no-first-run", "--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            print("Acessando o Flow...")
            await page.goto("https://labs.google/flow", wait_until="networkidle")
            await page.wait_for_timeout(1500)

            # Popup Comece ja
            btn_popup = page.locator("text='Comece ja'")
            if await btn_popup.is_visible(timeout=3000):
                await btn_popup.click()
                await page.wait_for_timeout(1000)

            # Novo projeto
            btn_novo = page.locator("text='+ Novo projeto'")
            if await btn_novo.is_visible(timeout=3000):
                await btn_novo.first.click()
            else:
                await page.locator("button:has-text('Novo projeto')").first.click()

            # Textarea do prompt
            textarea = page.locator("textarea[placeholder*='O que voce quer criar']")
            await textarea.wait_for(state="visible")

            # Nano Banana 2 x2
            btn_model = page.locator("button:has-text('Nano Banana 2')").first
            if not await btn_model.is_visible(timeout=2000):
                btn_model = page.locator("button:has-text('Nano Banana')").first
            if await btn_model.is_visible():
                await btn_model.click()
                await page.wait_for_timeout(800)
                btn_x2 = page.locator("button:has-text('x2')").first
                if await btn_x2.is_visible(timeout=2000):
                    await btn_x2.click()
                    await page.wait_for_timeout(800)

            # Envia o prompt
            await textarea.fill("")
            await textarea.type(prompt, delay=25)
            await page.keyboard.press("Enter")

            # Espera a imagem
            print("Aguardando geracao da imagem (ate 2 min)...")
            img = page.locator("img[alt='Generated image'], img[src*='blob']").first
            await img.wait_for(state="visible", timeout=120_000)
            await img.click()

            # Download
            btn_dow = page.locator(
                "button[aria-label='Baixar'], button:has-text('Baixar'), .download-icon"
            ).first
            async with page.expect_download() as dl_info:
                await btn_dow.click()
                download = await dl_info.value
                dest = os.path.join(PASTA_OUTPUT, download.suggested_filename)
                await download.save_as(dest)
                print(f"Imagem salva: {dest}")
                os.startfile(dest)

        except Exception as e:
            print(f"Erro no Flow: {e}")
            await page.screenshot(path="erro_poltergeist.png")
        finally:
            await context.close()


if __name__ == "__main__":
    asyncio.run(main())
