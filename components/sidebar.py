
import tkinter as tk
from . import estilos as s


def criar(root, opcoes, sair):
    barra = tk.Frame(root, bg=s.NAV, width=245)
    barra.pack(side="left", fill="y")
    barra.pack_propagate(False)

    marca = tk.Frame(barra, bg=s.NAV)
    marca.pack(fill="x", padx=22, pady=(22, 20))

    tk.Label(
        marca, text="SentinelaLog", bg=s.NAV,
        fg=s.NAV_TEXT, font=(s.FONT, 19, "bold")
    ).pack(anchor="w")

    tk.Label(
        marca, text="Monitor de acessos",
        bg=s.NAV, fg=s.NAV_MUTED,
        font=(s.FONT, 8, "bold")
    ).pack(anchor="w", pady=(2, 0))

    tk.Frame(barra, bg=s.BORDER, height=1).pack(
        fill="x", padx=18, pady=(0, 14)
    )

    for simbolo, texto, comando in opcoes:
        tk.Button(
            barra, text=texto,
            command=comando, anchor="w",
            bg=s.NAV, fg=s.NAV_TEXT,
            activebackground=s.NAV_ACTIVE,
            activeforeground=s.NAV_TEXT,
            relief="flat", bd=0,
            padx=18, pady=6,
            font=(s.FONT, 10),
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=2)

    tk.Frame(barra, bg=s.BORDER, height=1).pack(
        fill="x", padx=18, pady=10
    )

    tk.Button(
        barra, text="0  Sair", command=sair,
        anchor="w", bg=s.NAV, fg=s.NAV_TEXT,
        activebackground=s.NAV_ACTIVE,
        activeforeground="#ffffff",
        relief="flat", bd=0,
        padx=18, pady=11,
        font=(s.FONT, 9, "bold"),
        cursor="hand2"
    ).pack(fill="x", padx=10, pady=5)

    tk.Label(
        barra,
        text="Dados fictícios\nExecução neste computador",
        bg=s.NAV, fg=s.NAV_MUTED,
        font=(s.FONT, 8), justify="left"
    ).pack(side="bottom", anchor="w", padx=22, pady=20)

    return barra
