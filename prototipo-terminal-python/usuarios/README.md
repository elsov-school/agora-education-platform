# Usuários e perfis

Branch: `feat/usuarios`. Arquivo: `usuarios.py`.

Planejado. Arquivo reservado para persistência futura: usuarios/usuarios.json. Campos: id, nome, email, perfil (coordenacao ou professor), turmas_lecionadas e ativo. O campo ativo permite desativação sem apagar o histórico.

## Funções e comportamento esperado

### `cadastrar_professor(nome, email, turmas_lecionadas)`

Validar nome e email único, gerar ID e salvar professor ativo.

### `listar_professores(incluir_inativos=False)`

Listar corpo docente e suas turmas; omitir inativos por padrão.

### `atualizar_turmas(usuario_id, turmas_lecionadas)`

Substituir atribuições de turmas de um professor existente.

### `desativar_usuario(usuario_id)`

Marcar usuário como inativo, preservando referências das provas.

### `verificar_permissao(usuario_id, acao)`

Conferir perfil e estado ativo. Coordenação gerencia usuários, aprova materiais e acessa métricas; professores acessam conteúdos aprovados e suas atividades.

O JSON desta pasta começa com uma lista vazia (`[]`). As operações planejadas ainda não o utilizam.

## Trabalho integrado do remoto

Esta branch preserva carregar_usuarios(), salvar_usuarios(), gerar_novo_id() e cadastrar_usuario(), além dos três usuários de demonstração já cadastrados. O JSON é lido na pasta deste módulo. As demais funções do contrato seguem planejadas.
