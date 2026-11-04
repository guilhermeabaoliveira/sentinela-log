def contar(acessos, campo):    
    contagens = {} 
    for acesso in acessos:        
        valor = acesso[campo]     
        contagens[valor] = contagens.get(valor, 0) + 1  
    return contagens 

def maiores(contagens):
    if not contagens:       
        return []
    maior = max(contagens.values())
    empatados = []
    for valor in contagens:
        if contagens[valor] == maior:
            empatados.append(valor)
    return empatados 

def totais(acessos):
    resultados = contar(acessos, "resultado")
    return {"acessos": len(acessos), "falhas": resultados.get("falha", 0)}

def resumir(estado): 
    resumo = totais(estado["acessos"]) 
    falhas = {} 
    horarios = {} 
    riscos = contar(estado["acessos"], "risco") 
    for acesso in estado["acessos"]: 
        hora = acesso["momento"][11:13] 
        horarios[hora] = horarios.get(hora, 0) + 1 
        if acesso["resultado"] == "falha": 
            matricula = acesso["matricula"] 
            falhas[matricula] = falhas.get(matricula, 0) + 1 
        resumo["mais_falhas"] = maiores(falhas) 
        resumo["pico"] = maiores(horarios) 
        resumo["suspeitos"] = riscos.get("suspeito", 0) 
        resumo["criticos"] = riscos.get("critico", 0) 
        resumo["falhas_por_usuario"] = falhas 
        resumo["por_hora"] = horarios 
        return resumo

def linhas_relatorio(estado):
    import usuarios
    resumo = resumir(estado)
    identidades = []
    for matricula in resumo["mais_falhas"]:
        usuario = usuarios.buscar(estado, matricula, False)
        if usuario is None:
            raise ValueError("Usuário do histórico não encontrado.")
        situacao = "ativo"
        if usuario["ativo"] == "0":
            situacao = "excluído"
        mascara = usuarios.mascarar(matricula)
        identidades.append(f'{usuario["nome"]} ({mascara}; {situacao})')
        return [f'Total de acessos: {resumo["acessos"]}',
            f'Total de falhas: {resumo["falhas"]}',
            'Usuários com mais falhas: ' + (", ".join(identidades) or "nenhum"),
            'Horas com mais movimento: ' + (", ".join(resumo["pico"]) or "nenhuma"),
            f'Suspeitos: {resumo["suspeitos"]}',
            f'Críticos: {resumo["criticos"]}']

def apresentar(estado):
    for linha in linhas_relatorio(estado):
        print(linha)
    return resumir(estado)