# Ágora - Protótipo em Python

## Objetivo

Representar uma biblioteca escolar da plataforma Ágora por meio de um protótipo
acadêmico de Fundamentos de Programação. Todo o programa funciona pelo terminal,
com funções simples e apenas as bibliotecas padrão `json` e `os`.

## Como executar

### 1. Preparar o projeto

Você precisa apenas de **Python 3**. O programa usa as bibliotecas padrão `json` e `os`; não é necessário instalar pacotes, criar um ambiente virtual ou iniciar a aplicação web.

Confira o Python com `python3 --version` no macOS/Linux ou `py --version` no Windows.

Se ainda não baixou o repositório, execute no terminal:

```bash
git clone https://github.com/elsov-school/agora-education-platform.git
cd agora-education-platform
```

Também é possível usar **Code → Download ZIP** no GitHub, extrair o arquivo e abrir um terminal na pasta extraída.

### 2. Iniciar o programa

Os comandos abaixo partem da **pasta principal do repositório**. Se o terminal já estiver dentro de `prototipo-terminal-python`, pule o comando `cd prototipo-terminal-python`.

**macOS ou Linux:**

```bash
cd prototipo-terminal-python
python3 main.py
```

**Windows (PowerShell ou Prompt de Comando):**

```powershell
cd prototipo-terminal-python
py main.py
```

Se `py` não existir mas `python --version` funcionar, use `python main.py`.

O programa aparece no próprio terminal. Não é necessário abrir o navegador.

### 3. Usar o menu

```text
1 - Adicionar material
2 - Gerenciar materiais
3 - Pesquisar material
4 - Gerar atividade
5 - Consultar conteúdo
6 - Resumo da biblioteca
0 - Sair
```

Digite o número da opção desejada e pressione **Enter**.

Para testar o CRUD:

1. Use **1** para cadastrar um material e preencher os campos solicitados.
2. Use **2** para listar, visualizar, editar ou excluir materiais.
3. Ao editar, pressione **Enter** nos campos que deseja manter.
4. Ao excluir, confirme com **s** quando solicitado.

Disciplinas e bimestres também são escolhidos por números. A opção **0** encerra o programa no menu principal; em **Gerenciar materiais**, volta ao menu principal.

### Usar no VS Code

Abra a pasta `prototipo-terminal-python`, escolha **Terminal → Novo Terminal** e execute `python3 main.py` (macOS/Linux) ou `py main.py` (Windows). Não é necessário configurar o F5.

### Executar novamente e manter os dados

Dentro de `prototipo-terminal-python`, use novamente o mesmo comando de execução. Os cadastros, as edições e as exclusões são salvos em `dados.json`, na pasta do programa, e permanecem entre execuções.

## Problemas comuns

- **Python não encontrado:** instale Python 3 e reabra o terminal. No Windows, habilite a opção de adicionar o Python ao PATH durante a instalação.
- **`can't open file` ou arquivo não encontrado:** confirme que o terminal está dentro de `prototipo-terminal-python`, onde fica `main.py`.
- **O programa abre e fecha rapidamente:** execute pelo terminal para conseguir ler o menu e digitar as opções.
- **`JSON inválido`:** o programa informa o erro e encerra sem sobrescrever `dados.json`. Faça uma cópia do arquivo antes de corrigi-lo. Para reiniciar com os quatro exemplos, renomeie o arquivo e execute novamente.

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

Os materiais são mantidos entre execuções. Uma biblioteca vazia recebe novamente
os quatro exemplos na próxima inicialização.
