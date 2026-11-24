from datetime import datetime

PERFIS = ["estudante", "professor", "administrador"]

def validar(nome, matricula, perfil, inicio, fim, observacoes):
    valores = [nome, matricula, perfil, inicio, fim, observacoes]
    for valor in valores:
        if not isinstance(valor, str) or "|" in valor or "\n" in valor or "\r" in valor:
            raise ValueError("Texto inválido no cadastro")

    if not nome.strip() or not matricula.isdigit():
        raise ValueError("Informe nome e matrícula numérica fictícios.")

    if perfil not in PERFIS:
        raise ValueError("Perfil deve ser estudante, professor ou administrador.")

    for horario in [inicio, fim]:
        if len(horario) != 5:
            raise ValueError("Use horário HH:MM")
        datetime.strptime(horario, "%H:%M")

    if inicio == fim:
        raise ValueError("Início e fim devem ser diferentes.")

    return True

def buscar(estado, matricula, somente_ativos=True):
    for usuario in estado["usuarios"]:
        if usuario["matricula"] == matricula:
            if not somente_ativos or usuario["ativo"] == "1": 
                return usuario
              
    return None

def cadastrar(estado, matricula, nome, perfil, inicio, fim, observacoes):
    validar(nome, matricula, perfil, inicio, fim, observacoes)
    if buscar(estado, matricula, False) is not None:
        raise ValueError("Matrícula já utilizada, inclusive em cadastro excluído.")
          
    usuario = {"matricula": matricula, "nome": nome, "perfil": perfil,
        "inicio": inicio, "fim": fim, "observacoes": observacoes, "ativo": "1"}
  
    estado["usuarios"].append(usuario)
  
    return usuario
  
def ativos(estado):
    registros = []
    for usuario in estado["usuarios"]:
        if usuario["ativo"] == "1":           
            registros.append(usuario)
                  
    return registros

def editar(estado, matricula, nome , perfil, inicio, fim, observacoes):
    validar(nome, matricula, perfil, inicio, fim, observacoes)
    usuario=buscar(estado, matricula)
    if usuario is None:
        raise ValueError("Usuário não encontrado.")
    usuario.update({"nome": nome, "perfil": perfil, "inicio": inicio,"fim": fim, "observacoes": observacoes})

    return usuario

def excluir(estado, matricula):
    usuario=buscar(estado, matricula)
    if usuario is None:
        raise ValueError("Usuário não encontrado.")
    usuario["ativo"] = "0"

def mascarar(matricula):
    if len(matricula) <=2:
        return "*" * len(matricula)
    return "*" * (len(matricula) - 2) + matricula[-2:]
        
def revelar(estado, matricula):
    usuario=buscar(estado, matricula, False)
    
    if usuario is None:
        raise ValueError("Matrícula não encontrada.")
    return usuario["matricula"]
        
def testar_mascara():
        assert mascarar("123456") == "****56"
        assert mascarar("12") == "**"
        assert mascarar("1") == "*"
        assert mascarar("") == ""
        return True

def nome_historico(estado, matricula):
    usuario = buscar(estado, matricula, False)
    if usuario is None:
        return "Usuário não encontrado"
    return usuario["nome"]
        
def identidade_publica(estado, matricula):
    usuario = buscar(estado, matricula, False)
    if usuario is None:
        raise ValueError("Usuário não encontrado.")
    situacao = "ativo"
    if usuario["ativo"] == "0":
        situacao = "excluído"
    return f'{usuario["nome"]} ({mascarar(matricula)}; {situacao})'

def testar_usuario_excluido():
    estado = {"usuarios": []}
    cadastrar(estado, "1001", "Pessoa Fictícia", "estudante", "07:00", "18:00", "")
    excluir(estado, "1001")
    assert buscar(estado, "1001") is None 
    assert buscar(estado, "1001", False)["ativo"] == "0"
    assert "excluído" in identidade_publica(estado, "1001")
    assert revelar(estado, "1001") == "1001"
    return True

def testar_edicao_historica():
    estado = {"usuarios": [], "acessos": [{"matricula": "1001", "risco": "normal"}]}
    cadastrar(estado, "1001", "Pessoa Fictícia", "estudante", "07:00", "18:00", "")
    editar(estado, "1001", "Pessoa Atualizada", "professor", "08:00", "19:00", "Texto")
    usuario = buscar(estado, "1001")
    assert usuario["matricula"] == "1001"
    assert usuario["nome"] == "Pessoa Atualizada"
    assert usuario["perfil"] == "professor"
    assert estado["acessos"] == [{"matricula": "1001", "risco": "normal"}]
    excluir(estado, "1001")
    try:
        cadastrar(estado, "1001", "Outra Pessoa", "estudante", "07:00", "18:00", "")
    except ValueError: 
        return True
    raise AssertionError("A matrícula histórica foi reutilizada.")

import usuarios

def testar_cadastros():
    estado = {"usuarios": []}
    usuarios.cadastrar(estado, "1234", "Pessoa Fictícia", "estudante", "07:00", "18:00", "")
    casos = [["1234", "Outra", "estudante", "07:00", "18:00", ""],
             ["9999", "", "estudante", "07:00", "18:00", ""],
             ["9999", " ", "inexistente", "07:00", "18:00", ""],
             ["9999", "Outra", "estudante", "07:00", "18:00", "A|B"]]
    for valores in casos:
        try:
            usuarios.cadastrar(estado, *valores)
        except ValueError:
            continue
        raise AssertionError("Cadastro inválido aceito.")
    assert len(estado["usuarios"]) == 1
    return True


def testar_identidade():
    assert usuarios.testar_mascara()
    assert usuarios.testar_usuario_excluido()
    assert usuarios.testar_edicao_historica()
    estado = {"usuarios": []}
    usuarios.cadastrar(estado, "4321", "Pessoa Fictícia", "administrador", "22:00", "06:00", "")
    publico = usuarios.identidade_publica(estado, "4321")
    assert "4321" not in publico
    assert "**21" in publico
    usuarios.excluir(estado, "4321")
    assert usuarios.ativos(estado) == []
    assert usuarios.revelar(estado, "4321") == "4321"
    assert usuarios.nome_historico(estado, "4321") == "Pessoa Fictícia"
    return True

        

    
    
    
    

  
  
