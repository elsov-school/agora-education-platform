# Ágora — Plataforma Educacional

> **Saber com fonte.**

A Ágora é um projeto acadêmico para organizar, consultar e produzir conteúdos educacionais com fontes e validação pedagógica. Este repositório reúne **dois protótipos independentes**, cada um em sua pasta.

## Qual versão executar?

| Projeto | Onde funciona | O que demonstra | Guia completo |
| --- | --- | --- | --- |
| `agora-app/` | Navegador | Biblioteca, atividades, consulta com evidências, verificação de conteúdo, validação e painel | [README da aplicação web](agora-app/README.md) |
| `prototipo-terminal-python/` | Terminal | CRUD de materiais, pesquisa, atividades fixas, consulta e resumo da biblioteca | [README do CRUD em Python](prototipo-terminal-python/README.md) |

Para testar o **CRUD simples**, escolha a versão de terminal. Para ver a **interface da plataforma**, escolha a aplicação web. Você pode executar apenas uma delas; os projetos usam dados separados.

Os protótipos atuais usam busca textual e geração local. Não precisam de conta em serviço de IA nem de chave de API. A integração com LLMs, embeddings e um pipeline RAG faz parte da proposta de evolução.

## 1. Baixar o repositório

Você precisa de **Python 3.9 ou superior**. Para usar o comando abaixo, também precisa de Git.

Abra um terminal (no VS Code: **Terminal → Novo Terminal**) e execute:

```bash
git clone https://github.com/elsov-school/agora-education-platform.git
cd agora-education-platform
```

Se preferir baixar sem Git, use **Code → Download ZIP** no GitHub, extraia o arquivo e abra um terminal na pasta extraída.

Confira se o Python está disponível:

- **macOS/Linux:** `python3 --version`
- **Windows:** `py --version`

No Windows, se `py` não existir mas `python --version` funcionar, substitua `py` por `python` nos comandos abaixo.

## 2. Executar o CRUD no terminal

Comece na pasta principal do repositório, onde estão as duas pastas de projetos.

### macOS ou Linux

```bash
cd prototipo-terminal-python
python3 main.py
```

### Windows (PowerShell ou Prompt de Comando)

```powershell
cd prototipo-terminal-python
py main.py
```

Não é necessário instalar pacotes. O menu aparece no próprio terminal:

- **1:** adicionar material;
- **2:** gerenciar materiais (listar, visualizar, editar e excluir);
- **3:** pesquisar material;
- **4:** gerar atividade;
- **5:** consultar conteúdo;
- **6:** ver o resumo da biblioteca;
- **0:** sair.

Digite o número e pressione **Enter**. Os materiais ficam salvos em `prototipo-terminal-python/dados.json`.

## 3. Executar a aplicação web

Comece na pasta principal do repositório. Se acabou de sair do CRUD e o terminal ainda estiver dentro de `prototipo-terminal-python`, execute `cd ..` primeiro.

### macOS ou Linux — primeira execução

```bash
cd agora-app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

### Windows — primeira execução

```powershell
cd agora-app
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Esses comandos usam diretamente o Python do ambiente virtual; não é necessário ativá-lo. A instalação das dependências requer internet.

Com o servidor rodando, abra **[http://127.0.0.1:5000](http://127.0.0.1:5000)** no navegador. Escolha um dos perfis de demonstração; o acesso é simulado e não pede senha.

- **Ana Souza, Carlos Lima e Marina Costa:** professores.
- **Paula Mendes:** coordenação, com acesso à validação, aos padrões e ao painel.

Mantenha o terminal aberto enquanto usa o site. Para encerrar o servidor, pressione **Ctrl+C** no terminal.

### Executar novamente

Depois da instalação inicial, entre em `agora-app` e use apenas:

- **macOS/Linux:** `.venv/bin/python app.py`
- **Windows:** `.\.venv\Scripts\python.exe app.py`

O SQLite cria e popula `agora-app/data/agora.db` automaticamente na primeira execução. Esse banco é local e não é enviado ao GitHub.

## Demonstração na Vercel

A versão web pode ser publicada na Vercel usando `agora-app` como **Root Directory**. Nessa publicação, os dados são temporários e podem ser reiniciados; para salvar cadastros permanentemente online, é necessário um banco externo. O uso local continua salvando os dados no SQLite normalmente.

Consulte a [configuração de publicação](agora-app/README.md#publicação-na-vercel) no guia da aplicação web.

## Estrutura do repositório

```text
agora-education-platform/
├── README.md
├── .gitignore
├── agora-app/
│   ├── README.md
│   ├── app.py
│   ├── requirements.txt
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── docs/
│   └── tests/
└── prototipo-terminal-python/
    ├── README.md
    ├── main.py
    └── dados.json
```

O ambiente `.venv/` e o banco `data/agora.db` são criados localmente durante a instalação e o uso da aplicação web.

## Se algo não funcionar

| Mensagem ou situação | Como resolver |
| --- | --- |
| `python3`, `py` ou `python` não encontrado | Instale Python 3.9+ e reabra o terminal. No Windows, habilite a opção de adicionar o Python ao PATH durante a instalação. |
| `can't open file`, arquivo não encontrado ou `requirements.txt` não encontrado | Confira a pasta atual: `app.py` fica em `agora-app`; `main.py` fica em `prototipo-terminal-python`. |
| `No module named flask` | Dentro de `agora-app`, repita o comando de instalação de dependências usando o Python de `.venv`. |
| Porta 5000 ocupada ou navegador não abre | Consulte a seção de solução de problemas no [guia da aplicação web](agora-app/README.md#problemas-comuns). |

## Proposta e evolução

A proposta da Ágora é manter conteúdos ligados à biblioteca curricular aprovada pela instituição, respeitando o contexto de cada professor e permitindo revisão pela coordenação.

A aplicação web já demonstra biblioteca, geração local de atividades, consulta com evidências, verificação de textos, validação institucional, padrões e painel. O protótipo de terminal demonstra as operações básicas da biblioteca com estruturas simples de Python.

Possíveis próximos passos incluem autenticação real, integração com modelos de linguagem, busca por embeddings, ingestão de documentos e exportação de avaliações. Essas funcionalidades não são necessárias para executar os protótipos atuais.

Para os detalhes acadêmicos da versão web, consulte [a descrição das funcionalidades](agora-app/docs/funcionalidades.md).
