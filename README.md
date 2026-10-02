# Ágora — Plataforma Institucional de IA para Educação

> **Saber com fonte.**

A **Ágora** é uma plataforma institucional de Inteligência Artificial voltada para instituições de ensino.

A solução utiliza **RAG (Retrieval-Augmented Generation)** para permitir que professores consultem informações, criem atividades e produzam materiais pedagógicos utilizando exclusivamente fontes previamente cadastradas e aprovadas pela instituição.

O princípio central da plataforma é simples:

> **A IA não responde fora da biblioteca curricular aprovada.**

Livros, apostilas, planos de aula e outros materiais utilizados pela escola formam uma base de conhecimento institucional. As respostas e conteúdos gerados pela IA são produzidos a partir dessa base e mantêm vínculo com suas respectivas fontes.

---

## Sobre o projeto

O uso de ferramentas de Inteligência Artificial na educação traz ganhos importantes de produtividade, mas também cria desafios relacionados à:

- confiabilidade das informações;
- ausência de referências;
- uso de fontes não aprovadas;
- geração de informações incorretas;
- falta de padronização entre professores;
- dificuldade de acompanhamento pela coordenação;
- alinhamento do conteúdo ao currículo da instituição.

A Ágora propõe uma camada institucional entre o professor e a Inteligência Artificial.

Em vez de utilizar uma IA genérica diretamente, a instituição define:

- quais materiais podem ser utilizados;
- quais conteúdos fazem parte de cada turma;
- quais regras pedagógicas devem ser seguidas;
- quais modelos e padrões devem ser aplicados;
- quais fontes são consideradas válidas.

A IA trabalha dentro desse contexto.

---

# Objetivo

Criar uma plataforma que permita o uso de Inteligência Artificial em ambientes educacionais com maior **controle, rastreabilidade, padronização e confiabilidade**.

A Ágora busca permitir que professores utilizem IA no cotidiano sem perder a relação com:

- o plano de ensino;
- o material adotado pela instituição;
- a série e a disciplina;
- o período letivo;
- as habilidades previstas;
- as regras pedagógicas da escola;
- as fontes utilizadas na geração.

---

# Perfis da plataforma

A solução possui diferentes níveis de utilização.

## Instituição

Responsável por estruturar o ambiente educacional da plataforma.

Entre suas responsabilidades estão:

- cadastrar anos letivos;
- cadastrar turmas;
- organizar disciplinas;
- cadastrar professores;
- definir padrões institucionais;
- cadastrar materiais curriculares;
- estruturar a biblioteca utilizada pela IA.

---

## Coordenação

Responsável pela governança pedagógica da plataforma.

A coordenação pode:

- revisar materiais;
- aprovar ou rejeitar fontes;
- acompanhar materiais pendentes;
- definir modelos de prova;
- configurar critérios de qualidade;
- estabelecer regras institucionais;
- acompanhar o uso da plataforma;
- visualizar indicadores por professor, série e disciplina.

---

## Professor

É o principal usuário das funcionalidades de IA.

Cada professor acessa somente as turmas e conteúdos relacionados às disciplinas que leciona.

O professor pode:

- consultar a biblioteca utilizando IA;
- receber respostas acompanhadas de evidências;
- gerar provas;
- gerar atividades;
- editar conteúdos;
- gerar gabaritos;
- definir critérios de correção;
- exportar materiais para utilização em sala.

---

# Funcionalidades principais

## Biblioteca curricular por ano letivo

A biblioteca curricular é o núcleo da Ágora.

A instituição cadastra os materiais autorizados para utilização pela plataforma, como:

- livros;
- apostilas;
- planos de aula;
- documentos;
- materiais complementares.

Cada material pode ser associado a informações acadêmicas como:

- ano letivo;
- série;
- disciplina;
- bimestre;
- turma;
- habilidade da BNCC.

Esses materiais passam por um processo de organização e validação antes de serem utilizados pela IA.

### Regra fundamental

```text
Sem fonte aprovada → sem resposta baseada naquele conteúdo.
```

A aplicação deve evitar completar uma resposta com conhecimento externo quando a biblioteca institucional não possui base suficiente.

