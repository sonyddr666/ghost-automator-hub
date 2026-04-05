#!/usr/bin/env python3
"""
api_server.py
Ghost Automator - API Fantasma

Transforma o Hub num servidor FastAPI local (localhost:8000).
Qualquer front-end, portal ou script pode invocar uma geracao via POST.

Instalar: pip install fastapi uvicorn
Rodar:    python api_server.py

Endpoints:
  POST /gerar          - inicia geracao de imagem com prompt
  GET  /status/{id}    - checa status de uma tarefa
  GET  /historico      - lista todas as geracoes
  GET  /health         - health check
"""

import os
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright

# Opcional: notificacao Telegram
try:
    from notificador_telegram import enviar_imagem
    TELEGRAM_ATIVO = True
except ImportError:
    TELEGRAM_ATIVO = False

# Config
CAMINHO_PERFIL = os.getenv(
    "CHROME_USER_DATA",
    r"C:\Users\SEU_USUARIO\AppData\Local\Google\Chrome\User Data"
)
PASTA_OUTPUT = Path("geracoes_flow")
PASTA_OUTPUT.mkdir(exist_ok=True)

# Estado em memoria das tarefas
tarefas: dict = {}

app = FastAPI(
    title="Ghost Automator API",
    description="API Fantasma que orquestra o Playwright headless para gerar imagens no Flow.",
    version="1.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class GeracaoRequest(BaseModel):
    prompt: str
    modelo: Optional[str] = "Nano Banana 2"
    resolucao: Optional[str] = "x2"
    notificar_telegram: Optional[bool] = True


class GeracaoResponse(BaseModel):
    id: str
    status: str
    mensagem: str
    prompt: str
    criado_em: str


async def executar_geracao(task_id: str, req: GeracaoRequest):
    tarefas[task_id]["status"] = "rodando"

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=CAMINHO_PERFIL,
            headless=True,
            args=["--headless=new", "--no-first-run", "--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            await page.goto("https://labs.google/flow", wait_until="networkidle")
            await page.wait_for_timeout(1500)

            btn_popup = page.locator("text='Comece ja'")
            if await btn_popup.is_visible(timeout=3000):
                await btn_popup.click()
                await page.wait_for_timeout(1000)

            btn_novo = page.locator("text='+ Novo projeto'")
            if await btn_novo.is_visible(timeout=3000):
                await btn_novo.first.click()
            else:
                await page.locator("button:has-text('Novo projeto')").first.click()

            textarea = page.locator("textarea[placeholder*='O que voce quer criar']")
            await textarea.wait_for(state="visible")

            btn_model = page.locator(f"button:has-text('{req.modelo}')").first
            if await btn_model.is_visible(timeout=2000):
                await btn_model.click()
                await page.wait_for_timeout(800)
                btn_res = page.locator(f"button:has-text('{req.resolucao}')").first
                if await btn_res.is_visible(timeout=2000):
                    await btn_res.click()
                    await page.wait_for_timeout(800)

            await textarea.fill("")
            await textarea.type(req.prompt, delay=25)
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

            tarefas[task_id]["status"] = "concluido"
            tarefas[task_id]["arquivo"] = str(dest)
            tarefas[task_id]["finalizado_em"] = datetime.now().isoformat()

            # Notifica o Telegram se ativo
            if req.notificar_telegram and TELEGRAM_ATIVO:
                await enviar_imagem(str(dest), req.prompt)

        except Exception as e:
            tarefas[task_id]["status"] = "erro"
            tarefas[task_id]["erro"] = str(e)
        finally:
            await context.close()


@app.post("/gerar", response_model=GeracaoResponse)
async def gerar(req: GeracaoRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())[:8]
    tarefas[task_id] = {
        "id": task_id,
        "status": "na_fila",
        "prompt": req.prompt,
        "criado_em": datetime.now().isoformat(),
        "arquivo": None,
        "erro": None
    }
    background_tasks.add_task(executar_geracao, task_id, req)
    return GeracaoResponse(
        id=task_id,
        status="na_fila",
        mensagem="Poltergeist invocado. Geracao iniciada em background.",
        prompt=req.prompt,
        criado_em=tarefas[task_id]["criado_em"]
    )


@app.get("/status/{task_id}")
async def status(task_id: str):
    if task_id not in tarefas:
        return {"erro": "Tarefa nao encontrada"}
    return tarefas[task_id]


@app.get("/historico")
async def historico():
    return list(tarefas.values())


@app.get("/health")
async def health():
    return {"status": "fantasma operacional", "versao": "1.5.0"}


if __name__ == "__main__":
    print("Ghost Automator API rodando em http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
