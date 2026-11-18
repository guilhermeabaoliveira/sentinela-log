# Modelo de dados

Campos e relações dos registros abrangidos pelo SentinelaLog. Os tipos indicam a natureza da informação; não definem um formato de serialização.

## Usuário

| Campo | Tipo | Descrição |
| --- | --- | --- |
| Nome | Texto | Nome do usuário fictício |
| Matrícula | Texto | Identificação do usuário |
| Perfil | Categoria | Estudante, professor ou administrador |
| Horário permitido | Faixa de horário | Período de acesso associado ao cadastro |
| Observações | Texto | Informações complementares do cadastro |

A matrícula é apresentada parcialmente nas listagens. A revelação completa corresponde a uma operação específica, registrada na auditoria.

## Acesso

| Campo | Tipo | Descrição |
| --- | --- | --- |
| Usuário | Referência ao cadastro | Usuário associado ao evento |
| Data e hora | Instante | Momento do acesso informado |
| Máquina de origem | Texto | Equipamento associado ao evento |
| Resultado | Categoria | Sucesso ou falha |
| Classificação | Categoria de risco | Resultado da análise do acesso |
| Motivos | Informações de análise | Condições que justificam a classificação |

O resultado de acesso e a classificação de risco têm significados distintos. Um evento de sucesso pode receber uma classificação de risco quando corresponder aos critérios adotados. Acesso registrado não é editável pelo menu.

## Auditoria

| Campo | Tipo | Descrição |
| --- | --- | --- |
| Operação | Texto | Ação relevante registrada pela aplicação |
| Usuário afetado | Referência ao cadastro | Cadastro relacionado à operação |
| Data e hora | Instante | Momento em que a operação ocorreu |

A auditoria inclui a revelação de matrícula e permite consultar o histórico de operações. O instante de auditoria descreve a operação na aplicação, enquanto o instante de acesso descreve o evento informado.

## Consulta de IA

O arquivo `dados/consultas_ia.txt` usa uma linha por estado da tentativa, com cinco campos separados por tabulação:

| Campo | Descrição |
| --- | --- |
| Operação | `CONSULTA_IA` |
| Pergunta | Texto tratado enviado ao assistente |
| Data e hora | Instante local do registro |
| Resultado | `INICIADA`, `CONCLUIDA` ou `ERRO` |
| Modelo | Identificador do modelo consultado |

A chave de API não faz parte desse registro. Usuários e acessos permanecem em `dados/estado.txt`.

## Origens bloqueadas

A lista contém identificações de máquinas ou origens bloqueadas, armazenadas em arquivo .txt. A presença de uma origem nessa lista exige aviso durante o registro do acesso.

## Relações

- Um usuário pode estar associado a vários acessos.
- Uma máquina pode aparecer em acessos de usuários diferentes.
- Uma operação relevante pode produzir um registro de auditoria associado ao usuário afetado.

Compartilhamento de máquina é identificado pela presença de usuários distintos na mesma origem. Repetições de acesso de um único usuário não representam compartilhamento entre pessoas diferentes.

## Retenção e privacidade

Usuários, acessos e auditoria fazem parte da persistência entre execuções. Matrícula mascarada protege a exibição; não equivale à criptografia dos arquivos. As condições de uso estão no [manual](manual.md) e as limitações em [segurança](seguranca.md).