---

## Gerador de provas e atividades

O professor pode gerar avaliações utilizando apenas os materiais autorizados para sua turma.

O fluxo permite selecionar:

```text
Turma
   ↓
Conteúdo
   ↓
Quantidade de questões
   ↓
Tipo de questão
   ↓
Nível de dificuldade
   ↓
Geração
```

Tipos de questão previstos:

- múltipla escolha;
- discursiva;
- verdadeiro ou falso.

A plataforma pode produzir:

- enunciados;
- alternativas;
- gabarito;
- critérios de correção.

Antes da aplicação, o professor pode:

- editar questões;
- excluir questões;
- solicitar novas questões;
- ajustar o conteúdo;
- revisar o gabarito;
- alterar critérios de correção.

Ao final, o material poderá ser exportado para formatos como:

- PDF;
- Word.

---

## Assistente de consulta com evidências

O professor pode realizar perguntas relacionadas aos conteúdos de suas turmas.

Exemplo:

```text
Professor
   ↓
Pergunta
   ↓
Busca na biblioteca curricular
   ↓
Recuperação dos trechos relevantes
   ↓
Construção do contexto
   ↓
LLM
   ↓
Resposta + evidências
```

As respostas devem indicar as fontes utilizadas.

Quando não houver informação suficiente na biblioteca, a plataforma deve informar que não existe uma fonte aprovada capaz de responder à solicitação.

Exemplo:

> Não foram encontradas fontes aprovadas suficientes para responder a esta pergunta.

O comportamento é preferível a gerar uma resposta sem sustentação documental.

---

## Padronização institucional

A Ágora permite que a instituição defina padrões que serão aplicados aos conteúdos gerados.

Exemplos:

- modelo de prova;
- quantidade ou distribuição de questões;
- estrutura de atividades;
- critérios pedagógicos;
- regras de qualidade;
- instruções institucionais;
- formatos de resposta.

Dessa forma, diferentes professores podem utilizar IA mantendo os padrões definidos pela escola.

---

## Painel da coordenação

A coordenação terá uma visão consolidada da utilização da plataforma.

Entre os indicadores previstos estão:

- quantidade de conteúdos criados;
- conteúdos aguardando validação;
- materiais mais utilizados;
- uso por professor;
- uso por disciplina;
- uso por série;
- fontes mais consultadas.

O objetivo do painel não é apenas medir utilização, mas permitir **governança sobre o uso da IA dentro da instituição**.

---

# Fluxo geral de uso

```text
INSTITUIÇÃO
    │
    ├── Define padrões institucionais
    │
    ├── Cadastra ano letivo
    │
    ├── Cadastra turmas e disciplinas
    │
    ├── Vincula professores
    │
    └── Cadastra materiais
             │
             ▼
      BIBLIOTECA CURRICULAR
             │
             ▼
        COORDENAÇÃO
             │
             ├── Revisa fontes
             │
             ├── Valida materiais
             │
             └── Define padrões
             │
             ▼
          PROFESSOR
             │
             ├── Consulta o assistente
             │
             └── Gera provas e atividades
             │
             ▼
             RAG
             │
             ├── Recupera fontes
             ├── Verifica relevância
             ├── Monta contexto
             └── Consulta o LLM
             │
             ▼
       CONTEÚDO + EVIDÊNCIAS
```

---

# Arquitetura

A arquitetura proposta separa a plataforma em diferentes responsabilidades.

```text
┌───────────────────────┐
│       Usuários        │
│                       │
│ Instituição           │
│ Coordenação           │
│ Professor             │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│    Aplicação Web      │
│                       │
│ Biblioteca            │
│ Plano de ensino       │
│ Assistente RAG        │
│ Geração de conteúdo   │
│ Validação             │
│ Dashboard             │
└──────────┬────────────┘
           │
           ▼
┌──────────────────────────┐
│ API + Regras de Negócio  │
│                          │
│ Perfis e permissões      │
│ Padronização             │
│ Fluxos de validação      │
└──────────┬───────────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
┌───────────────────┐   ┌─────────────────────┐
│ Banco de dados    │   │      Motor RAG      │
│                   │   │                     │
│ Instituições      │   │ Extração            │
│ Professores       │   │ Chunking             │
│ Turmas            │   │ Embeddings           │
│ Disciplinas       │   │ Indexação            │
│ Conteúdos         │   │ Recuperação          │
│ Regras            │   │ Reranking/relevância │
└───────────────────┘   │ Construção contexto  │
                        └──────────┬───────────┘
                                   │
                         ┌─────────┴─────────┐
                         ▼                   ▼
                ┌────────────────┐   ┌────────────────┐
                │ Índice vetorial│   │      LLM       │
                └────────────────┘   └────────────────┘
```

