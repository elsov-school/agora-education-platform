# Módulo 2 — Biblioteca curricular

## Entrega contrato v1

A coordenação pode cadastrar, consultar, editar, aprovar e excluir materiais. Um cadastro da coordenação já entra como `aprovado_coordenacao`. O professor sugere material para revisão. Na biblioteca, ele vê os aprovados que correspondem às suas atribuições de série e disciplina, incluindo a turma quando o material a especifica. Pode editar um material visível de sua autoria. A edição devolve o material à fila de aprovação.

### Operações

| Função | Comportamento |
| --- | --- |
| `gerenciar_materiais(usuario=None)` | Abre o menu da biblioteca com as ações do perfil ativo. |
| `adicionar_material(usuario=None)` | Pede título, disciplina, série, bimestre, BNCC, conteúdo, tipo e turma opcional. Registra o ID da sessão como autor e inicia o contador em zero. |
| `listar_materiais(usuario=None)`, `visualizar_material(usuario=None)` | Aplicam o mesmo filtro à listagem e à seleção por ID. Usam `usuarios.filtrar_materiais_do_professor` para professores. |
| `editar_material(usuario=None)` | Enter mantém um campo. Um hífen no campo turma remove a restrição de turma. Mantém ID, autoria e usos. |
| `aprovar_materiais_pendentes(usuario)` | Apresenta a fila à coordenação. Exibe o conteúdo do ID escolhido e pede confirmação antes de aprovar. |
| `excluir_material(usuario=None)` | Exige confirmação da coordenação e verifica `provas/atividades.json`. Bloqueia a exclusão se uma prova referencia o ID ou se o histórico está ausente ou ilegível. |
| `registrar_uso(material_id)` | Reabre o JSON, incrementa um uso e atualiza a lista compartilhada. Retorna `True` quando grava. Consultas e provas chamam essa função após uma consulta respondida ou uma prova salva. |
| `carregar_dados()`, `salvar_dados()` | Operações de persistência sobre a lista compartilhada `materiais`. Retornam `True` em caso de sucesso. A lista mantém sua identidade para quem a importou. |

As operações interativas recebem o dicionário da sessão. Sessões ausentes, inativas ou com perfil desconhecido não podem operar na biblioteca.

### Migração do acervo

`materiais.json` é a fonte de dados. Na primeira leitura de registros antigos, o módulo mantém IDs, títulos, campos extras e textos originais. Aceita os pares `bncc` e `habilidade_bncc`, `conteudo` e `conteudo_texto`, preenchendo o nome ausente com o valor existente. Se os dois nomes contêm valores divergentes, a leitura informa o registro que precisa de revisão e preserva o arquivo.

Para os quatro registros antigos, o tipo inicial é `capitulo`, a autoria desconhecida fica como `null`, o status é `pendente` e o contador começa em zero. Os tipos disponíveis no cadastro são `apostila`, `capitulo` e `plano_aula`. A ausência de turma indica material aplicável a todas as turmas daquela série e disciplina.

Uma biblioteca ausente é inicializada com os quatro exemplos. A lista vazia `[]` continua vazia após reiniciar. Um arquivo truncado, JSON inválido ou registro inconsistente gera uma mensagem e permanece disponível para recuperação. O contador relê a versão mais recente a cada tentativa. A edição informa quando outra operação modificou a biblioteca durante o preenchimento.

Cada gravação usa `materiais.json.tmp` na mesma pasta e substitui o original ao terminar. Se o processo for encerrado à força durante a gravação, esse temporário pode permanecer. Nesse caso, feche as instâncias do protótipo e remova apenas o temporário antes de repetir a operação.

### Testes

Na pasta `prototipo-terminal-python`, execute:

```console
py -m unittest discover -s tests -p "test_materiais.py" -v
```

Os testes usam arquivos temporários para verificar migração, cadastros, aprovação, permissões, referências de provas, disputa entre gravações e contagem de usos. Nos testes da tela do professor, uma lista simulada representa a resposta do filtro do módulo de usuários.
