# SentinelaLog — Documentação técnica (lógica da programação)

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

## 1. Objetivo e visão geral

O SentinelaLog é dividido em módulos pequenos, cada um com uma responsabilidade: o `main.py` coordena, os módulos aplicam as regras, o `armazenamento.py` grava, e só o assistente de IA acessa a internet. Esta documentação explica como as partes se ligam e por que cada decisão foi tomada; não repete o código linha a linha.

O núcleo usa apenas as bibliotecas `os` e `datetime` (mais `sys` no `main.py`, para reconhecer o executável e a opção `--terminal`). A janela gráfica (Tkinter) e a IA (`groq`) são camadas adicionais sobre o mesmo núcleo.

Caminho de uma operação: o ponto de entrada abre a janela ou o terminal; ambos chamam os módulos de usuários e acessos; o risco é calculado no registro do acesso; o armazenamento valida e grava `dados/estado.txt`. A consulta de IA segue um ramo separado: confirmação do envio, consulta à Groq com chave própria, validação local e registro em `dados/consultas_ia.txt`.

O desenho da arquitetura (o que cada módulo faz e como os dados circulam) está em [arquitetura.md](arquitetura.md).

## 2. Componentes

Cada arquivo tem um responsável e um conjunto pequeno de funções.

| Arquivo | Responsável | O que faz | Funções principais |
|---|---|---|---|
| `main.py` | Guilherme | Entrada do programa, menu e ligação das operações | `ler`, `tratar_usuario`, `tratar_acesso`, `executar`, `abertura` |
| `usuarios.py` | Cauã | Valida e guarda usuários; mascara a matrícula | `validar`, `cadastrar`, `buscar`, `editar`, `excluir`, `mascarar`, `revelar` |
| `acessos.py` | Kayo | Registra e consulta acessos; acha máquinas compartilhadas | `validar_entrada`, `registrar`, `consultar`, `compartilhadas` |
| `risco.py` | Samuel | Valida horários e classifica o risco com motivos | `momento_valido`, `fora_horario`, `ler_bloqueadas`, `classificar` |
| `armazenamento.py` | Gabriel | Valida, lê e grava os arquivos, com auditoria | `carregar`, `validar_estado`, `salvar` |
| `relatorios.py` | Pedro | Calcula totais, empates e o gráfico textual | `contar`, `maiores`, `resumir`, `grafico` |
| `interface.py`, `components/` | Pedro | Janela gráfica que chama as mesmas funções | Telas, tabelas, formulários e a barra lateral |
| `agente_ia.py`, `components/chat_ia.py` | Guilherme | Assistente de IA e sua tela | `proteger_pergunta`, `preparar`, `consultar`, `registrar_consulta` |

A interface não repete regras: ela chama os módulos do núcleo e mostra o resultado. Por isso terminal e janela se comportam do mesmo jeito.

## 3. Ciclo de uma operação no menu

Todas as opções, menos a IA, seguem o mesmo ciclo dentro de `executar()`, e o resultado só aparece depois de gravado.

1. `executar` mostra o menu e lê a opção com `ler`.
2. `armazenamento.carregar` lê e valida `estado.txt`. Se o arquivo for inválido, a operação para e nada é substituído.
3. `tratar_usuario` ou `tratar_acesso` chama o módulo certo e devolve o nome da operação e quem foi afetado.
4. `armazenamento.salvar` valida de novo, acrescenta a entrada de auditoria e grava.
5. Só então o programa mostra a classificação (em acessos), a matrícula (na revelação) e “Operação gravada com auditoria”.
6. Um erro (`OSError`, `ValueError` ou `UnicodeError`) vira a mensagem “Operação não concluída”, e nada é salvo.

| Opção | Módulo chamado | Operação na auditoria |
|---|---|---|
| 1 Cadastrar | `usuarios.cadastrar` | CADASTRO |
| 2 Usuários | `usuarios.ativos`, `mascarar` | CONSULTA_USUARIOS |
| 3 Editar | `usuarios.editar` | EDICAO |
| 4 Excluir | `usuarios.excluir` | EXCLUSAO |
| 5 Registrar acesso | `risco.classificar`, `acessos.registrar` | REGISTRO_ACESSO |
| 6 Acessos | `acessos.linhas_consulta` | CONSULTA_ACESSOS |
| 7 Auditoria | `armazenamento`, `agente_ia.listar_consultas` | CONSULTA_AUDITORIA |
| 8 Revelar matrícula | `usuarios.revelar` | REVELACAO_MATRICULA |
| 9 Segurança | `relatorios`, `acessos.compartilhadas` | RELATORIO_SEGURANCA |
| 10 Assistente IA | `agente_ia` | Registro próprio em `consultas_ia.txt` |

