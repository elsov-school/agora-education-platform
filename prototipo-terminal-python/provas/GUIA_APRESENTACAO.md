# Integrante 4 — Geração, revisão e CRUD de provas

**Responsabilidade:** CRUD 3 — Banco de provas e atividades. **Branch de trabalho:** `feat/provas`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte transforma o material aprovado em um rascunho de avaliação por regras locais. O professor escolhe tipo, dificuldade e quantidade, revisa e salva. Eu preservo autoria, histórico e referências e encaminho a prova salva para o colega que faz a exportação.

## 2. Dados e ligação com o restante do sistema

`atividades.json` é o banco único de provas. Cada registro tem id, professor_id, série, disciplina, bimestre, materiais_referenciados, questões, data_criacao e modelo_padrao. Cada questão tem enunciado, tipo, dificuldade, gabarito e criterio_correcao; múltipla escolha também tem alternativas.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Entre com professor ativo e fonte aprovada da sua atribuição. Menu do professor → 4: selecione o ID da fonte.
2. Escolha tipo 2 (discursiva), dificuldade 1 (fácil) e quantidade 1 para um primeiro ensaio. Explique que o limite é o menor entre regras da escola e trechos elegíveis.
3. Na revisão, escolha 2, questão 1, altere o enunciado e mantenha os demais campos com Enter. Depois escolha 1 para aprovar e salvar. Anote o ID da prova.
4. Menu do professor → 5 → 2: consulte o histórico. Depois opção 3 para editar uma questão salva. A tela usa números a partir de 1; a função recebe índice a partir de 0.
5. No mesmo submenu, opção 5 e ID da prova: exporte e passe a palavra ao responsável por padrões, que abre os dois arquivos.
6. Use uma segunda conta com a mesma atribuição para tentar acessar a prova do primeiro autor: não deve obter permissão. Exclua só uma prova descartável na opção 4, com s.
7. Se houver tempo, repita a geração escolhendo tipo 1 e tipo 3 para mostrar múltipla escolha e verdadeiro/falso. Não diga que são questões geradas por uma IA.

## 4. Dicionário completo de funções

