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