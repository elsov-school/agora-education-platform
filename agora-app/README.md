# Ágora — saber com fonte

Protótipo acadêmico de uma plataforma institucional para letramento em IA. O sistema ajuda professores a consultar e produzir conteúdos somente a partir de materiais previamente aprovados pela escola, mantendo fontes e um fluxo de validação pedagógica.

## Funcionalidades

1. **Biblioteca curricular:** cadastro, gestão, pesquisa e filtros de materiais; visão do professor restrita ao perfil.
2. **Gerador de provas e atividades:** geração local e determinística, edição, troca e remoção de questões, gabarito e fonte.
3. **Assistente com evidências:** busca textual nos materiais aprovados e recusa explícita quando não há evidência.
4. **Validação institucional:** rascunho, envio, aprovação/reprovação, responsável, data e justificativa.
5. **Padronização:** limites e regras persistentes que influenciam efetivamente o gerador.
6. **Painel da coordenação:** indicadores e gráficos calculados a partir dos dados do SQLite.

A descrição acadêmica completa está em [docs/funcionalidades.md](docs/funcionalidades.md).

## Tecnologias

- Python 3.9+
- Flask 3
- SQLite (biblioteca padrão do Python)
- Jinja2, HTML, CSS e JavaScript sem frameworks adicionais
- `unittest` para os testes automatizados

O gerador e o assistente são locais. A aplicação não usa API externa nem depende de chave paga.

## Identidade visual

A interface aplica a identidade institucional Ágora: Azul Egeu (`#10233F`), Marfim (`#F6F1E7`), Terracota (`#B84A2B`), Oliva (`#3F6B45`) e Areia (`#D8CDB6`). Fraunces é usada nos títulos, Instrument Sans na interface e IBM Plex Mono em citações e metadados. Os logotipos, grafismos e a ilustração de fontes aprovadas ficam em `static/brand/`.

O sistema continua utilizável sem internet; caso as fontes web não estejam disponíveis, são usados fallbacks locais equivalentes.

## Fluxos navegáveis

A interface segue os três fluxos do wireframe acadêmico no Figma:

1. **Criar atividade:** entrada conversacional, seleção de fontes, geração, rastreabilidade, edição e envio para validação.
2. **Verificar conteúdo externo:** texto colado pelo professor, seleção de materiais e diagnóstico por afirmação — suportada, parcialmente suportada ou não localizada.
3. **Gerenciar conhecimento:** biblioteca unificada com abas para materiais, atividades/provas e conteúdos verificados.

O fluxo de verificação amplia a FN-03, mantendo exatamente as seis macrofuncionalidades acadêmicas originais.

## Instalação e execução

### 1. Preparar o projeto

Você precisa de **Python 3.9 ou superior** e de um navegador. Confira com `python3 --version` no macOS/Linux ou `py --version` no Windows.

Se ainda não baixou o repositório, execute no terminal:

```bash
git clone https://github.com/elsov-school/agora-education-platform.git
cd agora-education-platform
```

Também é possível usar **Code → Download ZIP** no GitHub, extrair o arquivo e abrir um terminal na pasta extraída.

Os comandos abaixo partem da **pasta principal do repositório**. Se seu terminal já estiver dentro de `agora-app`, pule o comando `cd agora-app`.

### 2. Instalar e iniciar — macOS ou Linux

```bash
cd agora-app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

### 2. Instalar e iniciar — Windows

No PowerShell ou no Prompt de Comando:

```powershell
cd agora-app
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Se `py` não existir mas `python --version` funcionar, use `python -m venv .venv` para criar o ambiente.

Os comandos usam diretamente o Python do ambiente `.venv`, sem precisar ativá-lo. A criação do ambiente e a instalação das dependências são necessárias apenas na primeira vez. A instalação requer internet; o uso dos dados e das funcionalidades é local.

### 3. Abrir no navegador

