
import tkinter as tk
from . import estilos as s


def botao(pai, texto, comando, cor="#1e3854"):
    primaria = cor == "#087e68"
    perigo = cor == "#7b3040"
    fundo = s.BLUE if primaria else ("#f5e6e6" if perigo else s.BUTTON)
    frente = "#ffffff" if primaria else (s.RED if perigo else s.TEXT)
    return tk.Button(
        pai, text=texto, command=comando,
        bg=fundo, fg=frente,
        activebackground="#214c75" if primaria else "#dce2e9",
        activeforeground="#ffffff" if primaria else frente,
        relief="flat", bd=0,
        padx=16, pady=10,
        font=(s.FONT, 10),
        cursor="hand2"
    )


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
    card = tk.Frame(
        pai, bg=s.CARD,
        highlightthickness=1,
        highlightbackground=s.BORDER
    )

    tk.Label(
        card, text=titulo, bg=s.CARD,
        fg=s.MUTED, font=(s.FONT, 10)
    ).pack(anchor="w", padx=16, pady=(14, 5))

    tk.Label(
        card, text=str(valor), bg=s.CARD,
        fg=cor if cor in [s.RED, s.YELLOW] else s.TEXT, font=(s.FONT, 26, "bold")
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


def texto(pai, valor, cor=s.TEXT, fonte=9, **kwargs):
    tk.Label(
        pai, text=valor,
        bg=kwargs.pop("bg", s.CARD),
        fg=cor,
        font=(kwargs.pop("familia", s.FONT), fonte),
        anchor="w", justify="left", **kwargs
    ).pack(anchor="w", padx=20, pady=3)
