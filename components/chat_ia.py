"""Página de consulta Groq usando os estilos da interface do grupo."""
import queue
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

import agente_ia
import armazenamento
from . import estilos as s
from .widgets import botao


class ChatIA:
    def __init__(self, app, pasta):
        self.app = app
        self.pasta = pasta
        self.frame = tk.Frame(app.content, bg=s.BG)
        self.frame.pack(fill="both", expand=True)
        self.resultados = queue.Queue()
        tk.Label(self.frame, text="Consulta de leitura aos registros",
                 bg=s.BG, fg=s.TEXT, font=(s.FONT, 11, "bold")).pack(anchor="w")
        tk.Label(self.frame, text="A resposta usa fatos calculados pelo sistema. "
                 "Aliases U1 e M1 substituem usuários e máquinas.",
                 bg=s.BG, fg=s.MUTED, wraplength=740, justify="left").pack(anchor="w", pady=8)
        self.conversa = ScrolledText(self.frame, wrap="word", bg=s.CARD, fg=s.TEXT,
                                    font=(s.FONT, 11), relief="flat", height=10,
                                    highlightthickness=1, highlightbackground=s.BORDER)
        self.conversa.pack(fill="both", expand=True, pady=8)
        self.conversa.configure(state="disabled")
        for pergunta, resposta in app.historico_ia:
            self.escrever("Você", pergunta)
            self.escrever("SentinelaLog", resposta)
        self.entrada = tk.Entry(self.frame, bg=s.FIELD, fg=s.TEXT,
                                insertbackground=s.TEXT, font=(s.FONT, 11), relief="flat",
                                highlightthickness=1, highlightbackground=s.BORDER, highlightcolor=s.BLUE)
        self.entrada.pack(fill="x", ipady=10, pady=8)
        self.entrada.bind("<Return>", lambda evento: self.enviar())
        controles = tk.Frame(self.frame, bg=s.BG)
        controles.pack(fill="x")
        self.enviar_botao = botao(controles, "Enviar pergunta", self.enviar, "#087e68")
        self.enviar_botao.pack(side="left", padx=(0, 8))
        botao(controles, "Configurar chave", self.configurar_chave).pack(side="left", padx=4)
        self.limpar_botao = botao(controles, "Limpar conversa", self.limpar)
        self.limpar_botao.pack(side="left", padx=4)
        self.status = tk.Label(self.frame, text="Pronto. Exemplo: quantas falhas foram registradas?",
                               bg=s.BG, fg=s.MUTED, anchor="w", wraplength=740)
        self.status.pack(fill="x", pady=10)

    def escrever(self, autor, texto):
        self.conversa.configure(state="normal")
        self.conversa.insert("end", autor + "\n" + texto + "\n\n")
        self.conversa.see("end")
        self.conversa.configure(state="disabled")

    def configurar_chave(self):
        chave = simpledialog.askstring("Chave Groq", "Cole sua GROQ_API_KEY. "
                    "A chave ficará somente na memória desta sessão.",
                    show="*", parent=self.app.root)
        if chave is not None:
            self.app.chave_groq = chave.strip()
            self.status.configure(text="Configuração da chave atualizada para esta sessão.")

    def limpar(self):
        if self.app.ia_ocupada:
            return
        self.app.historico_ia.clear()
        self.conversa.configure(state="normal")
        self.conversa.delete("1.0", "end")
        self.conversa.configure(state="disabled")
        self.status.configure(text="Conversa limpa. O registro local de consultas foi preservado.")

    def enviar(self):
        if self.app.ia_ocupada:
            return
        try:
            estado = armazenamento.carregar(self.pasta)
            preparado = agente_ia.preparar(self.entrada.get(), estado,
                                         [p for p, r in self.app.historico_ia])
        except (ValueError, OSError) as erro:
            messagebox.showerror("Consulta de IA", str(erro), parent=self.app.root)
            return
        if not messagebox.askyesno("Enviar para Groq", "Serão enviados fatos do laboratório "
                "com aliases, regras e a pergunta abaixo. Os nomes e as matrículas cadastrados "
                "são substituídos por aliases. Observações e auditoria ficam fora dos fatos. "
                "Confira a pergunta antes de autorizar.\n\n"
                + preparado["pergunta"] + "\n\nAutorizar esta consulta externa?",
                parent=self.app.root):
            return
        self.app.ia_ocupada = True
        self.enviar_botao.configure(state="disabled")
        self.limpar_botao.configure(state="disabled")
        self.entrada.delete(0, "end")
        self.escrever("Você", preparado["pergunta"])
        self.status.configure(text="Consultando a Groq… uma chamada, sem repetição automática.")
        chave = self.app.chave_groq
        threading.Thread(target=self._trabalhar, args=(preparado, chave), daemon=True).start()
        self.app.root.after(100, lambda: self._receber(preparado["pergunta"]))

    def _trabalhar(self, preparado, chave):
        try:
            resposta = agente_ia.consultar(preparado, self.pasta, chave)
            self.resultados.put((True, resposta))
        except (ValueError, OSError) as erro:
            self.resultados.put((False, str(erro)))
        except Exception:
            # O detalhe de bibliotecas externas pode conter cabeçalhos e credenciais.
            self.resultados.put((False, "Não foi possível concluir a consulta."))

    def _receber(self, pergunta):
        try:
            ok, resposta = self.resultados.get_nowait()
        except queue.Empty:
            self.app.root.after(100, lambda: self._receber(pergunta))
            return
        self.app.ia_ocupada = False
        if ok:
            self.app.historico_ia.append((pergunta, resposta))
            self.app.historico_ia[:] = self.app.historico_ia[-10:]
        if not self.frame.winfo_exists():
            return
        self.escrever("SentinelaLog" if ok else "Aviso", resposta)
        self.status.configure(text="Consulta concluída e registrada." if ok else resposta)
        self.enviar_botao.configure(state="normal")
        self.limpar_botao.configure(state="normal")