**Total neste escopo: 25 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `provas/provas.py` | [`_ler_atividades`](#fn-provas-_ler_atividades) | Auxiliar interna |
| `provas/provas.py` | [`_gravar_atividades`](#fn-provas-_gravar_atividades) | Auxiliar interna |
| `provas/provas.py` | [`_usuario_ativo`](#fn-provas-_usuario_ativo) | Auxiliar interna |
| `provas/provas.py` | [`verificar_autoria`](#fn-provas-verificar_autoria) | Entrada ou função reutilizável |
| `provas/provas.py` | [`_atividade_permitida`](#fn-provas-_atividade_permitida) | Auxiliar interna |
| `provas/provas.py` | [`_materiais_aprovados`](#fn-provas-_materiais_aprovados) | Auxiliar interna |
| `provas/provas.py` | [`_limite_questoes`](#fn-provas-_limite_questoes) | Auxiliar interna |
| `provas/provas.py` | [`_referencias_permitidas`](#fn-provas-_referencias_permitidas) | Auxiliar interna |
| `provas/provas.py` | [`salvar_prova`](#fn-provas-salvar_prova) | Entrada ou função reutilizável |
| `provas/provas.py` | [`gerar_prova`](#fn-provas-gerar_prova) | Entrada ou função reutilizável |
| `provas/provas.py` | [`gerar_atividade`](#fn-provas-gerar_atividade) | Entrada ou função reutilizável |
| `provas/provas.py` | [`_ordem_criacao`](#fn-provas-_ordem_criacao) | Auxiliar interna |
| `provas/provas.py` | [`listar_historico`](#fn-provas-listar_historico) | Entrada ou função reutilizável |
| `provas/provas.py` | [`editar_questao`](#fn-provas-editar_questao) | Entrada ou função reutilizável |
| `provas/provas.py` | [`excluir_prova`](#fn-provas-excluir_prova) | Entrada ou função reutilizável |
| `provas/provas.py` | [`exportar_prova`](#fn-provas-exportar_prova) | Entrada ou função reutilizável |
| `provas/provas.py` | [`_editar_no_menu`](#fn-provas-_editar_no_menu) | Auxiliar interna |
| `provas/provas.py` | [`gerenciar_provas`](#fn-provas-gerenciar_provas) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`questoes_do_material`](#fn-geracao-questoes_do_material) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`montar_questao`](#fn-geracao-montar_questao) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`questao_valida`](#fn-geracao-questao_valida) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`ler_numero`](#fn-geracao-ler_numero) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`mostrar_questao`](#fn-geracao-mostrar_questao) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`revisar_questao`](#fn-geracao-revisar_questao) | Entrada ou função reutilizável |
| `provas/geracao.py` | [`editar_prova_gerada`](#fn-geracao-editar_prova_gerada) | Entrada ou função reutilizável |

### Arquivo `provas/provas.py`

[Abrir fonte](provas.py)

<a id="fn-provas-_ler_atividades"></a>

#### 01. `_ler_atividades()`

**Onde está:** [provas/provas.py, linha 18](provas.py#L18).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê e valida o histórico: lista, IDs, autoria e campos das questões. Devolve lista ou None em erro, sem recriar/limpar arquivo inválido.

**Como apresentar:** Diferencie lista vazia legítima de None, que sinaliza que não é seguro continuar a gravação.

<a id="fn-provas-_gravar_atividades"></a>

#### 02. `_gravar_atividades(anteriores, novas)`

**Onde está:** [provas/provas.py, linha 50](provas.py#L50).

**Entradas:** `anteriores`: estado lido anteriormente, usado para detectar alteração concorrente; `novas`: nova lista de provas proposta para gravar.

**O que faz / resultado:** Reserva .tmp exclusivo, compara o histórico atual com anteriores, grava e substitui por os.replace; limpa temporário em falhas e devolve booleano.

**Como apresentar:** Mostre o teste de edição concorrente: uma revisão antiga não pode apagar uma alteração recém-gravada.

<a id="fn-provas-_usuario_ativo"></a>

#### 03. `_usuario_ativo(usuario)`

**Onde está:** [provas/provas.py, linha 82](provas.py#L82).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Relê o cadastro e devolve a conta atual se ID, ativo e perfil combinam com a sessão; caso contrário informa falha e devolve None.

**Como apresentar:** Aponte o controle em cada operação de prova. Esta função não pede senha; o login ocorreu no módulo usuários.

<a id="fn-provas-verificar_autoria"></a>

#### 04. `verificar_autoria(atividade, professor_id)`

**Onde está:** [provas/provas.py, linha 95](provas.py#L95).

**Entradas:** `atividade`: dicionário de prova/atividade; `professor_id`: ID do autor; não substitui uma sessão autenticada.

**O que faz / resultado:** Compara professor_id da prova com o ID informado e devolve booleano. Sozinha não autentica usuário nem lê cadastro.

**Como apresentar:** Explique a relação entre a referência professor_id e o id do cadastro de usuários.

<a id="fn-provas-_atividade_permitida"></a>

#### 05. `_atividade_permitida(registros, atividade_id, usuario)`

**Onde está:** [provas/provas.py, linha 99](provas.py#L99).

**Entradas:** `registros`: lista de registros recebida/lida; `atividade_id`: ID da prova salva; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Busca a prova na lista e devolve seu dicionário se pertence ao professor ou a sessão é da coordenação; em ausência/recusa devolve None.

**Como apresentar:** Tente exportar uma prova de outro professor e mostre que conhecer seu ID não autoriza acesso.

<a id="fn-provas-_materiais_aprovados"></a>

#### 06. `_materiais_aprovados(usuario)`

**Onde está:** [provas/provas.py, linha 111](provas.py#L111).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Carrega materiais, usa o filtro compartilhado e restringe a aprovados; devolve lista, ou [] se há erro/dependência indisponível.

**Como apresentar:** Aponte a mesma política usada em consultas; o gerador não escolhe fonte fora das atribuições do professor.

<a id="fn-provas-_limite_questoes"></a>

#### 07. `_limite_questoes()`

**Onde está:** [provas/provas.py, linha 125](provas.py#L125).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê max_questoes das regras, exige inteiro positivo e devolve o limite; retorna 0 e aviso quando a configuração falha.

**Como apresentar:** Mostre que uma configuração inválida bloqueia a geração em vez de usar um limite inventado.

<a id="fn-provas-_referencias_permitidas"></a>

#### 08. `_referencias_permitidas(dados, usuario)`

**Onde está:** [provas/provas.py, linha 139](provas.py#L139).

**Entradas:** `dados`: dicionário da prova em preparação; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Valida IDs de materiais contra fontes aprovadas acessíveis e exige série/disciplina/bimestre iguais aos da prova; elimina repetições. Devolve lista de IDs ou [].

**Como apresentar:** Explique que a fonte é conferida novamente antes de salvar, não só quando aparece na seleção.

<a id="fn-provas-salvar_prova"></a>

#### 09. `salvar_prova(professor_id, dados_prova, usuario=None)`

**Onde está:** [provas/provas.py, linha 160](provas.py#L160).

**Entradas:** `professor_id`: ID do autor; não substitui uma sessão autenticada; `dados_prova`: dicionário de prova/rascunho; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Valida sessão/autoria, campos, modelo, questões e fontes; gera ID/data e grava. Depois registra um uso por material. Devolve prova salva ou None.

**Como apresentar:** Mostre ID/data no histórico e explique que falha do contador gera aviso, mas não apaga uma prova que já foi salva.

<a id="fn-provas-gerar_prova"></a>

#### 10. `gerar_prova(usuario)`

**Onde está:** [provas/provas.py, linha 215](provas.py#L215).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Conduz seleção de material, tipo, dificuldade, quantidade e revisão; limita ao menor valor entre trechos elegíveis e regra escolar. Devolve prova salva ou None.

**Como apresentar:** Gere uma questão, tente quantidade maior que a permitida e aprove o rascunho. O conteúdo é montado por regras locais, sem IA.

<a id="fn-provas-gerar_atividade"></a>

#### 11. `gerar_atividade(usuario=None)`

**Onde está:** [provas/provas.py, linha 268](provas.py#L268).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Mantém a entrada antiga e devolve o resultado de gerar_prova(usuario), sem uma implementação paralela.

**Como apresentar:** Se o professor perguntar sobre código legado, mostre que esta função é um adaptador simples.

<a id="fn-provas-_ordem_criacao"></a>

#### 12. `_ordem_criacao(atividade)`

**Onde está:** [provas/provas.py, linha 273](provas.py#L273).

**Entradas:** `atividade`: dicionário de prova/atividade.

**O que faz / resultado:** Converte a data do histórico para datetime e devolve (data, id); datas ausentes/inválidas recebem datetime.min.

**Como apresentar:** Explique o desempate pelo ID quando duas provas foram criadas no mesmo minuto.

<a id="fn-provas-listar_historico"></a>

#### 13. `listar_historico(professor_id=None, usuario=None)`

**Onde está:** [provas/provas.py, linha 281](provas.py#L281).

**Entradas:** `professor_id`: ID do autor; não substitui uma sessão autenticada; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Autoriza e devolve/exibe provas da mais recente para a mais antiga. Professor só vê as próprias; coordenação pode filtrar autor ou ver todas; erro/ausência devolve [].

**Como apresentar:** Abra Histórico, aponte autoria e ordenação e compare a visualização de um segundo professor.

<a id="fn-provas-editar_questao"></a>

#### 14. `editar_questao(professor_id, atividade_id, indice_questao, dados_questao, usuario=None, prova_anterior=None)`

**Onde está:** [provas/provas.py, linha 303](provas.py#L303).

**Entradas:** `professor_id`: ID do autor; não substitui uma sessão autenticada; `atividade_id`: ID da prova salva; `indice_questao`: posição Python da questão, começando em 0; `dados_questao`: dicionário completo da nova questão; `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `prova_anterior`: versão da prova antes da revisão, para detectar conflito.

**O que faz / resultado:** Confere autoria, versão anterior opcional, índice e formato; substitui uma questão e grava. Devolve True/False, sem incrementar usos.

**Como apresentar:** Mostre que o número humano 1 corresponde ao índice 0 e que as demais questões permanecem iguais.

<a id="fn-provas-excluir_prova"></a>

#### 15. `excluir_prova(atividade_id, professor_id, usuario=None)`

**Onde está:** [provas/provas.py, linha 330](provas.py#L330).

**Entradas:** `atividade_id`: ID da prova salva; `professor_id`: ID do autor; não substitui uma sessão autenticada; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Autoriza, pede s, revalida usuário antes de gravar e remove a prova do histórico. Devolve booleano; não apaga materiais nem exportações antigas.

**Como apresentar:** Exclua só uma prova descartável depois de apresentar painel/exportação. O contador de usos não é decrementado.

<a id="fn-provas-exportar_prova"></a>

#### 16. `exportar_prova(atividade_id, usuario)`

**Onde está:** [provas/provas.py, linha 352](provas.py#L352).

**Entradas:** `atividade_id`: ID da prova salva; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Autoriza o acesso por ID, carrega a prova salva e chama padroes.exportar_prova_formatada; devolve dois caminhos ou [] em falha.

**Como apresentar:** Diferencie a autorização aqui da formatação no módulo padrões; não recria as questões na exportação.

<a id="fn-provas-_editar_no_menu"></a>

#### 17. `_editar_no_menu(atividade_id, usuario)`

**Onde está:** [provas/provas.py, linha 369](provas.py#L369).

**Entradas:** `atividade_id`: ID da prova salva; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Seleciona uma prova permitida, exibe questões, lê número humano e encaminha a revisão para editar_questao com a versão original.

**Como apresentar:** Mostre a passagem numero - 1 e prova_anterior; o usuário do terminal não informa índices Python.

<a id="fn-provas-gerenciar_provas"></a>

#### 18. `gerenciar_provas(usuario)`

**Onde está:** [provas/provas.py, linha 384](provas.py#L384).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Mantém submenu de gerar/histórico/editar/excluir/exportar e revalida a sessão no laço; 0 retorna ao menu de perfil.

**Como apresentar:** Apresente as cinco opções em ordem e evite apagar a prova antes de mostrar sua exportação e suas métricas.

### Arquivo `provas/geracao.py`

[Abrir fonte](geracao.py)

<a id="fn-geracao-questoes_do_material"></a>

#### 19. `questoes_do_material(material, tipo, dificuldade)`

**Onde está:** [provas/geracao.py, linha 9](geracao.py#L9).

**Entradas:** `material`: dicionário de um material; `tipo`: identificador do tipo de questão; `dificuldade`: facil, media ou dificil.

**O que faz / resultado:** Separa o texto por fim de frase/quebra de linha, descarta trechos normalizados repetidos e monta questões elegíveis; devolve lista.

**Como apresentar:** Explique o import re e que cada trecho elegível produz no máximo uma questão; texto curto pode limitar a quantidade.

<a id="fn-geracao-montar_questao"></a>

#### 20. `montar_questao(trecho, titulo, numero, tipo, dificuldade, indice)`

**Onde está:** [provas/geracao.py, linha 28](geracao.py#L28).

**Entradas:** `trecho`: frase/linha extraída do texto-base; `titulo`: título da tela ou do material; `numero`: número de exibição, iniciando em 1; `tipo`: identificador do tipo de questão; `dificuldade`: facil, media ou dificil; `indice`: posição da questão gerada, iniciando em 0.

**O que faz / resultado:** Usa palavras do trecho para montar um dicionário de questão ou None se o trecho tem menos de duas palavras. Dificuldade altera pistas/alternativas.

**Como apresentar:** Discursiva: paráfrase de trecho; múltipla escolha: completar lacuna; V/F: conferir palavra do original. Não prometa níveis pedagógicos validados.

<a id="fn-geracao-questao_valida"></a>

#### 21. `questao_valida(questao)`

**Onde está:** [provas/geracao.py, linha 87](geracao.py#L87).

**Entradas:** `questao`: dicionário de uma questão.

**O que faz / resultado:** Devolve booleano validando campos, tipo e dificuldade; múltipla escolha exige alternativas distintas e gabarito presente; V/F exige resposta reconhecida.

**Como apresentar:** Mostre no teste a recusa de alternativas duplicadas ou resposta que não pertence às opções.

<a id="fn-geracao-ler_numero"></a>

#### 22. `ler_numero(pergunta)`

**Onde está:** [provas/geracao.py, linha 111](geracao.py#L111).

**Entradas:** `pergunta`: texto exibido ao pedir entrada.

**O que faz / resultado:** Lê e converte para int; entrada inválida imprime aviso e devolve None. Os limites são validados pelo chamador.

**Como apresentar:** Digite letras na quantidade e explique por que o programa não encerra com erro de conversão.

<a id="fn-geracao-mostrar_questao"></a>

#### 23. `mostrar_questao(numero, questao)`

**Onde está:** [provas/geracao.py, linha 119](geracao.py#L119).

**Entradas:** `numero`: número de exibição, iniciando em 1; `questao`: dicionário de uma questão.

**O que faz / resultado:** Imprime enunciado, tipo, dificuldade, alternativas, gabarito e critério para revisão do professor; não gera arquivo nem salva.

**Como apresentar:** Explique que mostrar respostas na revisão é correto; elas são omitidas apenas na versão exportada para o aluno.

<a id="fn-geracao-revisar_questao"></a>

#### 24. `revisar_questao(questao)`

**Onde está:** [provas/geracao.py, linha 128](geracao.py#L128).

**Entradas:** `questao`: dicionário de uma questão.

**O que faz / resultado:** Copia a questão, permite editar enunciado/alternativas/gabarito/critério, mantém campos em branco e devolve edição válida ou None.

**Como apresentar:** Mude o enunciado e mantenha os outros campos com Enter. Tipo e dificuldade não são alterados nesta tela.

<a id="fn-geracao-editar_prova_gerada"></a>

#### 25. `editar_prova_gerada(prova)`

**Onde está:** [provas/geracao.py, linha 147](geracao.py#L147).

**Entradas:** `prova`: dicionário de prova salva ou rascunho conforme a função.

**O que faz / resultado:** Copia o rascunho e repete a revisão; devolve prova aprovada em memória ou None ao descartar. Não escreve JSON.

**Como apresentar:** Mostre as opções aprovar/editar/descartar e explique que só salvar_prova confirma a persistência.

## 5. Perguntas técnicas e respostas para ensaiar

### A dificuldade é inteligente?

Não. Ela altera regras de pistas e quantidade de alternativas. É um nível operacional do protótipo, não uma classificação pedagógica validada.

### Como a questão é construída?

Expressões regulares separam frases e localizam palavras. Discursivas pedem paráfrase; múltipla escolha completa lacuna; V/F compara uma palavra com o original.

### Por que separar geracao.py?

Ele concentra montagem e revisão do rascunho, enquanto provas.py cuida de autorização, persistência e menu. São módulos de funções, não camadas de classes.

### O que impede repetir infinitas questões?

Trechos normalizados repetidos são ignorados, trechos sem palavras suficientes são descartados e a quantidade solicitada respeita o limite disponível.

### O ID é len(lista)+1?

Não. É o maior ID presente mais 1, para evitar colisão ao remover um registro intermediário. Não é garantia de sequência eternamente crescente se o maior registro for apagado.

### Por que reler fonte antes de salvar?

O material pode ter mudado de aprovação ou permissão após a seleção. A prova só é criada com referências válidas no momento da validação.

### Deletar prova desfaz o uso?

Não. usos conta eventos realizados, não apenas referências atuais. O ranking de citações do histórico pode mudar ao excluir; o contador cumulativo não é decrementado.

### E a BNCC?

O material mantém um código cadastrado. O gerador não consulta uma base oficial nem certifica que a questão cobre a habilidade.

## 6. Limites que precisam ser apresentados com honestidade

A geração é determinística e de leitura, sem IA. O aluno precisa ter acesso ao material para responder certas tarefas. Revisão humana é necessária. A prova usa as regras atuais ao exportar e não congela uma cópia completa das regras escolares. Exclusão da prova não apaga TXT já exportado.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_provas.py -v
```

Para a suíte inteira: `py -B -m unittest discover -s tests -v`. A última verificação de código anterior a estes guias teve **77 testes aprovados**; a quantidade pode mudar em novas versões. Os testes usam dados temporários, não os cadastros pessoais da apresentação.

## 8. Checklist do integrante

- [ ] Sei resumir meu módulo sem ler o código inteiro.
- [ ] Sei apontar a função chamada pelo menu e as auxiliares que ela usa.
- [ ] Sei explicar os argumentos, o retorno e onde ocorre a gravação.
- [ ] Tenho uma conta e dados de ensaio; anotei os IDs reais produzidos, sem presumir que serão 1 ou 4.
- [ ] Demonstro um caso válido e um inválido sem corromper dados ou apagar a única coordenação.
- [ ] Sei qual parte do fluxo pertence ao colega e não atribuo a mim funções de outro módulo.
- [ ] Sei reconhecer os limites descritos acima sem prometer funcionalidades ausentes.
