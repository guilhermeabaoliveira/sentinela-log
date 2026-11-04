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
