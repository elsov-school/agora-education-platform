# CRUD 4 — Painel e menu

Branch: `feat/painel-menu`. Arquivo: `painel.py` e `main.py`.

O painel usa agregações sobre usuários, materiais e atividades; não terá JSON próprio. main.py continua sendo a entrada do programa. Controle de perfil e menus novos estão planejados.

## Funções e comportamento esperado

### `mostrar_resumo()`

Existente: total de materiais e contagem por disciplina e série.

### `contar_atividades_por_professor(atividades)`

Planejado: agrupar avaliações por professor_id.

### `contar_atividades_por_disciplina(atividades)`

Planejado: agrupar avaliações por disciplina.

### `listar_materiais_mais_citados(atividades, materiais)`

Planejado: contar referências por material e ordenar por frequência; consultas só poderão entrar na métrica quando houver registro de uso.

### `listar_materiais_pendentes(materiais)`

Planejado: mostrar fila com status pendente para coordenação.

### `menu_principal()`

Existente em main.py: carregar materiais, direcionar as seis opções e encerrar com 0. Futuro: selecionar usuário e exibir opções por perfil.
