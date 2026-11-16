def contar(acessos, campo):
    contagens = {}

    for acesso in acessos:
        valor = acesso[campo]
        contagens[valor] = contagens.get(valor, 0) + 1

    return contagens

def maiores(contagens):
    if not contagens:
        return []

    maior = max(contagens.values())
    empatados = []

    for valor in contagens:
        if contagens[valor] == maior:
            empatados.append(valor)

    return empatados

def totais(acessos):
    resultados = contar(acessos, "resultado")

    return {
        "acessos": len(acessos),
        "falhas": resultados.get("falha", 0)
    }

def resumir(estado):
    resumo = totais(estado["acessos"])

    falhas = {}
    horarios = {}

    riscos = contar(estado["acessos"], "risco")

    for acesso in estado["acessos"]:

        hora = acesso["momento"][11:13]

        horarios[hora] = horarios.get(hora, 0) + 1

        if acesso["resultado"] == "falha":
            matricula = acesso["matricula"]

            falhas[matricula] = falhas.get(matricula, 0) + 1

    resumo["mais_falhas"] = maiores(falhas)
    resumo["pico"] = maiores(horarios)

    resumo["suspeitos"] = riscos.get("suspeito", 0)
    resumo["criticos"] = riscos.get("critico", 0)

    resumo["falhas_por_usuario"] = falhas
    resumo["por_hora"] = horarios

    return resumo

def linhas_relatorio(estado):
    import usuarios

    resumo = resumir(estado)

    identidades = []

    for matricula in resumo["mais_falhas"]:

        usuario = usuarios.buscar(estado, matricula, False)

        if usuario is None:
            raise ValueError("Usuário do histórico não encontrado.")

        situacao = "ativo"

        if usuario["ativo"] == "0":
            situacao = "excluído"

        mascara = usuarios.mascarar(matricula)

        identidades.append(
            f'{usuario["nome"]} ({mascara}; {situacao})'
        )

    return [
        f'Total de acessos: {resumo["acessos"]}',
        f'Total de falhas: {resumo["falhas"]}',
        'Usuários com mais falhas: ' + (
            ", ".join(identidades) or "nenhum"
        ),
        'Horas com mais movimento: ' + (
            ", ".join(resumo["pico"]) or "nenhuma"
        ),
        f'Suspeitos: {resumo["suspeitos"]}',
        f'Críticos: {resumo["criticos"]}'
    ]

def apresentar(estado):
    for linha in linhas_relatorio(estado):
        print(linha)

    return resumir(estado)

def testar_relatorio_basico():
    vazio = {"acessos": []}

    resumo = resumir(vazio)

    assert resumo["acessos"] == 0
    assert resumo["falhas"] == 0
    assert resumo["mais_falhas"] == []
    assert resumo["pico"] == []

    assert maiores({
        "A": 2,
        "B": 2,
        "C": 1
    }) == ["A", "B"]

    acessos = [
        {
            "matricula": "111",
            "momento": "2026-10-26 10:00",
            "resultado": "falha",
            "risco": "suspeito"
        },
        {
            "matricula": "222",
            "momento": "2026-10-26 11:00",
            "resultado": "falha",
            "risco": "suspeito"
        }
    ]

    resumo = resumir({"acessos": acessos})

    assert resumo["mais_falhas"] == ["111", "222"]
    assert resumo["pico"] == ["10", "11"]
    assert resumo["suspeitos"] == 2

    return True

def grafico(estado):
    riscos = contar(estado["acessos"], "risco")

    linhas = []
    maior = 0

    if riscos:
        maior = max(riscos.values())

    for nivel in ["normal", "suspeito", "critico"]:

        quantidade = riscos.get(nivel, 0)

        barras = 0

        if maior:
            barras = quantidade * 20 // maior

            if quantidade and barras == 0:
                barras = 1

        linhas.append(
            f'{nivel}: {"#" * barras} ({quantidade})'
        )

    return linhas

def mostrar_grafico(estado):
    print("Gráfico de riscos: maior categoria ocupa 20 marcas.")

    for linha in grafico(estado):
        print(linha)

def testar_grafico():
    estado = {"acessos": []}

    linhas = grafico(estado)

    assert len(linhas) == 3

    for linha in linhas:
        assert "(0)" in linha

    estado["acessos"] = (
        [{"risco": "normal"}] * 25
        + [{"risco": "critico"}]
    )

    linhas = grafico(estado)

    assert linhas[0].count("#") == 20
    assert linhas[1].count("#") == 0
    assert linhas[2].count("#") == 1

    assert "(25)" in linhas[0]
    assert "(1)" in linhas[2]

    assert maiores({}) == []

    return True