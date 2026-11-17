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

    
def salvar(pasta, estado, operacao, afetado):
    campo_seguro(operacao)
    campo_seguro(afetado)
    os.makedirs(pasta, exist_ok=True)
    carregar(pasta)  # Arquivo corrompido existente nunca é substituído silenciosamente.
    copia = vazio()
    for chave in estado:
        for item in estado[chave]:
            copia[chave].append(dict(item))
    maior = 0
    for log in copia["auditoria"]:
        maior = max(maior, int(log["id"]))
    copia["auditoria"].append({"id": str(maior + 1),
        "momento": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "operacao": operacao, "afetado": afetado})
    validar_estado(copia)
    caminho = os.path.join(pasta, "estado.txt")
    temporario = caminho + ".tmp"
    try:
        with open(temporario, "x", encoding="utf-8", newline="\n") as arquivo:
            for tipo in CAMPOS:
                for registro in copia[COLECOES[tipo]]:
                    valores = [tipo]
                    for campo in CAMPOS[tipo]:
                        valores.append(registro[campo])
                    arquivo.write("|".join(valores) + "\n")
        os.replace(temporario, caminho)
    except OSError:
        # Temporário fica preservado para diagnóstico; nenhuma mensagem de sucesso.
        raise
    return copia


def consultar_auditoria(estado, operacao=""):
    resultado = []
    for registro in estado["auditoria"]:
        if not operacao or registro["operacao"] == operacao:
            resultado.append(dict(registro))
    return resultado

def conferir_serializacao(estado):
    validar_estado(estado)
    linhas = []
    for tipo in CAMPOS:
        for registro in estado[COLECOES[tipo]]:
            valores = [tipo]
            for campo in CAMPOS[tipo]:
                valores.append(campo_seguro(registro[campo]))
            linhas.append("|".join(valores))
    return linhas


def testar_reabertura(pasta):
    import usuarios
    estado = vazio()
    usuarios.cadastrar(estado, "9001", "Pessoa Fictícia", "professor", "08:00", "17:00", "")
    salvo = salvar(pasta, estado, "CADASTRO", "9001")
    lido = carregar(pasta)
    assert lido == salvo
    assert len(lido["auditoria"]) == 1
    assert lido["auditoria"][0]["operacao"] == "CADASTRO"
    retorno = consultar_auditoria(lido)
    retorno[0]["operacao"] = "ALTERADO"
    assert lido["auditoria"][0]["operacao"] == "CADASTRO"
    return True

def caminho_dados(pasta):
    return os.path.join(pasta, "estado.txt")

import armazenamento
import usuarios
import os

def testar_persistencia(pasta):
    assert armazenamento.testar_reabertura(pasta)
    estado = armazenamento.carregar(pasta)
    usuarios.excluir(estado, "9001")
    armazenamento.salvar(pasta, estado, "EXCLUSAO", "9001")
    lido = armazenamento.carregar(pasta)
    assert usuarios.buscar(lido, "9001") is None
    assert usuarios.buscar(lido, "9001", False) is not None
    assert len(lido["auditoria"]) == 2
    assert lido["auditoria"][-1]["operacao"] == "EXCLUSAO"
    assert armazenamento.conferir_serializacao(lido)
    return True

def testar_corrupcao(pasta):
    os.makedirs(pasta, exist_ok=True)
    caminho = armazenamento.caminho_dados(pasta)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("CONTEUDO_CORROMPIDO\n")
    for operacao in ["ler", "salvar"]:
        try:
            if operacao == "ler":
                armazenamento.carregar(pasta)
            else:
                armazenamento.salvar(pasta, armazenamento.vazio(), "TESTE", "-")
        except ValueError:
            pass
        else:
            raise AssertionError("Arquivo corrompido foi aceito.")
    with open(caminho, encoding="utf-8") as arquivo:
        assert arquivo.read() == "CONTEUDO_CORROMPIDO\n"
    return True

        


        


    
