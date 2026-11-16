import os
import armazenamento
import usuarios
import acessos
import risco
import relatorios

PASTA = os.path.join(os.path.dirname(__file__), "dados")

def ler(rotulo):
    return input(rotulo + ": ").strip()

def mostrar_menu():
    print("\nSentinelaLog — demonstração com dados fictícios")
    print("1 Cadastrar | 2 Usuários | 3 Editar | 4 Excluir")
    print("5 Registrar acesso | 6 Acessos | 7 Auditoria")
    print("8 Revelar matrícula | 9 Segurança | 10 IA reservada")
    print("0 Sair")

def dados_usuario():
    return [ler("Nome fictício"), ler("Perfil"), ler("Início HH:MM"),
            ler("Fim HH:MM"), ler("Observações")]


def tratar_usuario(opcao, estado):
    if opcao == "1":
        matricula = ler("Matrícula fictícia")
        valores = dados_usuario()
        usuarios.cadastrar(estado, matricula, *valores)
        return "CADASTRO", matricula
    if opcao == "2":
        for usuario in usuarios.ativos(estado):
            print(usuario["nome"], usuarios.mascarar(usuario["matricula"]),
                  usuario["perfil"], usuario["inicio"], usuario["fim"], usuario["observacoes"])
        return "CONSULTA_USUARIOS", "-"
    matricula = ler("Matrícula fictícia")
    if opcao == "3":
        usuarios.editar(estado, matricula, *dados_usuario())
        return "EDICAO", matricula
    usuarios.excluir(estado, matricula)
    return "EXCLUSAO", matricula


def tratar_acesso(opcao, estado, pasta):
    if opcao == "6":
        for linha in acessos.linhas_consulta(estado):
            print(linha)
        return "CONSULTA_ACESSOS", "-", None
    matricula = ler("Matrícula fictícia")
    usuario = usuarios.buscar(estado, matricula)
    if usuario is None:
        raise ValueError("Usuário ativo não encontrado.")
    momento = ler("Data e hora AAAA-MM-DD HH:MM")
    maquina = ler("Máquina fictícia")
    resultado = ler("Resultado: sucesso ou falha")
    bloqueadas = risco.ler_bloqueadas(os.path.join(pasta, "bloqueadas.txt"))
    registro = acessos.registrar(estado, usuario, momento, maquina, resultado, bloqueadas)
    # A classificação só será anunciada após a gravação persistente.
    return "REGISTRO_ACESSO", matricula, registro


def executar(pasta=PASTA):
    while True:
        mostrar_menu()
        try:
            opcao = ler("Opção")
            if opcao == "0":
                return
            estado = armazenamento.carregar(pasta)
            registro = None
            revelacao = None
            if opcao in ["1", "2", "3", "4"]:
                operacao, afetado = tratar_usuario(opcao, estado)
            elif opcao in ["5", "6"]:
                operacao, afetado, registro = tratar_acesso(opcao, estado, pasta)
            elif opcao == "7":
                for log in estado["auditoria"]:
                    print(log["momento"], log["operacao"], usuarios.mascarar(log["afetado"]))
                operacao, afetado = "CONSULTA_AUDITORIA", "-"
            elif opcao == "8":
                afetado = ler("Matrícula fictícia")
                revelacao = usuarios.revelar(estado, afetado)
                operacao = "REVELACAO_MATRICULA"
            elif opcao == "9":
                relatorios.apresentar(estado)
                relatorios.mostrar_grafico(estado)
                print("Máquinas compartilhadas:")
                linhas = acessos.linhas_compartilhadas(estado)
                if not linhas:
                    print("Nenhuma máquina compartilhada.")
                for linha in linhas:
                    print(linha)
                print("Compartilhamento não identifica autoria de uma ação.")
                operacao, afetado = "RELATORIO_SEGURANCA", "-"
            elif opcao == "10":
                print("Consulta ao agente indisponível.")
                continue
            else:
                print("Opção indisponível neste marco.")
                continue
            armazenamento.salvar(pasta, estado, operacao, afetado)
            if registro is not None:
                print(registro["risco"], registro["motivos"])
            if revelacao is not None:
                print("Matrícula:", revelacao)
            print("Operação gravada com auditoria.")
        except (OSError, ValueError, UnicodeError) as erro:
            print("Operação não concluída:", erro)
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado.")
            return

def abertura():
    print("Somente dados fictícios. Execução local por um processo.")
    print("Matrícula mascarada não é criptografia ou autenticação.")
    for linha in risco.descricao_regras():
        print(linha)
    print("Dados e auditoria ficam juntos no arquivo dados/estado.txt.")
    print("Origens bloqueadas são lidas de dados/bloqueadas.txt.")
    print("As regras são uma proposta didática, não exigência literal dos professores.")

if __name__ == "__main__":
    abertura()
    executar()
