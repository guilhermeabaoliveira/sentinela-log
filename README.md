# SentinelaLog

### Monitor de acessos e análise de risco.

O SentinelaLog é um projeto acadêmico em Python voltado ao registro de acessos a um laboratório fictício, à identificação de situações suspeitas e à consulta de informações de segurança.

[Documentação](docs/README.md) · [Manual](docs/manual.md) · [Escopo](docs/escopo.md) · [Segurança](docs/seguranca.md)

## Sobre o projeto

O sistema reúne cadastros de usuários, eventos de acesso e auditoria para responder a perguntas como: quais tentativas falharam, quais máquinas aparecem associadas a mais de um usuário e quais acessos acionaram um alerta.

**Estado atual:** aplicação local com interface Tkinter, modo terminal e consulta de leitura à Groq. A IA exige internet, uma chave própria e as dependências de requirements.txt.

## Funcionalidades do escopo

| Área | Finalidade |
| --- | --- |
| Usuários | Cadastrar, consultar, editar e excluir usuários com perfil e horário permitido |
| Acessos | Registrar usuário, data, hora, máquina e resultado; consultar o histórico sem editar eventos |
| Privacidade | Exibir matrículas parcialmente e permitir revelação por operação específica |
| Risco | Classificar acessos e apresentar os motivos, incluindo aviso de origem bloqueada |
| Máquinas compartilhadas | Identificar origens utilizadas por usuários distintos |
| Auditoria | Registrar operações relevantes e permitir sua consulta |
| Relatórios | Apresentar totais, falhas, usuários e horários de destaque e contagens de risco |
| IA | Consultar os registros em linguagem natural com a Groq |

O sistema mantém persistência entre execuções e um gráfico textual da distribuição de riscos. Consulte a [descrição completa](docs/escopo.md).

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| main.py | Inicialização gráfica ou execução pelo terminal |
| interface.py e components/ | Interface Tkinter e componentes visuais |
| agente_ia.py | Consultas Groq com fatos verificados e auditoria |
| usuarios.py | Cadastro e consulta de usuários |
| acessos.py | Registro e consulta de acessos |
| risco.py | Classificação e motivos dos alertas |
| armazenamento.py | Persistência e auditoria |
| relatorios.py | Resumos e indicadores de segurança |
| dados/ | Arquivos de dados fictícios |
| testes/ | Verificação dos comportamentos da aplicação |

## Ambiente

- Python 3.11 ou superior. A interface gráfica utiliza Tkinter.
- Dados exclusivamente fictícios.
- Persistência em arquivos de texto, conforme as restrições da disciplina.

Instale a dependência da IA e inicie a interface na pasta do projeto.

```powershell
python -m pip install -r requirements.txt
python main.py
```

Para executar pelo terminal, use `python main.py --terminal`. Na interface gráfica, abra **10 Assistente IA**. O botão **Configurar chave** recebe uma chave Groq em campo protegido e a mantém apenas durante a sessão. Alternativamente, defina `GROQ_API_KEY` no ambiente.

O [manual](docs/manual.md) explica as operações. A [integração de IA](docs/integracao_ia.md) descreve os dados enviados, os limites e os testes de segurança.

## Docker

Com Docker instalado, crie a imagem e abra o modo terminal.

```sh
docker build -t sentinelalog .
docker run --rm -it --mount source=sentinelalog-dados,target=/app/dados sentinelalog
```

Para habilitar a consulta de IA, defina `GROQ_API_KEY` no ambiente local e passe `-e GROQ_API_KEY` ao comando `docker run`. A imagem contém o código e a lista fictícia de bloqueadas. O volume mantém os dados entre execuções. A interface Tkinter pode ser executada diretamente no Windows com Python e Tkinter instalados. O contêiner abre o terminal por padrão. Para usar interface gráfica em contêiner, o ambiente precisa disponibilizar um servidor gráfico.

Cada instalação utiliza sua própria chave. Forneça a chave durante a execução. A configuração do provedor pode ter limites e cobrança de uso.

## Segurança

As classificações precisam ser acompanhadas de motivos. Matrícula mascarada protege a exibição; não cifra o armazenamento. A associação de uma máquina a vários usuários não comprova autoria de uma ação.

As limitações estão em [segurança](docs/seguranca.md). Os critérios adotados estão descritos no manual.

## Contexto acadêmico

Projeto de **Fundamentos de Programação — 2026.2**, com uso exclusivo de dados fictícios. A [integração de IA](docs/integracao_ia.md) faz parte do escopo acadêmico. Informações sobre assistência no desenvolvimento estão em [transparência](docs/transparencia.md).
