# Padrões e exportação de provas

## Entrega contrato v1

As regras demonstrativas em `regras.json` definem o nome Ágora, o limite de 10 questões por prova e a instrução “Leia cada questão com atenção e registre suas respostas.”. A coordenação pode alterar os três campos pelo terminal. A próxima validação ou exportação usa os valores salvos, inclusive para provas do histórico.

### Configuração

- `carregar_regras()` lê o JSON UTF-8 e devolve um dicionário com `nome_escola`, `max_questoes` e `instrucoes`. O nome e as instruções precisam conter texto. O limite precisa ser um inteiro positivo. Um arquivo inválido gera `ValueError` e um arquivo ausente gera `FileNotFoundError`.
- `configurar_padrao_escola(usuario)` recebe a sessão autenticada do menu. A função consulta o cadastro pelo ID da sessão e exige o perfil `coordenacao` com `ativo=True` tanto na sessão quanto no cadastro atual. Enter mantém o campo atual. A função devolve as regras salvas ou `None` se a operação for recusada ou falhar. Um erro de leitura ou entrada preserva o arquivo anterior.

### Exportação para aluno e professor

`exportar_prova_formatada(prova, destino=None)` recebe a prova salva após o módulo `provas` verificar a autoria ou o acesso da coordenação. O diretório padrão é `prototipo-terminal-python/exportacoes/`. Para selecionar outra pasta, passe seu caminho em `destino`.

A função retorna uma lista com dois caminhos, nesta ordem:

1. `prova_aluno_ID.txt` contém cabeçalho da escola, instruções, questões numeradas na ordem original e alternativas. O texto do aluno usa somente os campos de apresentação.
2. `gabarito_professor_ID.txt` contém o cabeçalho e, para cada número de questão, o gabarito e o critério de correção registrados na prova.

Os dois arquivos usam UTF-8. Uma nova exportação do mesmo ID atualiza ambos. A prova precisa ter ID numérico positivo, disciplina, série, bimestre e pelo menos uma questão dentro do limite vigente. Cada questão precisa de enunciado, tipo, dificuldade, gabarito e critério. Para múltipla escolha, `alternativas` deve ser uma lista com ao menos dois textos. A autorização por ID e a leitura de `atividades.json` ficam com o módulo `provas`.

Durante a gravação, `.exportando_ID/` reserva o par de arquivos. Se o processo for encerrado à força durante a exportação, essa pasta pode persistir. Com o programa fechado, remova a pasta de preparo daquele ID e exporte a prova salva novamente para recompor o par.

### Chamadas existentes

- `obter_modelo(nome="institucional_v1")` retorna uma cópia do modelo. Modelos desconhecidos geram `ValueError`.
- `validar_prova(dados_prova)` confere os campos e o limite institucional. Retorna `True` em caso de sucesso. A interface anterior continua aceitando questões sem os detalhes opcionais de tipo e dificuldade.
- `formatar_prova(dados_prova, modelo)` retorna o texto do aluno e aceita o nome ou o dicionário do modelo.
- `exportar_atividade(dados_prova, destino, incluir_gabarito=False)` mantém a exportação de arquivo único. O destino pode ser uma pasta ou um arquivo. Com `incluir_gabarito=True`, o gabarito e os critérios são anexados ao texto no mesmo arquivo.

As funções estão disponíveis no pacote `padroes` e em `padroes.padroes`.

### Testes

A partir de `prototipo-terminal-python/`, execute:

```console
python -m unittest discover -s tests -p test_padroes.py -v
```

Os testes usam arquivos temporários para verificar permissões, persistência das regras, limites, compatibilidade, separação do conteúdo e recuperação após erro de escrita.
