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
