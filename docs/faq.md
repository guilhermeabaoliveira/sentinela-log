# SentinelaLog — Para responder eventuais dúvidas

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

## A proposta

**1. O que é o SentinelaLog?**

É um monitor de acessos feito em Python. Ele cadastra usuários, registra cada acesso, classifica o risco com os motivos, guarda uma auditoria e gera relatórios. Um assistente de IA opcional responde perguntas sobre o histórico.

**2. Por que só dados fictícios?**

O trabalho simula um monitor de laboratório. Nomes, matrículas e máquinas são inventados, e o programa avisa isso na abertura.

**3. O programa monitora o computador de verdade?**

Não. Ele registra os eventos que o operador informa. Não lê o sistema operacional, não grava a tela e não funciona como antivírus.

**4. Por que ele roda localmente?**

Porque o trabalho pede um programa de terminal e porque assim não há servidor para manter. Chegamos a avaliar hospedar uma API na nuvem para guardar a chave da IA, mas isso exigiria login, limite de chamadas e uma interface web. Ficamos com o local: cada pessoa usa a própria chave.

## Como funciona

**5. O que é a matrícula fictícia e por que ela aparece mascarada?**

É um número inventado que identifica o cadastro e não muda. Nas listagens aparecem só os dois últimos dígitos (`****56`). A matrícula inteira só aparece pela opção Revelar matrícula, que fica registrada na auditoria. Mascarar não é criptografar.

**6. Como o risco de um acesso é decidido?**

Uma falha, ou um acesso fora do horário permitido, dá suspeito. As duas coisas juntas dão crítico. Uma origem na lista de bloqueadas também dá crítico. Sem nenhum sinal, o acesso é normal. Os critérios foram escolhidos pelo grupo e estão justificados no manual.

**7. Por que um acesso crítico é gravado mesmo assim?**

O sistema registra e avisa, não bloqueia. A origem bloqueada gera um aviso obrigatório, mas o evento entra no histórico, porque o objetivo é ter o registro completo.

**8. O que significa uma máquina compartilhada?**

É uma máquina que aparece em acessos de usuários diferentes. Isso não prova quem fez cada ação: o relatório só mostra a associação.

**9. O que acontece se alguém alterar o arquivo de dados à mão?**

Ao ler, o programa valida cada linha. Se algo estiver inválido, ele informa o erro e não substitui o arquivo. Por outro lado, quem tem acesso ao disco consegue editar os arquivos de texto: a auditoria não é à prova de adulteração.

**10. O que a auditoria registra?**

Cadastro, edição, exclusão, registro de acesso e revelação de matrícula, com o usuário afetado e a data e a hora. No modo terminal, as consultas locais também entram. As consultas de IA têm registro próprio.

**11. O que o sistema não detecta?**

Uma credencial roubada usada no horário e na origem de sempre, uma ação de outra pessoa em uma sessão compartilhada, um evento que ninguém registrou e qualquer alteração feita direto nos arquivos. O manual lista esses limites de propósito.

## Assistente de IA

**12. O assistente de IA é obrigatório?**

Não. O sistema inteiro funciona sem ele. A opção 10 só é usada se a pessoa tiver uma chave da Groq e quiser fazer perguntas sobre o histórico.

**13. O que é enviado para a Groq?**

A pergunta (até 600 caracteres) e uma lista de até 160 fatos já resumidos do histórico. Usuários e máquinas viram apelidos (U1, M1), então nomes e matrículas não saem. Observações livres e a auditoria não são enviadas. Antes de enviar, o programa mostra o que vai sair e pede confirmação.

**14. A IA pode alterar dados, bloquear alguém ou decidir o risco?**

Não. O risco é calculado pelas regras do próprio programa, antes e fora da IA. O assistente só lê fatos e devolve referências a eles. Ele não tem nenhuma função que escreva no sistema.

**15. E se a IA inventar uma resposta?**

A resposta precisa seguir um formato JSON rígido: ela só pode citar identificadores de fatos que realmente foram enviados, até 8, ou dizer que não há informação suficiente. O programa mostra apenas o texto local desses fatos, não texto livre escrito pelo modelo. Se a resposta vier fora do formato, ou cortada, é descartada.

