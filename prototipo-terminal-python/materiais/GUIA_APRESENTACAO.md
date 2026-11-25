# Integrante 2 — Biblioteca curricular e aprovação

**Responsabilidade:** CRUD 2 — Biblioteca curricular curada. **Branch de trabalho:** `feat/materiais`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte mantém a fonte de conteúdo do sistema. O professor sugere material, a coordenação revisa e aprova, e só então esse conteúdo pode ser usado nas consultas e nas provas. Também registro autoria e usos sem perder os cadastros antigos.

## 2. Dados e ligação com o restante do sistema

`materiais.json` contém lista de materiais com ID, título, disciplina, série, bimestre, tipo, turma opcional, conteúdo, habilidade, autor, status e usos. `bncc`/`habilidade_bncc` e `conteudo`/`conteudo_texto` são mantidos em pares iguais por compatibilidade. Estados: `pendente` e `aprovado_coordenacao`.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Entre com um professor cuja atribuição seja `6C | 6º ano | Ciências`. Menu do professor → 2: sugira um material; anote o ID.
2. Preencha título Material de demonstração; disciplina 3 (Ciências); série 6º ano; bimestre 1; habilidade DEMO_CIEN; conteúdo com duas frases; tipo 2 (capítulo); turma 6C. O código DEMO_CIEN é fictício, não uma habilidade oficial.
3. Mostre a confirmação pendente. A pesquisa/consulta do professor não deve apresentar a fonte como aprovada ainda.
4. Troque para coordenação (9 e login). Menu → 3: escolha o ID, revise detalhes e confirme com s.
5. Volte ao professor e consulte a biblioteca. Pelo menu 6 → 2, edite um material aprovado de sua autoria e explique a volta para pendente; reprove não existe, apenas não aprovar/manter pendente.
6. Crie uma segunda fonte descartável para mostrar exclusão pela coordenação. Não exclua a que será usada na prova; depois mostre que uma referência em prova bloqueia a exclusão.

## 4. Dicionário completo de funções

