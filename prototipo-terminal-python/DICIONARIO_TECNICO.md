# Dicionário técnico e respostas de defesa — Ágora

[Índice dos guias por integrante](GUIAS_APRESENTACAO.md)

Referência de estudo para o protótipo terminal na `main`, base `caf60f1`. Exemplos abaixo são didáticos: não execute operações de alteração sobre dados reais apenas para responder uma pergunta.

## 1. Resposta de arquitetura em um minuto

> A Ágora de terminal é um programa Python procedural dividido por módulos. O main faz o login e encaminha a sessão ao menu do perfil. Usuários verifica acesso; materiais mantém a biblioteca aprovada; consultas busca evidências; provas gera e guarda avaliações; padrões configura e exporta; painel agrega os dados. Os dados ficam em arquivos JSON locais. Não usamos um servidor, microsserviços, um banco relacional ou uma API de inteligência artificial nesse protótipo.

```text
main.py → login → menu por perfil
                   ├── usuários e atribuições
                   ├── biblioteca e aprovação
                   ├── consultas → materiais permitidos → uso registrado
                   ├── provas → fonte aprovada → revisão → atividades.json
                   │                                  └── padrões → dois TXT
                   └── painel → leitura e agregação dos mesmos cadastros
```

A aplicação web e a apresentação HTML do repositório são projetos separados. Não atribua ao terminal os recursos ou a persistência da versão web.

## 2. Dicionário de estruturas e fluxo Python

| Termo / construção | O que significa | Exemplo no projeto / como responder |
| --- | --- | --- |
| Variável | Nome associado a um valor | `usuario` aponta para o dicionário da sessão. |
| Função / `def` | Bloco nomeado que pode receber entradas e devolver resultado | `listar_historico` reúne a regra de seleção das provas. |
| Parâmetro | Nome declarado na assinatura | `usuario` em `gerar_prova(usuario)`. |
| Argumento | Valor fornecido na chamada | O dicionário da pessoa logada passado pelo menu. |
| Valor padrão | Usado quando o argumento é omitido | `incluir_inativos=False`; o padrão é omitir desativados. |
| `None` | Ausência de valor/resultado | Busca que não encontrou usuário; não significa a string `"None"`. |
| `True` / `False` | Valores booleanos | Autorização concedida ou recusada. |
| `return` | Devolve algo e termina a função | `return prova` permite ao chamador usar o registro salvo. |
| `print` | Mostra algo na tela | Não devolve o dado de negócio ao chamador. Uma função que imprime não necessariamente retorna uma lista. |
| `input` | Lê texto do teclado | Mesmo quando se digita 5, o resultado inicial é a string `"5"`. |
| `int` | Converte ou representa inteiro | Conversão do ID; letras geram `ValueError`. |
| `str` | Texto | Título, e-mail, enunciado. |
| `list` | Sequência mutável e ordenada | Lista de usuários ou de questões; pode acrescentar/remover itens. |
| `dict` | Mapa de chaves para valores | `material["titulo"]`; cada registro reúne campos nomeados. |
| Chave | Nome usado para acessar um valor no dicionário | `professor_id` guarda uma referência, não o nome inteiro do professor. |
| `tuple` | Sequência que não permite trocar seus itens diretamente | Tupla fixa de disciplinas; retorno `(data, id)` na ordenação do histórico. |
| `set` | Conjunto de valores sem duplicação | IDs vistos na validação e referências únicas dentro de uma prova. Não garante ordem de apresentação. |
| Índice | Posição de item em uma sequência, começando em 0 | A primeira questão é `questoes[0]`; a tela mostra 1 para o usuário. |
| ID | Identificador de registro | Não é a posição da lista. Após filtrar/ordenar, o ID continua o mesmo. |
| `if` / `elif` / `else` | Escolhem caminhos conforme condição | O menu encaminha a opção digitada. |
| `for` | Percorre uma coleção | Conferir cada material permitido. |
| `while` | Repete enquanto a condição for verdadeira | Menu fica aberto até voltar/sair ou perder autorização. |
| `break` | Encerra o laço mais próximo | Quando encontra correspondência ou encerra um fluxo. |
| `continue` | Passa para a próxima repetição | Ignorar material sem evidência, sem encerrar a busca inteira. |
| `in` | Verifica participação ou ocorrência | Item em uma lista/conjunto; termo dentro de uma string. |
| `len` | Quantidade de itens/caracteres | Limite de questões; não representa necessariamente o próximo ID. |
| `enumerate` | Percorre produzindo número e item | Numerar questões e alternativas para exibição. |
| `range` | Sequência de números usada em laços | Mostrar opções das tuplas de disciplinas e bimestres. |
| `isinstance` | Confere categoria de tipo | Verificar se a prova recebida é um dicionário. |
| `type(x) is int` | Exige exatamente um inteiro | Evita aceitar `True` como ID, pois bool é subclasse de int no Python. |
| `get` | Busca chave com padrão se estiver ausente | `material.get("usos", 0)`. Chave presente com None não é o mesmo que chave ausente. |
| `setdefault` | Completa chave ausente sem substituir a existente | Migração de campos do material. |
| `copy()` | Cópia superficial de lista/dicionário | Preparar edição sem trocar imediatamente o registro original; objetos aninhados podem continuar compartilhados. |
| Fatia `[:]` | Acesso/substituição do conteúdo de uma lista | `materiais[:] = novos` conserva a lista referenciada por outros módulos. |
| `strip` | Remove espaços externos | Validar nome não vazio. Não remove todo espaço do meio de um texto. |
| `split` / `splitlines` | Divide texto por separador / por linhas | Atribuições separadas por vírgula; trecho literal da consulta. |
| `lower` / `casefold` | Normalizam caixa para comparação | Comparar e-mails ou palavras sem distinguir maiúsculas. Não eliminam acentos em geral. |
| `join` | Junta sequência de textos | Montar o TXT com quebras de linha. |
| f-string | Insere valores num texto | `f"Prova {id}"`; permite alinhar colunas do painel. |
| `global` | Permite reatribuir nome no escopo do módulo | Estado da versão lida em materiais. Não significa variável compartilhada por vários computadores. |