Quando o terminal mostrar o servidor em execução, acesse **[http://127.0.0.1:5000](http://127.0.0.1:5000)**. Escolha um perfil para entrar; não é necessário cadastrar uma conta ou informar senha.

Mantenha o terminal aberto enquanto usa a aplicação. Para encerrar o servidor, pressione **Ctrl+C** nesse terminal.

### Próximas execuções

Abra um terminal **dentro de `agora-app`** e execute apenas o comando correspondente:

**macOS/Linux:**

```bash
.venv/bin/python app.py
```

**Windows:**

```powershell
.\.venv\Scripts\python.exe app.py
```

### Usar no VS Code

Abra a pasta `agora-app` no VS Code, escolha **Terminal → Novo Terminal** e use os comandos acima, pulando `cd agora-app`. A execução pelo terminal não depende de configurar o F5.

### Dados da demonstração

O banco `data/agora.db` é criado e populado automaticamente na primeira execução. Cadastros e alterações continuam salvos quando o servidor é encerrado. O banco é local e fica fora do Git.

Para voltar aos dados iniciais, encerre o servidor, faça uma cópia do banco se quiser preservar suas alterações, remova apenas `data/agora.db` e inicie a aplicação novamente. Isso apaga os cadastros e as alterações locais da demonstração.

## Problemas comuns

- **`No module named flask`:** dentro de `agora-app`, execute novamente o comando de instalação de `requirements.txt` com o Python de `.venv`.
- **Arquivo não encontrado:** confirme que o terminal está na pasta `agora-app`, onde ficam `app.py` e `requirements.txt`.
- **Python não encontrado:** instale Python 3.9+ e reabra o terminal. No Windows, habilite a opção de adicionar o Python ao PATH durante a instalação.
- **Porta 5000 ocupada (`Address already in use`):** encerre outro servidor que esteja usando essa porta ou use a porta 5001 com um dos comandos abaixo, dentro de `agora-app`.

**macOS/Linux:**

```bash
.venv/bin/python -m flask --app app run --port 5001
```

**Windows:**

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --port 5001
```

Nesse caso, abra **[http://127.0.0.1:5001](http://127.0.0.1:5001)**.

Se o navegador não conectar, confirme que o servidor ainda está rodando no terminal e que você abriu o endereço e a porta mostrados por ele.

## Perfis de demonstração

- **Ana Souza — Professora:** Ciências e Biologia; 8º ano A e 1º ano EM.
- **Carlos Lima — Professor:** Matemática; 8º ano A e 9º ano B.
- **Marina Costa — Professora:** Português; 8º ano A.
- **Paula Mendes — Coordenação:** biblioteca completa, validação, padrões e painel.

O acesso é simulado: basta escolher o perfil na tela inicial, sem senha.

## Roteiro rápido de apresentação

1. Entre como **Ana Souza**, filtre a biblioteca e abra “Citologia: organelas celulares”.
2. Gere uma atividade de Biologia para o 1º ano EM usando esse material; edite ou troque uma questão e envie para validação.
3. Pergunte ao assistente “Qual é a função da mitocôndria?” e observe a resposta e o trecho-fonte. Faça uma pergunta não coberta para demonstrar a recusa.
4. Troque para **Paula Mendes**, analise a atividade pendente e aprove ou reprove.
5. Em Padrões, reduza o limite de questões e confirme que o gerador respeita a nova regra.
6. Abra o Painel e observe os indicadores atualizados.

## Testes

Com as dependências instaladas, abra um terminal **dentro de `agora-app`**.

**macOS/Linux:**

```bash
.venv/bin/python -m unittest discover -s tests -v
```

**Windows:**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam um banco temporário para validar as operações, sem modificar os dados da demonstração.

## Estrutura

```text
app.py                     Rotas, perfis e composição das telas
config.py                  Tuplas fixas e configuração
database.py                Schema SQLite, conexão e dados iniciais
services/
  library.py               FN-01
  generator.py             FN-02
  assistant.py             FN-03
  verifier.py              Fluxo de verificação da FN-03
  validation.py            FN-04
  standards.py             FN-05
  dashboard.py             FN-06
templates/                 Páginas Jinja
static/brand/              Logotipos, grafismos e ilustração oficiais
static/css, static/js      Identidade visual e interações
data/agora.db              Banco persistente (gerado localmente)
docs/funcionalidades.md    Documentação acadêmica
tests/                     Testes funcionais e de regras
```

## Estruturas de dados Python

- **Lista:** materiais, sentenças, questões, evidências, séries do painel e dados iniciais.
- **Dicionário:** cada registro material/questão, filtros, configurações e indicadores.
- **Tupla:** `TIPOS_QUESTAO`, `DIFICULDADES`, `STATUS_CONTEUDO` e campos fixos dos materiais.
