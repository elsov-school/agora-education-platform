# Provas e atividades

## Entrega contrato v1

No menu de provas, escolha **Gerar prova**, selecione um material aprovado pelo ID e informe o tipo, a dificuldade e a quantidade de questões. A revisão exibe cada enunciado, as alternativas, o gabarito e o critério. É possível editar uma questão, aprovar a gravação ou descartar o rascunho.

### Como as questões são geradas

O gerador separa o conteúdo do material por frases e quebras de linha, ignora repetições e usa cada trecho elegível uma vez. A quantidade máxima é o menor valor entre os trechos disponíveis para o tipo escolhido e `max_questoes` de `padroes.carregar_regras()`.

| Tipo | Exercício | Efeito da dificuldade |
| --- | --- | --- |
| `multipla_escolha` | Completar uma lacuna com um termo do trecho original. | Até duas, três ou quatro alternativas, conforme o número de termos disponíveis. O gabarito contém o texto da opção correta. |
| `discursiva` | Localizar a passagem no material e explicar sua ideia com as próprias palavras. O trecho integral serve de referência para a correção. | O enunciado oferece até três, duas ou uma palavra inicial como pista. |
| `verdadeiro_falso` | Julgar se o termo indicado ocupa a lacuna no texto original. | O nível fácil mostra a inicial, o médio informa o comprimento e o difícil apresenta apenas a afirmação. |

Essas regras locais produzem o mesmo rascunho para as mesmas escolhas. A avaliação da pertinência das questões cabe a quem revisa a prova. O aluno precisa ter acesso ao material citado.

### Autoria e persistência

O menu passa o dicionário recebido no login. As operações consultam o cadastro atual para verificar o perfil e o estado ativo. Cada professor consulta, edita, exclui e exporta suas próprias provas. A coordenação ativa pode operar sobre qualquer prova. Toda criação registra o ID de quem a salvou, inclusive na coordenação. A criação exige material aprovado e acessível tanto na seleção quanto na gravação.

`atividades.json` guarda as provas. O salvamento mantém os IDs existentes, atribui o próximo ID após o maior presente e grava a data local. A edição preserva os demais campos da prova. Histórico e exportação usam o conteúdo salvo, inclusive após mudanças na biblioteca. A exclusão pede confirmação.

Cada ID de material conta uma vez por prova salva. A contagem ocorre após a gravação, por `materiais.registrar_uso`. Se a biblioteca informar falha, o terminal identifica a prova e o material afetados para conferência. Revisões, consultas ao histórico, exportações e exclusões não incrementam usos.

A gravação usa um temporário exclusivo e verifica se o histórico mudou desde a leitura. Um JSON ilegível bloqueia a alteração. Se o programa for interrompido abruptamente e restar `atividades.json.tmp`, feche as sessões de provas e confira o histórico e o temporário antes de retirar esse temporário da pasta.

### APIs de `provas.provas`

| Função | Resultado |
| --- | --- |
| `gerar_prova(usuario)` | Conduz a geração e a revisão. Devolve a prova salva ou `None`. |
| `editar_prova_gerada(prova)` | Revisa em memória. Devolve o rascunho aprovado ou `None`. |
| `gerenciar_provas(usuario)` | Abre o menu de geração, histórico, edição, exclusão e exportação. |
| `salvar_prova(professor_id, dados_prova, usuario=None)` | Valida autoria, modelo, questões e referências. Devolve o registro salvo ou `None`. |
| `editar_questao(professor_id, atividade_id, indice_questao, dados_questao, usuario=None)` | Substitui a questão do índice informado, contado a partir de zero. Devolve `True` se gravou. |
| `listar_historico(professor_id=None, usuario=None)` | Exibe e devolve as provas, da mais recente para a mais antiga. Sem filtro de professor, a coordenação recebe todo o histórico. |
| `excluir_prova(atividade_id, professor_id, usuario=None)` | Pede confirmação e devolve `True` se excluiu. |
| `exportar_prova(atividade_id, usuario)` | Consulta a prova salva, confere autoria e chama `padroes.exportar_prova_formatada(prova)`. Devolve os caminhos da prova do aluno e do gabarito do professor, nessa ordem, ou `[]` em caso de falha. |

As chamadas que já recebiam `professor_id` mantêm a ordem dos argumentos e recebem a sessão por `usuario=usuario`. Um ID isolado é insuficiente para autorizar a operação. `gerar_atividade(usuario=None)` permanece como entrada para o menu anterior.

### Verificação

Na raiz do repositório, execute `python -B -m unittest discover -s prototipo-terminal-python/tests -p test_provas.py -v`.

Os testes usam arquivos temporários de usuários, materiais e provas. Exercitam o menu, os três tipos, os limites de geração, a revisão, a autoria, a recarga do histórico, a exclusão e as falhas de gravação. Substitutos das APIs parceiras verificam o filtro aplicado, a leitura do limite institucional, a contagem de usos e o encaminhamento da prova salva para exportação.

Também foi executado um cenário temporário com as implementações reais de usuários (`393d965`), materiais (`1c61b2b`) e padrões (`b8eef27`). Após o login e a aprovação de um material pela coordenação, o professor gerou uma prova de cada tipo. Foram conferidos os três usos, os seis arquivos de aluno e gabarito, o histórico recarregado e a exclusão confirmada.
