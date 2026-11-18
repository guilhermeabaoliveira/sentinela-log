BG = "#f5f6f8"
PANEL = "#ffffff"
CARD = "#ffffff"
TOP = "#ffffff"
FIELD = "#ffffff"
BORDER = "#d8dde4"
TEXT = "#202833"
MUTED = "#596575"
BLUE = "#285d91"
GREEN = "#28734b"
RED = "#a33232"
PURPLE = BLUE
YELLOW = "#805b16"
FONT = "Segoe UI"
NAV = "#252c35"
NAV_TEXT = "#e4e8ee"
NAV_MUTED = "#afb8c4"
NAV_ACTIVE = "#3b4859"
BUTTON = "#e8ecf1"


def configurar(root):
    from tkinter import ttk

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background=CARD, foreground=TEXT,
                    fieldbackground=CARD, rowheight=36, borderwidth=0,
                    font=(FONT, 10))
    style.configure("Treeview.Heading", background="#e9edf2", foreground=TEXT,
                    font=(FONT, 10, "bold"), relief="flat", padding=10)
    style.map("Treeview", background=[("selected", "#dbe7f3")],
              foreground=[("selected", "#173b60")])
    style.configure("TCombobox", fieldbackground=FIELD, background=BUTTON,
                    foreground=TEXT, arrowcolor=MUTED, padding=5)
    style.map("TCombobox", fieldbackground=[("readonly", FIELD)],
              foreground=[("readonly", TEXT)], selectbackground=[("readonly", FIELD)],
              selectforeground=[("readonly", TEXT)])
    style.configure("TScrollbar", background="#c5ccd5", troughcolor=BG,
                    borderwidth=0, arrowcolor=MUTED)
