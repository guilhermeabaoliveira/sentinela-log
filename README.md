# SentinelaLog

### Monitor de acessos e análise de risco.

O SentinelaLog é um projeto acadêmico em Python voltado ao registro de acessos a um laboratório fictício, à identificação de situações suspeitas e à consulta de informações de segurança.

[Documentação](docs/README.md) · [Manual](docs/manual.md) · [Escopo](docs/escopo.md) · [Segurança](docs/seguranca.md) · [Arquitetura e pastas](docs/arquitetura.md)

[Explainer técnico e manual em PDF](docs/SentinelaLog_Explainer.pdf)

## Sobre o projeto

O sistema reúne cadastros de usuários, eventos de acesso e auditoria para responder a perguntas como: quais tentativas falharam, quais máquinas aparecem associadas a mais de um usuário e quais acessos acionaram um alerta.

Aplicação local com interface Tkinter, temas escuro e claro, modo terminal e assistente de leitura dos registros. As funções locais não exigem internet. O assistente usa a Groq e requer conexão, chave própria e a dependência de `requirements.txt`.

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
| dados/ | Estado local em TXT e lista de origens bloqueadas |
| testes/ | Verificações do menu, regras de risco e integração de IA |
| docs/ | Manual, escopo, modelo de dados e limites de segurança |
| requirements.txt | Dependência da integração Groq |

## Abrir no Windows sem instalar Python

Baixe a [versão portátil para Windows 64 bits](https://github.com/guilhermeabaoliveira/sentinela-log/releases/download/v2026.11.18-final.2/SentinelaLog-Windows-com-Codigo-Fonte.zip) na página de [downloads](https://github.com/guilhermeabaoliveira/sentinela-log/releases/tag/v2026.11.18-final.2).

1. Extraia o ZIP inteiro usando **Extrair Tudo**.
2. Abra a pasta **SentinelaLog** e dê dois cliques em **SentinelaLog.exe**.
3. Mantenha `_internal` e `dados` junto do executável.

O pacote inclui Python, Tkinter e as dependências da Groq. Não exige PowerShell, comandos ou Docker. Cadastros e acessos começam vazios; os registros são gravados na pasta `dados` ao lado do executável. Use uma pasta com permissão de gravação. O executável não tem assinatura digital de editor.

O assistente continua opcional: configure sua própria chave em **10 Assistente IA → Configurar chave** e tenha conexão com a internet. Nenhuma chave acompanha o download.

O pacote de download também inclui `codigo-fonte/`, com os módulos Python e a documentação. No VS Code, use **Arquivo → Abrir Pasta** e selecione `codigo-fonte`. O [mapa de arquivos](docs/arquitetura.md) indica o módulo de cada integrante e explica as dependências do executável.

O botão **Code → Download ZIP** baixa somente o código-fonte do repositório. O download de Releases reúne código e executável; ele não substitui a estrutura do repositório. Alterar um `.py` não atualiza o `.exe`: uma nova versão do executável precisa ser gerada após alterações no programa.

## Ambiente para executar o código-fonte

- Python 3.11 ou superior. A interface gráfica utiliza Tkinter.
- Dados exclusivamente fictícios.
- Persistência em arquivos de texto, conforme as restrições da disciplina.

Baixe o projeto em **Code → Download ZIP** e extraia o arquivo, ou clone o repositório. Abra um terminal na pasta que contém `main.py`. Instale a dependência da IA e inicie a interface:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Para executar pelo terminal, use `python main.py --terminal`. Na interface gráfica, abra **10 Assistente IA**. O botão **Configurar chave** recebe uma chave Groq em campo protegido e a mantém apenas durante a sessão. Alternativamente, defina `GROQ_API_KEY` no ambiente.

A interface abre em **tema escuro**. O botão no canto superior direito alterna para **Tema claro** e, depois, **Tema escuro**. A escolha vale para a sessão. Botões e itens do menu respondem ao mouse e ao foco do teclado; a página selecionada permanece marcada.

O [manual](docs/manual.md) apresenta instalação, cadastro, demonstração local, configuração da chave e solução de problemas. A [integração de IA](docs/integracao_ia.md) descreve os dados enviados, os limites e os testes de segurança.

## Verificação

Com as dependências instaladas, execute os testes da integração sem usar uma chave real:

```sh
python -m unittest discover -s testes -p test_ia.py -v
```

Os demais arquivos em `testes/` e as funções de verificação nos módulos cobrem comportamentos do menu, persistência, usuários, acessos, risco e relatórios.

## Segurança

As classificações precisam ser acompanhadas de motivos. Matrícula mascarada protege a exibição; não cifra o armazenamento. A associação de uma máquina a vários usuários não comprova autoria de uma ação.

As limitações estão em [segurança](docs/seguranca.md). Os critérios adotados estão descritos no manual.

## Contexto acadêmico

Projeto de **Fundamentos de Programação — 2026.2**, com uso exclusivo de dados fictícios. A [integração de IA](docs/integracao_ia.md) faz parte do escopo acadêmico. Informações sobre assistência no desenvolvimento estão em [transparência](docs/transparencia.md).
