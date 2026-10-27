# CRUD 3 — Provas e atividades

Branch: `feat/provas`. Arquivo: `provas.py`.

Somente a geração demonstrativa existe. Persistência futura: dados/atividades.json. Campos: id, professor_id, serie, disciplina, bimestre, materiais_referenciados, questoes, data_criacao, modelo_padrao. Cada questão terá enunciado, tipo, dificuldade, gabarito e criterio_correcao. Modelo inicial previsto: institucional_v1.

## Funções e comportamento esperado

### `gerar_atividade()`

Existente: exibir quatro perguntas fixas sobre um material; não salva prova nem produz gabarito.

### `salvar_prova(professor_id, dados_prova)`

Planejado: validar campos e referências, gerar ID/data e persistir a avaliação.

### `editar_questao(atividade_id, indice_questao, dados_questao)`

Planejado: atualizar ou substituir questão, gabarito e critério; validar autoria e índice.

### `listar_historico(professor_id)`

Planejado: listar avaliações do professor por data.

### `excluir_prova(atividade_id, professor_id)`

Planejado: remover avaliação após confirmar autoria e exclusão.

### `exportar_prova(atividade_id, destino)`

Planejado: encaminhar avaliação e padrão institucional ao módulo padroes, retornando caminho gerado.
