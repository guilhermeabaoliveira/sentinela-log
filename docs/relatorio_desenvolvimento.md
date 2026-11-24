# SentinelaLog — Relatório de desenvolvimento

**Fundamentos de Programação · 1º período de Ciência da Computação · CESAR School**

**Professores:** Ana Carolina Cândido de Melo e Victor Felipe Lourenço da Costa

**Grupo 07:**

- Guilherme Alcântara Batista Alencar de Oliveira
- Cauã Victor Pereira Santos
- Kayo Vinícius Messias Nascimento
- Samuel Bernardi Sá
- Gabriel Gomes Mendes
- Pedro Henrique de Freitas Veloso

Novembro de 2026

## 1. Visão Geral do Sistema

### 1.1. Conceito principal

O SentinelaLog é um monitor local de acessos, escrito em Python pelo Grupo 07 (Guilherme, Cauã, Kayo, Samuel, Gabriel e Pedro). Ele cadastra usuários fictícios, registra acessos, classifica cada acesso como normal, suspeito ou crítico explicando o motivo, guarda uma auditoria das operações e gera relatórios com um gráfico textual. Um assistente de IA opcional responde perguntas sobre o histórico. Tudo roda no computador; só a consulta à IA usa a internet.

### 1.2. Metas do Projeto

Uso: mostrar de forma clara o que aconteceu em cada acesso e por que ele recebeu aquela classificação, sem esconder as regras.

Aprendizado: organizar um programa em funções e módulos, tratar erros, guardar dados em arquivo, trabalhar em grupo com Git e integrar uma IA com cuidado com privacidade e segurança.

### 1.3. Público-Alvo

Pensamos em quem opera um monitor de acessos de laboratório (um cenário fictício) e em quem avalia o trabalho. Por isso o programa abre pelo terminal ou por uma janela gráfica, tem manual, e traz o código-fonte junto, para ser lido e explicado. Todos os dados são fictícios.

## 2. Ideação e Referências

### 2.1. Processo de ideação

O ponto de partida foi a especificação do projeto de Fundamentos de Programação (Turma B, 2026.2): um monitor de acessos pelo terminal, com cadastro, histórico, classificação de risco, auditoria, persistência em arquivo e relatório. As regras de risco não vinham prontas: o grupo as escolheu e as justificou no manual.

Três decisões de escopo moldaram o resultado:

- **Sistema local.** Chegamos a considerar hospedar uma API em um servidor (por exemplo na Cloudflare) para guardar a chave da IA. Descartamos: exigiria login, limite de chamadas e uma interface web, muito além do pedido. Cada pessoa usa a própria chave.
- **Executável como extra.** Para quem for testar não precisar instalar Python, empacotamos um `.exe`, com o código-fonte junto. Cogitamos um Dockerfile e o retiramos por não ser necessário.
- **IA só de leitura.** O assistente escolhe fatos que o Python já calculou, e não recebe nenhum poder de alterar dados.

### 2.2. Referências

Especificação do projeto SentinelaLog (Fundamentos de Programação, Turma B, 2026.2); aula “IA e Cibersegurança no seu projeto” e o artigo de apoio sobre segurança (Bifröst), fornecidos pela professora; documentação da Groq, usada na integração de IA.

## 3. Ferramentas e Recursos Utilizados

### 3.1. Linguagem e bibliotecas

- **Python.** O núcleo (`usuarios.py`, `acessos.py`, `risco.py`, `armazenamento.py` e `relatorios.py`) usa só `os` e `datetime`. O `main.py` acrescenta `sys`, para reconhecer o executável e a opção `--terminal`.
- **Tkinter.** Desenha a janela gráfica, que é um complemento: o modo terminal continua disponível e cumpre o enunciado.
- **groq (versão 1.7.0).** Usada somente no módulo de IA, com o modelo `openai/gpt-oss-120b`.
- **PyInstaller.** Empacota o programa em um `.exe` para Windows 64 bits.

