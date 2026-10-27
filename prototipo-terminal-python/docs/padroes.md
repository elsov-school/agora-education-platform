# Padrões e exportação

Branch: `feat/padroes-exportacao`. Arquivo: `padroes.py`.

Planejado. Usar exportacoes/ para os arquivos gerados. Formato inicial sugerido: texto UTF-8; outros formatos serão definidos pela equipe.

## Funções e comportamento esperado

### `obter_modelo(nome="institucional_v1")`

Retornar cabeçalho, campos e regras do padrão institucional; recusar modelos desconhecidos.

### `validar_prova(dados_prova)`

Verificar campos, questões, gabaritos e critérios obrigatórios antes de exportar.

### `formatar_prova(dados_prova, modelo)`

Montar cabeçalho e questões na ordem definida pelo padrão.

### `exportar_atividade(dados_prova, destino, incluir_gabarito=False)`

Gravar prova formatada; incluir gabarito apenas quando solicitado e retornar caminho do arquivo.
