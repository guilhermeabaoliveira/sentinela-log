# Segurança e limitações

Privacidade, rastreabilidade e limites de detecção do monitor de acessos. O uso do SentinelaLog é restrito a dados fictícios.

## Privacidade da matrícula

As listagens apresentam apenas parte da matrícula. A revelação completa ocorre por uma opção específica e deve gerar registro de auditoria. O mascaramento protege a exibição, mas não equivale a criptografia do arquivo.

## Histórico de acessos

Eventos registrados não podem ser editados pelo menu. Essa restrição não torna os arquivos invioláveis: alguém com acesso ao disco pode alterá-los externamente.

## Classificação explicada

Cada classificação deve ser acompanhada dos motivos que a produziram. Consulte a seção de [classificação de risco](manual.md#classificação-de-risco) no manual. Uma classificação normal não comprova legitimidade; indica apenas ausência dos sinais avaliados pela política adotada.

## Origens e compartilhamento

A lista de origens bloqueadas precisa produzir aviso quando houver correspondência. Uma máquina associada a usuários diferentes dificulta a atribuição de ações, mas não identifica quem estava fisicamente utilizando o equipamento.

## Auditoria

A trilha registra operações relevantes, usuário afetado e data/hora, incluindo revelações de matrícula. Falhas de gravação precisam ser informadas; não há garantia de auditoria quando o registro não puder ser persistido.

## Limites de detecção

O sistema pode deixar de identificar:

- Credencial comprometida usada no horário e origem habituais.
- Ação realizada por outra pessoa em uma sessão compartilhada.
- Evento que não foi registrado na aplicação.
- Alteração externa dos arquivos de dados ou da auditoria.
- Ameaça que não corresponda aos critérios adotados.

## Dados e integração

A integração de IA utiliza o módulo fornecido pela disciplina. A interface e as condições de uso estão descritas em [integração de IA](integracao_ia.md).
