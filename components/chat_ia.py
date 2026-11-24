"""Página de consulta Groq usando os estilos da interface do grupo."""
import queue
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

import agente_ia
import armazenamento
import acessos
import usuarios
import relatorios
from . import estilos as s
from .widgets import botao


class ChatIA:
    def __init__(self, app, pasta):
        self.app = app
        self.pasta = pasta
        self.frame = tk.Frame(app.content, bg=s.BG)
        self.frame.pack(fill="both", expand=True)
        self.resultados = queue.Queue()
        tk.Label(self.frame, text="Consulta de leitura aos registros",
                 bg=s.BG, fg=s.TEXT, font=(s.FONT, 11, "bold")).pack(anchor="w")
        tk.Label(self.frame, text="A resposta usa fatos calculados pelo sistema. "
                 "Aliases U1 e M1 substituem usuários e máquinas.",
                 bg=s.BG, fg=s.MUTED, wraplength=740, justify="left").pack(anchor="w", pady=8)
        self.conversa = ScrolledText(self.frame, wrap="word", bg=s.CARD, fg=s.TEXT,
                                    font=(s.FONT, 11), relief="flat", height=10,
                                    highlightthickness=1, highlightbackground=s.BORDER)
        self.conversa.pack(fill="both", expand=True, pady=8)
        self.conversa.configure(state="disabled")
        for pergunta, resposta in app.historico_ia:
            self.escrever("Você", pergunta)
            self.escrever("SentinelaLog", resposta)
        self.entrada = tk.Entry(self.frame, bg=s.FIELD, fg=s.TEXT,
                                insertbackground=s.TEXT, font=(s.FONT, 11), relief="flat",
                                highlightthickness=1, highlightbackground=s.BORDER, highlightcolor=s.BLUE)
        self.entrada.pack(fill="x", ipady=10, pady=8)
        self.entrada.bind("<Return>", lambda evento: self.enviar())
        controles = tk.Frame(self.frame, bg=s.BG)
        controles.pack(fill="x")
        self.enviar_botao = botao(controles, "Enviar pergunta", self.enviar, "#087e68")
        self.enviar_botao.pack(side="left", padx=(0, 8))
        botao(controles, "Configurar chave", self.configurar_chave).pack(side="left", padx=4)
        self.limpar_botao = botao(controles, "Limpar conversa", self.limpar)
        self.limpar_botao.pack(side="left", padx=4)
        self.status = tk.Label(self.frame, text="Pronto. Exemplo: quantas falhas foram registradas?",
                               bg=s.BG, fg=s.MUTED, anchor="w", wraplength=740)
        self.status.pack(fill="x", pady=10)
        self.criar_consultas_rapidas()
        
    def criar_consultas_rapidas(self):
        tk.Label(
            self.frame,
            text="Consultas rápidas — execução local",
            bg=s.BG, fg=s.TEXT,
            font=(s.FONT, 10, "bold")
        ).pack(anchor="w")

        painel = tk.Frame(self.frame, bg=s.BG)
        painel.pack(fill="x", pady=(4, 6))

        grupos = [
            ("Consulta de acessos", [
                ("Quantos acessos foram registrados?", "total_acessos"),
                ("Quais acessos tiveram falhas?", "falhas"),
                ("Quais acessos são críticos?", "criticos"),
                ("Resuma os acessos por nível de risco.", "riscos")
            ]),
            ("Exemplo MAQ-X", [
                ("Quais acessos vieram da MAQ-X?", "maq_x"),
                ("Por que o acesso da MAQ-X é crítico?", "motivos_maq_x"),
                ("Há máquinas compartilhadas?", "compartilhadas")
            ]),
            ("Consulta de usuários", [
                ("Quantos usuários estão cadastrados?", "total_usuarios"),
                ("Quais são os perfis dos usuários?", "perfis"),
                ("Resuma os registros disponíveis.", "resumo")
            ])
        ]

        for titulo, perguntas in grupos:
            botao(
                painel, titulo + " ▾",
                lambda t=titulo, p=perguntas:
                    self.abrir_consultas_rapidas(t, p)
            ).pack(side="left", padx=(0, 8))

        aviso = tk.Label(
            self.frame,
            text=(
                "OPERAÇÕES NÃO PERMITIDAS: "
                "Cadastrar uma matrícula | "
                "Editar uma matrícula ou cadastro | "
                "Excluir uma matrícula ou cadastro."
            ),
            bg=s.BG, fg=s.RED,
            font=(s.FONT, 9),
            justify="left", anchor="w"
        )
        aviso.pack(fill="x", pady=(2, 6))

        aviso.bind(
            "<Configure>",
            lambda evento: aviso.configure(
                wraplength=max(1, evento.width - 8)
            )
        )

    def abrir_consultas_rapidas(self, titulo, perguntas):
        anterior = getattr(self, "_janela_consultas", None)

        if anterior is not None and anterior.winfo_exists():
            anterior.destroy()

        janela = tk.Toplevel(self.frame)
        self._janela_consultas = janela
        janela.title("SentinelaLog — " + titulo)
        janela.configure(bg=s.BG)
        janela.transient(self.app.root)
        janela.resizable(False, False)

        painel = tk.Frame(janela, bg=s.BG, padx=16, pady=16)
        painel.pack(fill="both", expand=True)

        tk.Label(
            painel, text=titulo,
            bg=s.BG, fg=s.TEXT,
            font=(s.FONT, 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            painel,
            text="Consulta local, independente da API Groq.",
            bg=s.BG, fg=s.MUTED,
            font=(s.FONT, 10)
        ).pack(anchor="w", pady=(4, 10))

        def selecionar(pergunta, consulta):
            janela.destroy()
            self.consulta_local(pergunta, consulta)

        for pergunta, consulta in perguntas:
            botao(
                painel, pergunta,
                lambda p=pergunta, c=consulta: selecionar(p, c)
            ).pack(fill="x", pady=3)

        botao(
            painel, "Fechar", janela.destroy
        ).pack(anchor="e", pady=(10, 0))

        janela.bind("<Escape>", lambda evento: janela.destroy())
        janela.focus_set()

    def consulta_local(self, pergunta, consulta):
        try:
            estado = armazenamento.carregar(self.pasta)
            resposta = self.calcular_consulta_local(estado, consulta)

            self.escrever("Você | Consulta local", pergunta)
            self.escrever("SentinelaLog | Consulta local", resposta)

            self.status.configure(
                text="Consulta local concluída sem utilizar IA."
            )

        except (ValueError, OSError) as erro:
            messagebox.showerror(
                "Consulta local", str(erro),
                parent=self.app.root
            )

    @staticmethod
    def calcular_consulta_local(estado, consulta):
        eventos = acessos.consultar(estado)
        resumo = relatorios.resumir(estado)
        cadastrados = estado["usuarios"]
        ativos = usuarios.ativos(estado)

        aliases = {
            u["matricula"]: "U" + str(i)
            for i, u in enumerate(cadastrados, 1)
        }

        maquinas = {}
        for evento in eventos:
            maquina = evento["maquina"]
            if maquina not in maquinas:
                maquinas[maquina] = "M" + str(len(maquinas) + 1)

        permitidos = [
            "Falha de acesso",
            "Fora do horário permitido",
            "Origem bloqueada: aviso obrigatório",
            "Dentro das regras locais"
        ]

        def formatar(evento):
            usuario = aliases.get(evento["matricula"], "U?")
            maquina = maquinas[evento["maquina"]]

            if evento["maquina"] == "MAQ-X":
                maquina += " (MAQ-X)"

            motivos = [
                motivo for motivo in permitidos
                if motivo in evento["motivos"].split("; ")
            ]

            return (
                f'Evento {evento["id"]} | {evento["momento"]}\n'
                f'Usuário: {usuario} | Máquina: {maquina}\n'
                f'Resultado: {evento["resultado"]}\n'
                f'Risco: {evento["risco"].upper()}\n'
                'Motivos: ' +
                ("; ".join(motivos) or "Não disponível.")
            )

        def listar(registros):
            return "\n\n".join(
                formatar(e) for e in registros
            ) or "Nenhum registro encontrado."

        def resumo_riscos():
            contagem = relatorios.contar(eventos, "risco")
            return [
                f'Normais: {contagem.get("normal", 0)}',
                f'Suspeitos: {contagem.get("suspeito", 0)}',
                f'Críticos: {contagem.get("critico", 0)}'
            ]

        if consulta == "total_acessos":
            return f'Total de acessos: {resumo["acessos"]}'

        if consulta == "falhas":
            registros = [
                e for e in eventos
                if e["resultado"] == "falha"
            ]
            return (
                f'Total de falhas: {len(registros)}\n\n'
                + listar(registros)
            )

        if consulta == "criticos":
            registros = [
                e for e in eventos
                if e["risco"] == "critico"
            ]
            return (
                f'Total de acessos críticos: {len(registros)}\n\n'
                + listar(registros)
            )

        if consulta == "riscos":
            return "\n".join(resumo_riscos())

        if consulta == "maq_x":
            registros = acessos.por_maquina(estado, "MAQ-X")
            return (
                f'Acessos da MAQ-X: {len(registros)}\n\n'
                + listar(registros)
            )

        if consulta == "motivos_maq_x":
            registros = [
                e for e in acessos.por_maquina(estado, "MAQ-X")
                if e["risco"] == "critico"
            ]

            if not registros:
                return "Nenhum acesso crítico da MAQ-X registrado."

            return (
                "Motivos registrados nos acessos críticos "
                "da MAQ-X:\n\n"
                + listar(registros)
                + "\n\nClassificação preservada conforme as "
                  "regras aplicadas no momento do registro."
            )

        if consulta == "compartilhadas":
            compartilhadas = acessos.compartilhadas(estado)

            if not compartilhadas:
                return "Nenhuma máquina compartilhada encontrada."

            linhas = []
            for maquina, matriculas in compartilhadas.items():
                nome = maquinas[maquina]

                if maquina == "MAQ-X":
                    nome += " (MAQ-X)"

                linhas.append(
                    f'{nome}: {len(matriculas)} usuários distintos'
                )

            return (
                f'Máquinas compartilhadas: {len(compartilhadas)}\n\n'
                + "\n".join(linhas)
                + "\n\nCompartilhamento não identifica autoria."
            )

        if consulta == "total_usuarios":
            return "\n".join([
                f'Total de cadastros: {len(cadastrados)}',
                f'Usuários ativos: {len(ativos)}',
                f'Cadastros excluídos: {len(cadastrados) - len(ativos)}'
            ])

        if consulta == "perfis":
            contagem = relatorios.contar(ativos, "perfil")
            return "\n".join(
                f'{perfil.capitalize()}: {contagem.get(perfil, 0)}'
                for perfil in usuarios.PERFIS
            )

        if consulta == "resumo":
            return "\n".join([
                f'Usuários cadastrados: {len(cadastrados)}',
                f'Usuários ativos: {len(ativos)}',
                f'Total de acessos: {resumo["acessos"]}',
                f'Total de falhas: {resumo["falhas"]}',
                *resumo_riscos(),
                "Horários de pico: " +
                (", ".join(resumo["pico"]) or "nenhum"),
                "Máquinas compartilhadas: " +
                str(len(acessos.compartilhadas(estado)))
            ])

        raise ValueError("Consulta local desconhecida.")



    def escrever(self, autor, texto):
        self.conversa.configure(state="normal")
        self.conversa.insert("end", autor + "\n" + texto + "\n\n")
        self.conversa.see("end")
        self.conversa.configure(state="disabled")

    def configurar_chave(self):
        chave = simpledialog.askstring("Chave Groq", "Cole sua GROQ_API_KEY. "
                    "A chave ficará somente na memória desta sessão.",
                    show="*", parent=self.app.root)
        if chave is not None:
            self.app.chave_groq = chave.strip()
            self.status.configure(text="Configuração da chave atualizada para esta sessão.")

    def limpar(self):
        if self.app.ia_ocupada:
            return
        self.app.historico_ia.clear()
        self.conversa.configure(state="normal")
        self.conversa.delete("1.0", "end")
        self.conversa.configure(state="disabled")
        self.status.configure(text="Conversa limpa. O registro local de consultas foi preservado.")

    def enviar(self):
        if self.app.ia_ocupada:
            return
        try:
            estado = armazenamento.carregar(self.pasta)
            preparado = agente_ia.preparar(self.entrada.get(), estado,
                                         [p for p, r in self.app.historico_ia])
        except (ValueError, OSError) as erro:
            messagebox.showerror("Consulta de IA", str(erro), parent=self.app.root)
            return
        if not messagebox.askyesno("Enviar para Groq", "Serão enviados fatos do laboratório "
                "com aliases, regras e a pergunta abaixo. Os nomes e as matrículas cadastrados "
                "são substituídos por aliases. Observações e auditoria ficam fora dos fatos. "
                "Confira a pergunta antes de autorizar.\n\n"
                + preparado["pergunta"] + "\n\nAutorizar esta consulta externa?",
                parent=self.app.root):
            return
        self.app.ia_ocupada = True
        self.enviar_botao.configure(state="disabled")
        self.limpar_botao.configure(state="disabled")
        self.entrada.delete(0, "end")
        self.escrever("Você", preparado["pergunta"])
        self.status.configure(text="Consultando a Groq… uma chamada, sem repetição automática.")
        chave = self.app.chave_groq
        threading.Thread(target=self._trabalhar, args=(preparado, chave), daemon=True).start()
        self.app.root.after(100, lambda: self._receber(preparado["pergunta"]))

    def _trabalhar(self, preparado, chave):
        try:
            resposta = agente_ia.consultar(preparado, self.pasta, chave)
            self.resultados.put((True, resposta))
        except (ValueError, OSError) as erro:
            self.resultados.put((False, str(erro)))
        except Exception:
            # O detalhe de bibliotecas externas pode conter cabeçalhos e credenciais.
            self.resultados.put((False, "Não foi possível concluir a consulta."))

    def _receber(self, pergunta):
        try:
            ok, resposta = self.resultados.get_nowait()
        except queue.Empty:
            self.app.root.after(100, lambda: self._receber(pergunta))
            return
        self.app.ia_ocupada = False
        if ok:
            self.app.historico_ia.append((pergunta, resposta))
            self.app.historico_ia[:] = self.app.historico_ia[-10:]
        if not self.frame.winfo_exists():
            return
        self.escrever("SentinelaLog" if ok else "Aviso", resposta)
        self.status.configure(text="Consulta concluída e registrada." if ok else resposta)
        self.enviar_botao.configure(state="normal")
        self.limpar_botao.configure(state="normal")
