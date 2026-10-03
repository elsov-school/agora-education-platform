# Ágora - Protótipo em Python

## Objetivo

Representar uma biblioteca escolar da plataforma Ágora por meio de um protótipo
acadêmico de Fundamentos de Programação. Todo o programa funciona pelo terminal,
com funções simples e apenas as bibliotecas padrão `json` e `os`.

## Como executar

Com Python 3 instalado, abra o terminal ou PowerShell na pasta do projeto:

```text
cd prototipo-terminal-python
python main.py
```

Se o comando Python 3 do seu computador for `python3`, use `python3 main.py`.
Não é necessário instalar pacotes.

Digite o número da opção desejada. Disciplinas e bimestres também são escolhidos
por números. Para editar, pressione Enter nos campos que deseja manter.
A opção `0` encerra o programa; no gerenciamento, ela volta ao menu principal.

## Funcionalidades

1. Adicionar material: solicita os seis campos, gera um ID e salva no JSON.
2. Gerenciar materiais: lista, visualiza, edita e exclui materiais (CRUD).
   A exclusão só acontece após a resposta `s` à confirmação.
3. Pesquisar material: procura em título, disciplina, série, conteúdo e BNCC,
   sem diferenciar maiúsculas de minúsculas.
4. Gerar atividade: apresenta quatro perguntas fixas sobre o material escolhido.
5. Consultar conteúdo: procura uma palavra ou assunto nos conteúdos e mostra
   todos os resultados com sua fonte.
6. Resumo da biblioteca: calcula o total e as quantidades por disciplina e série.

Todas as funcionalidades estão em `main.py`, respectivamente nas funções
`adicionar_material()`, `gerenciar_materiais()`, `pesquisar_material()`,
`gerar_atividade()`, `consultar_conteudo()` e `mostrar_resumo()`.

O arquivo `dados.json` começa com Sistema Solar, Célula, Equação do Primeiro Grau
e Gêneros Textuais. Se estiver ausente, vazio ou com uma lista vazia, os exemplos
são criados ao iniciar. Cadastros, edições e exclusões atualizam esse arquivo.
Se o JSON tiver sintaxe inválida, o programa informa o problema e encerra sem
sobrescrever o arquivo. Os conteúdos e códigos BNCC são ilustrativos, usados
apenas para demonstração acadêmica.

Atividades e consultas usam os materiais locais e perguntas fixas, sem IA.

## Conceitos de Python utilizados

- Variáveis: armazenam títulos, termos de pesquisa e opções digitadas.
- `input` e `print`: recebem informações e apresentam os resultados no terminal.
- Condicionais: `if`, `elif` e `else` escolhem as ações e verificam resultados.
- Estruturas de repetição: `while` mantém os menus abertos; `for` percorre materiais
  na listagem, pesquisa, consulta, geração de IDs e contagens.
- Funções: organizam cada operação em uma sequência simples de instruções.
- Lista: `materiais = []` guarda a coleção; `perguntas` guarda as perguntas da atividade.
- Dicionário: cada `material` tem as chaves `id`, `titulo`, `disciplina`, `serie`,
  `bimestre`, `bncc` e `conteudo`. `por_disciplina` e `por_serie` guardam contagens.
- Tupla: `DISCIPLINAS` e `BIMESTRES`, no início do código, guardam opções fixas.
- JSON: `carregar_dados()` lê os materiais e `salvar_dados()` grava as alterações,
  preservando os acentos com codificação UTF-8.
- `try/except`: trata texto digitado no lugar de números e JSON inválido.

Os materiais são mantidos entre execuções. Como pedido, uma biblioteca vazia
recebe novamente os quatro exemplos na próxima inicialização.
