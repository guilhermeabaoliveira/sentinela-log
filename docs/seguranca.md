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

A trilha registra cadastro, edição, exclusão, registro de acesso e revelação de matrícula, com usuário afetado e data/hora. O modo terminal registra também suas consultas locais; navegar pelas listagens da interface gráfica não cria uma nova entrada de auditoria. Falhas de gravação precisam ser informadas; não há garantia de auditoria quando o registro não puder ser persistido.

## Limites de detecção

O sistema pode deixar de identificar:

- Credencial comprometida usada no horário e origem habituais.
- Ação realizada por outra pessoa em uma sessão compartilhada.
- Evento que não foi registrado na aplicação.
- Alteração externa dos arquivos de dados ou da auditoria.
- Ameaça que não corresponda aos critérios adotados.

## Dados e integração

A integração de IA consulta a Groq usando fatos selecionados e validados pelo sistema. A interface e as condições de uso estão descritas em [integração de IA](integracao_ia.md).


## Assistente e dados externos

O programa não executa SQL nem utiliza banco de dados SQL. Neste contexto, instruções maliciosas na pergunta ou nos registros caracterizam tentativa de injeção de prompt; elas não devem ser tratadas como comandos confiáveis.

Observações livres, nomes e matrículas não compõem os fatos enviados: identidades são substituídas por aliases. A pergunta tem limite de tamanho, substitui identidades cadastradas e rejeita alguns padrões de credenciais. Esse filtro não identifica todo dado pessoal possível: não digite segredos ou dados reais. Revise o envio antes de confirmar.

O modelo seleciona identificadores de fatos. A validação local rejeita referências desconhecidas e retornos incompletos; somente textos de fatos calculados pelo programa são exibidos. Isso limita respostas inventadas, mas não garante que a seleção seja pertinente à pergunta. Confira os resultados nos registros.

Cada envio usa uma chamada, sem repetição automática, com timeout de rede de 20 segundos e limite de 1.024 tokens de conclusão. O timeout não é um cronômetro absoluto da operação completa. Não há ferramentas de execução, alteração automática de registros ou acesso do assistente à chave configurada como conteúdo de conversa. A chave é usada pelo cliente HTTPS para autenticar a requisição.

## Distribuição local

A versão Windows inclui o interpretador e dependências; mantenha a pasta inteira. O código-fonte acompanha o pacote para consulta. O executável não é assinado digitalmente e foi verificado neste ambiente Windows, sem garantia de compatibilidade com todas as máquinas. A versão é destinada a Windows 64 bits.

Não há autenticação de operadores nem permissão por perfil; perfis são dados do cadastro fictício. Arquivos TXT não são cifrados e a auditoria não é inviolável. A aplicação não coleta a tela. Execute uma única instância por pasta de dados para evitar sobrescrita concorrente. Não inclua chaves nem logs de uso pessoal em commits ou distribuições.
