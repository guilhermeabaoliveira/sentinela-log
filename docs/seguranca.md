# Segurança e limitações

O SentinelaLog é uma aplicação didática com dados fictícios. As propriedades abaixo fazem parte do escopo e ainda precisam ser demonstradas pela versão funcional.

## Privacidade da matrícula

As listagens apresentam apenas parte da matrícula. A revelação completa ocorre por uma opção específica e deve gerar registro de auditoria. O mascaramento protege a exibição, mas não equivale a criptografia do arquivo.

## Histórico de acessos

Eventos registrados não podem ser editados pelo menu. Essa restrição não torna os arquivos invioláveis: alguém com acesso ao disco pode alterá-los externamente.

## Classificação explicada

Cada classificação deve ser acompanhada dos motivos que a produziram. Os critérios definitivos e suas justificativas serão descritos no [manual](manual.md#classificação-de-risco). Uma classificação normal não comprova legitimidade; indica apenas ausência dos sinais avaliados pela política adotada.

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

Usar exclusivamente dados fictícios. O módulo de IA deve seguir a interface fornecida pela disciplina. Suas limitações serão documentadas a partir do comportamento efetivamente disponível.
