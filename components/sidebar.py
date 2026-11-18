
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

    barra.itens = []
    for simbolo, texto, comando in opcoes:
        linha = tk.Frame(barra, bg=s.NAV)
        linha.pack(fill="x", padx=10, pady=2)
        marcador = tk.Frame(linha, width=3, bg=s.NAV)
        marcador.pack(side="left", fill="y")
        botao = tk.Button(
            linha, text=f"{simbolo}   {texto}", command=comando, anchor="w",
            relief="flat", bd=0, padx=13, pady=6,
            font=(s.FONT, 10), cursor="hand2"
        )
        botao.pack(side="left", fill="x", expand=True)
        botao._selecionado = False
        botao._hover = False

        def atualizar(botao=botao, marcador=marcador):
            fundo = s.NAV_ACTIVE if botao._selecionado else s.NAV
            botao.configure(bg=s.NAV_HOVER if botao._hover else fundo,
                            fg=s.NAV_TEXT, activebackground=s.NAV_HOVER,
                            activeforeground=s.NAV_TEXT)
            marcador.configure(bg=s.ACCENT if botao._selecionado else s.NAV)

        def realcar(evento, botao=botao):
            botao._hover = evento.type.name in ["Enter", "FocusIn"]
            botao._atualizar_aparencia()

        botao._atualizar_aparencia = atualizar
        for evento in ["<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>"]:
            botao.bind(evento, realcar, add="+")
        atualizar()
        barra.itens.append((texto, botao))

    tk.Frame(barra, bg=s.BORDER, height=1).pack(
        fill="x", padx=18, pady=10
    )

    saida = tk.Button(
        barra, text="⏻   0  Sair", command=sair,
        anchor="w", relief="flat", bd=0, padx=18, pady=11,
        font=(s.FONT, 9, "bold"), cursor="hand2"
    )
    saida.pack(fill="x", padx=10, pady=5)
    saida._hover = False

    def atualizar_saida():
        saida.configure(bg=s.EXIT_HOVER if saida._hover else s.EXIT, fg=s.EXIT_TEXT,
                        activebackground=s.EXIT_HOVER, activeforeground=s.EXIT_TEXT)

    def realcar_saida(evento):
        saida._hover = evento.type.name in ["Enter", "FocusIn"]
        atualizar_saida()

    saida._atualizar_aparencia = atualizar_saida
    for evento in ["<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>"]:
        saida.bind(evento, realcar_saida, add="+")
    atualizar_saida()

    tk.Label(
        barra,
        text="Dados fictícios\nExecução neste computador",
        bg=s.NAV, fg=s.NAV_MUTED,
        font=(s.FONT, 8), justify="left"
    ).pack(side="bottom", anchor="w", padx=22, pady=20)

    return barra


def selecionar(barra, titulo):
    titulo = " ".join(titulo.split())
    if titulo == "Consultas de IA":
        titulo = "7 Auditoria"
    for texto, botao in barra.itens:
        botao._selecionado = " ".join(texto.split()) == titulo
        botao._atualizar_aparencia()
