"""Classificação de acessos e explicação dos sinais de risco."""

from datetime import datetime

def momento_valido(texto):
    momento = datetime.strptime(texto, "%Y-%m-%d %H:%M")
    if momento.strftime("%Y-%m-%d %H:%M") != texto:
        raise ValueError("Use data e hora no formato AAAA-MM-DD HH:MM.")
    return momento

def fora_horario(momento, inicio, fim):
    horario = momento_valido(momento).strftime("%H:%M")
    for texto in [inicio, fim]:
        if len(texto) != 5:
            raise ValueError("Use horário HH:MM.")
        datetime.strptime(texto, "%H:%M")
    if inicio == fim:
        raise ValueError("Janela sem duração definida.")
    if inicio < fim:
        return horario < inicio or horario > fim
    # Janela que começa à noite e termina na manhã seguinte.
    return fim < horario < inicio

def ler_bloqueadas(caminho):
    bloqueadas = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            maquina = linha.strip()
            if maquina:
                bloqueadas.append(maquina)
    return bloqueadas

def classificar(usuario, momento, maquina, resultado, bloqueadas):
    motivos = []
    if resultado == "falha":
        motivos.append("Falha de acesso")
    if fora_horario(momento, usuario["inicio"], usuario["fim"]):
        motivos.append("Fora do horário permitido")
    if maquina in bloqueadas:
        motivos.append("Origem bloqueada: aviso obrigatório")
        return "critico", "; ".join(motivos)
    if len(motivos) > 1:
        return "critico", "; ".join(motivos)
    if motivos:
        return "suspeito", "; ".join(motivos)
    return "normal", "Dentro das regras locais"

def exemplos_fronteira():
 usuario = {"inicio": "07:00", "fim": "18:00"}
 dentro = classificar(usuario, "2026-10-26 10:00", "MAQ-A", "sucesso", [])
 fora = classificar(usuario, "2026-10-26 03:00", "MAQ-A", "sucesso", [])
 falha = classificar(usuario, "2026-10-26 03:00", "MAQ-A", "falha", [])
 bloqueio = classificar(usuario, "2026-10-26 10:00", "MAQ-X", "sucesso", ["MAQ-X"])
 assert dentro[0] == "normal"
 assert fora[0] == "suspeito"
 assert falha[0] == "critico"
 assert bloqueio[0] == "critico"
 return [dentro, fora, falha, bloqueio]

def descricao_regras():
 return ["Uma falha OU acesso fora do horário: suspeito.",
         "Falha E acesso fora do horário: crítico.",
         "Origem bloqueada: crítico e aviso, sem impedir gravação.",
         "Nenhuma condição: normal.",
         "Limites de início e fim inclusivos; janela noturna permitida."]

def testar_janela_noturna():
    inicio = "22:00"
    fim = "06:00"
    assert not fora_horario("2026-10-26 22:00", inicio, fim)
    assert not fora_horario("2026-10-27 06:00", inicio, fim)
    assert not fora_horario("2026-10-26 23:59", inicio, fim)
    assert fora_horario("2026-10-26 12:00", inicio, fim)
    return True

def testar_motivos_combinados():
    usuario = {"inicio": "07:00", "fim": "18:00"}
    nivel, motivos = classificar(usuario, "2026-10-26 03:00", "MAQ-X", "falha", ["MAQ-X"])
    assert nivel == "critico"
    assert "Falha" in motivos
    assert "Fora do horário" in motivos
    assert "Origem bloqueada" in motivos
    return True

def conferir_lista(caminho):
    maquinas = ler_bloqueadas(caminho)
    conferidas = []
    for maquina in maquinas:
        if "|" in maquina or "\r" in maquina or "\n" in maquina:
            raise ValueError("Origem inválida no arquivo de bloqueadas.")
        if maquina not in conferidas:
            conferidas.append(maquina)
    return conferidas

def testar_limites_diurnos():
    assert not fora_horario("2026-10-26 07:00", "07:00", "18:00")
    assert not fora_horario("2026-10-26 18:00", "07:00", "18:00")
    assert fora_horario("2026-10-26 06:59", "07:00", "18:00")
    assert fora_horario("2026-10-26 18:01", "07:00", "18:00")
    return True

def testar_datas_invalidas():
    for texto in ["2026-02-30 10:00", "2026-10-26 25:00", "26/10/2026 10:00"]:
        try:
            momento_valido(texto)
        except ValueError:
            continue
        raise AssertionError("Data inválida aceita.")
    return True

def testar_origem_bloqueada():
    usuario = {"inicio": "07:00", "fim": "18:00"}
    nivel, motivos = classificar(usuario, "2026-10-26 10:00", "MAQ-X", "sucesso", ["MAQ-X"])
    assert nivel == "critico"
    assert "bloqueada" in motivos
    assert "Falha" not in motivos
    return True
