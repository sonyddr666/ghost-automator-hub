#!/usr/bin/env python3
"""
automator_hub.py
Ghost Automator 1.5 Pro Plus Max

Hub GUI multi-tab. Por padrao roda 100% local (Modo PC).
Modos avancados (Telegram, API) so aparecem se ativados no .env.
"""

import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

from config import (
    PASTA_AUTOMACOES, PASTA_PERFIS, PASTA_GERACOES,
    CHROME_USER_DATA, MODO_AVANCADO, MODO_TELEGRAM, MODO_API
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AutomatorProMax(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ghost Automator 1.5 Pro Plus Max")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._montar_sidebar()
        self._montar_tabview()
        self.carregar_dados()

    # ==========================================
    # SIDEBAR
    # ==========================================
    def _montar_sidebar(self):
        sb = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#111111")
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            sb, text="GHOST HUB\nPro Max",
            font=("Consolas", 22, "bold"), text_color="#00ffcc"
        ).grid(row=0, column=0, padx=20, pady=(30, 10))

        # Badge de modo
        modo_txt  = "MODO AVANCADO ON" if MODO_AVANCADO else "MODO PC"
        modo_cor  = "#e67e22"           if MODO_AVANCADO else "#00ffcc"
        ctk.CTkLabel(
            sb, text=modo_txt,
            font=("Consolas", 10, "bold"), text_color=modo_cor
        ).grid(row=1, column=0, padx=20, pady=(0, 10))

        ctk.CTkButton(
            sb, text="Recarregar Matriz",
            command=self.carregar_dados,
            fg_color="#333333", hover_color="#555555"
        ).grid(row=2, column=0, padx=20, pady=6)

        # Botao API so aparece se MODO_API ativo
        if MODO_API:
            ctk.CTkButton(
                sb, text="Iniciar API Server",
                command=self._iniciar_api,
                fg_color="#1a5276", hover_color="#2e86c1"
            ).grid(row=3, column=0, padx=20, pady=6)

        # Indicadores de modulos
        tg_cor  = "#27ae60" if MODO_TELEGRAM else "#555555"
        api_cor = "#27ae60" if MODO_API      else "#555555"
        ctk.CTkLabel(sb, text=f"Telegram: {'ON' if MODO_TELEGRAM else 'off'}",
                     font=("Consolas", 10), text_color=tg_cor
                     ).grid(row=4, column=0, padx=20, pady=2)
        ctk.CTkLabel(sb, text=f"API REST: {'ON' if MODO_API else 'off'}",
                     font=("Consolas", 10), text_color=api_cor
                     ).grid(row=5, column=0, padx=20, pady=2)

        ctk.CTkLabel(
            sb, text="Existindo e Andando",
            font=("Arial", 10), text_color="gray"
        ).grid(row=7, column=0, padx=20, pady=20, sticky="s")

    # ==========================================
    # TABVIEW
    # ==========================================
    def _montar_tabview(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.tabview.add("Executar")
        self.tabview.add("Perfis e Configs")
        self.tabview.add("Gravador (Codegen)")
        self.tabview.add("Terminal de Aura")

        # Aba extra so se modo avancado ativo
        if MODO_AVANCADO:
            self.tabview.add("Modo Avancado")
            self._montar_aba_avancado()

        self._montar_aba_executar()
        self._montar_aba_perfis()
        self._montar_aba_gravador()
        self._montar_aba_terminal()

    # ==========================================
    # ABA EXECUTAR
    # ==========================================
    def _montar_aba_executar(self):
        tab = self.tabview.tab("Executar")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Escolha o Script:",
                     font=("Arial", 14, "bold")
                     ).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.menu_scripts = ctk.CTkOptionMenu(tab, values=["Vazio"], width=320)
        self.menu_scripts.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Prompt / Argumentos:",
                     font=("Arial", 14, "bold")
                     ).grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")

        self.txt_prompt = ctk.CTkTextbox(tab, height=100)
        self.txt_prompt.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.txt_prompt.insert("0.0", "Um samurai cibernetico, 4k cinematic...")

        self.btn_run = ctk.CTkButton(
            tab, text="INICIAR COLAPSO ESTETICO",
            height=50, font=("Arial", 14, "bold"),
            fg_color="#27ae60", hover_color="#2ecc71",
            command=self._iniciar_thread
        )
        self.btn_run.grid(row=4, column=0, padx=20, pady=30, sticky="ew")

    # ==========================================
    # ABA PERFIS
    # ==========================================
    def _montar_aba_perfis(self):
        tab = self.tabview.tab("Perfis e Configs")

        ctk.CTkLabel(tab, text="Configuracao do Chrome",
                     font=("Arial", 16, "bold")
                     ).pack(pady=20)

        ctk.CTkLabel(tab, text="Caminho do perfil Chrome (User Data):",
                     font=("Arial", 12)
                     ).pack()

        self.entry_perfil = ctk.CTkEntry(tab, width=450,
                                         placeholder_text=CHROME_USER_DATA)
        self.entry_perfil.pack(pady=10)
        self.entry_perfil.insert(0, CHROME_USER_DATA)

        ctk.CTkButton(
            tab, text="Salvar no .env",
            command=self._salvar_perfil
        ).pack(pady=10)

        ctk.CTkLabel(
            tab,
            text="Dica: edita o .env na raiz do projeto para persistir essa configuracao.",
            text_color="gray", font=("Arial", 11)
        ).pack(pady=6)

    # ==========================================
    # ABA GRAVADOR
    # ==========================================
    def _montar_aba_gravador(self):
        tab = self.tabview.tab("Gravador (Codegen)")

        ctk.CTkLabel(tab, text="Grave Automacoes sem Escrever Codigo",
                     font=("Arial", 16, "bold")
                     ).pack(pady=20)

        ctk.CTkLabel(
            tab,
            text="Abre o Playwright Inspector no site escolhido.\n"
                 "Cada clique vira codigo Python automaticamente.\n"
                 "Salva o .py gerado em automacoes/ e recarrega a matriz.",
            justify="center"
        ).pack(pady=10)

        self.entry_url = ctk.CTkEntry(tab, width=420,
                                      placeholder_text="https://site.que.quer.automatizar.com")
        self.entry_url.pack(pady=20)

        ctk.CTkButton(
            tab, text="INICIAR GRAVACAO",
            height=45, fg_color="#c0392b", hover_color="#e74c3c",
            command=self._rodar_gravador
        ).pack(pady=10)

    # ==========================================
    # ABA TERMINAL
    # ==========================================
    def _montar_aba_terminal(self):
        tab = self.tabview.tab("Terminal de Aura")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.console = ctk.CTkTextbox(
            tab, font=("Consolas", 12),
            fg_color="#000000", text_color="#00ff00"
        )
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._log("SISTEMA INICIADO. Modo PC ativo.")
        if MODO_AVANCADO:
            self._log("MODO AVANCADO detectado no .env.")
            if MODO_TELEGRAM: self._log("  Telegram: ON")
            if MODO_API:      self._log("  API REST: ON (rode api_server.py)")

    # ==========================================
    # ABA MODO AVANCADO (so se MODO_AVANCADO=true)
    # ==========================================
    def _montar_aba_avancado(self):
        tab = self.tabview.tab("Modo Avancado")

        ctk.CTkLabel(tab, text="Modulos Externos",
                     font=("Arial", 16, "bold")
                     ).pack(pady=20)

        # Status Telegram
        tg_status = "ATIVO" if MODO_TELEGRAM else "inativo (ATIVAR_TELEGRAM=true no .env)"
        ctk.CTkLabel(
            tab,
            text=f"Telegram: {tg_status}",
            text_color="#27ae60" if MODO_TELEGRAM else "gray"
        ).pack(pady=6)

        # Status API
        api_status = "ATIVO" if MODO_API else "inativo (ATIVAR_API=true no .env)"
        ctk.CTkLabel(
            tab,
            text=f"API REST: {api_status}",
            text_color="#27ae60" if MODO_API else "gray"
        ).pack(pady=6)

        ctk.CTkLabel(
            tab,
            text="Para ligar cada modulo, edita o .env na raiz do projeto.",
            text_color="gray", font=("Arial", 11)
        ).pack(pady=20)

        if MODO_API:
            ctk.CTkButton(
                tab, text="Abrir Docs da API (localhost:8000/docs)",
                command=lambda: subprocess.Popen(["start", "http://localhost:8000/docs"], shell=True)
            ).pack(pady=10)

    # ==========================================
    # LOGICA
    # ==========================================
    def carregar_dados(self):
        arquivos = sorted(p.name for p in PASTA_AUTOMACOES.glob("*.py"))
        if arquivos:
            self.menu_scripts.configure(values=arquivos)
            self.menu_scripts.set(arquivos[0])
            self._log(f"Carregados {len(arquivos)} scripts.")
        else:
            self.menu_scripts.configure(values=["Nenhum script encontrado"])
            self.menu_scripts.set("Nenhum script encontrado")

    def _log(self, msg):
        hora = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{hora}] {msg}\n")
        self.console.see("end")

    def _salvar_perfil(self):
        novo = self.entry_perfil.get().strip()
        env_path = Path(".env")
        linhas = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
        novas = [l for l in linhas if not l.startswith("CHROME_USER_DATA")]
        novas.append(f"CHROME_USER_DATA={novo}")
        env_path.write_text("\n".join(novas) + "\n", encoding="utf-8")
        self._log(f"Perfil salvo no .env: {novo}")

    def _rodar_gravador(self):
        url = self.entry_url.get().strip() or "about:blank"
        self._log(f"Abrindo codegen: {url}")
        try:
            subprocess.Popen(["playwright", "codegen", url])
        except Exception as e:
            self._log(f"Erro ao abrir codegen: {e}")

    def _iniciar_api(self):
        self._log("Iniciando API server em localhost:8000...")
        threading.Thread(
            target=lambda: subprocess.run(["python", "api_server.py"]),
            daemon=True
        ).start()

    def _iniciar_thread(self):
        threading.Thread(target=self._executar_script).start()

    def _executar_script(self):
        script = self.menu_scripts.get()
        prompt = self.txt_prompt.get("0.0", "end").strip()

        if script in ("Nenhum script encontrado", "Vazio") or not script:
            self._log("ERRO: Nenhum script selecionado.")
            messagebox.showerror("Erro", "Seleciona um script valido!")
            return

        caminho = PASTA_AUTOMACOES / script
        if not caminho.exists():
            self._log(f"ERRO: {caminho} nao encontrado.")
            return

        self._log(f"Invocando: {script}")
        self.btn_run.configure(state="disabled", text="TRABALHANDO...")

        try:
            proc = subprocess.run(
                ["python", str(caminho), prompt],
                capture_output=True, text=True
            )
            if proc.returncode == 0:
                self._log(f"SUCESSO: {script} concluido.")
                if proc.stdout:
                    self._log(f"Output: {proc.stdout.strip()}")
            else:
                self._log(f"ERRO: {proc.stderr.strip()}")
        except Exception as e:
            self._log(f"ERRO FATAL: {e}")
        finally:
            self.btn_run.configure(state="normal", text="INICIAR COLAPSO ESTETICO")


if __name__ == "__main__":
    app = AutomatorProMax()
    app.mainloop()
