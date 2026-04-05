#!/usr/bin/env python3
"""
flow_batch.py
Versao batch do Flow: le prompts de um .txt e gera um PNG por linha.

Uso:
    python flow_batch.py prompts.txt
"""

import sys
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

CAMINHO_PERFIL = r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
PASTA_OUTPUT = Path("geracoes_flow")
PASTA_OUTPUT.mkdir(exist_ok=True)


async def gerar(prompt):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=CAMINHO_PERFIL,
            headless=True,
            args=["--headless=new"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            await page.goto("https://labs.google/flow", wait_until="networkidle")
            await page.wait_for_timeout(1500)

            btn_popup = page.locator("text='Comece ja'")
            if await btn_popup.is_visible(timeout=3000):
                await btn_popup.click()

            btn_novo = page.locator("text='+ Novo projeto'")
            if await btn_novo.is_visible(timeout=3000):
                await btn_novo.first.click()
            else:
                await page.locator("button:has-text('Novo projeto')").first.click()

            textarea = page.locator("textarea[placeholder*='O que voce quer criar']")
            await textarea.wait_for(state="visible")

            btn_model = page.locator("button:has-text('Nano Banana 2')").first
            if not await btn_model.is_visible(timeout=2000):
                btn_model = page.locator("button:has-text('Nano Banana')").first
            if await btn_model.is_visible():
                await btn_model.click()
                await page.wait_for_timeout(800)
                btn_x2 = page.locator("button:has-text('x2')").first
                if await btn_x2.is_visible(timeout=2000):
                    await btn_x2.click()

            await textarea.fill("")
            await textarea.type(prompt, delay=25)
            await page.keyboard.press("Enter")

            img = page.locator("img[alt='Generated image'], img[src*='blob']").first
            await img.wait_for(state="visible", timeout=120_000)
            await img.click()

            btn_dow = page.locator(
                "button[aria-label='Baixar'], button:has-text('Baixar'), .download-icon"
            ).first
            async with page.expect_download() as dl_info:
                await btn_dow.click()
                download = await dl_info.value
                dest = PASTA_OUTPUT / download.suggested_filename
                await download.save_as(str(dest))
                print(f"Salvo: {dest.name}")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            await context.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python flow_batch.py prompts.txt")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo {path} nao encontrado.")
        sys.exit(1)

    prompts = [p.strip() for p in path.read_text(encoding="utf-8").splitlines() if p.strip()]
    print(f"Gerando {len(prompts)} imagens...")

    for i, p in enumerate(prompts, 1):
        print(f"{i}/{len(prompts)}: {p[:50]}...")
        asyncio.run(gerar(p))