---

# Como o RAG funciona

A Ágora utiliza o padrão **Retrieval-Augmented Generation**.

O objetivo é fornecer ao modelo apenas informações relacionadas às fontes autorizadas.

## Etapa A — Ingestão

Quando uma fonte é aprovada:

```text
Material
   ↓
Extração do texto
   ↓
Divisão em trechos
   ↓
Geração de embeddings
   ↓
Indexação
   ↓
Fonte disponível para consulta
```

Cada trecho deve manter informações que permitam identificar sua origem.

---

## Etapa B — Consulta

Quando um professor realiza uma solicitação:

```text
Pergunta
   ↓
Identificação do escopo
   ↓
Busca no índice
   ↓
Recuperação dos trechos relevantes
   ↓
Verificação de relevância
   ↓
Construção do prompt
   ↓
LLM
   ↓
Resposta
   ↓
Referências utilizadas
```

---

# Princípios do sistema

## Fonte antes da geração

A recuperação das fontes acontece antes da geração da resposta.

---

## Rastreabilidade

Conteúdos gerados devem permitir identificar quais materiais deram origem à informação apresentada.

---

## Escopo institucional

O contexto da IA deve respeitar:

```text
Instituição
    ↓
Ano letivo
    ↓
Turma
    ↓
Disciplina
    ↓
Conteúdo
```

---

## Controle de acesso

Professores não devem possuir acesso irrestrito a todo o conteúdo da instituição.

O sistema deve considerar os vínculos entre:

```text
Professor ↔ Disciplina ↔ Turma
```

---

## Falta de evidência é uma resposta válida

Caso nenhum material aprovado cubra adequadamente uma solicitação, o sistema não deve completar a informação utilizando conteúdo não autorizado.

---

# Dados principais

A plataforma deverá trabalhar com entidades relacionadas ao contexto acadêmico e ao funcionamento do RAG.

Entre elas:

### Instituição

Representa a organização responsável pelo ambiente.

### Usuário

Representa professores, coordenadores e outros perfis autorizados.

### Ano letivo

Define o período ao qual determinado conteúdo pertence.

### Série

Identifica o nível escolar.

### Disciplina

Representa a matéria associada ao conteúdo.

### Turma

Relaciona alunos, professores e disciplinas.

### Fonte

Representa um material enviado para a biblioteca.

### Conteúdo curricular

Relaciona uma fonte ao contexto pedagógico no qual ela pode ser utilizada.

### Plano de ensino

Organiza conteúdos previstos para determinado período.

### Conteúdo gerado

Registra materiais produzidos utilizando a plataforma.

### Evidência

Relaciona uma parte do conteúdo gerado aos trechos utilizados pelo RAG.

### Parâmetros de geração

Registra informações como:

- quantidade de questões;
- tipo;
- dificuldade;
- turma;
- conteúdo escolhido.

---

# Exemplo de rastreabilidade

Uma resposta não deve ser armazenada apenas como texto.

Idealmente, o sistema mantém também a relação:

```text
Resposta
 ├── trecho 1
 │    └── Fonte A
 │
 ├── trecho 2
 │    └── Fonte A
 │
 └── trecho 3
      └── Fonte B
```

Isso permite apresentar evidências diretamente na interface.

---

# Regras de negócio

Algumas das principais regras previstas são:

