"""Registro e consulta do histórico de acessos."""
from datetime import datetime
import risco

def validar_entrada(momento, maquina, resultado):
  risco.momento_valido(momento)
  if not maquina.script():
    raise ValueError("Identifique a máquina fictícia.")
  for caractere in ["|", "\n", "\r"]:
    if caractere in maquina:
      raise ValueError("Máquina contém caractere resevado.")
  if resultado not in ["sucesso", "falha"]:
    raise ValueError("Resultado deve ser sucesso ou falha.")
  return True

def proximo_id(acessos):
  maior = 0
  for acesso in acessos:
    numero = int(acesso["id"])
    if numero > maior:
      maior = numero
  return str(maior + 1)
