# Painel da coordenação e menus

## Entrega contrato v1

Entre como coordenação em `py main.py`, escolha **5 — Painel de métricas** e **5 — Painel completo** para ver todas as seções. Para executar apenas o painel, use `py -m painel.painel` a partir da pasta do protótipo e informe um ID de coordenação ativa. No Linux/macOS, use `python3`.

| Métrica | Como é calculada |
| --- | --- |
| Biblioteca e fila | Total de materiais, aprovados e pendentes, distribuição por disciplina e série. Um registro anterior ao campo `status_validacao` entra na fila por ID. |
| Provas por professor | Conta cada registro em `provas/atividades.json`. Professores ativos sem provas aparecem com zero. O histórico preserva autores inativos ou ausentes do cadastro. |
| Provas por série e disciplina | Usa a série e a disciplina gravadas na prova. Os percentuais tomam o total de provas como denominador. |
| Três materiais mais usados | Usa o contador `usos` do material. Mostra até três com uso positivo, com desempate por título e ID. |
| Citações nas provas | Conta cada material uma vez por prova, mesmo com ID repetido. Referências históricas a materiais removidos continuam na contagem. |

O painel relê os JSONs necessários a cada escolha. Se uma fonte estiver ilegível, a tela informa o erro e permite voltar. As telas de métricas abrem os arquivos apenas para leitura. A coordenação aprova materiais em **Aprovar materiais pendentes** ou no menu da biblioteca.

### APIs

- `main.menu_principal()` carrega os dados, solicita login e encaminha a sessão.
- `main.menu_coordenacao(usuario)` e `main.menu_professor(usuario)` abrem os menus por perfil. A opção **9** troca o usuário e **0** encerra o programa.
- `menu_painel(usuario=None)` recebe a sessão ou solicita ID na execução isolada. A permissão exigida é `acessar_metricas`.
- `contar_atividades_por_professor(atividades)`, `contar_atividades_por_serie(atividades)` e `contar_atividades_por_disciplina(atividades)` retornam dicionários de contagem.
- `listar_materiais_mais_usados(materiais)` e `listar_materiais_mais_citados(atividades, materiais)` retornam listas de tuplas `(id, titulo, total)`.
- `listar_materiais_pendentes(materiais)` retorna a fila. `mostrar_resumo()` e `mostrar_painel_completo(atividades)` continuam disponíveis para quem já carregou a biblioteca.

### Testes

Execute os comandos na pasta `prototipo-terminal-python`.

```sh
python -m unittest discover -s tests -p "test_painel.py" -v
python -m unittest discover -s tests -p "test_integracao.py" -v
```

O teste de ponta a ponta inicia o terminal com os seis módulos reais em uma escola temporária. Ele verifica que uma pesquisa preserva o contador, que a consulta e a prova salva somam dois usos e que exportação e leitura do painel preservam essa contagem. Os testes específicos do painel também cobrem empates, referências históricas, JSON inválido e perda de permissão enquanto o menu aguarda uma escolha.
