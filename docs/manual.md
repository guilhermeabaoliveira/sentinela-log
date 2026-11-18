# Manual do usuário

Referência das operações de cadastro, registro de acessos, consultas e relatórios do SentinelaLog.

## Iniciar

Na pasta do programa, execute `python -m pip install -r requirements.txt` e depois `python main.py` para abrir a interface gráfica. O modo terminal utiliza `python main.py --terminal`.

## Finalidade

Registrar acessos fictícios a um laboratório e consultar sua análise de risco. O sistema permite organizar usuários, eventos e auditoria em uma interface gráfica e no modo terminal.

## Operações

| Operação | Dados envolvidos | Finalidade |
| --- | --- | --- |
| Cadastrar usuário | Nome, matrícula, perfil, horário permitido e observações | Cadastro disponível para consulta |
| Consultar usuários | Usuário selecionado ou listagem | Informações com matrícula parcial |
| Editar ou excluir usuário | Identificação de um cadastro existente | Atualização do cadastro e registro de operação relevante |
| Revelar matrícula | Usuário selecionado | Valor completo e auditoria da revelação |
| Registrar acesso | Usuário, data/hora, máquina e sucesso/falha | Evento, classificação e motivos |
| Consultar acessos | Histórico registrado | Eventos sem edição posterior |
| Consultar auditoria | Histórico de operações | Operação, usuário afetado e data/hora |
| Gerar relatório | Histórico de acessos | Totais, falhas, horários e indicadores de risco |

## Campos e interpretação

- **Matrícula:** identificação do usuário. Sua exibição completa ocorre por operação específica.
- **Perfil:** estudante, professor ou administrador.
- **Horário permitido:** faixa de acesso associada ao cadastro.
- **Data/hora do acesso:** instante do evento registrado.
- **Máquina de origem:** equipamento informado no acesso.
- **Sucesso/falha:** resultado do acesso, distinto de sua classificação de risco.
- **Classificação e motivos:** conclusão da análise e condições que a justificam.
- **Data/hora da auditoria:** instante da operação realizada na aplicação.

## Classificação de risco

A classificação reúne uma categoria de risco e os motivos associados ao acesso. Um acesso sem sinais é normal. Falha ou horário fora da faixa permitida gera suspeito. Falha combinada com horário fora da faixa gera crítico. Uma origem da lista de bloqueadas também gera crítico e aviso. Os limites do horário são inclusivos e faixas noturnas são aceitas. Esses sinais priorizam a revisão dos registros.

Origens presentes na lista de bloqueadas exigem um aviso. A identificação de máquina compartilhada indica usuários distintos naquela origem, sem comprovar autoria física de uma ação.

## Persistência e falhas

A persistência abrange cadastros, acessos e auditoria entre execuções. Mensagens de erro devem identificar entradas inválidas e falhas de leitura ou gravação. A confirmação de uma operação depende da gravação correspondente.

## Restrições

O uso é restrito a dados fictícios. Mascaramento de matrícula não cifra arquivos e a ausência de edição no menu não impede alterações externas no disco. Consulte [segurança](seguranca.md).

## Perguntas em linguagem natural

Abra a opção **10 Assistente IA**, configure sua chave Groq e faça uma pergunta sobre os acessos fictícios. Revise o texto e confirme o envio externo. Consulte [integração de IA](integracao_ia.md) para os dados enviados, os limites e o registro local de consultas.
