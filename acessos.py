"""Registro e consulta do histórico de acessos."""
from datetime import datetime
import risco

def validar_entrada(momento, maquina, resultado):
  risco.momento_valido(momento)
  if not maquina.strip():
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



def linhas_consulta(estado, matricula=""):
    import usuarios
    linhas = []
    for acesso in consultar(estado, matricula):
        mascara = usuarios.mascarar(acesso["matricula"])
        linhas.append(f'{acesso["id"]} {mascara} {acesso["momento"]} '
                      f'{acesso["maquina"]} {acesso["resultado"]} '
                      f'{acesso["risco"]}: {acesso["motivos"]}')
    return linhas

def conferir_consulta_independente():
    registro = {"id": "1", "matricula": "1234"}
    estado = {"acessos": [registro]}
    copia = consultar(estado)
    copia[0]["id"] = "999"
    assert estado["acessos"][0]["id"] == "1"
    assert consultar(estado, "0000") == []
    return True

def por_maquina(estado, maquina):
    registros = []
    for acesso in estado["acessos"]:
        if acesso["maquina"] == maquina:
            registros.append(dict(acesso))
    return registros

def testar_identificadores():
    assert proximo_id([]) == "1"
    assert proximo_id([{"id": "4"}, {"id": "2"}]) == "5"
    estado = {"acessos": [{"id": "1", "maquina": "A"},
                          {"id": "2", "maquina": "B"}]}
    resultado = por_maquina(estado, "A")
    assert len(resultado) == 1
    resultado[0]["id"] = "99"
    assert estado["acessos"][0]["id"] == "1"
    return True


def compartilhadas(estado):
    por_origem = {}
    for acesso in estado["acessos"]:
        maquina = acesso["maquina"]
        matricula = acesso["matricula"]
        if maquina not in por_origem:
            por_origem[maquina] = []
        if matricula not in por_origem[maquina]:
            por_origem[maquina].append(matricula)
    resultado = {}
    for maquina in por_origem:
        if len(por_origem[maquina]) > 1:
            resultado[maquina] = por_origem[maquina]
    return resultado

def linhas_compartilhadas(estado):
    import usuarios
    linhas = []
    for maquina, matriculas in compartilhadas(estado).items():
        identidades = []
        for item in matriculas:
            identidades.append(usuarios.identidade_publica(estado, item))
        linhas.append(maquina + ": " + ", ".join(identidades))
    return linhas


def testar_compartilhamento():
    estado = {"acessos": [
        {"maquina": "A", "matricula": "111"},
        {"maquina": "A", "matricula": "111"},
        {"maquina": "B", "matricula": "222"}
    ]}
    assert compartilhadas(estado) == {}
    estado["acessos"].append({"maquina": "A", "matricula": "222"})
    assert compartilhadas(estado) == {"A": ["111", "222"]}
    assert len(por_maquina(estado, "A")) == 3
    assert len(consultar(estado, "111")) == 2
    copia = por_maquina(estado, "A")
    copia[0]["matricula"] = "999"
    assert estado["acessos"][0]["matricula"] == "111"
    return True