## 3. Dicionário de módulos, dados e responsabilidades

| Termo | Significado no projeto |
| --- | --- |
| Módulo | Arquivo Python importável, como geracao.py. |
| Pacote | Pasta importável com organização de módulos; o projeto usa `__init__.py`. |
| `import` / `from` | Reutilizam implementações sem copiar a regra em cada arquivo. |
| Alias `as` | Nome local para um módulo importado, como `biblioteca`. |
| `__name__ == "__main__"` | Executa a entrada somente quando o arquivo é iniciado diretamente. Importá-lo não deve abrir o menu. |
| Helper com `_` | Convenção de função auxiliar interna. O sublinhado não bloqueia chamadas. |
| Contrato de função | Acordo sobre argumentos, retorno, efeitos e erros esperados pelo outro módulo. |
| Sessão | Dicionário do usuário que fez login, mantido em memória; não é token web nem sessão de servidor. |
| Autenticação | Verificar e-mail e senha para identificar quem entra. |
| Autorização | Decidir se essa pessoa pode realizar a operação ou acessar a fonte. |
| Perfil | Papel geral: professor ou coordenação. |
| Atribuição | Relação explícita de turma, série e disciplina que delimita o acesso do professor. |
| CRUD | Create, Read, Update, Delete: criar, ler, atualizar, excluir. |
| Exclusão lógica | Alterar ativo=False, sem apagar a pessoa; usada em usuários. |
| Exclusão física | Remover o registro da coleção; ocorre em provas e em materiais sem referência, com permissões/confirmação. |
| Referência | Um ID usado para ligar registros, como professor_id ou materiais_referenciados. O JSON não aplica chaves estrangeiras automaticamente. |
| Curadoria | Aprovação humana da coordenação; não é validação automática do conteúdo por IA. |
| Evidência literal | Linha real do texto-base que contém o termo e é exibida com a fonte. |
| Gabarito | Resposta esperada da questão. |
| Critério de correção | Orientação para avaliar a resposta; diferente do próprio gabarito. |
| BNCC | Código cadastrado de habilidade; a presença do código não comprova alinhamento pedagógico oficial. |
| Determinístico | As mesmas entradas no gerador local produzem o mesmo rascunho, sem chamada a modelo de linguagem. |
| Agregação | Agrupar dados e calcular contagens/percentuais; o painel não precisa guardar métricas duplicadas. |
| Uso | Evento contado pela consulta com evidência ou pelo salvamento da prova, uma vez por fonte correspondente/referenciada. |
| Citação | Referência de um material em uma prova do histórico atual; material repetido na mesma prova conta uma vez no ranking. |

