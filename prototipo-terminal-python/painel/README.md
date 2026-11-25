# CRUD 4 — Painel da Coordenação & Métricas

Branch: `feat/painel-menu`. Arquivos: `painel.py` e `main.py` (opção 7). Responsáveis: Paulo e Leo.

O painel não tem JSON próprio: todas as métricas são consultas e agregações feitas, **somente leitura**, sobre os outros CRUDs.

| Fonte | CRUD | Uso no painel |
| --- | --- | --- |
| `usuarios/usuarios.json` | 1 — Usuários | nomes dos professores e permissão `acessar_metricas` |
| `materiais/materiais.json` | 2 — Materiais | títulos e `status_validacao` |
| `provas/atividades.json` | 3 — Provas | `professor_id`, `disciplina` e `materiais_referenciados` |

O acesso é restrito à coordenação: o menu pede o ID do usuário e usa `verificar_permissao(usuario_id, "acessar_metricas")` do CRUD 1. Nos dados de demonstração, o ID 1 (Paula Mendes) é da coordenação.

## Como executar

Na pasta `prototipo-terminal-python`:

- Programa completo: `py main.py` (Windows) ou `python3 main.py` → opção **7 - Painel da coordenação**.
- Só o painel: `py -m painel.painel` ou `python3 -m painel.painel`.
- Testes: `py -m unittest painel.teste_painel` ou `python3 -m unittest painel.teste_painel`.

## Funções e comportamento

### `contar_atividades_por_professor(atividades)`

Implementado. Agrupa as atividades por `professor_id` e devolve um dicionário `{professor_id: total}`. Na tela, os IDs viram nomes; professores ativos sem atividades aparecem com 0, e professores desativados continuam contando, marcados como "(inativo)", porque o histórico é preservado.

### `contar_atividades_por_disciplina(atividades)`

Implementado. Agrupa as atividades por disciplina e devolve `{disciplina: total}`. A tela mostra o total e o percentual de cada disciplina, do maior para o menor.

### `listar_materiais_mais_citados(atividades, materiais)`

Implementado. Conta em quantas atividades cada material aparece em `materiais_referenciados` e devolve uma lista de tuplas `(material_id, titulo, total)`, da mais citada para a menos citada; empates ficam em ordem alfabética. Um material repetido na mesma atividade conta uma única vez. Uma referência a um material que foi excluído aparece como "(material removido da biblioteca)". As consultas só vão entrar nesta métrica quando o módulo de consultas passar a registrar o uso.

### `listar_materiais_pendentes(materiais)`

Implementado. Devolve a fila de materiais com `status_validacao == "pendente"`, em ordem de cadastro (ID). Materiais sem esse campo, que foram cadastrados antes da evolução do CRUD 2, ainda não foram validados e por isso também entram na fila. A aprovação em si é feita por `aprovar_material()` no CRUD 2; o painel só mostra a fila.

### `mostrar_resumo()`

Existente: total de materiais e contagem por disciplina e série. Continua disponível na opção 6 do menu principal e dentro do painel.

### `menu_painel()`

Implementado. Confere a permissão e abre o submenu: atividades por professor, atividades por disciplina, materiais mais citados, fila de pendentes, painel completo (indicadores e todas as seções juntas) e resumo da biblioteca. As atividades são relidas a cada escolha, então o painel sempre mostra os dados atuais.

### Funções de apoio

- `ler_atividades()`: lê `provas/atividades.json` sem alterá-lo. Arquivo ausente, vazio ou inválido devolve `[]`; no caso de JSON inválido, também mostra um aviso.
- `ler_usuarios_por_id()`: dicionário `{id: usuário}` montado a partir de `carregar_usuarios()`.
- `mostrar_*()`: telas do terminal. As funções do contrato acima não usam `input` nem `print`, por isso são testadas isoladamente em `teste_painel.py`.

## Estruturas de dados usadas

- **Dicionários:** contagens por professor e por disciplina, mapa de usuários por ID e mapa de títulos.
- **Listas:** atividades, materiais, ranking e fila de pendentes.
- **Tuplas:** itens do ranking `(material_id, titulo, total)`, linhas `(nome, total)` e a tupla fixa `STATUS_VALIDACAO`.
- **Conjunto:** elimina IDs de materiais repetidos dentro da mesma atividade.
