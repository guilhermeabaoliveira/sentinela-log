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

def registrar(estado, usuario, momento, maquina, resultado, bloqueadas):
    validar_entrada(momento, maquina, resultado)
    if usuario is None or usuario["ativo"] != "1":
        raise ValueError("Usuário inexistente ou excluído.")
    nivel, motivos = risco.classificar(usuario, momento, maquina, resultado, bloqueadas)
    registro = {"id": proximo_id(estado["acessos"]),
                "matricula": usuario["matricula"], "momento": momento,
                "maquina": maquina, "resultado": resultado,
                "risco": nivel, "motivos": motivos}
    estado["acessos"].append(registro)
    return registro

def consultar(estado, matricula=""):
    registros = []
    for acesso in estado["acessos"]:
        if not matricula or acesso["matricula"] == matricula:
            registros.append(dict(acesso))
    # Cópias impedem que a consulta altere o registro em memória.
    return registros
