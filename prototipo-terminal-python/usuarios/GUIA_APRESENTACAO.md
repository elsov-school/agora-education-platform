# Integrante 1 — Usuários, login e permissões

**Responsabilidade:** CRUD 1 — Gestão de usuários e perfis. **Branch de trabalho:** `feat/usuarios`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte controla quem entra e o que cada perfil pode fazer. O login usa e-mail e senha; a coordenação administra professores e atribuições. O mesmo filtro de acesso é reutilizado pela biblioteca, pelas consultas e pelas provas.

## 2. Dados e ligação com o restante do sistema

`usuarios.json` é uma lista. Cada pessoa tem `id`, `nome`, `email`, `perfil`, `ativo`, `turmas_lecionadas` e `atribuicoes`. Cada atribuição junta `turma`, `serie` e `disciplina`. Uma conta com senha tem `senha_salt`, `senha_hash` e `senha_iteracoes`; a senha original não é persistida.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Antes da aula, configure a conta local com `py configurar_acesso.py`, se necessário. O e-mail pode ser escolhido; use somente contas de ensaio e não exponha senhas ou hashes.
2. Execute `py main.py`; mostre uma tentativa errada e entre com e-mail e senha da coordenação. IDs não são aceitos como login.
3. Coordenação → 1 → 1: cadastre Docente Demonstração, `docente@example.test`, atribuição `6C | 6º ano | Ciências`, senha e confirmação escolhidas no ensaio. Anote o ID.
4. Gestão → 2 e 3: compare ativos e todos. Opção 4: substitua atribuições e mostre o resultado. Use a opção 6 para demonstrar redefinição somente em uma conta descartável.
5. Volte com 0 e troque de usuário com 9. Entre como o docente e mostre que recebe o menu de professor; o colega de materiais demonstra o filtro por turma.
6. Por último, desative o professor descartável na opção 5 e mostre que não consegue mais entrar. Não desative a única coordenação.

## 4. Dicionário completo de funções

