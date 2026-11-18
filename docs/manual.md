# Manual do usuário

O SentinelaLog registra acessos fictícios de um laboratório, aplica regras de risco e permite consultar o histórico. O aplicativo funciona no computador; somente o assistente de IA utiliza um serviço externo.

## 1. Instalação e execução

### Windows: abrir sem instalar Python

1. Baixe **SentinelaLog-Windows-com-Codigo-Fonte.zip** em [Releases](https://github.com/guilhermeabaoliveira/sentinela-log/releases/tag/v2026.11.18-final). Esse arquivo é diferente de **Code → Download ZIP**, que contém o código-fonte.
2. Clique com o botão direito no ZIP e selecione **Extrair Tudo**.
3. Abra a pasta extraída **SentinelaLog** e dê dois cliques em **SentinelaLog.exe**.
4. Mantenha a pasta `_internal` junto do executável. Ela contém o ambiente Python e as dependências.

Não é necessário instalar Python nem executar comandos. A pasta `dados`, ao lado do executável, guarda os registros; o pacote começa sem cadastros ou acessos. Extraia para uma pasta do seu usuário com permissão de gravação. O executável não possui assinatura digital de editor.

Para usar o assistente, consulte a seção 7: sua chave Groq e a conexão com a internet continuam necessárias. Para migrar registros de outra cópia, feche ambas as instâncias e copie seus arquivos de dados para a pasta `dados` da versão portátil, preservando antes uma cópia de segurança.

### Executar pelo código-fonte

1. Tenha Python 3.11 ou superior instalado. Para a janela gráfica, o ambiente Python precisa incluir Tkinter.
2. Baixe o ZIP do repositório e extraia o conteúdo, ou use uma cópia clonada.
3. Abra um terminal na pasta que contém `main.py`.
4. Execute:

```sh
python -m pip install -r requirements.txt
python main.py
```

No Windows, se o comando disponível for `py`, use-o no lugar de `python`. O programa pode ser iniciado pelo terminal sem abrir a interface gráfica:

```sh
python main.py --terminal
```

A dependência `groq` habilita o assistente. Cadastros, acessos, relatórios e auditoria local funcionam sem chave e sem internet. O arquivo `.env.example` informa o nome da variável da chave; ele não configura a aplicação automaticamente.

## 2. Navegação e aparência

O painel inicial apresenta totais e atalhos. O menu lateral mantém as mesmas operações numeradas do terminal. A página selecionada fica marcada; botões e itens do menu recebem realce ao passar o mouse ou obter foco pelo teclado.

A interface inicia em tema escuro. O botão **Tema claro**, no canto superior direito, alterna a aparência. Depois da troca, **Tema escuro** permite retornar. A escolha vale durante a sessão e não apaga campos ou a conversa. Use **0 Sair** para encerrar, confirmando a saída.

## 3. Usuários

Em **1 Cadastrar**, informe:

| Campo | Formato e significado |
| --- | --- |
| Matrícula fictícia | Identificador numérico estável do cadastro, digitado pelo operador |
| Nome fictício | Nome de exemplo, sem informações reais |
| Perfil | estudante, professor ou administrador |
| Horários inicial e final | `HH:MM`, por exemplo `07:00` e `18:00`; precisam ser diferentes |
| Observações | Texto complementar opcional |

A matrícula não é um número sorteado a cada login. Não se pode reutilizar a matrícula de um cadastro excluído. Os campos não aceitam o separador `|` nem quebras de linha.

**2 Usuários** lista os cadastros ativos com matrícula parcialmente mascarada. **3 Editar** altera os dados do cadastro. **4 Excluir** desativa o usuário, preservando o histórico. Nessas operações, informe a matrícula quando solicitada.

**8 Revelar matrícula** é a operação específica para exibir o identificador completo e registrar essa revelação na auditoria. O perfil cadastrado descreve o usuário fictício; não representa um login ou um controle de permissões da aplicação.

## 4. Registrar e consultar acessos

Em **5 Registrar acesso**, selecione o usuário ativo na interface gráfica; no terminal, informe a matrícula fictícia. Depois, informe:

- Data e hora no formato `AAAA-MM-DD HH:MM`.
- Nome da máquina fictícia.
- Resultado `sucesso` ou `falha`.

A seleção exibe o nome e a matrícula mascarada; o sistema mantém a associação com o cadastro correto. Após a gravação, a mensagem informa a classificação e os motivos. **6 Acessos** mostra o histórico. Os eventos não podem ser editados pelo menu.

## 5. Classificação de risco

| Condição | Classificação | Justificativa |
| --- | --- | --- |
| Sucesso dentro do horário, em origem não bloqueada | Normal | Nenhum sinal das regras adotadas foi encontrado |
| Falha ou horário fora da faixa permitida | Suspeito | Há falha de acesso ou uso em horário inesperado |
| Falha combinada com horário fora da faixa | Crítico | Dois sinais de risco ocorrem no mesmo evento |
| Origem presente em `dados/bloqueadas.txt` | Crítico, com aviso | A origem consta na lista de bloqueios |

Os limites inicial e final do horário são inclusivos; faixas que atravessam a meia-noite são aceitas. Uma origem bloqueada gera aviso e classificação crítica: o evento continua sendo registrado. O sistema não bloqueia fisicamente uma máquina nem impede acessos no sistema operacional.

## 6. Auditoria e relatório

**7 Auditoria** apresenta operações, usuário afetado e data/hora. Na interface gráfica, **Consultas de IA** abre o registro das perguntas ao assistente. No terminal, a mesma opção 7 inclui os dois históricos.

**9 Segurança** reúne totais de acessos e falhas, usuários com mais falhas, horários de maior movimento, quantidades por risco, gráfico textual e máquinas associadas a usuários distintos. Compartilhamento indica associação nos registros, não comprova quem estava fisicamente utilizando uma máquina.

## 7. Assistente de IA

1. Crie uma chave em sua própria conta na Groq. Não publique essa chave no GitHub nem a inclua no ZIP do projeto.
2. Abra **10 Assistente IA → Configurar chave** e cole a chave no campo protegido. Ela permanece na memória da sessão e precisa ser informada novamente após fechar o programa.
3. Tenha pelo menos um acesso registrado e digite, por exemplo, **Quantos acessos e quantas falhas foram registrados?**
4. Revise a pergunta tratada e confirme o envio externo. Nomes e matrículas cadastrados são substituídos por identificadores como U1; os fatos não incluem observações livres nem auditoria.
5. Aguarde a conclusão. A IA consulta fatos; não altera cadastros, acessos ou classificações.

**Limpar conversa** remove o histórico visível e o contexto da sessão, preservando a auditoria. No terminal, configure `GROQ_API_KEY` no ambiente antes de iniciar; o botão de configuração existe apenas na interface gráfica. Consulte [integração de IA](integracao_ia.md) para os limites e os dados enviados.

## 8. Exemplo de demonstração local

O exemplo abaixo acrescenta registros fictícios. Use uma matrícula ainda não cadastrada.

1. Cadastre `Pessoa Exemplo`, matrícula `900100`, perfil `estudante`, horário de `07:00` a `18:00`.
2. Registre um acesso às `2026-11-18 10:00`, na máquina `MAQ-A`, com `sucesso`: resultado esperado **normal**.
3. Registre outro às `2026-11-18 10:05`, na mesma máquina, com `falha`: resultado esperado **suspeito**.
4. Registre um acesso às `2026-11-18 10:10`, na máquina `MAQ-X`, com `sucesso`: resultado esperado **crítico**, desde que `MAQ-X` permaneça no arquivo de bloqueadas fornecido.
5. Consulte **6 Acessos**, **7 Auditoria** e **9 Segurança**. Os totais incluem também qualquer registro anterior existente.
6. Se a chave estiver configurada e houver internet, faça uma pergunta ao assistente sobre esses registros.
7. Feche e reabra o programa para conferir a persistência. A chave da interface precisará ser informada novamente.

## 9. Arquivos e cuidados de uso

| Arquivo | Conteúdo |
| --- | --- |
| `dados/estado.txt` | Usuários, acessos e auditoria das operações |
| `dados/bloqueadas.txt` | Uma origem bloqueada por linha |
| `dados/consultas_ia.txt` | Operação, pergunta tratada, data/hora, resultado e modelo, separados por tabulação |

O arquivo de consultas é criado no primeiro uso do assistente. Para preservar a base, faça uma cópia dos arquivos de dados com o programa fechado. Evite editar o estado manualmente e execute uma única instância por pasta de dados. Ambientes virtuais, chaves e registros locais de consultas não fazem parte da entrega do código.

Mascaramento protege a exibição, não cifra o arquivo. O histórico é protegido contra edição pelo menu, mas alguém com acesso ao disco pode alterá-lo externamente. Use somente dados fictícios. Consulte [segurança e limitações](seguranca.md).

## 10. Solução de problemas

| Situação | Orientação |
| --- | --- |
| Python não encontrado | Confira a instalação e tente o comando `py` no Windows |
| Erro ao importar Tkinter | Use uma instalação Python com Tkinter ou execute pelo terminal |
| Dependência Groq ausente | Execute `python -m pip install -r requirements.txt` |
| Chave ausente ou recusada | Configure uma chave válida; verifique a validade na sua conta Groq |
| Histórico vazio | Registre um acesso antes de consultar o assistente |
| Falha de conexão ou limite do provedor | Confira a conexão e aguarde antes de tentar novamente |
| Arquivo inválido ou falha de gravação | Preserve os arquivos, confira permissões e restaure uma cópia válida se necessário |

## 11. Consultar os códigos no VS Code

No pacote de Releases, abra **Arquivo → Abrir Pasta → SentinelaLog/codigo-fonte** no VS Code. Os seis módulos do grupo estão diretamente nessa pasta; a interface está em `interface.py` e `components/`. Consulte o [mapa de arquivos e responsabilidades](arquitetura.md).

Para executar a distribuição pronta, volte à pasta principal e abra `SentinelaLog.exe`. Não é necessário iniciar os `.py` para usar o executável. Para executar pelo fonte, siga a seção 1.

O executável grava em `dados/` ao lado de `SentinelaLog.exe`. Ao executar o fonte, a base fica em `codigo-fonte/dados/`. São bases independentes; abrir uma delas não importa os registros da outra. Os arquivos fornecidos no fonte podem incluir um cadastro fictício de exemplo.

A cópia de `codigo-fonte` fornecida no ZIP serve para leitura e execução com Python. Ela não contém o histórico `.git`. Para sincronizar commits pelo VS Code, abra uma cópia clonada do repositório.
