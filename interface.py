
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

import armazenamento
import usuarios
import acessos
import risco
import relatorios

from components import estilos, sidebar, widgets, tabelas, formularios
from components.chat_ia import ChatIA

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")


class SentinelaLogApp:
    def __init__(self, root):
        self.root = root
        root.title("SentinelaLog | Gerenciamento de Acessos")
        root.geometry("1180x740")
        root.minsize(980, 620)
        root.configure(bg=estilos.BG)

        estilos.configurar(root)
        self.estado = armazenamento.carregar(PASTA)
        self.historico_ia = []
        self.chave_groq = ""
        self.ia_ocupada = False
        self._estrutura()
        self.mostrar_inicio()

    def _estrutura(self):
        opcoes = [
            ("⌂", "Painel inicial", self.mostrar_inicio),
            ("＋", "1  Cadastrar", self.cadastrar_usuario),
            ("▤", "2  Usuários", self.mostrar_usuarios),
            ("✎", "3  Editar", self.editar_usuario),
            ("×", "4  Excluir", self.excluir_usuario),
            ("↗", "5  Registrar acesso", self.registrar_acesso),
            ("≡", "6  Acessos", self.mostrar_acessos),
            ("▧", "7  Auditoria", self.mostrar_auditoria),
            ("◉", "8  Revelar matrícula", self.revelar_matricula),
            ("⚙", "9  Segurança", self.mostrar_seguranca),
            ("✧", "10  Assistente IA", self.mostrar_ia)
        ]

        sidebar.criar(self.root, opcoes, self.sair)

        principal = tk.Frame(self.root, bg=estilos.BG)
        principal.pack(side="left", fill="both", expand=True)

        topo = tk.Frame(principal, bg=estilos.TOP, height=66)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        self.page_title = tk.Label(
            topo, text="Painel inicial",
            bg=estilos.TOP, fg=estilos.TEXT,
            font=(estilos.FONT, 16, "bold")
        )
        self.page_title.pack(side="left", padx=28)

        tk.Label(
            topo, text="●  SISTEMA LOCAL",
            bg=estilos.TOP, fg=estilos.GREEN,
            font=(estilos.FONT, 8, "bold")
        ).pack(side="right", padx=28)

        self.content = tk.Frame(principal, bg=estilos.BG)
        self.content.pack(fill="both", expand=True, padx=26, pady=22)

    def _limpar(self, titulo, descricao):
        for item in self.content.winfo_children():
            item.destroy()

        self.page_title.configure(text=titulo)
        self.estado = armazenamento.carregar(PASTA)
        widgets.titulo(self.content, titulo, descricao)

    def _salvar(self, operacao, afetado="-"):
        self.estado = armazenamento.salvar(
            PASTA, self.estado, operacao, afetado
        )

    def _perguntar_matricula(self, titulo):
        return simpledialog.askstring(
            titulo, "Informe a matrícula fictícia:",
            parent=self.root
        )

    def _usuario(self, matricula):
        self.estado = armazenamento.carregar(PASTA)
        usuario = usuarios.buscar(self.estado, matricula)

        if usuario is None:
            messagebox.showwarning(
                "SentinelaLog",
                "Usuário ativo não encontrado.",
                parent=self.root
            )

        return usuario

    def _cards(self, dados):
        grade = tk.Frame(self.content, bg=estilos.BG)
        grade.pack(fill="x")

        for i, (nome, valor, detalhe, cor) in enumerate(dados):
            widgets.cartao(
                grade, nome, valor, detalhe, cor
            ).grid(
                row=0, column=i, sticky="nsew",
                padx=(0 if i == 0 else 9, 0)
            )
            grade.columnconfigure(i, weight=1)

    def _form(self, titulo, campos, confirmar, callback, tamanho="500x650"):
        formularios.abrir(
            self.root, titulo, campos,
            confirmar, callback, tamanho
        )

    def _tabela(self, colunas, larguras, linhas):
        tree = tabelas.criar(self.content, colunas, larguras)
        tabelas.preencher(tree, linhas)
        return tree

    def mostrar_inicio(self):
        self._limpar(
            "Painel inicial",
            "Gerencie usuários, registre acessos e consulte o histórico do sistema."
        )

        resumo = relatorios.resumir(self.estado)

        self._cards([
            ("Usuários cadastrados", len(self.estado["usuarios"]),
             "Cadastros existentes", estilos.BLUE),
            ("Usuários ativos", len(usuarios.ativos(self.estado)),
             "Disponíveis para acesso", estilos.GREEN),
            ("Acessos registrados", resumo["acessos"],
             "Histórico total", estilos.PURPLE),
            ("Falhas de acesso", resumo["falhas"],
             "Tentativas com falha", estilos.RED)
        ])

        bloco = tk.Frame(self.content, bg=estilos.BG)
        bloco.pack(fill="x", pady=(25, 8))

        tk.Label(
            bloco, text="Acesso rápido",
            bg=estilos.BG, fg=estilos.TEXT,
            font=(estilos.FONT, 13, "bold")
        ).pack(anchor="w")

        tk.Label(
            bloco,
            text="As operações do menu original em uma interface gráfica.",
            bg=estilos.BG, fg=estilos.MUTED,
            font=(estilos.FONT, 9)
        ).pack(anchor="w", pady=(3, 0))

        acoes = [
            ("1  Cadastrar", self.cadastrar_usuario, "#087e68"),
            ("2  Usuários", self.mostrar_usuarios, "#1e3854"),
            ("3  Editar", self.editar_usuario, "#1e3854"),
            ("4  Excluir", self.excluir_usuario, "#7b3040"),
            ("5  Registrar acesso", self.registrar_acesso, "#1e3854"),
            ("6  Acessos", self.mostrar_acessos, "#1e3854"),
            ("7  Auditoria", self.mostrar_auditoria, "#1e3854"),
            ("8  Revelar matrícula", self.revelar_matricula, "#1e3854"),
            ("9  Segurança", self.mostrar_seguranca, "#1e3854"),
            ("10  Assistente IA", self.mostrar_ia, "#514078")
        ]

        grade = tk.Frame(self.content, bg=estilos.BG)
        grade.pack(fill="x", pady=10)

        for i, (texto, comando, cor) in enumerate(acoes):
            widgets.botao(
                grade, texto, comando, cor
            ).grid(
                row=i // 2, column=i % 2,
                sticky="ew", padx=(0, 10),
                pady=5, ipady=4
            )

        for coluna in range(2):
            grade.columnconfigure(coluna, weight=1)

        tk.Label(
            self.content,
            text="Dados locais em dados/estado.txt. Utilize somente dados fictícios.",
            bg=estilos.BG, fg="#71849d",
            font=(estilos.FONT, 8)
        ).pack(anchor="w", pady=(12, 0))

    def cadastrar_usuario(self):
        campos = [
            ("Matrícula fictícia", "matricula"),
            ("Nome fictício", "nome"),
            ("Perfil", "perfil", "estudante", "combo", usuarios.PERFIS),
            ("Horário inicial (HH:MM)", "inicio", "07:00"),
            ("Horário final (HH:MM)", "fim", "18:00"),
            ("Observações", "observacoes")
        ]

        def salvar(v):
            usuarios.cadastrar(
                self.estado, v["matricula"], v["nome"],
                v["perfil"], v["inicio"], v["fim"],
                v["observacoes"]
            )
            self._salvar("CADASTRO", v["matricula"])
            messagebox.showinfo(
                "SentinelaLog", "Usuário cadastrado com sucesso.",
                parent=self.root
            )
            self.mostrar_usuarios()

        self._form("Cadastrar usuário", campos, "Cadastrar usuário", salvar)

    def mostrar_usuarios(self):
        self._limpar(
            "2  Usuários",
            "Consulte os cadastros ativos no SentinelaLog."
        )

        widgets.botao(
            self.content, "+ Cadastrar usuário",
            self.cadastrar_usuario, "#087e68"
        ).pack(anchor="w")

        linhas = [
            (
                usuarios.mascarar(u["matricula"]),
                u["nome"], u["perfil"], u["inicio"],
                u["fim"], "Ativo"
            )
            for u in usuarios.ativos(self.estado)
        ]

        self._tabela(
            ("matricula", "nome", "perfil", "inicio", "fim", "situacao"),
            (130, 240, 150, 100, 100, 100),
            linhas
        )

        widgets.texto(
            self.content,
            "As matrículas são exibidas parcialmente por privacidade.",
            cor="#71849d", fonte=8, bg=estilos.BG
        )

    def editar_usuario(self):
        matricula = self._perguntar_matricula("Editar usuário")
        if not matricula:
            return

        usuario = self._usuario(matricula)
        if not usuario:
            return

        campos = [
            ("Nome fictício", "nome", usuario["nome"]),
            ("Perfil", "perfil", usuario["perfil"], "combo", usuarios.PERFIS),
            ("Horário inicial (HH:MM)", "inicio", usuario["inicio"]),
            ("Horário final (HH:MM)", "fim", usuario["fim"]),
            ("Observações", "observacoes", usuario["observacoes"])
        ]

        def salvar(v):
            usuarios.editar(
                self.estado, matricula, v["nome"], v["perfil"],
                v["inicio"], v["fim"], v["observacoes"]
            )
            self._salvar("EDICAO", matricula)
            messagebox.showinfo(
                "SentinelaLog", "Cadastro atualizado com sucesso.",
                parent=self.root
            )
            self.mostrar_usuarios()

        self._form("Editar usuário", campos, "Salvar alterações", salvar)

    def excluir_usuario(self):
        matricula = self._perguntar_matricula("Excluir usuário")
        if not matricula:
            return

        usuario = self._usuario(matricula)
        if not usuario:
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o cadastro de {usuario['nome']}?\n\n"
            "O histórico será preservado.",
            parent=self.root
        )

        if not confirmar:
            return

        try:
            usuarios.excluir(self.estado, matricula)
            self._salvar("EXCLUSAO", matricula)
            messagebox.showinfo(
                "SentinelaLog",
                "Usuário excluído. Histórico preservado.",
                parent=self.root
            )
            self.mostrar_usuarios()
        except (ValueError, OSError) as erro:
            messagebox.showerror("Erro", str(erro), parent=self.root)

    def registrar_acesso(self):
        self.estado = armazenamento.carregar(PASTA)
        ativos = usuarios.ativos(self.estado)

        if not ativos:
            messagebox.showwarning(
                "SentinelaLog",
                "Cadastre um usuário antes de registrar acessos.",
                parent=self.root
            )
            return

        opcoes = [
            f"{u['matricula']} | {u['nome']}"
            for u in ativos
        ]

        campos = [
            ("Usuário", "usuario", opcoes[0], "combo", opcoes),
            (
                "Data e hora (AAAA-MM-DD HH:MM)",
                "momento",
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ),
            ("Máquina fictícia", "maquina"),
            ("Resultado", "resultado", "sucesso", "combo", ["sucesso", "falha"])
        ]

        def salvar(v):
            matricula = v["usuario"].split(" | ", 1)[0]
            usuario = usuarios.buscar(self.estado, matricula)
            bloqueadas = risco.ler_bloqueadas(
                os.path.join(PASTA, "bloqueadas.txt")
            )

            registro = acessos.registrar(
                self.estado, usuario, v["momento"],
                v["maquina"], v["resultado"], bloqueadas
            )

            self._salvar("REGISTRO_ACESSO", matricula)

            messagebox.showinfo(
                "Acesso registrado",
                f"Registro salvo com sucesso.\n\n"
                f"Classificação: {registro['risco'].upper()}\n"
                f"Motivos: {registro['motivos']}",
                parent=self.root
            )

            self.mostrar_acessos()

        self._form(
            "Registrar acesso", campos,
            "Registrar acesso", salvar, "520x490"
        )

    def mostrar_acessos(self):
        self._limpar(
            "6  Acessos",
            "Consulte os eventos registrados. Os registros históricos não são editáveis."
        )

        linhas = [
            (
                a["id"], usuarios.mascarar(a["matricula"]),
                a["momento"], a["maquina"], a["resultado"],
                a["risco"].upper(), a["motivos"]
            )
            for a in reversed(acessos.consultar(self.estado))
        ]

        self._tabela(
            ("id", "matricula", "momento", "maquina",
             "resultado", "risco", "motivos"),
            (55, 100, 145, 120, 90, 90, 280),
            linhas
        )

    def mostrar_auditoria(self):
        self._limpar(
            "7  Auditoria",
            "Histórico das operações persistidas no sistema."
        )

        widgets.botao(self.content, "Consultas de IA", self.mostrar_auditoria_ia).pack(anchor="w")

        linhas = []

        for item in reversed(armazenamento.consultar_auditoria(self.estado)):
            afetado = (
                usuarios.mascarar(item["afetado"])
                if item["afetado"].isdigit()
                else item["afetado"]
            )
            linhas.append((
                item["id"], item["momento"],
                item["operacao"], afetado
            ))

        self._tabela(
            ("id", "momento", "operacao", "afetado"),
            (65, 180, 230, 180),
            linhas
        )

    def mostrar_auditoria_ia(self):
        import agente_ia
        try:
            registros = agente_ia.listar_consultas(PASTA)
        except (ValueError, OSError) as erro:
            messagebox.showerror("Auditoria de IA", str(erro), parent=self.root)
            return
        self._limpar("Consultas de IA", "Pergunta tratada, data e hora e resultado de cada tentativa.")
        self._tabela(("momento", "operacao", "pergunta", "resultado"), (170, 130, 340, 110),
                     [(r["momento"], r["operacao"], r["pergunta"], r["resultado"])
                      for r in reversed(registros)])

    def revelar_matricula(self):
        matricula = self._perguntar_matricula("Revelar matrícula")
        if not matricula:
            return

        self.estado = armazenamento.carregar(PASTA)

        try:
            valor = usuarios.revelar(self.estado, matricula)

            confirmar = messagebox.askyesno(
                "Confirmação de privacidade",
                "A revelação será registrada na auditoria. Deseja continuar?",
                parent=self.root
            )

            if not confirmar:
                return

            self._salvar("REVELACAO_MATRICULA", matricula)

            messagebox.showinfo(
                "Matrícula revelada",
                f"Matrícula: {valor}",
                parent=self.root
            )

            self.mostrar_auditoria()

        except (ValueError, OSError) as erro:
            messagebox.showerror(
                "Não foi possível revelar",
                str(erro), parent=self.root
            )

    def mostrar_seguranca(self):
        self._limpar(
            "9  Segurança",
            "Indicadores derivados do histórico e regras locais de classificação."
        )

        resumo = relatorios.resumir(self.estado)

        self._cards([
            (nome, resumo[chave], "Total registrado", cor)
            for nome, chave, cor in [
                ("Acessos", "acessos", estilos.BLUE),
                ("Falhas", "falhas", estilos.RED),
                ("Suspeitos", "suspeitos", estilos.YELLOW),
                ("Críticos", "criticos", estilos.RED)
            ]
        ])

        corpo = tk.Frame(self.content, bg=estilos.CARD)
        corpo.pack(fill="both", expand=True, pady=(20, 0))

        widgets.secao(corpo, "Regras de classificação")

        for regra in risco.descricao_regras():
            widgets.texto(corpo, "•  " + regra, wraplength=800)

        widgets.secao(corpo, "Distribuição de risco")

        for linha in relatorios.grafico(self.estado):
            widgets.texto(
                corpo, linha, cor="#e5edf8",
                familia="Consolas", fonte=10
            )

        widgets.secao(corpo, "Máquinas compartilhadas")

        linhas = acessos.linhas_compartilhadas(self.estado) or [
            "Nenhuma máquina compartilhada identificada."
        ]

        for linha in linhas:
            widgets.texto(corpo, linha, wraplength=850)

        widgets.texto(
            corpo,
            "Compartilhamento não comprova quem realizou uma ação.",
            cor=estilos.MUTED, fonte=8
        )

    def mostrar_ia(self):
        self._limpar(
            "10  Assistente IA",
            "Consulte os dados fictícios em linguagem natural."
        )
        self.chat = ChatIA(self, PASTA)

    def sair(self):
        if messagebox.askyesno(
            "Sair", "Deseja encerrar o SentinelaLog?",
            parent=self.root
        ):
            self.root.destroy()


def executar():
    root = tk.Tk()
    SentinelaLogApp(root)
    root.mainloop()


if __name__ == "__main__":
    executar()
