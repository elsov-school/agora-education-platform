# CRUD 2 — Biblioteca curricular

Branch: `feat/materiais`. Arquivo: `materiais.py`.

Parcialmente implementado em materiais.py. Persistência atual: materiais/materiais.json. Campos atuais: id, titulo, disciplina, serie, bimestre, bncc, conteudo. Evolução prevista: tipo (apostila, capitulo ou plano_aula), habilidade_bncc, conteudo_texto, status_validacao (pendente ou aprovado_coordenacao), autor_upload. A migração de bncc/conteudo e o preenchimento dos novos campos ainda não foram feitos.

## Funções e comportamento esperado

### `materiais_exemplo()`

Existente: devolver quatro materiais ilustrativos.

### `carregar_dados()`

Existente: carregar JSON; inicializar exemplos se ausente ou vazio; recusar JSON inválido.

### `salvar_dados()`

Existente: persistir a lista em UTF-8.

### `ler_texto(pergunta, valor_atual="")`

Existente: solicitar texto obrigatório; permitir manter valor na edição.

### `escolher_opcao(titulo, opcoes, valor_atual="")`

Existente: validar seleção numérica de opções fixas.

### `buscar_material_por_id(pergunta="ID: ")`

Existente: ler ID e localizar material, informando erros.

### `adicionar_material()`

Existente: ler campos, gerar ID e salvar. Futuro: registrar autor, tipo e status pendente.

### `listar_materiais()`

Existente: mostrar ID, título, disciplina e série.

### `mostrar_material(material)`

Existente: mostrar todos os campos atuais.

### `visualizar_material()`

Existente: localizar e exibir material.

### `editar_material()`

Existente: editar campos e salvar. Futuro: validar permissão e definir necessidade de nova aprovação.

### `excluir_material()`

Existente: excluir após confirmação. Futuro: impedir perda de referências em atividades.

### `gerenciar_materiais()`

Existente: submenu de visualização, edição e exclusão.

### `aprovar_material(material_id, coordenador_id)`

Planejado: verificar perfil e aprovar conteúdo pendente.

### `buscar_materiais(habilidade_bncc=None, serie=None)`

Planejado: filtrar por BNCC e/ou série, restringindo professores a materiais aprovados.
