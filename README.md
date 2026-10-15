# SentinelaLog

### Monitor de acessos e análise de risco pelo terminal.

O SentinelaLog é um projeto acadêmico em Python voltado ao registro de acessos a um laboratório fictício, à identificação de situações suspeitas e à consulta de informações de segurança.

[Documentação](docs/README.md) · [Manual](docs/manual.md) · [Escopo](docs/escopo.md) · [Segurança](docs/seguranca.md)

## Sobre o projeto

O sistema reúne cadastros de usuários, eventos de acesso e auditoria para responder a perguntas como: quais tentativas falharam, quais máquinas aparecem associadas a mais de um usuário e quais acessos acionaram um alerta.

**Estado atual:** em desenvolvimento, sem versão executável disponível. As funcionalidades descritas representam o escopo do projeto.

## Funcionalidades do escopo

| Área | Finalidade |
| --- | --- |
| Usuários | Cadastrar, consultar, editar e excluir usuários com perfil e horário permitido |
| Acessos | Registrar usuário, data, hora, máquina e resultado; consultar o histórico sem editar eventos |
| Privacidade | Exibir matrículas parcialmente e permitir revelação por operação específica |
| Risco | Classificar acessos e apresentar os motivos, incluindo aviso de origem bloqueada |
| Máquinas compartilhadas | Identificar origens utilizadas por usuários distintos |
| Auditoria | Registrar operações relevantes e permitir sua consulta |
| Relatórios | Apresentar totais, falhas, usuários e horários de destaque e contagens de risco |
| IA | Integrar o módulo de perguntas em linguagem natural fornecido na disciplina |

O escopo inclui persistência entre execuções e uma funcionalidade adicional, ainda não definida. Consulte a [descrição completa](docs/escopo.md).

## Ambiente

- Python com entrada e saída pelo terminal.
- Dados exclusivamente fictícios.
- Persistência em arquivos de texto, conforme as restrições da disciplina.

Instruções de execução acompanharão a primeira versão funcional. O [manual](docs/manual.md) apresenta o uso previsto, os campos e as restrições do sistema.

## Segurança

As classificações precisam ser acompanhadas de motivos. Matrícula mascarada protege a exibição; não cifra o armazenamento. A associação de uma máquina a vários usuários não comprova autoria de uma ação.

As limitações estão em [segurança](docs/seguranca.md). Os critérios adotados e suas justificativas integrarão o manual quando definidos.

## Contexto acadêmico

Projeto de **Fundamentos de Programação — 2026.2**, com uso exclusivo de dados fictícios. A [integração de IA](docs/integracao_ia.md) faz parte do escopo acadêmico. Informações sobre assistência no desenvolvimento estão em [transparência](docs/transparencia.md).
