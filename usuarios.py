"""Cadastro e consulta de usuários do laboratório fictício."""

from datetime import datetime

PERFIS = ["estudante", "professor", "administrador"]

def validar(nome, matricula, perfil, inicio, fim, observacoes):
  valores = [nome, matricula, perfil, inicio, fim, observacoes]
  for valor in valores:
    if not isinstance(valor, str) or "|" in valor or "\n" in valor or "\r" in valor:
      raise ValueError("Texto inválido no cadastro")

  if not nome.strip() or not matricula.isdigit():
    raise ValueError("Informe nome e matrícula numérica.")

  if perfil not in PERFIS:
    raise ValueError("Perfil deve ser estudante, professor ou administrador.")

  for horario in [inicio, fim]:
    if len(horario) != 5:
      raise ValueError("Use horário HH:MM")
    datetime.strptime(horario, "%H:%M")

  if inicio == fim:
    raise ValueError("Início e fim devem ser diferentes.")

  return True
