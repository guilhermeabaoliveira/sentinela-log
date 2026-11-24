
import tkinter as tk
from tkinter import ttk
from . import estilos as s


def criar(pai, colunas, larguras=None):
    frame = tk.Frame(pai, bg=s.BG)
    frame.pack(fill="both", expand=True, pady=(10, 0))

    tree = ttk.Treeview(frame, columns=colunas, show="headings")

    titulos = {"matricula": "Matrícula", "nome": "Nome", "perfil": "Perfil",
               "inicio": "Início", "fim": "Fim", "situacao": "Situação",
               "id": "ID", "momento": "Data e hora", "maquina": "Máquina",
               "resultado": "Resultado", "risco": "Risco", "motivos": "Motivos",
               "operacao": "Operação", "afetado": "Usuário afetado", "pergunta": "Pergunta"}
    for i, coluna in enumerate(colunas):
        tree.heading(coluna, text=titulos.get(coluna, coluna))
        tree.column(
            coluna,
            width=larguras[i] if larguras else 130,
            minwidth=70,
            anchor="w"
        )

    vertical = ttk.Scrollbar(
        frame, orient="vertical", command=tree.yview
    )
    horizontal = ttk.Scrollbar(
        frame, orient="horizontal", command=tree.xview
    )

    tree.configure(
        yscrollcommand=vertical.set,
        xscrollcommand=horizontal.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    return tree


def preencher(tree, linhas):
    tree.tag_configure("alternada", background=s.ALT)
    for indice, linha in enumerate(linhas):
        tree.insert("", "end", values=linha, tags=("alternada",) if indice % 2 else ())
