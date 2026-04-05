#!/usr/bin/env python3
"""
flow_swarm.py
Modo Enxame Headless (Swarm Mode)

Abre N contextos paralelos do Playwright e gera multiplas imagens
de uma vez, sem fila. Puro asyncio pesado.

Uso:
  python automacoes/flow_swarm.py prompts.txt
  python automacoes/flow_swarm.py prompts.txt --workers 4
"""

import sys
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

CAMINHO_PERFIL = os.getenv(
    "CHROME_USER_DATA",
    r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
)
PASTA_OUTPUT = Path("geracoes_flow")
PASTA_OUTPUT.mkdir(exist_ok=True)

DEFAULT_WORKERS = 3  # quantos contextos paralelos abrir


async def gerar_uma(semaforo: asyncio.Semaphore, prompt: str, indice: int, total: int):
    async with semaforo:
        print(f"[{indice}/{total}] Iniciando: {prompt[:50]}...")
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=CAMINHO_PERFIL,
                headless=True,
                args=["--headless=new", "--no-first-run"]
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
                if await btn_model.is_visible(timeout=2000):
                    await btn_model.click()
                    await page.wait_for_timeout(800)
                    btn_x2 = page.locator("button:has-text('x2')").first
                    if await btn_x2.is_visible(timeout=2000):
                        await btn_x2.click()

                await textarea.fill("")
                await textarea.type(prompt, delay=20)
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
                    print(f"[{indice}/{total}] Salvo: {dest.name}")

            except Exception as e:
                print(f"[{indice}/{total}] Erro: {e}")
            finally:
                await context.close()


async def swarm(prompts: list[str], workers: int):
    semaforo = asyncio.Semaphore(workers)
    tarefas = [
        gerar_uma(semaforo, prompt, i + 1, len(prompts))
        for i, prompt in enumerate(prompts)
    ]
    print(f"Swarm ativado: {len(prompts)} prompts | {workers} workers paralelos")
    await asyncio.gather(*tarefas)
    print(f"Enxame concluido. {len(prompts)} imagens em geracoes_flow/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python flow_swarm.py prompts.txt [--workers N]")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo {path} nao encontrado.")
        sys.exit(1)

    workers = DEFAULT_WORKERS
    if "--workers" in sys.argv:
        idx = sys.argv.index("--workers")
        workers = int(sys.argv[idx + 1])

    prompts = [p.strip() for p in path.read_text(encoding="utf-8").splitlines() if p.strip()]
    asyncio.run(swarm(prompts, workers))
