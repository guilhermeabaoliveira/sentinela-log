
import tkinter as tk
from . import estilos as s


def botao(pai, texto, comando, cor="#1e3854"):
    return tk.Button(
        pai, text=texto, command=comando,
        bg=cor, fg="#f4f8ff",
        activebackground="#28618b",
        activeforeground="#ffffff",
        relief="flat", bd=0,
        padx=15, pady=10,
        font=(s.FONT, 9, "bold"),
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
        highlightbackground="#20344e"
    )

    tk.Label(
        card, text=titulo.upper(), bg=s.CARD,
        fg="#91a4bd", font=(s.FONT, 8, "bold")
    ).pack(anchor="w", padx=16, pady=(14, 5))

    tk.Label(
        card, text=str(valor), bg=s.CARD,
        fg=cor, font=(s.FONT, 25, "bold")
    ).pack(anchor="w", padx=16)

    tk.Label(
        card, text=detalhe, bg=s.CARD,
        fg="#71849d", font=(s.FONT, 8)
    ).pack(anchor="w", padx=16, pady=(2, 14))

    return card


def secao(pai, texto):
    tk.Label(
        pai, text=texto.upper(), bg=s.CARD,
        fg=s.BLUE, font=(s.FONT, 10, "bold")
    ).pack(anchor="w", padx=18, pady=(16, 8))


def texto(pai, valor, cor="#d4deeb", fonte=9, **kwargs):
    tk.Label(
        pai, text=valor,
        bg=kwargs.pop("bg", s.CARD),
        fg=cor,
        font=(kwargs.pop("familia", s.FONT), fonte),
        anchor="w", justify="left", **kwargs
    ).pack(anchor="w", padx=20, pady=3)