### 3.2. Outros recursos

Git e GitHub guardam o código e o histórico de cada integrante. Os dados ficam em arquivos de texto simples: `estado.txt` (usuários, acessos e auditoria), `bloqueadas.txt` (origens bloqueadas) e `consultas_ia.txt` (registro das consultas de IA). O VS Code serve para abrir e explicar o código.

### 3.3. Créditos e licenciamento

Python, Tkinter e a biblioteca groq acompanham o executável, e os textos das licenças das dependências distribuídas estão na pasta `licencas` do pacote. O projeto usa somente dados fictícios.

### 3.4. Uso de IA generativa

O grupo usou IA generativa (ChatGPT/Codex) como apoio no desenvolvimento, nos testes e na documentação. A divisão do trabalho, a revisão do código e a validação ficaram com o grupo, e cada integrante consegue explicar o que entregou. Esse apoio é diferente do assistente de IA que existe dentro do programa.

## 4. Planejamento e Desenvolvimento

### 4.1. Funcionalidades e resultado

| Funcionalidade | Prioridade | Resultado |
|---|---|---|
| Cadastrar, listar, editar e excluir (de forma lógica) usuários | Essencial | Implementada |
| Matrícula mascarada e revelação com auditoria | Essencial | Implementada |
| Registrar e consultar acessos, sem edição posterior | Essencial | Implementada |
| Classificar o risco com motivos e avisar sobre origem bloqueada | Essencial | Implementada |
| Identificar máquinas compartilhadas | Essencial | Implementada |
| Auditoria e persistência em arquivo de texto | Essencial | Implementada |
| Relatório de segurança | Essencial | Implementada |
| Gráfico textual da distribuição de riscos | Extra pedido | Implementada |
| Assistente de IA (Groq) | Integração da aula | Implementada; testes com a Groq simulada |
| Janela gráfica (Tkinter) | Complemento | Implementada |
| Executável Windows com código-fonte | Complemento | Implementada |

### 4.2. Fluxo de uma operação

1. O operador escolhe uma opção no menu, pelo terminal ou pela janela.
2. O `main.py` chama o módulo responsável (usuários, acessos, relatórios).
3. Em um acesso, o `risco.py` classifica e devolve os motivos.
4. O `armazenamento.py` valida os dados e grava `estado.txt`, com a auditoria.
5. Só depois de gravar, o programa mostra a classificação e “Operação gravada com auditoria”.

O assistente de IA é um ramo à parte: não grava nada e só ele acessa a internet. O desenho completo está na [documentação técnica](documentacao_tecnica.md).

### 4.3. Divisão de responsabilidades

| Integrante | Arquivos | Responsabilidade |
|---|---|---|
| Guilherme Alcântara Batista Alencar de Oliveira | `main.py`, `agente_ia.py`, `components/chat_ia.py` | Menu, integração das operações, assistente de IA e pacote executável |
| Cauã Victor Pereira Santos | `usuarios.py` | Validação, cadastro, edição, exclusão lógica e mascaramento |
| Kayo Vinícius Messias Nascimento | `acessos.py` | Registro e consulta de acessos, máquinas compartilhadas |
| Samuel Bernardi Sá | `risco.py` | Horários, origens bloqueadas e classificação com motivos |
| Gabriel Gomes Mendes | `armazenamento.py` | Validação, persistência em TXT e auditoria |
| Pedro Henrique de Freitas Veloso | `relatorios.py`, `interface.py`, `components/` | Totais, empates, gráfico textual e a janela gráfica |

### 4.4. Marcos do projeto

| Marco | Período | Situação |
|---|---|---|
| Entrega parcial: cadastro, acessos e risco funcionando | Até 05/11 | Cumprido |
| Persistência, auditoria e relatórios | 02 a 15/11 | Concluído |
| Integração da IA e da janela gráfica | 09 a 18/11 | Concluído |
| Pacote final, documentação e entrega no Classroom | Semana de 16/11 | Entregue |