**Total neste escopo: 26 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `materiais/materiais.py` | [`materiais_exemplo`](#fn-materiais-materiais_exemplo) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_migrar`](#fn-materiais-_migrar) | Auxiliar interna |
| `materiais/materiais.py` | [`_ler_arquivo`](#fn-materiais-_ler_arquivo) | Auxiliar interna |
| `materiais/materiais.py` | [`_gravar`](#fn-materiais-_gravar) | Auxiliar interna |
| `materiais/materiais.py` | [`carregar_dados`](#fn-materiais-carregar_dados) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_salvar`](#fn-materiais-_salvar) | Auxiliar interna |
| `materiais/materiais.py` | [`salvar_dados`](#fn-materiais-salvar_dados) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`ler_texto`](#fn-materiais-ler_texto) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`escolher_opcao`](#fn-materiais-escolher_opcao) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_autorizado`](#fn-materiais-_autorizado) | Auxiliar interna |
| `materiais/materiais.py` | [`_visiveis`](#fn-materiais-_visiveis) | Auxiliar interna |
| `materiais/materiais.py` | [`_selecionar`](#fn-materiais-_selecionar) | Auxiliar interna |
| `materiais/materiais.py` | [`buscar_material_por_id`](#fn-materiais-buscar_material_por_id) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_ler_campos`](#fn-materiais-_ler_campos) | Auxiliar interna |
| `materiais/materiais.py` | [`adicionar_material`](#fn-materiais-adicionar_material) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_listar`](#fn-materiais-_listar) | Auxiliar interna |
| `materiais/materiais.py` | [`listar_materiais`](#fn-materiais-listar_materiais) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`mostrar_material`](#fn-materiais-mostrar_material) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`visualizar_material`](#fn-materiais-visualizar_material) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_atualizar`](#fn-materiais-_atualizar) | Auxiliar interna |
| `materiais/materiais.py` | [`editar_material`](#fn-materiais-editar_material) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`aprovar_materiais_pendentes`](#fn-materiais-aprovar_materiais_pendentes) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`_pode_excluir`](#fn-materiais-_pode_excluir) | Auxiliar interna |
| `materiais/materiais.py` | [`excluir_material`](#fn-materiais-excluir_material) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`registrar_uso`](#fn-materiais-registrar_uso) | Entrada ou função reutilizável |
| `materiais/materiais.py` | [`gerenciar_materiais`](#fn-materiais-gerenciar_materiais) | Entrada ou função reutilizável |

### Arquivo `materiais/materiais.py`

[Abrir fonte](materiais.py)

<a id="fn-materiais-materiais_exemplo"></a>

#### 01. `materiais_exemplo()`

**Onde está:** [materiais/materiais.py, linha 31](materiais.py#L31).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Devolve quatro dicionários demonstrativos. Não lê nem grava arquivos; os exemplos só são usados na inicialização de arquivo ausente.

**Como apresentar:** Explique que os conteúdos e códigos BNCC dessa base são ilustrativos e não validação pedagógica oficial.

<a id="fn-materiais-_migrar"></a>

#### 02. `_migrar(registros)`

**Onde está:** [materiais/materiais.py, linha 83](materiais.py#L83).

**Entradas:** `registros`: lista de registros recebida/lida.

**O que faz / resultado:** Valida cada material e devolve uma lista de cópias com campos antigos/novos compatíveis. Completa tipo, autoria desconhecida, pendente e usos=0 quando faltam.

**Como apresentar:** Mostre bncc/habilidade_bncc e conteudo/conteudo_texto. Se os pares conflitam, recusa os dados; não escolhe um silenciosamente.

<a id="fn-materiais-_ler_arquivo"></a>

#### 03. `_ler_arquivo()`

**Onde está:** [materiais/materiais.py, linha 118](materiais.py#L118).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê e devolve o texto bruto de materiais.json; ausência devolve None. Não converte para lista.

**Como apresentar:** Diferencie o texto usado para comparar versões dos dicionários usados nas operações.

<a id="fn-materiais-_gravar"></a>

#### 04. `_gravar(novos, esperado)`

**Onde está:** [materiais/materiais.py, linha 126](materiais.py#L126).

**Entradas:** `novos`: lista proposta para gravar; `esperado`: texto/versão que o arquivo tinha quando foi lido.

**O que faz / resultado:** Confere a versão esperada, escreve .tmp exclusivo e usa os.replace; depois atualiza materiais[:] e _texto_lido. Não tem retorno explícito.

**Como apresentar:** Aponte a atualização por fatia: conserva a identidade da lista compartilhada. Não prometa transação entre arquivos diferentes.

<a id="fn-materiais-carregar_dados"></a>

#### 05. `carregar_dados()`

**Onde está:** [materiais/materiais.py, linha 145](materiais.py#L145).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê, converte e migra materiais; inicializa exemplos só se arquivo não existe. Devolve True/False. Lista vazia válida fica vazia; JSON inválido não é sobrescrito.

**Como apresentar:** Mostre o tratamento de erro pelos testes. Atenção: arquivo vazio não é o mesmo que JSON [] e não recebe exemplos automaticamente.

<a id="fn-materiais-_salvar"></a>

#### 06. `_salvar(novos, esperado, usuario=None)`

**Onde está:** [materiais/materiais.py, linha 164](materiais.py#L164).

**Entradas:** `novos`: lista proposta para gravar; `esperado`: texto/versão que o arquivo tinha quando foi lido; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Quando recebe usuário, revalida autorização; valida/migra novos registros e chama _gravar. Devolve True/False e mensagens em caso de erro ou concorrência.

**Como apresentar:** Explique que a gravação pode falhar se o arquivo mudou desde a leitura; a orientação é reler e repetir.

<a id="fn-materiais-salvar_dados"></a>

#### 07. `salvar_dados()`

**Onde está:** [materiais/materiais.py, linha 177](materiais.py#L177).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Compatibilidade interna: salva a lista compartilhada usando a versão _texto_lido; devolve True/False. Não é o ponto público de autorização do menu.

**Como apresentar:** Mostre que operações do usuário usam funções protegidas. Não apresente salvar_dados como uma API de segurança isolada.

<a id="fn-materiais-ler_texto"></a>

#### 08. `ler_texto(pergunta, valor_atual='')`

**Onde está:** [materiais/materiais.py, linha 182](materiais.py#L182).

**Entradas:** `pergunta`: texto exibido ao pedir entrada; `valor_atual`: valor mantido ao pressionar Enter.

**O que faz / resultado:** Repete a pergunta até receber texto não vazio; com valor_atual aceita Enter para manter o valor. Devolve str.

**Como apresentar:** Na edição, deixe o título em branco e explique que esse Enter preserva o valor existente.

<a id="fn-materiais-escolher_opcao"></a>

#### 09. `escolher_opcao(titulo, opcoes, valor_atual='')`

**Onde está:** [materiais/materiais.py, linha 194](materiais.py#L194).

**Entradas:** `titulo`: título da tela ou do material; `opcoes`: sequência de alternativas válidas do menu; `valor_atual`: valor mantido ao pressionar Enter.

**O que faz / resultado:** Enumera opções fixas, lê uma escolha numérica válida e devolve o texto correspondente; permite manter valor atual durante edição.

**Como apresentar:** Mostre as tuplas DISCIPLINAS/BIMESTRES/TIPOS e a conversão de escolha humana 1 para índice Python 0.

<a id="fn-materiais-_autorizado"></a>

#### 10. `_autorizado(usuario, perfis=('professor', 'coordenacao'))`

**Onde está:** [materiais/materiais.py, linha 215](materiais.py#L215).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `perfis`: tupla de perfis autorizados.

**O que faz / resultado:** Verifica formato da sessão e relê ativo/perfil no cadastro; aceita só os perfis indicados. Devolve booleano e trata falhas de leitura.

**Como apresentar:** Explique a recusa a um usuário desativado após entrar. Não diga que esta função faz login ou compara senha: essa etapa está em usuários.

<a id="fn-materiais-_visiveis"></a>

#### 11. `_visiveis(usuario)`

**Onde está:** [materiais/materiais.py, linha 229](materiais.py#L229).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Devolve a biblioteca inteira para coordenação ou usa o filtro de atribuições de usuários para professor; dependência ausente devolve [].

**Como apresentar:** Compare o que a coordenação vê com a biblioteca do professor; o JSON é o mesmo para os dois.

<a id="fn-materiais-_selecionar"></a>

#### 12. `_selecionar(lista, pergunta='ID: ')`

**Onde está:** [materiais/materiais.py, linha 239](materiais.py#L239).

**Entradas:** `lista`: lista de materiais já delimitada; `pergunta`: texto exibido ao pedir entrada.

**O que faz / resultado:** Pede um ID, procura somente dentro da lista recebida e devolve o material ou None; entrada inválida gera mensagem.

**Como apresentar:** Explique que conhecer um ID não permite escapar da lista de materiais visíveis.

<a id="fn-materiais-buscar_material_por_id"></a>

#### 13. `buscar_material_por_id(pergunta='ID: ', usuario=None)`

**Onde está:** [materiais/materiais.py, linha 252](materiais.py#L252).

**Entradas:** `pergunta`: texto exibido ao pedir entrada; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Autoriza o usuário, carrega dados e seleciona dentro de _visiveis; devolve material ou None.

**Como apresentar:** Aponte esta função como entrada para visualizar e editar, com o filtro aplicado antes da busca.

<a id="fn-materiais-_ler_campos"></a>

#### 14. `_ler_campos(atual)`

**Onde está:** [materiais/materiais.py, linha 257](materiais.py#L257).

**Entradas:** `atual`: dicionário dos valores anteriores de um material.

**O que faz / resultado:** Lê título, disciplina, série, bimestre, BNCC, conteúdo, tipo e turma; devolve um dicionário sincronizando campos antigos/novos.

**Como apresentar:** Mostre que a turma é opcional e que - remove turma durante edição; não há extração automática de PDF/upload binário.

<a id="fn-materiais-adicionar_material"></a>

#### 15. `adicionar_material(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 277](materiais.py#L277).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Lê os campos, gera ID, registra autor/usos e salva. Coordenação cria aprovado; professor cria pendente. Devolve True/False.

**Como apresentar:** Faça uma sugestão como professor e mostre que ela ainda depende da coordenação para aparecer em consultas.

<a id="fn-materiais-_listar"></a>

#### 16. `_listar(lista)`

**Onde está:** [materiais/materiais.py, linha 295](materiais.py#L295).

**Entradas:** `lista`: lista de materiais já delimitada.

**O que faz / resultado:** Imprime uma lista resumida com ID, título, disciplina, série e status. Não devolve lista nem grava.

**Como apresentar:** Mostre a listagem e diga que ela é apenas apresentação dos dados já filtrados.

<a id="fn-materiais-listar_materiais"></a>

#### 17. `listar_materiais(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 303](materiais.py#L303).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Autoriza, recarrega e imprime somente materiais visíveis. O efeito é a tela; não retorna a lista.

**Como apresentar:** Use a biblioteca do professor após a aprovação para comprovar o filtro.

<a id="fn-materiais-mostrar_material"></a>

#### 18. `mostrar_material(material)`

**Onde está:** [materiais/materiais.py, linha 308](materiais.py#L308).

**Entradas:** `material`: dicionário de um material.

**O que faz / resultado:** Imprime os detalhes do dicionário, incluindo autoria, status, turma e usos. Não valida sessão por si só nem altera dados.

**Como apresentar:** Mostre os detalhes durante revisão da coordenação; a autorização é feita pelo chamador protegido.

<a id="fn-materiais-visualizar_material"></a>

#### 19. `visualizar_material(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 323](materiais.py#L323).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Busca um material permitido por ID e imprime os detalhes; não grava nem tem retorno explícito.

**Como apresentar:** Abra a opção 1 da biblioteca e acompanhe buscar_material_por_id → mostrar_material.

<a id="fn-materiais-_atualizar"></a>

#### 20. `_atualizar(material, campos, versao, usuario)`

**Onde está:** [materiais/materiais.py, linha 329](materiais.py#L329).

**Entradas:** `material`: dicionário de um material; `campos`: dicionário de alterações a aplicar; `versao`: texto da biblioteca antes da edição; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Cria cópias da lista e do material, aplica os campos e chama _salvar com a versão lida e o usuário; devolve booleano.

**Como apresentar:** Explique a diferença entre preparar a alteração em memória e confirmar a substituição no disco.

<a id="fn-materiais-editar_material"></a>

#### 21. `editar_material(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 337](materiais.py#L337).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Seleciona um material visível; professor só edita se for autor e a edição volta a pendente. Coordenação pode editar. Salva e devolve True/False.

**Como apresentar:** Edite um material de teste já aprovado pelo próprio professor e mostre a necessidade de nova aprovação.

<a id="fn-materiais-aprovar_materiais_pendentes"></a>

#### 22. `aprovar_materiais_pendentes(usuario)`

**Onde está:** [materiais/materiais.py, linha 357](materiais.py#L357).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Só coordenação: lista pendentes, lê ID, mostra detalhes e exige s para aprovar; grava aprovado_coordenacao e devolve booleano.

**Como apresentar:** Aprove a sugestão usada na apresentação e anote o ID para consultas e provas.

<a id="fn-materiais-_pode_excluir"></a>

#### 23. `_pode_excluir(material_id)`

**Onde está:** [materiais/materiais.py, linha 379](materiais.py#L379).

**Entradas:** `material_id`: ID inteiro do material.

**O que faz / resultado:** Lê o histórico de provas e devolve False se o material está referenciado ou se não é possível validar o histórico; não exclui nada.

**Como apresentar:** Mostre a proteção por teste ou tente excluir uma fonte que já gerou prova, sem apagar o histórico.

<a id="fn-materiais-excluir_material"></a>

#### 24. `excluir_material(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 400](materiais.py#L400).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Só coordenação: seleciona material, pede confirmação, verifica referências e grava lista sem ele. Devolve True/False.

**Como apresentar:** Use uma fonte descartável sem referências para excluir; compare com o bloqueio de uma fonte citada em prova.

<a id="fn-materiais-registrar_uso"></a>

#### 25. `registrar_uso(material_id)`

**Onde está:** [materiais/materiais.py, linha 421](materiais.py#L421).

**Entradas:** `material_id`: ID inteiro do material.

**O que faz / resultado:** Recebe ID positivo, relê a biblioteca, soma um e grava; tenta até 8 vezes em conflitos breves. Devolve booleano. Não confere usuário por si só.

**Como apresentar:** Diga que consultas/provas autorizadas chamam esta função. Um uso é evento registrado, não um acesso HTTP nem uma pessoa distinta.

<a id="fn-materiais-gerenciar_materiais"></a>

#### 26. `gerenciar_materiais(usuario=None)`

**Onde está:** [materiais/materiais.py, linha 449](materiais.py#L449).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Mantém o submenu da biblioteca, revalida e recarrega a cada ciclo; opções variam pelo perfil. Encerra com 0 ou perda de autorização.

**Como apresentar:** Mostre visualizar/editar/sugerir no professor e excluir/aprovar na coordenação. Quem usa o sistema não precisa chamar funções manualmente.

## 5. Perguntas técnicas e respostas para ensaiar

### O arquivo é carregado uma única vez?

Não. As operações recarregam para obter a versão atual. Há uma lista compartilhada em memória, mas o JSON é a persistência.

### O que ocorre se o JSON estiver inválido?

A leitura informa falha e não sobrescreve o original. [] é lista vazia válida; arquivo vazio não é um JSON válido.

### Por que materiais[:] = novos?

Atualiza o conteúdo mantendo o mesmo objeto lista. Quem já referencia a lista compartilhada continua vendo os dados atualizados.

### O que é migração aqui?

Completar o formato antigo com novos campos e manter os nomes legados compatíveis. Um material sem aprovação não vira aprovado automaticamente.

### Como funciona uma edição concorrente?

O código compara o texto atual com o esperado e reserva um temporário exclusivo. Se mudou, recusa ou tenta novamente no contador. Isso é proteção simples de arquivo, não banco transacional.

### Upload já lê PDF?

Não. O cadastro atual recebe texto no terminal. Não existe extração automática de documentos neste módulo.

### A aprovação certifica o conteúdo?

Registra a decisão da coordenação. O programa não avalia cientificamente o texto nem verifica o código BNCC em uma base oficial.

## 6. Limites que precisam ser apresentados com honestidade

O material precisa ser digitado/colado como texto. A biblioteca é compartilhada, sem um banco de dados de rede. A exclusão física de material é limitada à coordenação e bloqueada por referências em provas. Chamadas auxiliares internas de persistência não substituem o fluxo autorizado dos menus.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_materiais.py -v
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
