# Guias de apresentação e defesa técnica — Ágora

Estes guias explicam o código da `main` no commit `caf60f1`, incluindo login por e-mail e senha. As branches individuais podem estar em uma versão anterior; estude a versão que será efetivamente apresentada. A documentação não publica credenciais nem substitui o código.

## Divisão entre os integrantes

Há **quatro blocos funcionais de CRUD e seis módulos de responsabilidade**. Consultas e padrões apoiam os CRUDs; o painel é uma consulta agregada, sem coleção própria para inserir e excluir métricas.

| Integrante / área | Responsabilidade | Funções definidas no escopo | Guia | Branch de trabalho |
| --- | --- | --- | --- | --- |
| 1 | Usuários, login, atribuições e permissões | 31, incluindo o configurador inicial | [Guia de usuários](usuarios/GUIA_APRESENTACAO.md) | `feat/usuarios` |
| 2 | Biblioteca e aprovação de materiais | 26 | [Guia de materiais](materiais/GUIA_APRESENTACAO.md) | `feat/materiais` |
| 3 | Pesquisa e consultas com evidência | 8 | [Guia de consultas](consultas/GUIA_APRESENTACAO.md) | `feat/consultas` |
| 4 | Geração, revisão e banco de provas | 25 nos dois arquivos do módulo | [Guia de provas](provas/GUIA_APRESENTACAO.md) | `feat/provas` |
| 5 | Regras institucionais e exportação | 16 | [Guia de padrões](padroes/GUIA_APRESENTACAO.md) | `feat/padroes-exportacao` |
| 6 | Painel, menus e integração | 24, incluindo o `main.py` | [Guia de painel e menu](painel/GUIA_APRESENTACAO.md) | `feat/painel-menu` |

**Total: 130 funções de aplicação documentadas.** Funções importadas da biblioteca padrão e funções de testes não são contadas como implementações do grupo. Uma função importada do colega não vira uma nova função só porque está disponível em outro módulo.

O [dicionário técnico comum](DICIONARIO_TECNICO.md) explica os termos, as estruturas Python e as perguntas gerais que qualquer integrante deve saber responder.

## Como estudar cada guia

1. Leia a fala de abertura para saber resumir sua responsabilidade em 30 segundos.
2. Faça o roteiro prático e anote os IDs realmente gerados no seu ensaio.
3. Estude a lista completa: assinatura, argumentos, resultado/efeitos e como explicar cada função.
4. Para funções pequenas, mostre o trecho de código; não é necessário criar uma opção de menu para cada helper.
5. Ensaiem as perguntas técnicas e saibam reconhecer limites. Evitem decorar respostas que não consigam apontar no código.
6. Em apresentação curta, demonstrem o fluxo principal; usem as funções auxiliares como material de consulta para a arguição.

## Preparação do grupo

- Use uma cópia de ensaio com contas e dados fictícios. Não projete e-mails reais, senhas, hashes ou cadastros pessoais. Não apague a única coordenação para reiniciar uma demonstração.
- Se ainda não existir senha de coordenação, execute `py configurar_acesso.py` na pasta do protótipo e escolha o acesso local. Se já existir, use o acesso preparado no ensaio, sem repetir o bootstrap.
- O professor de teste deve ter atribuição explícita, por exemplo `6C | 6º ano | Ciências`.
- Prepare texto com frases suficientes para a quantidade de questões. O limite da escola também precisa permitir a quantidade escolhida.
- Código BNCC de demonstração não é uma certificação de alinhamento. Use `DEMO_CIEN` para um exemplo fictício e explique essa escolha.
- Todos executam a partir de `prototipo-terminal-python`: `py main.py`. A opção 9 troca de usuário; 0 volta ou encerra conforme o menu indicado.

## Roteiro integrado: ordem de passagem da apresentação

| Ordem | Quem fala | O que demonstra | O que entrega ao próximo |
| --- | --- | --- | --- |
| 1 | Usuários | Login, cadastro de professor e atribuição | Conta ativa com permissão e turma definida |
| 2 | Materiais | Sugestão pendente e aprovação pela coordenação | ID de uma fonte aprovada e permitida |
| 3 | Consultas | Termo encontrado, trecho literal e fonte | Consulta registrada; um uso na fonte |
| 4 | Provas | Escolha, geração, revisão, gravação e histórico | ID e objeto de prova salva; mais um uso na fonte |
| 5 | Padrões | Regras da escola e dois TXT exportados | Prova do aluno e gabarito do professor |
| 6 | Painel/menu | Fluxo por perfil, agregações e reinício | Visão conjunta dos resultados persistidos |

Para um material novo com exatamente uma consulta com evidência e uma prova salva, o contador deve terminar com **2 usos**. Pesquisa simples, histórico, revisão e exportação não somam usos. Se mais fontes corresponderem à consulta ou se repetirem a operação, os resultados serão diferentes.

Depois da exportação e do painel, uma prova descartável pode ser excluída para demonstrar o D do CRUD. Não excluam a prova principal antes de mostrar o histórico, as referências e os arquivos.

## O que mostrar em caso de pergunta sobre testes

Na pasta do protótipo:

```powershell
py -B -m unittest discover -s tests -v
```

O cenário real de ponta a ponta pode ser mostrado isoladamente:

```powershell
py -B -m unittest discover -s tests -p test_integracao.py -k TestEscolaTemporaria -v
```

A verificação de código imediatamente anterior a estes guias teve **77 testes aprovados**. Isso é evidência dos cenários cobertos nessa versão, não garantia de ausência de qualquer defeito. Os guias acrescentam documentação; não alteram a aplicação nem os JSONs.

## Como explicar a relação com o nível da disciplina

A base do sistema usa funções, decisões, repetições, listas, dicionários e arquivos, em linha com o exemplo escolar e os temas da ementa enviada. O projeto também contém recursos que podem precisar de explicação complementar: expressões regulares, funções `lambda`, compreensões, context managers, temporários e derivação de senha da biblioteca padrão.

Não afirmem que cada construção foi ensinada em sala: a ementa não detalha toda a sintaxe de Fundamentos. Expliquem o que cada recurso resolve e apontem seu uso. O código da aplicação é procedural; algumas classes aparecem nos testes por exigência do `unittest`, não como arquitetura orientada a objetos da aplicação.
