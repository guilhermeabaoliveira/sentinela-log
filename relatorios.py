
from datetime import datetime


def gerar_relatorio():
    relatorio = {
        "projeto": "Sistema de Histórico de Acessos - Sentinela Log",
        "data": datetime.now().strftime("%d/%m/%Y"),

        "funcionalidades_desenvolvidas": [
            "Criação da estrutura para validar os dados de entrada dos acessos.",
            "Validação do momento do acesso por meio do módulo risco.",
            "Verificação da identificação da máquina fictícia.",
            "Prevenção de caracteres reservados nos campos de texto.",
            "Validação do resultado do acesso, aceitando sucesso ou falha.",
            "Geração automática do próximo ID com base nos registros existentes.",
            "Criação da estrutura de armazenamento para usuários, acessos e auditoria.",
            "Definição dos campos necessários para cada coleção de dados.",
            "Implementação de uma função para inicializar as coleções vazias.",
            "Criação de uma função para validar campos de texto e impedir separadores e quebras de linha.",
            "Definição dos perfis de usuário: estudante, professor e administrador.",
            "Implementação da validação do nome e da matrícula dos usuários.",
            "Validação dos perfis permitidos no cadastro.",
            "Validação dos horários de início e fim utilizando datetime.",
            "Verificação para impedir horários de início e fim iguais."
        ],

        "modulos_utilizados": [
            "datetime: utilizado para trabalhar com datas e horários.",
            "risco: utilizado para validar o momento do acesso.",
            "os: utilizado como suporte a operações do sistema de arquivos."
        ],

        "organizacao_dos_dados": [
            "Coleção U: armazenamento dos dados dos usuários.",
            "Coleção A: armazenamento dos registros de acesso.",
            "Coleção L: armazenamento dos registros de auditoria.",
            "Definição dos campos de identificação, horários, perfis e situações dos usuários.",
            "Definição dos campos de identificação, máquina, resultado e risco dos acessos.",
            "Definição dos campos de operação e elemento afetado na auditoria."
        ],

        "planejamento_futuro": [
            "Implementar um CRUD completo para os usuários.",
            "Implementar um CRUD completo para os registros de acesso.",
            "Permitir cadastrar novos usuários e acessos.",
            "Permitir consultar os dados registrados.",
            "Permitir atualizar registros existentes.",
            "Permitir excluir registros.",
            "Integrar as operações a uma estrutura persistente de armazenamento de dados.",
            "Implementar o registro automático das operações na auditoria.",
            "Integrar os módulos de validação, usuários, acessos e auditoria.",
            "Desenvolver uma interface para facilitar a utilização do sistema."
        ],

        "status": (
            "O projeto avançou na estruturação dos dados, na validação "
            "dos cadastros de usuários e na preparação das coleções "
            "de armazenamento e auditoria. Também foram estabelecidas "
            "regras para validação de horários, perfis e campos de texto. "
            "As próximas etapas envolvem a implementação do CRUD, "
            "a persistência dos dados e a integração dos módulos."
        )
    }

    return relatorio


def exibir_relatorio():
    relatorio = gerar_relatorio()

    print("=" * 60)
    print("RELATÓRIO DO PROJETO")
    print("=" * 60)

    print(f"Projeto: {relatorio['projeto']}")
    print(f"Data: {relatorio['data']}")

    print("\nFuncionalidades desenvolvidas:")
    for item in relatorio["funcionalidades_desenvolvidas"]:
        print(f"- {item}")

    print("\nMódulos utilizados:")
    for item in relatorio["modulos_utilizados"]:
        print(f"- {item}")

    print("\nOrganização dos dados:")
    for item in relatorio["organizacao_dos_dados"]:
        print(f"- {item}")

    print("\nPlanejamento futuro:")
    for item in relatorio["planejamento_futuro"]:
        print(f"- {item}")

    print(f"\nStatus atual: {relatorio['status']}")
    print("=" * 60)


if __name__ == "__main__":
    exibir_relatorio()
