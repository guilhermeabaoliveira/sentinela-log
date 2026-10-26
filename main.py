import os
import armazenamento
import usuarios
import acessos
import risco
import relatorios

PASTA = os.path.join(os.path.dirname(__file__), "dados")

def ler(rotulo):
    return input(rotulo + ": ").strip()

def mostrar_menu():
    print("\nSentinelaLog — demonstração com dados fictícios")
    print("1 Cadastrar | 2 Usuários | 3 Editar | 4 Excluir")
    print("5 Registrar acesso | 6 Acessos | 7 Auditoria")
    print("8 Revelar matrícula | 9 Segurança | 10 IA reservada")
    print("0 Sair")

def dados_usuario():
    return [ler("Nome fictício"), ler("Perfil"), ler("Início HH:MM"),
            ler("Fim HH:MM"), ler("Observações")]