### 4.5. Desafios e Soluções

- **Gravação que falhava na integração.** Na auditoria da entrega, o programa caiu ao salvar porque a função `salvar()` estava indentada dentro de outra. A correção veio no `armazenamento.py`, e um teste confere que a revelação de matrícula deixa auditoria gravada.
- **Relatório com histórico vazio.** O relatório falhava sem nenhum acesso. Hoje ele devolve zeros e um teste cobre esse caso.
- **Arquivo de dados inválido.** O programa não substitui um arquivo corrompido: informa o erro e preserva o conteúdo, como o teste mostra.
- **Privacidade na IA.** Nomes e matrículas viram apelidos antes do envio, observações livres não saem, e o programa pede confirmação.
- **Muitas pastas no executável.** A pasta `_internal` é o Python e as bibliotecas empacotados. Como os `.py` ficam compilados, o pacote inclui a pasta `codigo-fonte` para leitura.

## 5. Produto Final

### 5.1. Como executar

Existem dois caminhos. No pacote Windows, basta extrair o ZIP inteiro e abrir `SentinelaLog.exe`, sem instalar nada; as outras pastas precisam ficar ao lado dele. Pelo código-fonte, instala-se Python e a dependência com `python -m pip install -r requirements.txt`, e executa-se `python main.py` (janela) ou `python main.py --terminal` (terminal).

O programa funciona sem chave e sem internet. Só o assistente de IA precisa dos dois, e cada pessoa cria a sua chave na Groq, configurada pelo botão Configurar chave.

### 5.2. O que foi entregue

No Google Classroom: o ZIP completo (código-fonte, executável, manual e explainer em PDF), o link do repositório no GitHub e os nomes do Grupo 07. O mesmo pacote está em Releases no GitHub.

### 5.3. Onde está o código

Os seis módulos ficam na raiz do repositório, junto de `interface.py`, `agente_ia.py` e das pastas `components/`, `dados/`, `docs/` e `testes/`. A pasta `docs/` reúne o manual, o escopo, a arquitetura, o modelo de dados, a segurança, a integração de IA e a transparência acadêmica. Os testes automáticos ficam em `testes/`.

## 6. Reflexão

### 6.1. Vantagens e limitações

Python puro e arquivos de texto deixam o código fácil de ler e de explicar, e dispensam banco de dados. Em troca, o sistema tem limites que estão escritos na documentação de segurança: a matrícula mascarada não é criptografia, não há autenticação de operadores, os arquivos de texto não são cifrados, a auditoria pode ser alterada por quem tiver acesso aos arquivos, e deve haver uma só instância por pasta de dados. O executável é para Windows 64 bits e não tem assinatura digital.

### 6.2. Retomada das metas

A meta de uso foi cumprida: cada acesso mostra sua classificação e os motivos, e o relatório e o gráfico resumem o histórico. A meta de aprendizado apareceu no trabalho em módulos, nos testes, nos commits de cada integrante e na integração de uma IA que só lê fatos calculados pelo programa.

### 6.3. Aprendizados

- Definir o escopo antes de ampliar: avaliamos um servidor na nuvem e um Dockerfile e ficamos com o que o trabalho pede.
- Em um sistema com IA, o limite fica fora do modelo: o Python calcula, valida e decide o que aparece; a IA só escolhe entre fatos prontos.
- Dizer o que o sistema não detecta faz parte da segurança, e por isso o manual lista esses limites.
- Revisar a integração inteira, e não só o módulo de cada um: foi assim que apareceu o erro de gravação descrito em 4.5.

### 6.4. Conclusão

O SentinelaLog entrega o que a especificação pede, com um extra pedido (o gráfico de riscos), a integração de IA da aula e dois complementos (janela gráfica e executável) que não substituem o terminal nem o código-fonte. Cada parte foi feita por um integrante, e o grupo consegue explicar o sistema de ponta a ponta.
