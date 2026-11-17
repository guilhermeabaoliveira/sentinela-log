
import tkinter as tk
from . import estilos as s


def criar(root, opcoes, sair):
    barra = tk.Frame(root, bg=s.PANEL, width=245)
    barra.pack(side="left", fill="y")
    barra.pack_propagate(False)

    marca = tk.Frame(barra, bg=s.PANEL)
    marca.pack(fill="x", padx=22, pady=(25, 24))

    tk.Label(
        marca, text="SENTINELA", bg=s.PANEL,
        fg=s.BLUE, font=(s.FONT, 21, "bold")
    ).pack(anchor="w")

    tk.Label(
        marca, text="LOG  /  ACCESS MANAGEMENT",
        bg=s.PANEL, fg=s.MUTED,
        font=(s.FONT, 8, "bold")
    ).pack(anchor="w", pady=(2, 0))

    tk.Frame(barra, bg=s.BORDER, height=1).pack(
        fill="x", padx=18, pady=(0, 14)
    )

    for simbolo, texto, comando in opcoes:
        tk.Button(
            barra, text=f"{simbolo}   {texto}",
            command=comando, anchor="w",
            bg=s.PANEL, fg="#cbd7e6",
            activebackground="#203650",
            activeforeground=s.BLUE,
            relief="flat", bd=0,
            padx=18, pady=10,
            font=(s.FONT, 9),
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=2)

    tk.Frame(barra, bg=s.BORDER, height=1).pack(
        fill="x", padx=18, pady=15
    )

    tk.Button(
        barra, text="⏻   0  Sair", command=sair,
        anchor="w", bg="#2b1d2a", fg="#ffb4bd",
        activebackground="#542936",
        activeforeground="#ffffff",
        relief="flat", bd=0,
        padx=18, pady=11,
        font=(s.FONT, 9, "bold"),
        cursor="hand2"
    ).pack(fill="x", padx=10, pady=5)

    tk.Label(
        barra,
        text="AMBIENTE ACADÊMICO\nDados fictícios • Execução local",
        bg=s.PANEL, fg="#718198",
        font=(s.FONT, 8), justify="left"
    ).pack(side="bottom", anchor="w", padx=22, pady=20)

    return barra
