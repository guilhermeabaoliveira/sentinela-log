
BG = "#0b1220"
PANEL = "#111c2e"
CARD = "#142238"
TOP = "#0f1929"
FIELD = "#0d1727"
BORDER = "#263750"
TEXT = "#f0f6ff"
MUTED = "#8293aa"
BLUE = "#55c7ff"
GREEN = "#65d6a4"
RED = "#ff8795"
PURPLE = "#a78bfa"
YELLOW = "#f5c66b"
FONT = "Segoe UI"


def configurar(root):
    from tkinter import ttk

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background=PANEL,
        foreground="#e5edf8",
        fieldbackground=PANEL,
        rowheight=34,
        borderwidth=0,
        font=(FONT, 10)
    )
    style.configure(
        "Treeview.Heading",
        background="#1b2a40",
        foreground="#9bdcff",
        font=(FONT, 9, "bold"),
        relief="flat",
        padding=9
    )
    style.map(
        "Treeview",
        background=[("selected", "#24476b")],
        foreground=[("selected", "#ffffff")]
    )
    style.configure(
        "TCombobox",
        fieldbackground=PANEL,
        background="#1b2a40",
        foreground="#ffffff",
        arrowcolor=BLUE
    )