**16. E se um registro tiver uma instrução escondida (prompt injection)?**

O texto livre não vai para o modelo, e o que volta é só identificador. Mesmo que o modelo seja enganado, ele não tem como executar nada. Ainda assim, é uma defesa por desenho: o grupo ainda não registrou um teste real desse ataque.

**17. Onde fica a chave da Groq?**

Só na memória da sessão ou na variável de ambiente `GROQ_API_KEY`. Ela não é gravada em arquivo nem entra no repositório.

**18. E se a internet cair ou a Groq demorar?**

A chamada tem limite de 20 segundos e não tenta de novo. Em caso de erro, o programa avisa e volta ao menu, sem travar e sem perder dados. A consulta fica no registro como erro.

**19. As perguntas à IA ficam registradas?**

Sim, em `consultas_ia.txt`: pergunta, momento, situação (iniciada, concluída ou erro) e modelo. Esse arquivo é separado da auditoria dos dados.

**20. Vocês usaram MCP?**

Não, de propósito. MCP serve para ligar um modelo a várias ferramentas e fontes. Aqui há uma única chamada, com um conjunto fixo de fatos, então uma chamada direta e controlada é mais simples e mais segura. É um conceito que vimos no curso de IA e que serve para comparar, não algo que o projeto usa.

## Executável, interface, GitHub e como testar

**21. Por que entregar um executável?**

Para quem avalia poder abrir o programa sem instalar Python. O PyInstaller empacota o interpretador e as bibliotecas na pasta `_internal`. É um extra: o código-fonte vai junto, em `codigo-fonte`, e o programa também roda pelo terminal com `--terminal`.

**22. E se o executável não abrir no computador do professor?**

O .exe é para Windows 64 bits e não é assinado digitalmente, então o Windows pode mostrar um aviso de segurança. Nesse caso, basta rodar o código-fonte: `python main.py --terminal`.

**23. O que seria preciso sem o executável?**

Entregar o código-fonte e pedir que a pessoa tenha Python instalado. Outra opção era Docker, que dá o mesmo ambiente em qualquer máquina mas exige instalar o Docker. Para uso remoto seria preciso um servidor, com login e limite de chamadas. Avaliamos o Docker e um servidor, e descartamos os dois por serem desproporcionais ao escopo.

**24. Por que o código usa bibliotecas além de `os`, `datetime` e `random`?**

O núcleo (cadastro, acessos, risco, armazenamento e relatórios) usa só a biblioteca padrão. O Tkinter (interface gráfica) e a Groq (IA) são extras acima do que foi pedido, e cada um fica em módulo próprio. O terminal funciona sem eles.

**25. Onde está o código e como acompanhar o trabalho de cada um?**

No GitHub do grupo, com o mesmo link entregue no Classroom. O histórico de commits mostra o que cada pessoa fez, e cada módulo tem um responsável.

**26. Como testar rapidamente?**

Descompactar o ZIP, abrir o executável (ou rodar `python main.py`) e usar o menu: cadastrar um usuário, registrar um acesso fora do horário com falha, ver o risco crítico, listar acessos e consultar a auditoria. O guia com os testes planejados está na documentação do projeto.

## Trabalho em grupo

**27. Como o grupo dividiu o trabalho?**

Por módulo: Guilherme ficou com o `main.py` (menu e fluxo) e o assistente de IA; Cauã com usuários; Kayo com acessos; Samuel com a regra de risco; Gabriel com o armazenamento; Pedro com relatórios e a interface. Cada um explica os commits da sua parte na apresentação.

**28. Como as partes se encaixam?**

O `main.py` chama os módulos. Eles trocam dados por estruturas simples e o armazenamento é o único que lê e grava arquivos. Isso permitiu que cada pessoa trabalhasse sem quebrar a parte do outro.

**29. O que o grupo faria com mais tempo?**

Registrar testes reais do assistente de IA e da injeção de comandos, revisar os comentários do código e padronizar a formatação. Esses pontos estão apontados nos documentos como limites conhecidos.
