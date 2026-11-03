"""Persistência dos registros e da auditoria."""
import os
from datetime import datetime

CAMPOS = {
    "U": ["matricula", "nome", "perfil", "inicio", "fim", "observacoes", "ativo"],
    "A": ["id", "matricula", "momento", "maquina", "resultado", "risco", "motivos"],
    "L": ["id", "momento", "operacao", "afetado"]
}
COLECOES = {"U": "usuarios", "A": "acessos", "L": "auditoria"}

def vazio():
    return {"usuarios": [], "acessos": [], "auditoria": []}

def campo_seguro(valor):
    if not isinstance(valor, str):
        raise ValueError("Campos devem ser textos.")
    if "|" in valor or "\n" in valor or "\r" in valor:
        raise ValueError("Campo contém separador ou quebra de linha.")
    return valor


def carregar(pasta):
    caminho = os.path.join(pasta, "estado.txt")
    estado = vazio()
    try:
        arquivo = open(caminho, "r", encoding="utf-8")
    except FileNotFoundError:
        return estado
    with arquivo:
        numero = 0
        for linha in arquivo:
            numero += 1
            partes = linha.rstrip("\n").split("|")
            tipo = partes[0]
            if tipo not in CAMPOS or len(partes) != len(CAMPOS[tipo]) + 1:
                raise ValueError(f"Arquivo inválido na linha {numero}; nada foi substituído.")
            registro = {}
            for indice in range(len(CAMPOS[tipo])):
                campo = CAMPOS[tipo][indice]
                registro[campo] = partes[indice + 1]
            estado[COLECOES[tipo]].append(registro)
    validar_estado(estado)
    return estado
    
    
def validar_estado(estado):
    import usuarios
    import acessos
    matriculas = []
    for usuario in estado["usuarios"]:
        usuarios.validar(usuario["nome"], usuario["matricula"], usuario["perfil"],
                         usuario["inicio"], usuario["fim"], usuario["observacoes"])
        if usuario["matricula"] in matriculas or usuario["ativo"] not in ["0", "1"]:
            raise ValueError("Usuário duplicado ou estado inválido no arquivo.")
        matriculas.append(usuario["matricula"])
    for tipo in ["A", "L"]:
        identificadores = []
        for registro in estado[COLECOES[tipo]]:
            if not registro["id"].isdigit() or int(registro["id"]) < 1 or registro["id"] in identificadores:
                raise ValueError("Identificador inválido ou duplicado.")
            identificadores.append(registro["id"])
            datetime.strptime(registro["momento"], "%Y-%m-%d %H:%M")
            if tipo == "A":
                acessos.validar_entrada(registro["momento"], registro["maquina"], registro["resultado"])
                if registro["matricula"] not in matriculas or registro["risco"] not in ["normal", "suspeito", "critico"]:
                    raise ValueError("Referência ou risco inválido no acesso.")
    for tipo in CAMPOS:
        for registro in estado[COLECOES[tipo]]:
            for campo in CAMPOS[tipo]:
                campo_seguro(registro[campo])
    
