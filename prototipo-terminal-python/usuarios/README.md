# Usuários e perfis

## Entrega contrato v1

O módulo identifica quem está usando o terminal, mantém o cadastro docente e decide quais materiais a pessoa pode abrir. O login é demonstrativo, por ID ou e-mail, sem senha. Na base inicial, o ID 1 pertence à coordenação, o ID 2 a uma professora ativa e o ID 3 a um professor inativo.

### Uso no terminal

A partir de `prototipo-terminal-python`, execute `py -m usuarios.usuarios` para abrir o login e a gestão isolada. Digite `0` no login para sair. No menu de coordenação, a opção 1 cadastra um professor e a opção 4 substitui suas turmas e atribuições. Separe as turmas por vírgula. Por exemplo, a entrada `6A_CIEN, 8B | 8º ano | História` dá acesso a Ciências do 6º ano na 6A e a História do 8º ano na 8B. Para retirar todas as atribuições, deixe a entrada vazia na opção 4.

### Cadastro e permissões

`usuarios.json` mantém o ID, nome, e-mail, perfil, situação e os códigos de `turmas_lecionadas`. Cada item de `atribuicoes` contém `turma`, `serie` e `disciplina`. A desativação mantém a pessoa e o ID no arquivo para preservar o histórico de provas.

| Código antigo | Turma | Série | Disciplina |
| --- | --- | --- | --- |
| 6A_CIEN | 6A | 6º ano | Ciências |
| 7B_CIEN | 7B | 7º ano | Ciências |
| 8A_MAT | 8A | 8º ano | Matemática |
| 9A_MAT | 9A | 9º ano | Matemática |

A leitura de um registro antigo sem `atribuicoes` usa esta tabela. Outros códigos permanecem no cadastro e dependem de a coordenação preencher a atribuição completa pela opção 4. Uma lista explícita de atribuições vazia mantém o professor sem acesso a materiais.

| Função em `usuarios.usuarios` | Comportamento |
| --- | --- |
| `fazer_login()` | Retorna o dicionário do usuário ativo. Aceita ID ou e-mail. Uma tentativa inválida permite tentar novamente. A opção 0 ou um erro de leitura encerra o login com `None`. |
| `gerenciar_usuarios(usuario=None)` | Abre o menu para a coordenação ativa. |
| `cadastrar_professor(nome, email, turmas_lecionadas, usuario=None, atribuicoes=None)` | Valida nome e e-mail único, gera o próximo ID e retorna o professor salvo. |
| `listar_professores(incluir_inativos=False, usuario=None)` | Retorna os docentes e suas atribuições. |
| `atualizar_turmas(usuario_id, turmas_lecionadas, usuario=None, atribuicoes=None)` | Substitui as turmas e atribuições do professor escolhido. |
| `desativar_usuario(usuario_id, usuario=None)` | Marca o cadastro como inativo e devolve o registro atualizado. |
| `verificar_permissao(usuario_id, acao)` | Consulta o cadastro atual e as ações previstas em `PERMISSOES`. |
| `usuario_pode_acessar_material(usuario, material)` | Retorna um booleano para um material. |
| `filtrar_materiais_do_professor(usuario, lista_materiais)` | Retorna os materiais permitidos na ordem de entrada. |

Nas chamadas de gestão, passe em `usuario` o dicionário devolvido pelo login da coordenação. As operações diretas de cadastro, listagem, atualização e desativação lançam `PermissionError` quando a sessão não tem permissão. As operações de gestão e os filtros consultam o cadastro atual para respeitar a desativação ou troca de atribuições durante a sessão.

A coordenação ativa vê todos os materiais. Para o professor, o filtro exige `status_validacao` igual a `aprovado_coordenacao` e correspondência de série e disciplina na **mesma** atribuição. Se o material informar a turma, ela também precisa coincidir. Um material sem turma abrange o par série e disciplina. A comparação ignora maiúsculas e espaços nas extremidades e conserva os acentos.

### Persistência e testes

A leitura de JSON inválido informa erro e preserva o arquivo. A gravação usa `usuarios.json.tmp` na mesma pasta e substitui o cadastro quando o conteúdo está completo. Se o processo for encerrado à força durante a gravação, poderá restar um temporário. Nesse caso, feche as instâncias do terminal e confira o cadastro e o temporário antes de remover o temporário para retomar as gravações.

A partir de `prototipo-terminal-python`, execute:

```powershell
py -m unittest discover -s tests -p test_usuarios.py -v
```

Os testes exercitam o login, o menu de cadastro, as operações diretas, os códigos antigos, o filtro de materiais e a recuperação de falhas de gravação. Usam um JSON em uma pasta temporária.
