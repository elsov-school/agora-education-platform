# Integrante 3 — Consultas com evidências

**Responsabilidade:** Módulo de consulta — usa o CRUD 2; não tem banco próprio. **Branch de trabalho:** `feat/consultas`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte pesquisa somente o conteúdo aprovado e permitido para a pessoa logada. Quando encontra o termo, apresenta um trecho literal com a fonte. Não gera uma resposta inventada: se não houver evidência, o sistema informa a ausência.

## 2. Dados e ligação com o restante do sistema

Não há consultas.json. O módulo lê materiais pela biblioteca e recebe o usuário da sessão. O único efeito persistente da consulta bem-sucedida é pedir à biblioteca o incremento do campo usos.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Combine com usuários/materiais uma conta professora ativa com atribuição e uma fonte aprovada acessível. Não presuma que todo material da base já foi aprovado.
2. Menu do professor → 1: pesquise por título ou código da fonte. Mostre ID, disciplina e série; essa pesquisa não aumenta usos.
3. Menu → 3: consulte uma palavra literalmente presente no conteúdo. Aponte trecho, título, série, disciplina e BNCC.
4. Explique que a comparação usa minúsculas, mas o trecho exibido preserva o texto original, inclusive espaços. A primeira linha correspondente é exibida por material.
5. Pesquise algo que não existe, por exemplo termo_inexistente_ensaio. Mostre a mensagem de ausência e não invente uma resposta oral como se fosse do sistema.
6. Peça ao painel para conferir o uso registrado. Se duas fontes corresponderem, cada uma recebe um incremento; várias ocorrências na mesma fonte não multiplicam o uso naquela consulta.

## 4. Dicionário completo de funções

