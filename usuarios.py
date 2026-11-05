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
        

    
    
    

  
  