A opção 10 sai do ciclo (`continue`) sem salvar nada em `estado.txt`: o assistente só lê.

## 4. Regras de negócio

### Cadastro (`usuarios.py`)

`validar` recusa textos com o separador `|` ou quebra de linha, exige matrícula numérica, perfil entre estudante, professor e administrador, horários no formato HH:MM e início diferente do fim. Uma matrícula nunca é reutilizada, nem a de um cadastro excluído, para não misturar históricos. A exclusão é lógica: o campo `ativo` vira `0` e o histórico continua apontando para a pessoa.

`mascarar` mostra só os dois últimos dígitos (`123456` vira `****56`). Mascarar não é criptografia; `revelar` é a operação específica que mostra a matrícula inteira, e ela entra na auditoria.

### Acessos (`acessos.py`)

`validar_entrada` confere a data e a hora (AAAA-MM-DD HH:MM), exige máquina preenchida e resultado `sucesso` ou `falha`. `registrar` só aceita usuário ativo, chama `risco.classificar` no mesmo instante, gera um identificador sequencial e guarda o nível e os motivos no evento. Um acesso não é editado depois, e `consultar` devolve cópias, para a consulta não alterar o registro. Uma máquina é compartilhada quando aparece com mais de uma matrícula; isso não prova quem agiu.

### Classificação de risco (`risco.py`)

| Situação do acesso | Nível |
|---|---|
| Nenhum sinal | normal |
| Falha, ou fora do horário permitido | suspeito |
| Falha e fora do horário | crítico |
| Origem na lista de bloqueadas | crítico, com aviso, e o acesso é gravado mesmo assim |

Os limites de início e fim são inclusivos. Quando o início é maior que o fim (por exemplo 22:00 a 06:00), a janela atravessa a meia-noite. Cada classificação guarda os motivos, e alterar o cadastro depois não muda o que já foi classificado.

### Relatórios (`relatorios.py`)

`resumir` calcula o total de acessos e falhas, os usuários com mais falhas, as horas de pico e as quantidades de suspeitos e críticos; `maiores` preserva empates. O gráfico textual desenha uma barra por nível de risco, em que a maior categoria ocupa 20 marcas e qualquer categoria não vazia mostra ao menos uma. Sem acessos, o relatório mostra zeros.

## 5. Persistência e auditoria

Usuários, acessos e auditoria ficam juntos em `dados/estado.txt`, uma linha por registro, com campos separados por `|`. A primeira letra diz o tipo da linha.

| Tipo | Registro | Campos, nesta ordem |
|---|---|---|
| U | Usuário | matrícula, nome, perfil, início, fim, observações, ativo |
| A | Acesso | id, matrícula, momento, máquina, resultado, risco, motivos |
| L | Auditoria | id, momento, operação, afetado |

As origens bloqueadas ficam em `dados/bloqueadas.txt`, uma por linha, e são lidas a cada registro de acesso.

**Gravação segura.** `salvar` carrega o arquivo atual (se ele estiver corrompido, para ali), copia o estado, acrescenta a entrada de auditoria com o próximo id e a hora, valida tudo de novo e escreve em um arquivo temporário (`estado.txt.tmp`). Só no fim o `os.replace` troca o temporário pelo arquivo final. Assim, uma falha no meio não deixa o arquivo pela metade, e a mensagem de sucesso só aparece depois.

**Validação.** `validar_estado` confere os campos de cada usuário, matrículas sem repetição, identificadores únicos, que cada acesso aponte para uma matrícula existente, que o risco seja normal, suspeito ou crítico, e que nenhum campo contenha o separador. Um arquivo inválido gera “nada foi substituído”: o teste de corrupção confere que o conteúdo original continua lá.

## 6. Assistente de IA

O assistente é uma consulta de leitura: o Python calcula os fatos, a Groq só escolhe quais fatos respondem à pergunta, e o programa valida a escolha antes de mostrar. Ele está em `agente_ia.py` e na tela `components/chat_ia.py`, com o modelo `openai/gpt-oss-120b`.

