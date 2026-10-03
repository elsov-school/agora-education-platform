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

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Acesse `http://127.0.0.1:5000`. O banco `data/agora.db` é criado e populado automaticamente na primeira execução. Para reiniciar a demonstração, encerre a aplicação, remova somente esse arquivo e execute novamente.

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

```bash
python3 -m unittest discover -s tests -v
```

Os testes usam um banco temporário, sem modificar os dados da demonstração.

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