## 4. Persistência, integridade e falhas

| Termo | O que explicar |
| --- | --- |
| Persistência | Dados continuam no disco depois que o processo termina. |
| JSON | Formato de texto para representar objetos e listas; não é um banco relacional. |
| `json.load` / `json.dump` | Leem/gravam objetos Python em um arquivo JSON aberto. |
| `json.loads` / `json.dumps` | Convertem entre string JSON e objetos; o s indica string. |
| UTF-8 | Codificação que representa acentos; `ensure_ascii=False` mantém os caracteres legíveis no JSON. |
| `with open(...)` | Abre o recurso e garante seu fechamento ao sair do bloco, inclusive em erro. |
| Modo `r` | Leitura. |
| Modo `w` | Escrita; pode truncar o arquivo imediatamente. Por isso o projeto prepara temporário antes de substituir dados importantes. |
| Modo `x` | Criação exclusiva; falha se o temporário já existe. Usado como reserva simples da escrita. |
| Temporário `.tmp` | Arquivo preparado antes de publicar a nova versão. Não deve ser apagado sem investigar se há uma operação ativa. |
| `os.replace` | Substitui um arquivo pelo preparado. Uma troca individual não é transação entre todos os JSONs do sistema. |
| Versão esperada | Dados/texto que foram lidos antes da edição. Se a versão atual mudou, o sistema recusa sobrescrever com uma cópia antiga. |
| Concorrência | Duas execuções tentando operar ao mesmo tempo. Há proteção simples de temporário/comparação em algumas operações, não garantias de um banco multiusuário completo. |
| Migração | Adequar registros antigos aos campos novos sem perder IDs/conteúdo e sem conceder aprovação silenciosamente. |
| Validação sintática | Conferir que o JSON pode ser interpretado. |
| Validação dos dados | Conferir tipos, campos obrigatórios, IDs duplicados, permissões e limites depois de interpretar o JSON. |
| Exceção / `raise` | Sinaliza erro para o chamador, diferente de apenas devolver False. |
| `try` / `except` | Tratam os erros previstos e oferecem uma mensagem/recusa compreensível. |
| `finally` | Executa limpeza ao encerrar o bloco, com ou sem erro; não garante recuperação de um processo encerrado à força. |
| `ValueError` | Valor inválido, por exemplo limite zero ou cadastro inconsistente. |
| `PermissionError` | Operação recusada por falta de permissão; é uma especialização de OSError. |
| `FileNotFoundError` | Arquivo ausente; o comportamento depende do módulo. Não diga que todos recriam exemplos. |
| `FileExistsError` | Reserva exclusiva já ocupada ou conflito reportado pelo código de materiais. |
| `OSError` | Família de falhas de arquivo/sistema, como falta de permissão ou erro de escrita. |
| Recuperação de exportação | O par de TXT é preparado antes da troca e possui recuperação para falha detectada ao publicar o segundo; não é garantia contra toda interrupção abrupta. |

