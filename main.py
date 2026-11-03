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
