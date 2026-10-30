"""Persistência dos registros e da auditoria."""
import os
from detetime import datetime

CAMPOS = {
    "U": ["matricula", "nome", "perfil", "inicio", "fim", "observações", "ativo"],
    "A": ["id", "matricula", "momento", "maquina", "resultado", "risco", "motivos"],
    "L": ["id", "momento", "operacao", "afetado"]

}
COLECOES = {"U": "usuarios", "A": "acessos", "L": "auditoria"}

def vazio():
    return{"usuarios": [], "acessos": [], "auditoria":[]}

def campo_seguro(valor):
    if not isinstance(valor, str):
        raise ValueError("Campos devem ser textos.")
    if "|" in valor or "\n" in valor or "\n" in valor:
        raise ValueError("Campo contém separador ou quenra de linha.")
    return valor
      