**Diferença que o professor pode cobrar:** uma função que imprime e termina sem `return valor` devolve None. Algumas APIs retornam False, outras retornam [] ou None, e outras lançam erro. Cada guia registra o comportamento real; não use “todas devolvem True/False” como resposta genérica.

## 5. Senhas: como explicar sem inventar segurança

| Termo | Explicação |
| --- | --- |
| `getpass` | Lê senha sem exibir os caracteres em terminal interativo. Entrada redirecionada para testes segue outro caminho. |
| Hash de senha | Resumo derivado da senha, guardado em vez do texto original. Não é feito para ser revertido. |
| Salt | Valor aleatório por senha. Ajuda a produzir resultados diferentes para senhas iguais; não é a senha e não precisa ficar secreto. |
| PBKDF2-HMAC-SHA256 | Função da biblioteca padrão que deriva o hash repetindo operações criptográficas. O projeto não implementou sua própria criptografia. |
| Iterações | Repetições que tornam a derivação mais custosa. O cadastro atual usa 600.000. |
| `secrets` | Biblioteca para gerar o salt com aleatoriedade apropriada a esse uso. |
| `hmac.compare_digest` | Faz a comparação do resumo com uma rotina destinada a esse tipo de dado, em vez de comparação comum da senha em texto. |
| Bootstrap / primeiro acesso | Configuração local inicial de uma coordenação já existente. Não é autocadastro público de administrador. |

Resposta sugerida: “Usamos uma rotina de derivação já disponível no Python. Guardamos o resultado, o salt e as iterações; no login recalculamos com a senha digitada. Isso melhora o armazenamento, mas não protege o sistema de alguém que tem acesso para editar os próprios arquivos.”

Limites reais: não há recuperação por e-mail, MFA, bloqueio por tentativas ou servidor de identidade. Alguns caminhos isolados de diagnóstico, como o painel por ID, permanecem no código; não os apresente como equivalentes ao login por senha. Não mostre hashes pessoais no projetor.

## 6. Recursos do código que podem parecer mais avançados

| Recurso | Para que é usado | Como explicar de forma simples |
| --- | --- | --- |
| Compreensão de lista | Construir uma lista filtrada em uma expressão | É uma forma compacta de escrever um for com if; mostre a condição concreta. |
| Expressão geradora | Percorrer valores sem montar outra lista inteira | `sum(1 for ...)` soma 1 para cada registro que atende à condição. |
| `lambda` | Função curta, como chave de ordenação | No ranking, `-usos` coloca o maior primeiro; título/ID resolvem empates. |
| `sort(key=...)` | Ordenação conforme uma regra | Altera a lista em memória; não salva a ordem no JSON por conta própria. |
| `re` / regex | Reconhecer padrões de texto | O gerador separa frases e encontra palavras; não entende o significado do conteúdo. |
| `datetime.strptime` | Interpretar uma data textual | Permite ordenar por data real, sem depender de comparação alfabética de dd/mm/aaaa. |
| `tempfile` | Criar diretórios temporários | Preparação de exportações e dados isolados nos testes. |
| `shutil` | Copiar/remover arquivos e pastas | Cópia de uma versão anterior para recuperação da exportação, ou escola temporária no teste. |
| `hasattr` | Conferir se um objeto/módulo expõe uma função | Compatibilidade entre módulos; não substitui testes de integração nem validação de permissão. |
| `**dicionario` | Expandir campos em outro dicionário ou argumentos nomeados | Aparece em fixtures dos testes; não é necessário para explicar o fluxo de negócio. |
| Classe `unittest.TestCase` | Organiza testes e suas verificações | A aplicação é procedural. A classe é usada pela ferramenta de testes, não como modelo de usuário/prova na aplicação. |