### Passo a passo de uma pergunta

1. `proteger_pergunta` limita a pergunta a 600 caracteres, recusa chaves de API digitadas nela e troca nomes e matrículas cadastrados por apelidos como “Usuário U1”.
2. `preparar` monta até 160 fatos numerados (F1, F2, ...) a partir de `relatorios` e `acessos`. Máquinas viram “Máquina M1”.
3. O programa mostra o que será enviado e pede confirmação.
4. `consultar` grava `INICIADA` em `consultas_ia.txt` antes da chamada.
5. `_consultar` lê a chave (do botão Configurar chave ou da variável `GROQ_API_KEY`), exige ao menos um acesso registrado e chama a Groq.
6. A resposta vem em JSON com a lista de identificadores escolhidos e um aviso “insuficiente”. O programa valida e mostra só os textos dos fatos escolhidos.
7. O desfecho é gravado como `CONCLUIDA` ou `ERRO`.

### O que sai e o que não sai do computador

| Sai | Não sai |
|---|---|
| A pergunta tratada e até três anteriores | Nomes e matrículas reais (viram apelidos) |
| Até 160 fatos calculados, com totais de todos os eventos e detalhes de até 20 eventos e 15 dias | Observações livres do cadastro |
| Motivos de risco, só entre os quatro previstos nas regras | O arquivo de auditoria e o conteúdo de `estado.txt` |
| A chave, só para autenticar a conexão | A chave nunca entra no código, no repositório nem no registro |

### Controles e critérios de parada

| Controle | Como funciona |
|---|---|
| Escopo de leitura | O modelo não recebe ferramentas e não altera registros nem classificações |
| Uma chamada por pergunta | `max_retries=0`: sem repetição automática |
| Tempo limite | `timeout=20.0` segundos de rede |
| Tamanho | Pergunta de até 600 caracteres e resposta de até 1.024 tokens |
| Validação da saída | Resposta truncada, estrutura inválida, mais de 8 fatos ou identificador desconhecido são recusados |
| Dados como dados | O texto do sistema trata perguntas e fatos como dados, não como instruções |
| Confirmação | Nada é enviado sem o operador autorizar |

### Registro de consultas

Cada consulta gera linhas em `dados/consultas_ia.txt`, com cinco campos separados por tabulação: operação, pergunta tratada, data e hora, resultado (`INICIADA`, `CONCLUIDA` ou `ERRO`) e modelo. A opção 7 Auditoria mostra essas linhas.

Sem chave, sem internet, com limite do serviço atingido ou sem acessos registrados, o programa mostra uma mensagem clara e o menu continua funcionando. Os testes de `testes/test_ia.py` simulam a Groq e cobrem a minimização dos dados, a auditoria, a falha de rede, a chave ausente, o histórico vazio e a rejeição de resposta truncada.

## 7. Execução e distribuição

O `main.py` decide como o programa abre: com `--terminal`, mostra as regras e executa o menu de texto; sem o argumento, abre a janela de `interface.py`. Os dados ficam na pasta `dados` ao lado do `main.py` ou, no executável, ao lado do `.exe`. Na janela, a consulta de IA roda em segundo plano (fila e thread em `chat_ia.py`), para a tela não travar enquanto espera a resposta.

O executável é gerado com PyInstaller. Ele leva dentro o Python, o Tkinter e a biblioteca `groq`: por isso a pasta `_internal` é grande, e esses arquivos não são código novo do grupo. Como os `.py` ficam compilados, o pacote traz também a pasta `codigo-fonte`, com todos os arquivos legíveis para estudo e execução.

| Caminho de distribuição | O que cada pessoa precisa fazer | Situação |
|---|---|---|
| Executável mais código-fonte | Extrair o ZIP e abrir `SentinelaLog.exe` | Escolhido; nada para instalar |
| Só o código-fonte | Instalar Python e rodar `python -m pip install -r requirements.txt` | Disponível como alternativa |
| Docker | Instalar o Docker e construir a imagem | Retirado: não era necessário |
| Versão web com servidor | Hospedar uma API que guarda a chave, com login e limite de chamadas | Avaliada e descartada: vai além do pedido |

O executável é para Windows 64 bits, não tem assinatura digital e deve rodar com uma única instância por pasta de dados.
