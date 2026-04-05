#!/usr/bin/env python3
"""
ghost_automator_hub.py
Ghost Automator 1.5 Pro Plus Max
Hub com abas: Executar, Perfis, Gravador (Codegen) e Terminal.
Le scripts de ./automacoes/, passa o prompt via sys.argv e roda via subprocess.
"""

import os
import sys
import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# ==========================================
# ESTETICA DE AURA: DARK MODE SUPREMO
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AutomatorProMax(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ghost Automator 1.5 Pro Plus Max")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.pasta_automacoes = "automacoes"
        self.pasta_perfis = "perfis"
        for pasta in [self.pasta_automacoes, self.pasta_perfis]:
            if not os.path.exists(pasta):
                os.makedirs(pasta)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar,
            text="GHOST HUB\nPro Max",
            font=("Consolas", 22, "bold"),
            text_color="#00ffcc"
        )
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_atualizar = ctk.CTkButton(
            self.sidebar,
            text="Recarregar Matriz",
            command=self.carregar_dados,
            fg_color="#333333",
            hover_color="#555555"
        )
        self.btn_atualizar.grid(row=1, column=0, padx=20, pady=10)

        self.lbl_status = ctk.CTkLabel(
            self.sidebar,
            text="Status: Existindo e Andando",
            font=("Arial", 10),
            text_color="gray"
        )
        self.lbl_status.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # Tabview
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.tabview.add("Executar")
        self.tabview.add("Perfis e Configs")
        self.tabview.add("Gravador (Codegen)")
        self.tabview.add("Terminal de Aura")

        self.montar_aba_executar()
        self.montar_aba_perfis()
        self.montar_aba_gravador()
        self.montar_aba_terminal()

        self.carregar_dados()

    def montar_aba_executar(self):
        tab = self.tabview.tab("Executar")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Escolha o Script:", font=("Arial", 14, "bold")).grid(
            row=0, column=0, padx=20, pady=(20, 5), sticky="w"
        )

        self.menu_scripts = ctk.CTkOptionMenu(tab, values=["Vazio"], width=300)
        self.menu_scripts.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        ctk.CTkLabel(tab, text="Prompt / Argumentos:", font=("Arial", 14, "bold")).grid(
            row=2, column=0, padx=20, pady=(20, 5), sticky="w"
        )

        self.txt_prompt = ctk.CTkTextbox(tab, height=100)
        self.txt_prompt.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.txt_prompt.insert("0.0", "Um samurai cibernetico no Rio de Janeiro, 4k...")

        self.btn_run = ctk.CTkButton(
            tab,
            text="INICIAR COLAPSO ESTETICO",
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="#27ae60",
            hover_color="#2ecc71",
            command=self.iniciar_thread_execucao
        )
        self.btn_run.grid(row=4, column=0, padx=20, pady=30, sticky="ew")

    def montar_aba_perfis(self):
        tab = self.tabview.tab("Perfis e Configs")

        ctk.CTkLabel(tab, text="Mapeamento de Perfis do Chrome", font=("Arial", 16, "bold")).pack(pady=20)

        self.entry_perfil = ctk.CTkEntry(
            tab,
            width=400,
            placeholder_text="C:/Users/SEU_NOME/AppData/Local/Google/Chrome/User Data"
        )
        self.entry_perfil.pack(pady=10)

        ctk.CTkButton(
            tab,
            text="Salvar Perfil Padrao",
            command=lambda: self.log_no_terminal("Perfil salvo! (Simulado por enquanto)")
        ).pack(pady=10)

        ctk.CTkLabel(
            tab,
            text="* No futuro, os scripts puxarao a rota daqui automaticamente.",
            text_color="gray"
        ).pack(pady=10)

    def montar_aba_gravador(self):
        tab = self.tabview.tab("Gravador (Codegen)")

        ctk.CTkLabel(tab, text="Grave sua Automacao sem Escrever Codigo", font=("Arial", 16, "bold")).pack(pady=20)

        ctk.CTkLabel(
            tab,
            text="Isso vai abrir o Playwright Inspector.\nTudo que voce clicar sera transformado em um script Python.\nCopie o codigo, salve como .py na pasta automacoes e recarregue a matriz.",
            justify="center"
        ).pack(pady=10)

        self.entry_url_record = ctk.CTkEntry(
            tab,
            width=400,
            placeholder_text="Qual site tu quer invadir? Ex: https://google.com"
        )
        self.entry_url_record.pack(pady=20)

        ctk.CTkButton(
            tab,
            text="INICIAR GRAVACAO",
            height=50,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            command=self.rodar_gravador
        ).pack(pady=10)

    def montar_aba_terminal(self):
        tab = self.tabview.tab("Terminal de Aura")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.console = ctk.CTkTextbox(
            tab,
            font=("Consolas", 12),
            fg_color="#000000",
            text_color="#00ff00"
        )
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_no_terminal("SISTEMA INICIADO. A matriz esta pronta para receber comandos.")

    def carregar_dados(self):
        if not os.path.exists(self.pasta_automacoes):
            os.makedirs(self.pasta_automacoes)
        arquivos = [f for f in os.listdir(self.pasta_automacoes) if f.endswith(".py")]
        if arquivos:
            self.menu_scripts.configure(values=arquivos)
            self.menu_scripts.set(arquivos[0])
            self.log_no_terminal(f"Carregados {len(arquivos)} scripts de alma.")
        else:
            self.menu_scripts.configure(values=["Nenhuma alma encontrada"])
            self.menu_scripts.set("Nenhuma alma encontrada")

    def log_no_terminal(self, mensagem):
        hora = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{hora}] {mensagem}\n")
        self.console.see("end")

    def rodar_gravador(self):
        url = self.entry_url_record.get()
        if not url:
            url = "about:blank"
        self.log_no_terminal(f"Abrindo fenda de gravacao para: {url}")
        try:
            subprocess.Popen(["playwright", "codegen", url])
        except Exception as e:
            self.log_no_terminal(f"Erro ao abrir o codegen: {e}")

    def iniciar_thread_execucao(self):
        thread = threading.Thread(target=self.executar_script)
        thread.start()

    def executar_script(self):
        script = self.menu_scripts.get()
        prompt = self.txt_prompt.get("0.0", "end").strip()

        if script in ("Nenhuma alma encontrada", "Vazio") or not script:
            self.log_no_terminal("ERRO: Tentou rodar o vazio. Ta morno.")
            messagebox.showerror("Erro de Aura", "Seleciona um script valido!")
            return

        caminho_script = os.path.join(self.pasta_automacoes, script)
        if not os.path.exists(caminho_script):
            self.log_no_terminal(f"ERRO: Script nao encontrado: {caminho_script}")
            messagebox.showerror("Erro", "Arquivo nao encontrado.")
            return

        self.log_no_terminal(f"INVOCANDO ENTIDADE: {script}")
        self.btn_run.configure(state="disabled", text="MATRIZ TRABALHANDO...")

        try:
            processo = subprocess.run(
                ["python", caminho_script, prompt],
                capture_output=True,
                text=True
            )
            if processo.returncode == 0:
                self.log_no_terminal(f"SUCESSO: O poltergeist '{script}' cumpriu o pacto.")
                if processo.stdout:
                    self.log_no_terminal(f"Output: {processo.stdout}")
            else:
                self.log_no_terminal(f"COLAPSO: Falha na execucao.\nErro: {processo.stderr}")
        except Exception as e:
            self.log_no_terminal(f"ERRO FATAL: {e}")
        finally:
            self.btn_run.configure(state="normal", text="INICIAR COLAPSO ESTETICO")


if __name__ == "__main__":
    app = AutomatorProMax()
    app.mainloop()