Esses recursos constam do código atual, mas a ementa enviada não confirma que toda essa sintaxe foi ensinada. Se perguntado, explique o objetivo do recurso e que a base do MVP continua sendo função, condição, repetição e arquivo.

## 7. Testes e versionamento

| Termo | Significado |
| --- | --- |
| Teste unitário | Verifica uma função/regra em cenário controlado. |
| Teste de integração | Confere módulos funcionando juntos e seus contratos. |
| Ponta a ponta | Executa o programa pela entrada real e verifica efeitos finais, como TXT e persistência após reinício. |
| Fixture | Dados preparados para um teste, não cadastros reais. |
| Mock / patch | Substituição temporária de uma dependência ou entrada; permite simular teclado, falha de escrita e outros casos. Um teste só com mocks não prova integração real. |
| Assertion / assert | Verificação de que o resultado observado coincide com o esperado. |
| `subprocess` | Inicia outro processo Python; o teste integrado usa main.py real em uma escola temporária. |
| `-B` | Evita escrever cache bytecode durante a execução. |
| Branch | Linha de desenvolvimento, como feat/provas. Não é uma pasta nem impede sozinha interferência entre diretórios de trabalho. |
| Commit | Registro versionado de uma mudança. |
| Fetch | Busca referências remotas, sem misturar automaticamente mudanças no diretório atual. |
| Pull | Busca e integra a branch remota correspondente segundo a estratégia escolhida. |
| Merge | Integra históricos; pode exigir resolução de conflitos. |
| Push | Publica commits no remoto. Não envia automaticamente toda alteração não commitada. |
| main / develop / feat | Nesta equipe: main é a versão consolidada; develop reúne e valida integrações; feat é o trabalho do módulo. Senhas e cadastros pessoais locais ficaram fora do commit. |

## 8. Perguntas gerais: respostas curtas

**“Os quatro CRUDs estão em quatro bancos?”** São quatro blocos funcionais. Usuários, materiais e provas têm coleções JSON; o painel calcula sobre elas. Regras têm um JSON próprio de configuração. Consultas não possuem banco próprio.

**“O sistema usa IA generativa?”** Não no protótipo terminal. Consulta é recuperação literal, e questões são montadas por regras locais.

**“Qual a diferença entre banco de dados e JSON?”** JSON é formato de arquivo. O grupo implementa manualmente leitura, validação, referências e gravação; não possui os recursos de um SGBD relacional.

**“Como preservaram o que já existia?”** Mantivemos IDs e campos antigos, migramos campos novos com padrões explícitos e integramos branches por merge, sem force push. Os testes verificaram cenários de persistência e falha.

**“Se os testes passam, acabou?”** Eles dão confiança nos cenários programados. Novos requisitos, entradas e situações concorrentes podem revelar outros problemas.

**“Qual melhoria faria depois?”** Aperfeiçoar os caminhos de autenticação isolados, tornar a persistência mais adequada a uso simultâneo e ampliar a validação pedagógica. Apresente isso como evolução, não como recurso já implementado.

## 9. O que não dizer na apresentação

- “A senha é criptografada e depois descriptografada.” O código deriva e compara hash.
- “Qualquer pergunta recebe uma resposta.” Só há correspondência textual na base permitida.
- “A IA gera questões alinhadas à BNCC.” Não há IA nem verificação oficial de alinhamento.
- “Temos transações como num banco de dados.” Há proteções de arquivo, com limites.
- “Não há respostas no TXT do aluno em nenhuma hipótese.” Os campos de gabarito são omitidos, mas texto livre pode ter sido escrito inadequadamente pelo próprio autor.
- “Excluir uma prova apaga o gabarito exportado e desfaz o uso.” Os TXT e o contador de eventos permanecem.
- “Toda função verifica senha.” O login autentica; os demais módulos recebem sessão e aplicam verificações específicas.
- “Todos os seis módulos são CRUDs completos separados.” Consultas/exportação são apoio e o painel é agregação.