1. Uma fonte precisa estar aprovada antes de poder alimentar o RAG.
2. Professores acessam apenas as turmas às quais estão vinculados.
3. Consultas devem respeitar o contexto selecionado pelo usuário.
4. Conteúdos gerados devem utilizar fontes autorizadas.
5. O sistema deve manter referência às evidências utilizadas.
6. Padrões definidos pela instituição devem ser adicionados às solicitações de geração.
7. Quando não houver evidência suficiente, o sistema deve informar essa condição.
8. Materiais rejeitados ou pendentes não devem participar da recuperação.
9. A coordenação deve possuir mecanismos para acompanhar e validar o uso da plataforma.

---

# Do protótipo ao produto

O projeto foi pensado para permitir uma evolução incremental.

| MVP / protótipo | Evolução do produto |
|---|---|
| Interface simples | Aplicação web com autenticação e perfis |
| Arquivo local para dados | Banco de dados relacional |
| Busca textual | Embeddings + índice vetorial |
| Recuperação básica | Pipeline RAG estruturado |
| Geração através de modelo | LLM integrado ao contexto recuperado |
| Arquivos de texto | Upload de PDF/DOCX com extração |
| Configuração em código | Regras configuráveis pela instituição |
| Uso local | Plataforma institucional multiusuário |

---

# Escopo do MVP

O MVP deve comprovar principalmente o ciclo:

```text
Cadastrar fonte
      ↓
Aprovar fonte
      ↓
Processar documento
      ↓
Indexar conteúdo
      ↓
Realizar uma pergunta
      ↓
Recuperar evidências
      ↓
Gerar resposta
      ↓
Exibir as fontes utilizadas
```

A partir desse núcleo, funcionalidades como geração de provas, padronização e dashboard podem evoluir sobre a mesma arquitetura.

---

# Estrutura sugerida do repositório

```text
agora-ai-platform/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── models/
│   └── repositories/
│
├── frontend/
│
├── rag/
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   └── generation/
│
├── data/
│
├── docs/
│   ├── requirements/
│   ├── architecture/
│   ├── diagrams/
│   └── research/
│
├── tests/
│
├── README.md
└── requirements.txt
```

A estrutura poderá ser alterada conforme a implementação evoluir.

---

# Fluxo técnico resumido

```text
Coordenação cadastra uma fonte
              ↓
         Fonte aprovada
              ↓
     Extração do conteúdo
              ↓
      Divisão em trechos
              ↓
           Embeddings
              ↓
        Índice vetorial
              ↓
Professor realiza uma solicitação
              ↓
API aplica permissões e regras
              ↓
Motor RAG recupera trechos relevantes
              ↓
Contexto + regras institucionais
              ↓
              LLM
              ↓
Resposta + evidências
              ↓
Professor revisa o resultado
```

---

# Segurança e governança

Por se tratar de uma plataforma institucional, a arquitetura deve considerar desde o início:

- autenticação;
- autorização baseada em perfil;
- isolamento entre instituições;
- controle de acesso por turma;
- histórico de alterações;
- identificação da origem dos conteúdos;
- estado de aprovação das fontes;
- rastreabilidade de conteúdos gerados.

---

# Visão futura

A evolução da Ágora pode incluir:

- dashboard institucional;
- histórico de gerações;
- templates personalizados;
- geração de planos de aula;
- novos formatos de avaliação;
- integração com sistemas acadêmicos;
- gestão mais detalhada de habilidades da BNCC;
- revisão colaborativa;
- métricas de uso;
- comparação entre versões;
- workflows de aprovação;
- novas fontes e formatos de arquivo.

---

# Diferencial da Ágora

A proposta da Ágora não é simplesmente adicionar um chatbot a uma escola.

A plataforma organiza o uso da Inteligência Artificial ao redor de três elementos:

### Contexto

A IA conhece o contexto pedagógico em que está sendo utilizada.

### Fonte

A geração é fundamentada nos materiais autorizados pela instituição.

### Governança

A instituição continua definindo seus padrões, materiais e critérios.

Por isso:

> **A IA serve à instituição — e não substitui seu currículo, suas fontes ou sua autonomia pedagógica.**

---

# Identidade

**Ágora**

**Saber com fonte.**

Uma plataforma institucional para criação, consulta e validação de conteúdos educacionais utilizando Inteligência Artificial baseada em fontes aprovadas.
