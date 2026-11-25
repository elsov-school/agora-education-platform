# Integrante 5 — Padrões institucionais e exportação

**Responsabilidade:** Módulo de configuração/exportação — apoia o CRUD 3. **Branch de trabalho:** `feat/padroes-exportacao`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte garante uma apresentação comum para as provas. A coordenação configura escola, instruções e limite de questões. Eu valido os dados e produzo dois arquivos separados: a prova do aluno e o gabarito do professor.

## 2. Dados e ligação com o restante do sistema

`regras.json` é um objeto com nome_escola, max_questoes e instrucoes. `institucional_v1` é a estrutura de modelo reconhecida no código. A prova chega como dicionário do módulo provas; os TXT ficam em exportacoes/. Não existe uma segunda base de provas neste módulo.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Entre como coordenação. Menu → 4: altere nome da escola e instruções de ensaio; use um limite positivo. Não use valores pessoais ou definitivos só para demonstrar.
2. Repita a configuração com limite 0 para mostrar recusa; depois use Enter para manter os valores atuais e confirme a persistência.
3. Receba do responsável por provas o ID de uma avaliação salva. Como autor ou coordenação, abra o menu de provas → 5 e informe o ID.
4. Abra exportacoes/prova_aluno_ID.txt e mostre cabeçalho, instruções, enunciados e alternativas. Abra gabarito_professor_ID.txt para respostas e critérios.
5. Explique que exportar_prova, no módulo provas, confere autoria e carrega o objeto; exportar_prova_formatada recebe o objeto pronto para formatar.
6. Se o professor perguntar sobre falhas, mostre o teste de recuperação da segunda gravação; não simule uma queda do computador nem corrompa o arquivo real.

## 4. Dicionário completo de funções

