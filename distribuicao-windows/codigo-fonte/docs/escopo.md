# Escopo da aplicação

Requisitos funcionais e técnicos do monitor de acessos.

## Usuários

Adicionar, visualizar, editar e excluir usuários. Cada cadastro contém nome, matrícula, perfil (estudante, professor ou administrador), horário permitido e observações.

A listagem deve mostrar a matrícula parcialmente. Uma opção específica permite revelar seu valor completo, com registro na auditoria.

## Acessos

Registrar e consultar usuário, data/hora, máquina de origem e resultado (sucesso ou falha). Um acesso registrado não pode ser editado depois.

## Classificação e alertas

Avaliar o acesso no momento do registro, classificá-lo e explicar os motivos. Os critérios são definidos pela equipe e devem constar no manual com as justificativas de segurança.

Consultar um arquivo .txt de origens bloqueadas e avisar quando a máquina informada estiver nessa lista. Identificar máquinas utilizadas por usuários diferentes e informar quais usuários aparecem associados a elas.

## Auditoria e persistência

Registrar operações relevantes com operação, usuário afetado e data/hora. Incluir revelação de matrícula e permitir consulta da auditoria pelo menu.

Usuários, acessos e auditoria devem permanecer disponíveis entre execuções, em arquivos .csv ou .txt.

## Relatório

Apresentar total de acessos e falhas, usuários com mais falhas, horários de maior movimento e quantidades de acessos classificados como suspeitos ou críticos. As regras de contagem e a apresentação de empates devem ser consistentes com o histórico.

## Complementos

A funcionalidade extra é o gráfico textual da distribuição dos riscos. A [integração de IA](integracao_ia.md) permite perguntas sobre os registros, conforme a finalidade prevista no enunciado.

## Requisitos técnicos

Python pelo terminal, organização em funções, tratamento de exceções e legibilidade. Bibliotecas expressamente admitidas: os, datetime e random. Outras dependências exigem consulta aos professores. Na implementação, o núcleo (usuários, acessos, risco, armazenamento e relatórios) usa apenas `os` e `datetime`, e o `main.py` acrescenta `sys` para reconhecer o executável. O Tkinter (janela gráfica) e a biblioteca `groq` (integração de IA) são camadas adicionais, cada uma em módulos próprios, e o modo terminal (`python main.py --terminal`) funciona sem elas.

Usar somente dados fictícios. A documentação de uso abrange restrições, critérios de classificação e justificativas de segurança.

## Base acadêmica

Especificação do projeto de Fundamentos de Programação, Turma B, semestre 2026.2. Os materiais da disciplina definem os requisitos e os critérios de avaliação.
