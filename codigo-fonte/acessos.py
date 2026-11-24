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
import acessos
import usuarios

def testar_historico():
    estado = {"usuarios": [], "acessos": []}
    pessoa = usuarios.cadastrar(estado, "1234", "Pessoa Fictícia", "estudante", "07:00", "18:00", "")
    registro = acessos.registrar(estado, pessoa, "2026-10-26 03:00", "A", "sucesso", [])
    assert registro["risco"] == "suspeito"
    usuarios.editar(estado, "1234", "Pessoa Fictícia", "estudante", "00:00", "23:59", "")
    usuarios.excluir(estado, "1234")
    assert acessos.consultar(estado)[0]["risco"] == "suspeito"
    assert len(acessos.consultar(estado)) == 1
    assert "1234" not in acessos.linhas_consulta(estado)[0]
    assert acessos.testar_identificadores()
    return True


def testar_consultas():
    assert acessos.conferir_consulta_independente()
    assert acessos.testar_compartilhamento()
    estado = {"usuarios": [], "acessos": []}
    for matricula in ["1001", "1002"]:
        pessoa = usuarios.cadastrar(estado, matricula, "Pessoa " + matricula[-1], "estudante", "07:00", "18:00", "")
        acessos.registrar(estado, pessoa, "2026-10-26 10:00", "A", "sucesso", [])
    usuarios.excluir(estado, "1001")
    linhas = acessos.linhas_compartilhadas(estado)
    assert len(linhas) == 1
    assert "excluído" in linhas[0]
    assert "1001" not in linhas[0]
    assert "1002" not in linhas[0]
    return True
