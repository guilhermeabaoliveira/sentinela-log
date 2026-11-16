import main
import armazenamento
import usuarios
import os

def testar_revelacao(pasta):
    estado = armazenamento.vazio()
    usuarios.cadastrar(estado, "1234", "Pessoa Fictícia", "estudante", "07:00", "18:00", "")
    armazenamento.salvar(pasta, estado, "CADASTRO", "1234")
    entradas = ["8", "1234", "0"]
    posicao = [0]
    def entrada_simulada(rotulo):
        valor = entradas[posicao[0]]
        posicao[0] += 1
        return valor
    original = main.ler
    main.ler = entrada_simulada
    try:
        main.executar(pasta)
    finally:
        main.ler = original
    logs = armazenamento.carregar(pasta)["auditoria"]
    assert logs[-1]["operacao"] == "REVELACAO_MATRICULA"
    return True


def testar_menu_corrompido(pasta):
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, "estado.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("INVALIDO\n")
    entradas = ["2", "0"]
    posicao = [0]
    def entrada_simulada(rotulo):
        valor = entradas[posicao[0]]
        posicao[0] += 1
        return valor
    original = main.ler
    main.ler = entrada_simulada
    try:
        main.executar(pasta)
    finally:
        main.ler = original
    with open(caminho, encoding="utf-8") as arquivo:
        assert arquivo.read() == "INVALIDO\n"
    return True