**Total neste escopo: 31 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `usuarios/usuarios.py` | [`ler_senha`](#fn-usuarios-ler_senha) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`preparar_senha`](#fn-usuarios-preparar_senha) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`conferir_senha`](#fn-usuarios-conferir_senha) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`pedir_nova_senha`](#fn-usuarios-pedir_nova_senha) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`normalizar_turmas`](#fn-usuarios-normalizar_turmas) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`preparar_atribuicoes`](#fn-usuarios-preparar_atribuicoes) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`validar_cadastro`](#fn-usuarios-validar_cadastro) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`carregar_usuarios`](#fn-usuarios-carregar_usuarios) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`gerar_novo_id`](#fn-usuarios-gerar_novo_id) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`buscar_usuario`](#fn-usuarios-buscar_usuario) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`usuario_da_sessao`](#fn-usuarios-usuario_da_sessao) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`exigir_coordenacao`](#fn-usuarios-exigir_coordenacao) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`salvar_usuarios`](#fn-usuarios-salvar_usuarios) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`cadastrar_professor`](#fn-usuarios-cadastrar_professor) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`definir_senha`](#fn-usuarios-definir_senha) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`configurar_primeiro_acesso`](#fn-usuarios-configurar_primeiro_acesso) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`listar_professores`](#fn-usuarios-listar_professores) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`atualizar_turmas`](#fn-usuarios-atualizar_turmas) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`desativar_usuario`](#fn-usuarios-desativar_usuario) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`_usuarios_para_acesso`](#fn-usuarios-_usuarios_para_acesso) | Auxiliar interna |
| `usuarios/usuarios.py` | [`verificar_permissao`](#fn-usuarios-verificar_permissao) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`_material_permitido`](#fn-usuarios-_material_permitido) | Auxiliar interna |
| `usuarios/usuarios.py` | [`usuario_pode_acessar_material`](#fn-usuarios-usuario_pode_acessar_material) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`filtrar_materiais_do_professor`](#fn-usuarios-filtrar_materiais_do_professor) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`fazer_login`](#fn-usuarios-fazer_login) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`ler_turmas`](#fn-usuarios-ler_turmas) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`ler_turmas_e_atribuicoes`](#fn-usuarios-ler_turmas_e_atribuicoes) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`ler_id`](#fn-usuarios-ler_id) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`mostrar_professores`](#fn-usuarios-mostrar_professores) | Entrada ou função reutilizável |
| `usuarios/usuarios.py` | [`gerenciar_usuarios`](#fn-usuarios-gerenciar_usuarios) | Entrada ou função reutilizável |
| `configurar_acesso.py` | [`configurar_acesso`](#fn-configurar_acesso-configurar_acesso) | Entrada ou função reutilizável |

### Arquivo `usuarios/usuarios.py`

[Abrir fonte](usuarios.py)

<a id="fn-usuarios-ler_senha"></a>

#### 01. `ler_senha(pergunta='Senha: ')`

**Onde está:** [usuarios/usuarios.py, linha 16](usuarios.py#L16).

**Entradas:** `pergunta`: texto exibido ao pedir entrada.

**O que faz / resultado:** Lê uma senha como texto. No terminal usa getpass, sem ecoar caracteres; em entrada redirecionada usa input para permitir testes.

**Como apresentar:** Mostre a digitação oculta e explique o ramo sys.stdin.isatty(); a senha só fica em memória durante a operação.

<a id="fn-usuarios-preparar_senha"></a>

#### 02. `preparar_senha(senha)`

**Onde está:** [usuarios/usuarios.py, linha 23](usuarios.py#L23).

**Entradas:** `senha`: texto da senha digitada, sem imprimir.

**O que faz / resultado:** Exige pelo menos 8 caracteres e devolve um dicionário com salt aleatório, hash PBKDF2-SHA256 e 600.000 iterações; não grava o JSON.

**Como apresentar:** Mostre o código, sem mostrar a senha real. Explique que senhas iguais podem gerar hashes diferentes por causa do salt.

<a id="fn-usuarios-conferir_senha"></a>

#### 03. `conferir_senha(usuario, senha)`

**Onde está:** [usuarios/usuarios.py, linha 32](usuarios.py#L32).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `senha`: texto da senha digitada, sem imprimir.

**O que faz / resultado:** Deriva o resumo da senha digitada usando o salt e as iterações do cadastro e devolve True ou False por comparação com hmac.compare_digest.

**Como apresentar:** Demonstre login com uma senha incorreta e depois correta. Não diga que a função descriptografa a senha.

<a id="fn-usuarios-pedir_nova_senha"></a>

#### 04. `pedir_nova_senha()`

**Onde está:** [usuarios/usuarios.py, linha 40](usuarios.py#L40).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Solicita a nova senha duas vezes, lança ValueError se forem diferentes e devolve a senha confirmada. O tamanho mínimo é conferido ao preparar o hash.

**Como apresentar:** Na criação de professor, digite duas senhas diferentes para mostrar a recusa sem salvar o cadastro.

<a id="fn-usuarios-normalizar_turmas"></a>

#### 05. `normalizar_turmas(turmas_lecionadas)`

**Onde está:** [usuarios/usuarios.py, linha 59](usuarios.py#L59).

**Entradas:** `turmas_lecionadas`: lista de códigos de turmas.

**O que faz / resultado:** Valida uma lista de códigos, remove espaços externos, converte para maiúsculas e elimina códigos vazios ou repetidos; devolve uma lista.

**Como apresentar:** No código, acompanhe a transformação de [" 6a_cien ", "6A_CIEN", ""] em ["6A_CIEN"].

<a id="fn-usuarios-preparar_atribuicoes"></a>

#### 06. `preparar_atribuicoes(turmas, atribuicoes)`

**Onde está:** [usuarios/usuarios.py, linha 72](usuarios.py#L72).

**Entradas:** `turmas`: códigos já normalizados; `atribuicoes`: lista de turma/série/disciplina; None permite migração dos códigos conhecidos.

**O que faz / resultado:** Devolve atribuições validadas de turma, série e disciplina. Quando recebe None usa o mapa dos códigos antigos conhecidos; lista vazia explícita permanece vazia.

**Como apresentar:** Explique por que 6A_CIEN pode ser migrado, mas um código desconhecido não concede acesso sem atribuição explícita.

<a id="fn-usuarios-validar_cadastro"></a>

#### 07. `validar_cadastro(usuarios)`

**Onde está:** [usuarios/usuarios.py, linha 99](usuarios.py#L99).

**Entradas:** `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista).

**O que faz / resultado:** Valida lista de usuários, IDs, e-mails únicos, perfil, ativo, códigos e formato dos campos de senha. Completa atribuições antigas em memória. Não retorna valor útil; lança ValueError.

**Como apresentar:** Mostre a conferência de IDs repetidos e explique que JSON sintaticamente válido também precisa ter dados coerentes.

<a id="fn-usuarios-carregar_usuarios"></a>

#### 08. `carregar_usuarios()`

**Onde está:** [usuarios/usuarios.py, linha 139](usuarios.py#L139).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê usuarios.json, valida os registros e devolve a lista. Arquivo ausente devolve []; JSON ilegível gera ValueError. A leitura não grava a migração.

**Como apresentar:** Relacione json.load à lista em memória. Use o teste de corrupção, sem estragar o cadastro real.

<a id="fn-usuarios-gerar_novo_id"></a>

#### 09. `gerar_novo_id(usuarios)`

**Onde está:** [usuarios/usuarios.py, linha 152](usuarios.py#L152).

**Entradas:** `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista).

**O que faz / resultado:** Devolve 1 para a lista vazia ou o maior ID existente mais 1. Não preenche lacunas de IDs excluídos.

**Como apresentar:** Use o exemplo de IDs 1, 4 e 7: o próximo é 8, não o tamanho da lista mais 1.

<a id="fn-usuarios-buscar_usuario"></a>

#### 10. `buscar_usuario(usuarios, usuario_id)`

**Onde está:** [usuarios/usuarios.py, linha 158](usuarios.py#L158).

**Entradas:** `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista); `usuario_id`: ID inteiro do cadastro-alvo.

**O que faz / resultado:** Procura um ID inteiro na lista recebida e devolve o dicionário correspondente ou None; não lê arquivo.

**Como apresentar:** Diferencie a busca em memória do carregar_usuarios, que acessa o disco.

<a id="fn-usuarios-usuario_da_sessao"></a>

#### 11. `usuario_da_sessao(usuario, usuarios)`

**Onde está:** [usuarios/usuarios.py, linha 166](usuarios.py#L166).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista).

**O que faz / resultado:** Devolve o cadastro atual se a sessão está ativa e ainda coincide em ID, perfil e hash de senha; caso contrário devolve None.

**Como apresentar:** Explique que uma senha redefinida invalida a sessão antiga neste verificador; atribuições válidas vêm da leitura atual.

<a id="fn-usuarios-exigir_coordenacao"></a>

#### 12. `exigir_coordenacao(usuario, usuarios)`

**Onde está:** [usuarios/usuarios.py, linha 177](usuarios.py#L177).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista).

**O que faz / resultado:** Confere a sessão contra a lista atual e lança PermissionError se não for coordenação ativa. No sucesso não tem retorno explícito.

**Como apresentar:** Mostre que cadastrar_professor chama essa verificação antes de criar dados; esconder uma opção do menu não basta.

<a id="fn-usuarios-salvar_usuarios"></a>

#### 13. `salvar_usuarios(usuarios, usuario=None, anteriores=None)`

**Onde está:** [usuarios/usuarios.py, linha 183](usuarios.py#L183).

**Entradas:** `usuarios`: lista de cadastros (em salvar_usuarios, a nova lista); `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `anteriores`: estado lido anteriormente, usado para detectar alteração concorrente.

**O que faz / resultado:** Exige coordenação, compara o estado anterior quando fornecido, valida a nova lista, grava .tmp em modo exclusivo e substitui usuarios.json com os.replace. Não tem retorno explícito.

**Como apresentar:** Explique a sequência validar → temporário → substituir. A comparação evita sobrescrever uma alteração posterior à leitura.

<a id="fn-usuarios-cadastrar_professor"></a>

#### 14. `cadastrar_professor(nome, email, turmas_lecionadas, usuario=None, atribuicoes=None, senha=None)`

**Onde está:** [usuarios/usuarios.py, linha 207](usuarios.py#L207).

**Entradas:** `nome`: nome do professor ou nome do modelo, conforme a função; `email`: e-mail de login/cadastro; `turmas_lecionadas`: lista de códigos de turmas; `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `atribuicoes`: lista de turma/série/disciplina; None permite migração dos códigos conhecidos; `senha`: texto da senha digitada, sem imprimir.

**O que faz / resultado:** Valida nome/e-mail, prepara atribuições, gera ID e salva professor ativo; se recebeu senha, inclui o hash. Devolve o dicionário criado.

**Como apresentar:** Cadastre pelo menu e mostre a listagem. A API aceita senha=None por compatibilidade, mas essa conta só entra após definir senha.

<a id="fn-usuarios-definir_senha"></a>

#### 15. `definir_senha(usuario_id, senha, usuario=None)`

**Onde está:** [usuarios/usuarios.py, linha 238](usuarios.py#L238).

**Entradas:** `usuario_id`: ID inteiro do cadastro-alvo; `senha`: texto da senha digitada, sem imprimir; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Exige coordenação e usuário-alvo ativo, substitui apenas os campos de senha e devolve o cadastro atualizado; salva com proteção de versão.

**Como apresentar:** Mostre a opção 6 da gestão usando um usuário de teste. Não imprima a senha nem o hash na apresentação.

<a id="fn-usuarios-configurar_primeiro_acesso"></a>

#### 16. `configurar_primeiro_acesso(email, senha, email_atual=None)`

**Onde está:** [usuarios/usuarios.py, linha 253](usuarios.py#L253).

**Entradas:** `email`: e-mail de login/cadastro; `senha`: texto da senha digitada, sem imprimir; `email_atual`: e-mail anterior da coordenação selecionada, quando vai trocá-lo.

**O que faz / resultado:** Inicializa uma coordenação existente enquanto nenhuma coordenação ativa tem senha. Pode atualizar seu e-mail usando email_atual; preserva ID/perfil, grava e devolve a conta.

**Como apresentar:** Apresente como preparação local, não como cadastro público. A repetição é recusada depois da inicialização.

<a id="fn-usuarios-listar_professores"></a>

#### 17. `listar_professores(incluir_inativos=False, usuario=None)`

**Onde está:** [usuarios/usuarios.py, linha 282](usuarios.py#L282).

**Entradas:** `incluir_inativos`: booleano para incluir professores desativados; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Exige coordenação e devolve professores ativos; incluir_inativos=True inclui desativados. Não imprime por conta própria.

**Como apresentar:** Compare opções 2 e 3 do menu e explique o argumento booleano.

<a id="fn-usuarios-atualizar_turmas"></a>

#### 18. `atualizar_turmas(usuario_id, turmas_lecionadas, usuario=None, atribuicoes=None)`

**Onde está:** [usuarios/usuarios.py, linha 292](usuarios.py#L292).

**Entradas:** `usuario_id`: ID inteiro do cadastro-alvo; `turmas_lecionadas`: lista de códigos de turmas; `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `atribuicoes`: lista de turma/série/disciplina; None permite migração dos códigos conhecidos.

**O que faz / resultado:** Exige coordenação, prepara turmas e atribuições, substitui os campos do professor e salva; devolve o cadastro atualizado.

**Como apresentar:** Altere a atribuição de um professor de teste. Não diga que acrescenta automaticamente: a entrada substitui a atribuição anterior.

<a id="fn-usuarios-desativar_usuario"></a>

#### 19. `desativar_usuario(usuario_id, usuario=None)`

**Onde está:** [usuarios/usuarios.py, linha 308](usuarios.py#L308).

**Entradas:** `usuario_id`: ID inteiro do cadastro-alvo; `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Exige coordenação, marca ativo=False e salva, mantendo ID e demais campos. Devolve o registro alterado; recusa alvo ausente ou já inativo.

**Como apresentar:** Desative somente um professor de teste e tente um novo login. Explique por que manter o registro preserva referências das provas.

<a id="fn-usuarios-_usuarios_para_acesso"></a>

#### 20. `_usuarios_para_acesso()`

**Onde está:** [usuarios/usuarios.py, linha 324](usuarios.py#L324).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Auxiliar que lê o cadastro para verificações de acesso; se houver erro de leitura/validação, informa o erro e devolve [].

**Como apresentar:** Diga que, sem conseguir validar o cadastro, o sistema nega o acesso em vez de presumir autorização.

<a id="fn-usuarios-verificar_permissao"></a>

#### 21. `verificar_permissao(usuario_id, acao)`

**Onde está:** [usuarios/usuarios.py, linha 332](usuarios.py#L332).

**Entradas:** `usuario_id`: ID inteiro do cadastro-alvo; `acao`: nome de permissão, como acessar_metricas.

**O que faz / resultado:** Busca o usuário atual e devolve booleano combinando ativo com a ação prevista em PERMISSOES. Recebe ID, não autentica senha.

**Como apresentar:** Mostre a ação acessar_metricas da coordenação. Diferencie essa consulta de permissão do fazer_login.

<a id="fn-usuarios-_material_permitido"></a>

#### 22. `_material_permitido(usuario, material)`

**Onde está:** [usuarios/usuarios.py, linha 337](usuarios.py#L337).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `material`: dicionário de um material.

**O que faz / resultado:** Decide acesso em memória: coordenação vê tudo; professor precisa de material aprovado e correspondência de série/disciplina na mesma atribuição, e turma quando informada.

**Como apresentar:** Use duas atribuições diferentes para explicar que não pode combinar a série de uma com a disciplina da outra.

<a id="fn-usuarios-usuario_pode_acessar_material"></a>

#### 23. `usuario_pode_acessar_material(usuario, material)`

**Onde está:** [usuarios/usuarios.py, linha 363](usuarios.py#L363).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `material`: dicionário de um material.

**O que faz / resultado:** Relê usuários, revalida a sessão e devolve o booleano de acesso a um único material.

**Como apresentar:** Mostre um material de outra turma sendo recusado, ainda que o professor conheça o ID dele.

<a id="fn-usuarios-filtrar_materiais_do_professor"></a>

#### 24. `filtrar_materiais_do_professor(usuario, lista_materiais)`

**Onde está:** [usuarios/usuarios.py, linha 368](usuarios.py#L368).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `lista_materiais`: lista de materiais a filtrar.

**O que faz / resultado:** Relê o cadastro, revalida a sessão e devolve uma nova lista só com os materiais permitidos, preservando a ordem recebida.

**Como apresentar:** Aponte que consultas e provas reutilizam esse filtro; ele não apaga materiais do JSON.

<a id="fn-usuarios-fazer_login"></a>

#### 25. `fazer_login()`

**Onde está:** [usuarios/usuarios.py, linha 377](usuarios.py#L377).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Solicita e-mail e senha, recusa IDs, não lista contas e devolve usuário ativo autenticado ou None ao sair/erro/configuração ausente. Relê a conta após a senha.

**Como apresentar:** Comece a apresentação por aqui: erro de credencial, login válido, menu correto. Use 0 no e-mail para sair.

<a id="fn-usuarios-ler_turmas"></a>

#### 26. `ler_turmas()`

**Onde está:** [usuarios/usuarios.py, linha 409](usuarios.py#L409).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê uma linha e devolve uma lista separando os itens por vírgula; a validação completa ocorre depois.

**Como apresentar:** Mostre a entrada 6A_CIEN, 7B | 7º ano | História e a separação em dois itens.

<a id="fn-usuarios-ler_turmas_e_atribuicoes"></a>

#### 27. `ler_turmas_e_atribuicoes()`

**Onde está:** [usuarios/usuarios.py, linha 414](usuarios.py#L414).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Interpreta códigos conhecidos ou turma | série | disciplina, monta duas listas e as devolve como tupla. Código desconhecido gera aviso sem atribuição automática.

**Como apresentar:** Explique os separadores: vírgula entre turmas, barra vertical entre os três campos de uma atribuição.

<a id="fn-usuarios-ler_id"></a>

#### 28. `ler_id(pergunta)`

**Onde está:** [usuarios/usuarios.py, linha 435](usuarios.py#L435).

**Entradas:** `pergunta`: texto exibido ao pedir entrada.

**O que faz / resultado:** Lê texto, exige dígitos decimais e devolve int; lança ValueError para entrada não numérica. A existência do ID é conferida pela operação seguinte.

**Como apresentar:** Digite letras no campo de ID do professor e mostre que o menu trata o erro.

<a id="fn-usuarios-mostrar_professores"></a>

#### 29. `mostrar_professores(professores)`

**Onde está:** [usuarios/usuarios.py, linha 442](usuarios.py#L442).

**Entradas:** `professores`: lista de professores a exibir.

**O que faz / resultado:** Imprime nome, e-mail, situação, turmas e atribuições da lista recebida. Não salva dados e não tem retorno útil.

**Como apresentar:** Abra a listagem e explique a separação entre obter os dados e mostrá-los.

<a id="fn-usuarios-gerenciar_usuarios"></a>

#### 30. `gerenciar_usuarios(usuario=None)`

**Onde está:** [usuarios/usuarios.py, linha 455](usuarios.py#L455).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Mantém o submenu da coordenação, revalida acesso a cada repetição e encaminha cadastro, listagens, atribuições, desativação e senhas. Retorna ao escolher 0.

**Como apresentar:** Apresente as seis opções, demonstrando em tela as principais e apontando no código o if/elif que chama cada função.

### Arquivo `configurar_acesso.py`

[Abrir fonte](../configurar_acesso.py)

<a id="fn-configurar_acesso-configurar_acesso"></a>

#### 31. `configurar_acesso()`

**Onde está:** [configurar_acesso.py, linha 6](../configurar_acesso.py#L6).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Utilitário de configuração local: seleciona coordenação ativa existente, permite escolher e-mail e senha, chama a inicialização e mostra o resultado. Não cria outra pessoa.

**Como apresentar:** Execute antes do ensaio apenas se ainda não configurou acesso. Se já configurado, explique a recusa, sem apagar senhas para repetir a demonstração.

## 5. Perguntas técnicas e respostas para ensaiar

### Por que desativar em vez de excluir?

As provas guardam professor_id. Manter o cadastro preserva autoria e histórico, enquanto ativo=False bloqueia novas operações.

### É criptografia de senha?

É derivação de hash PBKDF2-SHA256 com salt e iterações. Não há descriptografia; recalculamos e comparamos. Os recursos criptográficos são da biblioteca padrão, não um algoritmo inventado pelo grupo.

### Qual a diferença entre ID e posição na lista?

ID identifica o registro; posição muda se a lista for ordenada ou filtrada. Uma pessoa com ID 7 não precisa estar na posição 7.

### Como um professor é ligado à sua disciplina?

Por uma atribuição completa. A mesma entrada deve combinar série e disciplina; se o material especifica turma, ela também deve coincidir.

### Por que ler o cadastro de novo?

Uma conta pode ter sido desativada, ter mudado de perfil ou de atribuição durante a sessão. Não basta confiar no dicionário antigo.

### O primeiro acesso é um cadastro público?

Não. É um utilitário executado no computador local, antes de existir senha de coordenação ativa, para configurar uma conta já existente. Quem controla os arquivos locais controla o protótipo.

### Por que usar set, casefold e None?

set detecta duplicação; casefold normaliza texto para comparação sem depender de maiúsculas; None representa ausência e é diferente de lista vazia ou False.

## 6. Limites que precisam ser apresentados com honestidade

O login não é um serviço web de identidade: não há recuperação por e-mail, MFA, limite de tentativas ou proteção contra alguém que pode editar o JSON. As sessões são dicionários em memória. Não afirmar que todos os helpers de todos os módulos verificam hash de sessão: alguns revalidam apenas ID, perfil e ativo.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_usuarios.py -v
py -B -m unittest discover -s tests -p test_login.py -v
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
