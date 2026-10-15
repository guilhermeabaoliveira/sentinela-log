# Manual do usuário

**Disponibilidade:** a aplicação ainda não possui versão executável. Este manual apresenta o uso previsto no escopo; não representa uma demonstração funcional.

## Finalidade

Registrar acessos fictícios a um laboratório e consultar sua análise de risco. O sistema permite organizar usuários, eventos e auditoria em uma interface de terminal.

## Operações

| Operação | Dados envolvidos | Resultado previsto |
| --- | --- | --- |
| Cadastrar usuário | Nome, matrícula, perfil, horário permitido e observações | Cadastro disponível para consulta |
| Consultar usuários | Usuário selecionado ou listagem | Informações com matrícula parcial |
| Editar ou excluir usuário | Identificação de um cadastro existente | Atualização do cadastro e registro de operação relevante |
| Revelar matrícula | Usuário selecionado | Valor completo e auditoria da revelação |
| Registrar acesso | Usuário, data/hora, máquina e sucesso/falha | Evento, classificação e motivos |
| Consultar acessos | Histórico registrado | Eventos sem edição posterior |
| Consultar auditoria | Histórico de operações | Operação, usuário afetado e data/hora |
| Gerar relatório | Histórico de acessos | Totais, falhas, horários e indicadores de risco |

Os comandos de execução e as opções reais do menu serão documentados com a versão funcional.

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

A classificação deve considerar os critérios adotados pela equipe e apresentar seus motivos. A política definitiva, as categorias, os limites de horário e as justificativas de segurança ainda não foram definidos. Não há política implementada nesta versão documental.

Um aviso de origem bloqueada é obrigatório. A categoria atribuída ao evento depende da política adotada. A identificação de máquina compartilhada indica usuários distintos naquela origem, sem comprovar autoria física de uma ação.

## Persistência e falhas

Cadastros, acessos e auditoria devem permanecer disponíveis entre execuções. Entradas inválidas e falhas de arquivo precisam ser informadas de forma compreensível. A aplicação não deve anunciar gravação bem-sucedida quando ela não ocorreu.

O formato de entrada e a localização dos arquivos acompanharão a versão executável.

## Restrições

Utilizar somente dados fictícios. Mascaramento de matrícula não cifra arquivos e a ausência de edição no menu não impede alterações externas no disco. Consulte [segurança](seguranca.md).

## Perguntas em linguagem natural

A funcionalidade depende do módulo fornecido pela disciplina. Consulte [integração de IA](integracao_ia.md) para a finalidade e a disponibilidade.
