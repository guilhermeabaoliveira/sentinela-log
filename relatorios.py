from datetime import datetime

def gerar_relatorio():
    relatorio = {
        "projeto": "Sistema de Histórico de Acessos",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "funcionalidades_desenvolvidas": [
            "Criação da estrutura para validar os dados de entrada.",
            "Validação do momento do acesso por meio do módulo risco.",
            "Verificação da identificação da máquina fictícia.",
            "Prevenção de caracteres reservados no nome da máquina.",
            "Validação do resultado do acesso, aceitando sucesso ou falha.",
            "Geração automática do próximo ID com base nos registros existentes."
        ],
        "modulos_utilizados": [
            "datetime: utilizado para trabalhar com datas e horários.",
            "risco: utilizado para validar o momento do acesso."
        ],
        "planejamento_futuro": [
            "Implementar um CRUD para os registros de acesso.",
            "Permitir cadastrar novos acessos.",
            "Permitir consultar os acessos registrados.",
            "Permitir atualizar registros existentes.",
            "Permitir excluir registros.",
            "Integrar as operações a uma estrutura de armazenamento de dados."
        ],
        "status": (
            "Etapa inicial de validação e preparação dos registros. "
            "O CRUD será desenvolvido futuramente."
        )
    }

    return relatorio


def exibir_relatorio():
    relatorio = gerar_relatorio()

    print("=" * 50)
    print("RELATÓRIO DO PROJETO")
    print("=" * 50)

    print(f"Projeto: {relatorio['projeto']}")
    print(f"Data: {relatorio['data']}")

    print("\nFuncionalidades desenvolvidas:")
    for item in relatorio["funcionalidades_desenvolvidas"]:
        print(f"- {item}")

    print("\nMódulos utilizados:")
    for item in relatorio["modulos_utilizados"]:
        print(f"- {item}")

    print("\nPlanejamento futuro:")
    for item in relatorio["planejamento_futuro"]:
        print(f"- {item}")

    print(f"\nStatus atual: {relatorio['status']}")
    print("=" * 50)


if __name__ == "__main__":
    exibir_relatorio()
