# Ágora — Protótipo de terminal Python

Execute nesta pasta: `py main.py` (Windows) ou `python3 main.py` (Linux/macOS). Não há dependências externas.

Cada CRUD reúne código, documentação e dados na mesma pasta. Consultas, padrões e painel têm documentação e código próprios; não precisam de JSON separado. O painel calcula métricas sobre os outros CRUDs.

```text
prototipo-terminal-python/
├── main.py
├── README.md
├── usuarios/                  # CRUD 1 — feat/usuarios
│   ├── __init__.py
│   ├── usuarios.py
│   ├── README.md
│   └── usuarios.json
├── materiais/                 # CRUD 2 — feat/materiais
│   ├── __init__.py
│   ├── materiais.py
│   ├── README.md
│   └── materiais.json
├── provas/                    # CRUD 3 — feat/provas
│   ├── __init__.py
│   ├── provas.py
│   ├── README.md
│   └── atividades.json
├── painel/                    # CRUD 4 — feat/painel-menu
│   ├── __init__.py
│   ├── painel.py
│   └── README.md
├── consultas/                 # feat/consultas
│   ├── __init__.py
│   ├── consultas.py
│   └── README.md
├── padroes/                   # feat/padroes-exportacao
│   ├── __init__.py
│   ├── padroes.py
│   └── README.md
└── exportacoes/
    └── .gitkeep
```

## Documentação de cada módulo

- [Usuários e perfis](usuarios/README.md)
- [Biblioteca curricular — CRUD 2](materiais/README.md)
- [Provas e atividades](provas/README.md)
- [Painel e menu](painel/README.md)
- [Consultas](consultas/README.md)
- [Padrões e exportação](padroes/README.md)

## O que já funciona

O menu mantém cadastro, listagem, edição, exclusão, pesquisa de materiais, perguntas fixas, consulta e resumo. Os materiais existentes foram preservados em `materiais/materiais.json`. Os campos atuais ainda são `bncc` e `conteudo`; a evolução está descrita no README do módulo.

Os arquivos `usuarios/usuarios.json` e `provas/atividades.json` começam vazios (`[]`), preparados para os CRUDs futuros. As funções planejadas estão documentadas; autenticação, aprovação, persistência de provas e exportação ainda não estão implementadas.

JSON de materiais inválido é informado sem sobrescrever o arquivo. Arquivo ausente, vazio ou lista vazia recebe os quatro exemplos na inicialização. A exclusão pede confirmação com `s`. Conteúdos e códigos BNCC são ilustrativos; não há IA.

## Branches

Na raiz do repositório, use `git switch feat/usuarios`, substituindo pelo nome indicado na árvore. As seis branches locais compartilham esta estrutura organizada como base de desenvolvimento.
