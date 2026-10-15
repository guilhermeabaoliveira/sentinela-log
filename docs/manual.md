# Manual do usuário

Referência das operações de cadastro, registro de acessos, consultas e relatórios do SentinelaLog.

## Finalidade

Registrar acessos fictícios a um laboratório e consultar sua análise de risco. O sistema permite organizar usuários, eventos e auditoria em uma interface de terminal.

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

A classificação reúne uma categoria de risco e os motivos associados ao acesso. A política de classificação, incluindo categorias e limites de horário, está em definição.

Origens presentes na lista de bloqueadas exigem um aviso. A categoria atribuída ao evento depende da política de classificação. A identificação de máquina compartilhada indica usuários distintos naquela origem, sem comprovar autoria física de uma ação.

## Persistência e falhas

A persistência abrange cadastros, acessos e auditoria entre execuções. Mensagens de erro devem identificar entradas inválidas e falhas de leitura ou gravação. A confirmação de uma operação depende da gravação correspondente.

## Restrições

O uso é restrito a dados fictícios. Mascaramento de matrícula não cifra arquivos e a ausência de edição no menu não impede alterações externas no disco. Consulte [segurança](seguranca.md).

## Perguntas em linguagem natural

A funcionalidade depende do módulo fornecido pela disciplina. Consulte [integração de IA](integracao_ia.md) para a finalidade e a disponibilidade.