**Total neste escopo: 8 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `consultas/consultas.py` | [`_ler_termo`](#fn-consultas-_ler_termo) | Auxiliar interna |
| `consultas/consultas.py` | [`_materiais_aprovados`](#fn-consultas-_materiais_aprovados) | Auxiliar interna |
| `consultas/consultas.py` | [`_conteudo`](#fn-consultas-_conteudo) | Auxiliar interna |
| `consultas/consultas.py` | [`_habilidade`](#fn-consultas-_habilidade) | Auxiliar interna |
| `consultas/consultas.py` | [`pesquisar_material`](#fn-consultas-pesquisar_material) | Entrada ou função reutilizável |
| `consultas/consultas.py` | [`_trecho_literal`](#fn-consultas-_trecho_literal) | Auxiliar interna |
| `consultas/consultas.py` | [`consultar_com_evidencia`](#fn-consultas-consultar_com_evidencia) | Entrada ou função reutilizável |
| `consultas/consultas.py` | [`consultar_conteudo`](#fn-consultas-consultar_conteudo) | Entrada ou função reutilizável |

### Arquivo `consultas/consultas.py`

[Abrir fonte](consultas.py)

<a id="fn-consultas-_ler_termo"></a>

#### 01. `_ler_termo(usuario, pergunta)`

**Onde está:** [consultas/consultas.py, linha 7](consultas.py#L7).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida; `pergunta`: texto exibido ao pedir entrada.

**O que faz / resultado:** Exige uma sessão com ativo=True, usa ler_texto para entrada obrigatória e devolve o termo em minúsculas ou None.

**Como apresentar:** Mostre uma pesquisa sem diferenciar maiúsculas de minúsculas. A revalidação no cadastro acontece no filtro seguinte.

<a id="fn-consultas-_materiais_aprovados"></a>

#### 02. `_materiais_aprovados(usuario)`

**Onde está:** [consultas/consultas.py, linha 14](consultas.py#L14).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Carrega a biblioteca, aplica o filtro de usuários e mantém apenas aprovados, inclusive para consultas da coordenação. Devolve lista ou None em falha.

**Como apresentar:** Explique que coordenação pode ver pendentes na gestão, mas não usá-los como evidência nesta consulta.

<a id="fn-consultas-_conteudo"></a>

#### 03. `_conteudo(material)`

**Onde está:** [consultas/consultas.py, linha 32](consultas.py#L32).

**Entradas:** `material`: dicionário de um material.

**O que faz / resultado:** Devolve conteudo_texto ou, se a chave nova não existir, o campo legado conteudo; usa texto vazio como padrão final.

**Como apresentar:** Mostre no código a compatibilidade com materiais antigos, sem duplicar a base de dados.

<a id="fn-consultas-_habilidade"></a>

#### 04. `_habilidade(material)`

**Onde está:** [consultas/consultas.py, linha 36](consultas.py#L36).

**Entradas:** `material`: dicionário de um material.

**O que faz / resultado:** Devolve habilidade_bncc ou o campo legado bncc quando a chave nova não existe; padrão final é texto vazio.

**Como apresentar:** Explique que exibir um código cadastrado não equivale a certificar o alinhamento pedagógico à BNCC.

<a id="fn-consultas-pesquisar_material"></a>

#### 05. `pesquisar_material(usuario=None)`

**Onde está:** [consultas/consultas.py, linha 40](consultas.py#L40).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Busca termo em título, disciplina, série, conteúdo e habilidade dos materiais permitidos/aprovados; imprime resultados ou ausência. Não incrementa usos nem retorna lista.

**Como apresentar:** Pesquise pelo título e confira que o contador não muda só por listar uma fonte.

<a id="fn-consultas-_trecho_literal"></a>

#### 06. `_trecho_literal(material, termo)`

**Onde está:** [consultas/consultas.py, linha 64](consultas.py#L64).

**Entradas:** `material`: dicionário de um material; `termo`: texto normalizado que a consulta procura.

**O que faz / resultado:** Percorre linhas do conteúdo e devolve a primeira linha que contém o termo, preservando seus caracteres; se não encontrar, devolve None.

**Como apresentar:** Se o conteúdo tem uma única linha, ela será mostrada inteira; a função não resume nem busca por significado.

<a id="fn-consultas-consultar_com_evidencia"></a>

#### 07. `consultar_com_evidencia(usuario)`

**Onde está:** [consultas/consultas.py, linha 71](consultas.py#L71).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Exibe trecho e fonte de cada material correspondente; chama registrar_uso uma vez por material encontrado e avisa se essa contagem falhar. Não tem retorno explícito.

**Como apresentar:** Busque uma palavra real, aponte título/série/BNCC e teste uma palavra ausente. Mais ocorrências na mesma fonte não somam mais usos na mesma consulta.

<a id="fn-consultas-consultar_conteudo"></a>

#### 08. `consultar_conteudo(usuario=None)`

**Onde está:** [consultas/consultas.py, linha 102](consultas.py#L102).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Entrada de compatibilidade que encaminha ao consultar_com_evidencia com o usuário recebido; não acrescenta busca nem persistência própria.

**Como apresentar:** Explique a diferença entre um nome antigo mantido para compatibilidade e uma segunda implementação da mesma regra.

## 5. Perguntas técnicas e respostas para ensaiar

### Isso usa IA ou RAG?

Não usa modelo de linguagem, embeddings ou recuperação semântica. É busca textual em arquivos locais com identificação explícita da fonte.

### A palavra precisa ser exatamente igual?

É busca de substring sem distinguir maiúsculas. Não há normalização geral de acentos, sinônimos ou entendimento de perguntas.

### O que é uma evidência?

Uma linha real do conteúdo cadastrado que contém o termo, mostrada junto com sua origem; não é uma conclusão automaticamente validada.

### Por que duas funções para pesquisa e consulta?

Pesquisa ajuda a localizar materiais e não conta uso. Consulta apresenta trecho como evidência e registra o uso da fonte encontrada.

### Quem impede leitura de outra turma?

O filtro do módulo usuários, reaproveitado aqui antes da busca. A consulta ainda exige aprovado_coordenacao, inclusive para a coordenação.

### E se falhar a contagem?

O trecho já encontrado é apresentado, e o sistema avisa que não conseguiu registrar o uso. Não há uma transação única juntando impressão de tela e JSON.

## 6. Limites que precisam ser apresentados com honestidade

Não é chatbot nem gerador de resumo. Em material de linha única, a evidência pode ser o conteúdo inteiro. A busca não remove acentos nem registra um histórico de perguntas. Não prometer resposta para toda pergunta do professor.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_consultas.py -v
```

Para a suíte inteira: `py -B -m unittest discover -s tests -v`. A última verificação de código anterior a estes guias teve **77 testes aprovados**; a quantidade pode mudar em novas versões. Os testes usam dados temporários, não os cadastros pessoais da apresentação.

## 8. Checklist do integrante

- [ ] Sei resumir meu módulo sem ler o código inteiro.
- [ ] Sei apontar a função chamada pelo menu e as auxiliares que ela usa.
- [ ] Sei explicar os argumentos, o retorno e onde ocorre a gravação.
- [ ] Tenho uma conta e dados de ensaio; anotei os IDs reais produzidos, sem presumir que serão 1 ou 4.
- [ ] Demonstro um caso válido e um inválido sem corromper dados ou apagar a única coordenação.
- [ ] Sei qual parte do fluxo pertence ao colega e não atribuo a mim funções de outro módulo.
- [ ] Sei reconhecer os limites descritos acima sem prometer funcionalidades ausentes.
