from datetime import datetime


def gerar_relatorio(estado):
    acessos = estado.get("acessos", [])

    sucessos = [
        acesso for acesso in acessos
        if acesso.get("resultado") == "sucesso"
    ]

    falhas = [
        acesso for acesso in acessos
        if acesso.get("resultado") == "falha"
    ]

    usuarios = set()
    maquinas = set()
    riscos = {}

    for acesso in acessos:
        usuarios.add(acesso.get("matricula", "Não identificada"))
        maquinas.add(acesso.get("maquina", "Não identificada"))

        nivel = acesso.get("risco", "Não identificado")
        riscos[nivel] = riscos.get(nivel, 0) + 1

    relatorio = {
        "titulo": "Relatório de Logins - SentinelaLog",
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),

        "total_tentativas": len(acessos),
        "logins_sucesso": len(sucessos),
        "logins_falha": len(falhas),

        "usuarios_identificados": len(usuarios),
        "maquinas_utilizadas": len(maquinas),

        "riscos": riscos,

        "historico": acessos
    }

    return relatorio


def exibir_relatorio(estado):
    relatorio = gerar_relatorio(estado)

    print("\n" + "=" * 60)
    print(relatorio["titulo"])
    print("=" * 60)

    print(f"Data de geração: {relatorio['data']}")

    print("\nRESUMO DOS ACESSOS")
    print("-" * 60)

    print(f"Total de tentativas: {relatorio['total_tentativas']}")
    print(f"Logins bem-sucedidos: {relatorio['logins_sucesso']}")
    print(f"Logins com falha: {relatorio['logins_falha']}")

    print("\nIDENTIFICAÇÃO")
    print("-" * 60)

    print(
        f"Usuários identificados: "
        f"{relatorio['usuarios_identificados']}"
    )

    print(
        f"Máquinas utilizadas: "
        f"{relatorio['maquinas_utilizadas']}"
    )

    print("\nDISTRIBUIÇÃO DE RISCOS")
    print("-" * 60)

    if relatorio["riscos"]:
        for nivel, quantidade in relatorio["riscos"].items():
            print(f"{nivel}: {quantidade} ocorrência(s)")
    else:
        print("Nenhum registro de risco encontrado.")

    print("\nHISTÓRICO DE LOGINS")
    print("-" * 60)

    if not relatorio["historico"]:
        print("Nenhuma tentativa de acesso registrada.")

    for acesso in relatorio["historico"]:
        print(f"\nID: {acesso.get('id', '-')}")
        print(f"Matrícula: {acesso.get('matricula', '-')}")
        print(f"Data/Hora: {acesso.get('momento', '-')}")
        print(f"Máquina: {acesso.get('maquina', '-')}")
        print(f"Resultado: {acesso.get('resultado', '-')}")
        print(f"Risco: {acesso.get('risco', '-')}")
        print(f"Motivos: {acesso.get('motivos', '-')}")

    print("\n" + "=" * 60)
