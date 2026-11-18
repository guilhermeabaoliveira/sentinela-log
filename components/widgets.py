
import tkinter as tk
from . import estilos as s


def botao(pai, texto, comando, cor="#1e3854"):
    primaria = cor == "#087e68"
    perigo = cor == "#7b3040"
    botao = tk.Button(
        pai, text=texto, command=comando,
        relief="flat", bd=0, highlightthickness=1,
        padx=16, pady=10, font=(s.FONT, 10), cursor="hand2"
    )
    botao._hover = False

    def atualizar():
        destaque = botao._hover and str(botao.cget("state")) != "disabled"
        fundo = s.BLUE if primaria else (s.DANGER_BG if perigo else s.BUTTON)
        frente = "#ffffff" if primaria else (s.RED if perigo else s.TEXT)
        realce = s.PRIMARY_HOVER if primaria else s.HOVER
        botao.configure(bg=realce if destaque else fundo, fg=frente,
                        activebackground=realce, activeforeground=frente,
                        highlightbackground=s.ACCENT if destaque else s.BORDER,
                        highlightcolor=s.ACCENT, disabledforeground=s.MUTED)

    def realcar(evento):
        botao._hover = evento.type.name in ["Enter", "FocusIn"]
        atualizar()

    botao._atualizar_aparencia = atualizar
    for evento in ["<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>"]:
        botao.bind(evento, realcar, add="+")
    atualizar()
    return botao



def titulo(pai, texto, descricao):
    tk.Label(
        pai, text=texto, bg=s.BG,
        fg=s.TEXT, font=(s.FONT, 22, "bold")
    ).pack(anchor="w")

    tk.Label(
        pai, text=descricao, bg=s.BG,
        fg=s.MUTED, font=(s.FONT, 10)
    ).pack(anchor="w", pady=(4, 18))


def cartao(pai, titulo, valor, detalhe, cor):
    cor = s.ACCENT if cor == s.BLUE else cor
    card = tk.Frame(
        pai, bg=s.CARD,
        highlightthickness=1,
        highlightbackground=s.BORDER
    )

    tk.Frame(card, bg=cor, height=2).pack(fill="x")

    tk.Label(
        card, text=titulo, bg=s.CARD,
        fg=s.MUTED, font=(s.FONT, 10)
    ).pack(anchor="w", padx=16, pady=(14, 5))

    tk.Label(
        card, text=str(valor), bg=s.CARD,
        fg=cor, font=(s.FONT, 26, "bold")
    ).pack(anchor="w", padx=16)

    tk.Label(
        card, text=detalhe, bg=s.CARD,
        fg=s.MUTED, font=(s.FONT, 9)
    ).pack(anchor="w", padx=16, pady=(2, 14))

    return card


def secao(pai, texto):
    tk.Label(
        pai, text=texto, bg=s.CARD,
        fg=s.TEXT, font=(s.FONT, 11, "bold")
    ).pack(anchor="w", padx=18, pady=(16, 8))


def texto(pai, valor, cor=None, fonte=9, **kwargs):
    tk.Label(
        pai, text=valor,
        bg=kwargs.pop("bg", s.CARD),
        fg=cor or s.TEXT,
        font=(kwargs.pop("familia", s.FONT), fonte),
        anchor="w", justify="left", **kwargs
    ).pack(anchor="w", padx=20, pady=3)
