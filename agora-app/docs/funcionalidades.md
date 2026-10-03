# Descrição das funcionalidades implementadas

O **Agora** é um protótipo acadêmico de apoio ao letramento em inteligência artificial. A aplicação utiliza Python e restringe a geração e a consulta aos materiais institucionais aprovados, preservando a origem das informações.

## FN-01 — Biblioteca curricular

- **Objetivo:** centralizar o acervo pedagógico aprovado pela escola e transformá-lo na fonte institucional das demais funcionalidades.
- **Usuário:** coordenação (gestão completa) e professor (consulta restrita ao próprio perfil).
- **Descrição:** permite adicionar materiais e gerenciá-los por visualização, edição e exclusão. A listagem possui pesquisa textual e filtros por disciplina, turma, bimestre e habilidade BNCC. Professores visualizam somente as combinações de turma e disciplina associadas ao perfil simulado.
- **Entrada:** título, tipo, ano letivo, turma, disciplina, bimestre, BNCC, autor/fonte, conteúdo e status de aprovação; termos e filtros de pesquisa.
- **Processamento:** validação dos campos, persistência SQLite, composição dinâmica dos filtros e aplicação do recorte de acesso do professor. Somente materiais aprovados alimentam o gerador e o assistente.
- **Saída:** catálogo filtrado, página de detalhes e mensagens de confirmação ou erro.
- **Estruturas de dados Python utilizadas:** dicionários representam materiais e filtros; listas representam a coleção resultante; tupla `MATERIAL_FIELDS` define os campos persistidos.

## FN-02 — Gerador de provas e atividades

- **Objetivo:** criar atividades rastreáveis sem adicionar informação externa às fontes selecionadas.
- **Usuário:** professor.
- **Descrição:** o professor escolhe turma, disciplina, fontes aprovadas, quantidade, tipo e dificuldade. O gerador local extrai trechos dos materiais e cria questões de múltipla escolha, discursivas ou de verdadeiro/falso. No rascunho, é possível editar, excluir ou trocar uma questão e consultar o gabarito e a fonte.
- **Entrada:** contexto da turma e disciplina, IDs dos materiais, quantidade, tipo e dificuldade.
- **Processamento:** conferência do perfil, das regras institucionais e do status das fontes; separação do conteúdo em sentenças; construção determinística das questões; registro do vínculo entre atividade, questão e material.
- **Saída:** prova/atividade com cabeçalho, questões, gabaritos, dificuldade e referências.
- **Estruturas de dados Python utilizadas:** lista ordena o conjunto de questões e o conjunto de sentenças; dicionário representa cada questão gerada; tupla `TIPOS_QUESTAO` mantém as opções fixas aceitas.

## FN-03 — Assistente de consulta com evidências

- **Objetivo:** responder dúvidas do professor exclusivamente com evidências do acervo aprovado.
- **Usuário:** professor.
- **Descrição:** recebe uma pergunta contextualizada por turma e disciplina, compara seus termos aos trechos dos materiais aprovados e apresenta a resposta acompanhada das fontes. Quando a sobreposição textual é insuficiente, declara explicitamente que não encontrou evidência.
- **Fluxo complementar do wireframe:** o professor também pode colar um conteúdo externo. O sistema separa suas afirmações, compara cada uma à base aprovada e classifica o resultado como Suportado, Parcialmente suportado ou Não localizado, exibindo o trecho e o material que fundamentam cada diagnóstico.
- **Entrada:** turma, disciplina e pergunta em linguagem natural.
- **Processamento:** normalização de texto, remoção de palavras muito comuns, cálculo de sobreposição entre termos e classificação dos trechos relacionados.
- **Saída:** resposta extrativa com material, habilidade BNCC e trecho utilizado, ou mensagem de evidência insuficiente.
- **Saída complementar:** relatório persistente com contadores, afirmações analisadas, evidências localizadas e alertas de conteúdo sem sustentação institucional.
- **Estruturas de dados Python utilizadas:** conjunto para termos normalizados e palavras irrelevantes; lista de tuplas `(pontuação, trecho, material)` para classificação; lista de dicionários para as evidências exibidas.

## FN-04 — Validação e aprovação de conteúdos

- **Objetivo:** representar o controle institucional antes do uso de uma atividade em sala.
- **Usuário:** professor e coordenação.
- **Descrição:** atividades passam pelos estados Rascunho, Pendente de validação, Aprovado ou Reprovado. O professor envia um rascunho; a coordenação consulta as pendências, abre o conteúdo, aprova ou reprova e registra observação, responsável e data. Uma reprovação exige justificativa e pode ser corrigida e reenviada.
- **Entrada:** ação de envio; decisão da coordenação e observação/justificativa.
- **Processamento:** máquina de estados simples, validação das transições, bloqueio de edição enquanto o conteúdo aguarda análise e persistência do parecer.
- **Saída:** status atualizado, identificação do revisor, data e devolutiva institucional.
- **Estruturas de dados Python utilizadas:** tupla `STATUS_CONTEUDO` documenta os estados possíveis; dicionários representam atividades; listas representam a fila de pendências.

## FN-05 — Padronização institucional

- **Objetivo:** permitir que a escola governe a produção gerada pelo protótipo.
- **Usuário:** coordenação.
- **Descrição:** configura quantidade máxima de questões, tipos permitidos, dificuldade padrão, fonte obrigatória, cabeçalho, critérios de qualidade, regras de aprovação e instruções. Não é uma tela decorativa: quantidade e tipos são validados pelo serviço gerador; a dificuldade é pré-selecionada; a fonte acompanha cada questão; o cabeçalho e as instruções aparecem no fluxo.
- **Entrada:** regras numéricas, seleções e textos institucionais.
- **Processamento:** validação contra as opções fixas e armazenamento de tipos em JSON dentro do SQLite; leitura das configurações a cada geração e visualização.
- **Saída:** padrões persistidos e aplicados às atividades seguintes.
- **Estruturas de dados Python utilizadas:** dicionário concentra a configuração vigente; lista armazena os tipos habilitados; tuplas `TIPOS_QUESTAO` e `DIFICULDADES` validam opções fixas.

## FN-06 — Painel da coordenação

- **Objetivo:** oferecer uma visão consolidada do uso real do protótipo.
- **Usuário:** coordenação.
- **Descrição:** mostra total de materiais, materiais aprovados, pendências, atividades, distribuição por disciplina e turma, materiais mais utilizados, produção por professor e movimentações recentes.
- **Entrada:** registros persistidos nas tabelas de materiais, atividades, questões, usuários e uso de materiais.
- **Processamento:** consultas agregadas SQLite (`COUNT`, `GROUP BY` e ordenação) e cálculo da proporção das barras do gráfico no serviço Python.
- **Saída:** indicadores, gráfico simples e listas classificadas, sempre derivados do banco atual.
- **Estruturas de dados Python utilizadas:** dicionário agrupa os indicadores; listas de dicionários armazenam séries, rankings e atividades recentes.

## Estruturas exigidas na disciplina

As estruturas não são artificiais: listas são usadas para coleções ordenadas e resultados; dicionários modelam registros e configurações; tuplas representam conjuntos fixos ou itens de classificação. Exemplos explícitos estão comentados em `config.py`, `database.py`, `services/generator.py` e `services/assistant.py`.
