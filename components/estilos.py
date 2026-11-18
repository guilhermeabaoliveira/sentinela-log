FONT = "Segoe UI"
CLARO = False
TEMAS = {
    False: {
        "BG": "#191c20", "PANEL": "#22262b", "CARD": "#24292f",
        "TOP": "#1e2227", "FIELD": "#15191d", "BORDER": "#3c434c",
        "TEXT": "#e6e9ed", "MUTED": "#a8b0bb", "BLUE": "#356b9e",
        "GREEN": "#8fbd9c", "RED": "#e39a98", "YELLOW": "#d4b57b",
        "NAV": "#14171b", "NAV_TEXT": "#dee3e9", "NAV_MUTED": "#a1aab6",
        "NAV_ACTIVE": "#303944", "BUTTON": "#333b45", "HOVER": "#414d5c",
        "DANGER_BG": "#462e32", "ALT": "#292f36", "HEADING": "#303740",
        "SELECT": "#354e68", "SELECT_TEXT": "#f0f4f9", "SCROLL": "#596370", "ACCENT": "#78b7e9",
        "PRIMARY_HOVER": "#427fb6", "NAV_HOVER": "#263342",
        "EXIT": "#69323b", "EXIT_HOVER": "#8b3f4a", "EXIT_TEXT": "#fff5f4"
    },
    True: {
        "BG": "#f5f6f8", "PANEL": "#fafbfd", "CARD": "#ffffff",
        "TOP": "#fbfcfd", "FIELD": "#fefefe", "BORDER": "#d8dde4",
        "TEXT": "#202833", "MUTED": "#596575", "BLUE": "#285d91",
        "GREEN": "#28734b", "RED": "#a33232", "YELLOW": "#805b16",
        "NAV": "#252c35", "NAV_TEXT": "#e4e8ee", "NAV_MUTED": "#afb8c4",
        "NAV_ACTIVE": "#3b4859", "BUTTON": "#e8ecf1", "HOVER": "#dce2e9",
        "DANGER_BG": "#f5e6e6", "ALT": "#f0f3f7", "HEADING": "#e9edf2",
        "SELECT": "#dbe7f3", "SELECT_TEXT": "#173b60", "SCROLL": "#c5ccd5", "ACCENT": "#28679e",
        "PRIMARY_HOVER": "#3478b2", "NAV_HOVER": "#354353",
        "EXIT": "#873c46", "EXIT_HOVER": "#a64a56", "EXIT_TEXT": "#fff5f4"
    }
}
globals().update(TEMAS[CLARO])
PURPLE = BLUE


def configurar(root):
    from tkinter import ttk

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background=CARD, foreground=TEXT,
                    fieldbackground=CARD, rowheight=36, borderwidth=0,
                    font=(FONT, 10))
    style.configure("Treeview.Heading", background=HEADING, foreground=TEXT,
                    font=(FONT, 10, "bold"), relief="flat", padding=10)
    style.map("Treeview", background=[("selected", SELECT)],
              foreground=[("selected", SELECT_TEXT)])
    style.configure("TCombobox", fieldbackground=FIELD, background=BUTTON,
                    foreground=TEXT, arrowcolor=MUTED, padding=5)
    style.map("TCombobox", fieldbackground=[("readonly", FIELD)],
              foreground=[("readonly", TEXT)], selectbackground=[("readonly", FIELD)],
              selectforeground=[("readonly", TEXT)])
    style.configure("TScrollbar", background=SCROLL, troughcolor=BG,
                    borderwidth=0, arrowcolor=MUTED)


def alternar(root):
    """Troca cores sem recriar campos, conversa ou chave da sessão."""
    global CLARO, PURPLE
    anterior = TEMAS[CLARO]
    CLARO = not CLARO
    atual = TEMAS[CLARO]
    cores = {valor: atual[nome] for nome, valor in anterior.items()}
    globals().update(atual)
    PURPLE = BLUE
    configurar(root)

    def recolorir(widget):
        opcoes = widget.keys()
        primaria = "background" in opcoes and str(widget.cget("background")) == anterior["BLUE"]
        for nome in ["background", "foreground", "activebackground", "activeforeground",
                     "insertbackground", "highlightbackground", "highlightcolor",
                     "selectbackground", "selectforeground", "disabledforeground"]:
            if nome in opcoes:
                cor = str(widget.cget(nome))
                if primaria and nome in ["foreground", "activeforeground"]:
                    continue
                if cor in cores:
                    widget.configure(**{nome: cores[cor]})
        if widget.winfo_class() == "Treeview":
            widget.tag_configure("alternada", background=ALT)
        for filho in widget.winfo_children():
            recolorir(filho)
        if hasattr(widget, "_atualizar_aparencia"):
            widget._atualizar_aparencia()

    recolorir(root)
