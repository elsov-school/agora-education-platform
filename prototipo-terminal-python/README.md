# Ágora — Protótipo de terminal Python

Execute nesta pasta: `py main.py` (Windows) ou `python3 main.py` (Linux/macOS). Não há dependências externas.

O código existente foi separado por responsabilidade; os novos recursos estão descritos em Markdown, sem implementação. O menu continua oferecendo cadastro, gerenciamento, pesquisa, geração demonstrativa, consulta e resumo. As perguntas são fixas, sem IA. Autenticação, aprovação, persistência de provas e exportação estão planejadas.

## Estrutura e divisão da equipe

| Integrante | Branch | Arquivo principal | Contratos |
| --- | --- | --- | --- |
| 1 | `feat/usuarios` | `usuarios.py` | [Usuários](docs/usuarios.md) |
| 2 | `feat/materiais` | `materiais.py` | [Materiais — CRUD 2](docs/materiais.md) |
| 3 | `feat/consultas` | `consultas.py` | [Consultas](docs/consultas.md) |
| 4 | `feat/provas` | `provas.py` | [Provas — CRUD 3](docs/provas.md) |
| 5 | `feat/padroes-exportacao` | `padroes.py` | [Padrões e exportação](docs/padroes.md) |
| 6 | `feat/painel-menu` | `painel.py` e `main.py` | [Painel — CRUD 4 e menu](docs/painel.md) |

As seis branches são divisões de trabalho; não representam seis CRUDs. Consultas e padrões apoiam os quatro blocos funcionais das referências.

```text
prototipo-terminal-python/
├── main.py
├── usuarios.py
├── materiais.py
├── consultas.py
├── provas.py
├── padroes.py
├── painel.py
├── dados/
│   ├── README.md
│   └── materiais.json
├── docs/
│   ├── usuarios.md
│   ├── materiais.md
│   ├── consultas.md
│   ├── provas.md
│   ├── padroes.md
│   └── painel.md
└── exportacoes/
    └── .gitkeep
```

`usuarios.py` e `padroes.py` são arquivos reservados. Os demais preservam as funções existentes. `dados/materiais.json` mantém os registros e os campos antigos (`bncc`, `conteudo`); o contrato de evolução está na documentação do CRUD 2. Execute `main.py` para carregar os dados compartilhados antes de usar as operações.

## Trabalhar nas branches

As branches locais partem da mesma base organizada. Na raiz do repositório, entre na sua com `git switch feat/usuarios`, substituindo pelo nome da tabela. Elas pertencem ao repositório inteiro, embora esta divisão de trabalho seja para a pasta do protótipo. A publicação no remoto é feita separadamente, por exemplo: `git push -u origin feat/usuarios`.

## Dados e comportamento atual

As alterações de materiais são gravadas em `dados/materiais.json`. JSON inválido é informado sem sobrescrever o arquivo. Arquivo ausente, vazio ou lista vazia recebe os quatro exemplos na inicialização. A exclusão pede confirmação com `s`. Os códigos BNCC e conteúdos são ilustrativos.
