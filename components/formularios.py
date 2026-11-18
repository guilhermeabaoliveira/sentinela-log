
import tkinter as tk
from tkinter import ttk, messagebox
from . import estilos as s
from .widgets import botao


def abrir(root, titulo, campos, confirmar, callback, tamanho="500x650"):
    janela = tk.Toplevel(root)
    janela.title("SentinelaLog | " + titulo)
    janela.geometry(tamanho)
    janela.minsize(440, 420)
    janela.configure(bg=s.BG)
    janela.transient(root)
    janela.grab_set()

    tk.Label(
        janela, text=titulo, bg=s.BG,
        fg=s.TEXT, font=(s.FONT, 19, "bold")
    ).pack(anchor="w", padx=22, pady=(20, 4))

    tk.Label(
        janela, text="Preencha os campos abaixo.",
        bg=s.BG, fg=s.MUTED,
        font=(s.FONT, 9)
    ).pack(anchor="w", padx=22, pady=(0, 12))

    painel = tk.Frame(janela, bg=s.CARD)
    painel.pack(fill="both", expand=True, padx=18, pady=8)

    entradas = {}

    for campo in campos:
        nome, chave = campo[:2]
        valor = campo[2] if len(campo) > 2 else ""
        tipo = campo[3] if len(campo) > 3 else "entry"

        bloco = tk.Frame(painel, bg=s.CARD)
        bloco.pack(fill="x", padx=20, pady=6)

        tk.Label(
            bloco, text=nome, bg=s.CARD,
            fg=s.TEXT, font=(s.FONT, 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        if tipo == "combo":
            entrada = ttk.Combobox(
                bloco, values=campo[4], state="readonly"
            )
            entrada.pack(fill="x", ipady=5)
            entrada.set(valor or (campo[4][0] if campo[4] else ""))
        else:
            entrada = tk.Entry(
                bloco, bg=s.FIELD, fg=s.TEXT,
                insertbackground=s.TEXT,
                relief="flat", highlightthickness=1, highlightbackground=s.BORDER,
                highlightcolor=s.BLUE, font=(s.FONT, 10)
            )
            entrada.pack(fill="x", ipady=9)
            if valor:
                entrada.insert(0, valor)

        entradas[chave] = entrada

    def enviar():
        valores = {
            chave: entrada.get().strip()
            for chave, entrada in entradas.items()
        }

        try:
            callback(valores)
            janela.destroy()
        except (ValueError, OSError, KeyError) as erro:
            messagebox.showerror(
                "Não foi possível concluir",
                str(erro), parent=janela
            )

    rodape = tk.Frame(janela, bg=s.BG)
    rodape.pack(fill="x", padx=18, pady=15)

    botao(
        rodape, "Cancelar", janela.destroy, "#263449"
    ).pack(side="right", padx=(8, 0))

    botao(
        rodape, confirmar, enviar, "#087e68"
    ).pack(side="right")

    return janela
