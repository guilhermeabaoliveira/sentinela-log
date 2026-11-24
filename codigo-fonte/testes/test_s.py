import risco

def testar_riscos():
    assert risco.testar_janela_noturna()
    assert risco.testar_motivos_combinados()
    assert risco.testar_limites_diurnos()
    assert risco.testar_datas_invalidas()
    assert risco.testar_origem_bloqueada()
    assert len(risco.exemplos_fronteira()) == 4
    usuario = {"inicio": "07:00", "fim": "18:00"}
    for resultado, hora, esperado in [("sucesso", "10:00", "normal"),
                                     ("falha", "10:00", "suspeito"),
                                     ("sucesso", "03:00", "suspeito"),
                                     ("falha", "03:00", "critico")]:
        nivel, motivo = risco.classificar(usuario, "2026-10-26 " + hora, "A", resultado, [])
        assert nivel == esperado
        assert motivo
    return True

def testar_arquivo_bloqueadas(caminho):
    try:
        risco.ler_bloqueadas(caminho)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("O teste exige caminho novo.")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("MAQ-X\n\nMAQ-X\nMAQ-Y\n")
    assert risco.conferir_lista(caminho) == ["MAQ-X", "MAQ-Y"]
    usuario = {"inicio": "07:00", "fim": "18:00"}
    nivel, motivo = risco.classificar(usuario, "2026-10-26 10:00", "MAQ-Y", "sucesso", risco.conferir_lista(caminho))
    assert nivel == "critico"
    assert "bloqueada" in motivo
    return True