**Total neste escopo: 16 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `padroes/padroes.py` | [`obter_modelo`](#fn-padroes-obter_modelo) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`_tem_texto`](#fn-padroes-_tem_texto) | Auxiliar interna |
| `padroes/padroes.py` | [`carregar_regras`](#fn-padroes-carregar_regras) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`_gravar_texto`](#fn-padroes-_gravar_texto) | Auxiliar interna |
| `padroes/padroes.py` | [`_coordenacao_ativa`](#fn-padroes-_coordenacao_ativa) | Auxiliar interna |
| `padroes/padroes.py` | [`configurar_padrao_escola`](#fn-padroes-configurar_padrao_escola) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`_validar_questao`](#fn-padroes-_validar_questao) | Auxiliar interna |
| `padroes/padroes.py` | [`_validar_prova`](#fn-padroes-_validar_prova) | Auxiliar interna |
| `padroes/padroes.py` | [`validar_prova`](#fn-padroes-validar_prova) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`_cabecalho`](#fn-padroes-_cabecalho) | Auxiliar interna |
| `padroes/padroes.py` | [`_texto_aluno`](#fn-padroes-_texto_aluno) | Auxiliar interna |
| `padroes/padroes.py` | [`formatar_prova`](#fn-padroes-formatar_prova) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`_linhas_gabarito`](#fn-padroes-_linhas_gabarito) | Auxiliar interna |
| `padroes/padroes.py` | [`_id_para_arquivo`](#fn-padroes-_id_para_arquivo) | Auxiliar interna |
| `padroes/padroes.py` | [`exportar_prova_formatada`](#fn-padroes-exportar_prova_formatada) | Entrada ou função reutilizável |
| `padroes/padroes.py` | [`exportar_atividade`](#fn-padroes-exportar_atividade) | Entrada ou função reutilizável |

### Arquivo `padroes/padroes.py`

[Abrir fonte](padroes.py)

<a id="fn-padroes-obter_modelo"></a>

#### 01. `obter_modelo(nome='institucional_v1')`

**Onde está:** [padroes/padroes.py, linha 26](padroes.py#L26).

**Entradas:** `nome`: nome do professor ou nome do modelo, conforme a função.

**O que faz / resultado:** Aceita institucional_v1 e devolve uma cópia das listas e do dicionário de regras do modelo; nome desconhecido lança ValueError.

**Como apresentar:** Diferencie a estrutura fixa do modelo das regras escolares editáveis em regras.json.

<a id="fn-padroes-_tem_texto"></a>

#### 02. `_tem_texto(valor)`

**Onde está:** [padroes/padroes.py, linha 39](padroes.py#L39).

**Entradas:** `valor`: valor a validar.

**O que faz / resultado:** Devolve True apenas para string que não fica vazia após strip; não altera o valor original.

**Como apresentar:** Mostre por que uma string só com espaços não satisfaz campo obrigatório.

<a id="fn-padroes-carregar_regras"></a>

#### 03. `carregar_regras()`

**Onde está:** [padroes/padroes.py, linha 43](padroes.py#L43).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê regras.json, exige objeto com nome/instruções preenchidos e max_questoes inteiro positivo; devolve dicionário ou lança erro.

**Como apresentar:** Mostre os nomes dos campos usando regras demonstrativas, sem expor configurações pessoais.

<a id="fn-padroes-_gravar_texto"></a>

#### 04. `_gravar_texto(caminho, texto)`

**Onde está:** [padroes/padroes.py, linha 62](padroes.py#L62).

**Entradas:** `caminho`: caminho do arquivo; `texto`: string que será gravada/impressa.

**O que faz / resultado:** Escreve texto em diretório temporário ao lado do destino e substitui o arquivo com os.replace. Não tem retorno explícito.

**Como apresentar:** Explique que preparar o arquivo antes de substituir reduz risco de truncar o anterior numa falha de escrita.

<a id="fn-padroes-_coordenacao_ativa"></a>

#### 05. `_coordenacao_ativa(usuario)`

**Onde está:** [padroes/padroes.py, linha 72](padroes.py#L72).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Confere dicionário, perfil coordenacao e ativo=True; devolve booleano. Não consulta arquivo sozinha.

**Como apresentar:** Aponte que configurar_padrao_escola ainda relê o cadastro; este helper é só uma parte da autorização.

<a id="fn-padroes-configurar_padrao_escola"></a>

#### 06. `configurar_padrao_escola(usuario)`

**Onde está:** [padroes/padroes.py, linha 77](padroes.py#L77).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Confere coordenação ativa no cadastro, solicita nome da escola, limite e instruções, grava e devolve regras ou None em erro.

**Como apresentar:** Use Enter para manter um valor e tente limite 0. O limite inválido não deve alterar o arquivo.

<a id="fn-padroes-_validar_questao"></a>

#### 07. `_validar_questao(questao, numero, exigir_detalhes)`

**Onde está:** [padroes/padroes.py, linha 110](padroes.py#L110).

**Entradas:** `questao`: dicionário de uma questão; `numero`: número de exibição, iniciando em 1; `exigir_detalhes`: booleano que exige tipo e dificuldade.

**O que faz / resultado:** Confere enunciado, resposta, critério e alternativas; exigir_detalhes determina se tipo/dificuldade são obrigatórios. Lança erros, sem retorno útil.

**Como apresentar:** Explique a compatibilidade da API antiga e o rigor maior ao gerar o par de arquivos atual.

<a id="fn-padroes-_validar_prova"></a>

#### 08. `_validar_prova(dados_prova, regras, exigir_detalhes=False)`

**Onde está:** [padroes/padroes.py, linha 137](padroes.py#L137).

**Entradas:** `dados_prova`: dicionário de prova/rascunho; `regras`: dicionário de regras institucionais; `exigir_detalhes`: booleano que exige tipo e dificuldade.

**O que faz / resultado:** Valida dicionário, campos de contexto, lista não vazia de questões, limite escolar e modelo. Chama o validador de cada questão; não grava.

**Como apresentar:** Aponte a comparação len(questoes) > max_questoes como regra institucional aplicada na exportação.

<a id="fn-padroes-validar_prova"></a>

#### 09. `validar_prova(dados_prova)`

**Onde está:** [padroes/padroes.py, linha 157](padroes.py#L157).

**Entradas:** `dados_prova`: dicionário de prova/rascunho.

**O que faz / resultado:** Lê regras atuais, chama a validação interna e devolve True se não houver exceção. Erros sobem para o chamador tratar.

**Como apresentar:** Diferencie retorno False de exceção: nesta função o caminho inválido lança erro.

<a id="fn-padroes-_cabecalho"></a>

#### 10. `_cabecalho(titulo, prova, regras)`

**Onde está:** [padroes/padroes.py, linha 163](padroes.py#L163).

**Entradas:** `titulo`: título da tela ou do material; `prova`: dicionário de prova salva ou rascunho conforme a função; `regras`: dicionário de regras institucionais.

**O que faz / resultado:** Monta e devolve lista de linhas com título, escola, disciplina, série, bimestre e professor/número de autor quando disponível.

**Como apresentar:** Mostre a reutilização do mesmo cabeçalho nos arquivos do aluno e do professor.

<a id="fn-padroes-_texto_aluno"></a>

#### 11. `_texto_aluno(prova, regras)`

**Onde está:** [padroes/padroes.py, linha 178](padroes.py#L178).

**Entradas:** `prova`: dicionário de prova salva ou rascunho conforme a função; `regras`: dicionário de regras institucionais.

**O que faz / resultado:** Monta e devolve texto da prova com instruções, questões numeradas e alternativas rotuladas; não acrescenta gabarito nem critérios.

**Como apresentar:** Abra o TXT do aluno e aponte que só recebe os campos destinados à prova, sem afirmar inspeção semântica do texto livre.

<a id="fn-padroes-formatar_prova"></a>

#### 12. `formatar_prova(dados_prova, modelo)`

**Onde está:** [padroes/padroes.py, linha 201](padroes.py#L201).

**Entradas:** `dados_prova`: dicionário de prova/rascunho; `modelo`: nome ou dicionário do modelo.

**O que faz / resultado:** Aceita modelo por nome/dicionário, valida contra regras vigentes e devolve texto do aluno sem criar arquivo.

**Como apresentar:** Explique que montar uma string e persistir essa string são etapas diferentes.

<a id="fn-padroes-_linhas_gabarito"></a>

#### 13. `_linhas_gabarito(prova)`

**Onde está:** [padroes/padroes.py, linha 213](padroes.py#L213).

**Entradas:** `prova`: dicionário de prova salva ou rascunho conforme a função.

**O que faz / resultado:** Devolve linhas numeradas com respostas e critérios de correção, mais uma linha final de separação.

**Como apresentar:** Compare com o aluno para mostrar onde as respostas são incluídas de propósito.

<a id="fn-padroes-_id_para_arquivo"></a>

#### 14. `_id_para_arquivo(atividade_id)`

**Onde está:** [padroes/padroes.py, linha 222](padroes.py#L222).

**Entradas:** `atividade_id`: ID da prova salva.

**O que faz / resultado:** Converte ID para texto e exige dígitos ASCII de um inteiro positivo; devolve o texto ou lança ValueError.

**Como apresentar:** Mostre que ../arquivo não é aceito como ID para compor o nome do TXT.

<a id="fn-padroes-exportar_prova_formatada"></a>

#### 15. `exportar_prova_formatada(prova, destino=None)`

**Onde está:** [padroes/padroes.py, linha 229](padroes.py#L229).

**Entradas:** `prova`: dicionário de prova salva ou rascunho conforme a função; `destino`: diretório ou caminho de saída, conforme a API; None usa exportacoes/.

**O que faz / resultado:** Valida a prova, prepara as duas versões em pasta exclusiva por ID e publica aluno/gabarito; devolve [caminho_aluno, caminho_professor]. Tem recuperação para falha na segunda substituição.

**Como apresentar:** Abra ambos os arquivos. Explique que reexportar o mesmo ID atualiza as versões e que isso não é transação de banco nem proteção contra toda queda do computador.

<a id="fn-padroes-exportar_atividade"></a>

#### 16. `exportar_atividade(dados_prova, destino, incluir_gabarito=False)`

**Onde está:** [padroes/padroes.py, linha 272](padroes.py#L272).

**Entradas:** `dados_prova`: dicionário de prova/rascunho; `destino`: diretório ou caminho de saída, conforme a API; None usa exportacoes/; `incluir_gabarito`: booleano para acrescentar gabarito ao arquivo da API antiga.

**O que faz / resultado:** API anterior: exporta um único TXT, com gabarito opcional no mesmo arquivo, e devolve o caminho. Usa as regras vigentes.

**Como apresentar:** Diferencie esta compatibilidade do fluxo principal, que usa exportar_prova_formatada para separar aluno e professor.

## 5. Perguntas técnicas e respostas para ensaiar

### Por que gerar dois arquivos?

Aluno recebe questões, professor recebe respostas e critérios. O código monta textos distintos em vez de reutilizar o texto de revisão inteiro.

### O aluno nunca verá resposta?

A montagem não acrescenta campos gabarito/criterio_correcao. Ela não detecta se alguém escreveu uma resposta dentro do próprio enunciado ou das instruções; a revisão humana continua necessária.

### Quem confere autoria?

O módulo provas faz autorização e leitura por ID. Padrões valida o objeto e o formato, não faz novo login nem substitui a verificação de autoria.

### Por que validar de novo ao exportar?

Uma prova antiga ou recebida por outra chamada pode estar incompleta ou exceder o limite institucional atual.

### O TXT é PDF ou Word?

Não. É texto UTF-8. Não há dependências de editor de texto nem geração de PDF neste fluxo.

### As regras são guardadas por prova?

Não. A exportação aplica regras.json vigente. Alterar a escola ou o limite pode mudar ou impedir uma reexportação futura.

### Como evitar arquivo pela metade?

O texto é preparado antes da substituição. O par usa diretório exclusivo e recuperação se falhar a troca do gabarito. Isso reduz falhas comuns, sem equivaler a uma transação durável em dois arquivos.

## 6. Limites que precisam ser apresentados com honestidade

Sem PDF, DOCX, envio de e-mail ou impressão automática. Só institucional_v1 é reconhecido. Reexportação do mesmo ID substitui os TXT; não há histórico de versões de exportação. As permissões do sistema operacional sobre a pasta continuam importantes.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_padroes.py -v
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
