# Histórico de versões

## 2026-11-23 — Desde a entrega via Classroom

Registro do que foi melhorado depois da entrega. O código-fonte e o executável entregues não foram alterados: as melhorias são de documentação e de organização do material de apresentação.

### Documentação nova

- `docs/relatorio_desenvolvimento.md`: relatório de desenvolvimento com visão geral, ideação, ferramentas, planejamento, divisão de responsabilidades, desafios e reflexão do grupo.
- `docs/documentacao_tecnica.md`: lógica da programação, módulo a módulo, com o diagrama de arquitetura, o ciclo de cada operação do menu, as regras de negócio, a gravação segura e o assistente de IA.
- `docs/faq.md`: respostas para as dúvidas mais prováveis (proposta, funcionamento, IA, executável, GitHub, trabalho em grupo), incluindo o que o sistema não detecta.

### Documentação revisada

- `docs/escopo.md`: os requisitos técnicos passam a dizer o que o núcleo usa (`os`, `datetime` e `sys`) e que Tkinter e `groq` são camadas adicionais em módulos próprios, com o modo terminal funcionando sem elas.
- `docs/transparencia.md`: o texto sobre os registros da entrega passa a falar de documentação das decisões e histórico dos prompts, sem prometer comentários no código.
- `README.md`: a lista de documentos e o resumo de `docs/` incluem os novos arquivos.
- Decisões de distribuição registradas: o Docker foi retirado (já constava abaixo) e uma versão web com servidor, que guardaria a chave da IA, foi avaliada e descartada por exigir login, limite de chamadas e interface web além do pedido.

### O que não mudou

- Nenhum arquivo `.py` do programa, nenhum teste e nenhum dado foram alterados.
- O executável da release `v2026.11.18-final.2` continua sendo o entregue.

## 2026-11-18

- Interface Tkinter com tema escuro inicial e alternância para tema claro.
- Realce de ações ao passar o mouse ou receber foco, identificação da página selecionada e botão de saída destacado.
- Consulta de leitura à Groq com configuração da chave por sessão, confirmação de envio e validação dos fatos retornados.
- Auditoria das consultas em arquivo TXT, acessível pela interface e pelo terminal.
- Matrículas mascaradas também na seleção de usuário para registrar acessos.
- Tratamento de base inválida na abertura gráfica, sem substituir o arquivo original.
- Relatório gráfico com usuários com mais falhas, horários de pico e rolagem para consultar todo o conteúdo.
- Manual de instalação, operações, demonstração e solução de problemas atualizado.
- Distribuição concentrada em execução local: removida a alternativa Docker, que não era necessária para o pacote Windows.
- Código-fonte e mapa das pastas incluídos no pacote de distribuição, com orientações para consulta no VS Code.
- Distribuição portátil para Windows 64 bits, com Python e dependências incluídos e abertura confirmada no Windows.

O repositório mantém o código-fonte Python. A versão portátil está em Releases e não exige instalador. Nenhuma distribuição inclui chave de API.
