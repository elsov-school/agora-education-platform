# Integrante 6 — Painel, menus e integração

**Responsabilidade:** CRUD 4 — Consultas agregadas e coordenação do fluxo. **Branch de trabalho:** `feat/painel-menu`.

**Base conferida:** código da main no commit `caf60f1`. Este guia contém as funções de aplicação, inclusive auxiliares; não lista funções dos arquivos de teste nem métodos da biblioteca padrão como se fossem funções criadas pelo grupo.

[Índice dos seis guias](../GUIAS_APRESENTACAO.md) · [Dicionário técnico comum](../DICIONARIO_TECNICO.md)

## 1. Abertura: o que falar em 30 segundos

> Minha parte liga os módulos em um único programa. O main faz login e abre o menu correto para cada perfil. O painel relê os arquivos e transforma provas e materiais em contagens, porcentagens, rankings e fila de aprovação, sem gravar um banco de métricas.

## 2. Dados e ligação com o restante do sistema

Não há painel.json. O painel lê usuarios/usuarios.json, materiais/materiais.json e provas/atividades.json. Cálculos usam dicionários de contagem e listas de tuplas. O main recebe o dicionário autenticado e o passa aos módulos.

Leia o código, não o JSON pessoal de quem está apresentando. Não projete senhas, hashes ou e-mails reais. Cada integrante deve saber qual função recebe do colega e qual entrega para o seguinte.

## 3. Roteiro prático de apresentação

1. Execute py main.py e entre com e-mail/senha da coordenação; mostre as seis opções. Use 9 para trocar e mostre o menu diferente de um professor.
2. Retorne à coordenação → 5: apresente as opções 1 (professor), 2 (disciplina), 7 (série), 4 (fila) e 6 (resumo de materiais).
3. Após o grupo fazer uma consulta e salvar uma prova com uma fonte nova, mostre opção 8: a fonte terá dois usos se foi usada exatamente nessas duas operações.
4. Mostre opção 3 de citações para distinguir referência presente em prova do contador de usos. Uma consulta aumenta usos, mas não cria uma citação no histórico de provas.
5. Use opção 5 para painel completo. Aponte aprovados/pendentes, autores inativos preservados e professores ativos sem provas com total zero.
6. Explique que 0 sai do painel para o menu e 0 no menu de perfil encerra o programa. Reabra o programa e mostre o histórico persistente.
7. Apresente o teste integrado: ele executa main.py em processos separados com cópias temporárias e verifica permissões, exportação, reinício e que o painel não alterou os JSONs.

## 4. Dicionário completo de funções

**Total neste escopo: 24 funções definidas.** A ordem abaixo acompanha o código. A assinatura mostra os argumentos e valores padrão; `None` não é uma sessão autorizada. As auxiliares com `_` são convenção interna, não barreira de segurança.

Para cada item: a assinatura diz o que entra; a descrição informa resultado, efeito e principais recusas; a fala indicada ensina como demonstrar. Helpers não precisam de uma opção própria no menu: apresente seu papel no código ou nos testes.

### Lista rápida para consulta

| Arquivo | Função | Papel |
| --- | --- | --- |
| `painel/painel.py` | [`ler_lista`](#fn-painel-ler_lista) | Entrada ou função reutilizável |
| `painel/painel.py` | [`ler_atividades`](#fn-painel-ler_atividades) | Entrada ou função reutilizável |
| `painel/painel.py` | [`ler_usuarios_por_id`](#fn-painel-ler_usuarios_por_id) | Entrada ou função reutilizável |
| `painel/painel.py` | [`contar_atividades_por_professor`](#fn-painel-contar_atividades_por_professor) | Entrada ou função reutilizável |
| `painel/painel.py` | [`contar_atividades_por_disciplina`](#fn-painel-contar_atividades_por_disciplina) | Entrada ou função reutilizável |
| `painel/painel.py` | [`contar_atividades_por_serie`](#fn-painel-contar_atividades_por_serie) | Entrada ou função reutilizável |
| `painel/painel.py` | [`listar_materiais_mais_usados`](#fn-painel-listar_materiais_mais_usados) | Entrada ou função reutilizável |
| `painel/painel.py` | [`listar_materiais_mais_citados`](#fn-painel-listar_materiais_mais_citados) | Entrada ou função reutilizável |
| `painel/painel.py` | [`listar_materiais_pendentes`](#fn-painel-listar_materiais_pendentes) | Entrada ou função reutilizável |
| `painel/painel.py` | [`titulo_secao`](#fn-painel-titulo_secao) | Entrada ou função reutilizável |
| `painel/painel.py` | [`percentual`](#fn-painel-percentual) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_atividades_por_professor`](#fn-painel-mostrar_atividades_por_professor) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_atividades_por_disciplina`](#fn-painel-mostrar_atividades_por_disciplina) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_atividades_por_serie`](#fn-painel-mostrar_atividades_por_serie) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_distribuicao`](#fn-painel-mostrar_distribuicao) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_materiais_mais_citados`](#fn-painel-mostrar_materiais_mais_citados) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_materiais_mais_usados`](#fn-painel-mostrar_materiais_mais_usados) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_fila_pendentes`](#fn-painel-mostrar_fila_pendentes) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_resumo`](#fn-painel-mostrar_resumo) | Entrada ou função reutilizável |
| `painel/painel.py` | [`mostrar_painel_completo`](#fn-painel-mostrar_painel_completo) | Entrada ou função reutilizável |
| `painel/painel.py` | [`menu_painel`](#fn-painel-menu_painel) | Entrada ou função reutilizável |
| `main.py` | [`menu_coordenacao`](#fn-main-menu_coordenacao) | Entrada ou função reutilizável |
| `main.py` | [`menu_professor`](#fn-main-menu_professor) | Entrada ou função reutilizável |
| `main.py` | [`menu_principal`](#fn-main-menu_principal) | Entrada ou função reutilizável |

### Arquivo `painel/painel.py`

[Abrir fonte](painel.py)

<a id="fn-painel-ler_lista"></a>

#### 01. `ler_lista(caminho)`

**Onde está:** [painel/painel.py, linha 30](painel.py#L30).

**Entradas:** `caminho`: caminho do arquivo.

**O que faz / resultado:** Lê JSON de um caminho e exige lista de dicionários; devolve a lista ou lança erro. Não inicia exemplos nem migra/grava dados.

**Como apresentar:** Diga que calcular uma métrica não deve mudar o arquivo usado como fonte.

<a id="fn-painel-ler_atividades"></a>

#### 02. `ler_atividades()`

**Onde está:** [painel/painel.py, linha 39](painel.py#L39).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Compatibilidade: chama ler_lista para atividades e devolve [] com aviso em caso de erro.

**Como apresentar:** Explique que o menu usa leituras com tratamento explícito de erro; não alegue que [] sempre prova ausência de dados.

<a id="fn-painel-ler_usuarios_por_id"></a>

#### 03. `ler_usuarios_por_id()`

**Onde está:** [painel/painel.py, linha 48](painel.py#L48).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Lê usuários e devolve mapa {id: dicionário}; facilita ligar professor_id ao nome exibido.

**Como apresentar:** Mostre como uma referência numérica vira nome sem duplicar o nome dentro de toda prova.

<a id="fn-painel-contar_atividades_por_professor"></a>

#### 04. `contar_atividades_por_professor(atividades)`

**Onde está:** [painel/painel.py, linha 60](painel.py#L60).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Agrupa a lista recebida por professor_id e devolve {id: quantidade}; não lê arquivo nem imprime.

**Como apresentar:** Com dois registros do mesmo autor, acompanhe a soma de 0 para 1 e de 1 para 2.

<a id="fn-painel-contar_atividades_por_disciplina"></a>

#### 05. `contar_atividades_por_disciplina(atividades)`

**Onde está:** [painel/painel.py, linha 72](painel.py#L72).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Agrupa provas por disciplina, usando Sem disciplina quando falta valor, e devolve dicionário de contagens.

**Como apresentar:** Explique a diferença entre quantidade de provas e quantidade de questões dentro das provas.

<a id="fn-painel-contar_atividades_por_serie"></a>

#### 06. `contar_atividades_por_serie(atividades)`

**Onde está:** [painel/painel.py, linha 83](painel.py#L83).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Agrupa provas por série, usando Sem série para valor ausente, e devolve dicionário de contagens.

**Como apresentar:** Mostre a opção 7 do painel e relacione o resultado ao campo serie salvo nas provas.

<a id="fn-painel-listar_materiais_mais_usados"></a>

#### 07. `listar_materiais_mais_usados(materiais)`

**Onde está:** [painel/painel.py, linha 91](painel.py#L91).

**Entradas:** `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Devolve até três tuplas (id, título, usos), só com usos inteiros positivos; ordena por usos decrescentes, título sem caixa e ID.

**Como apresentar:** Mostre o Top 3 e explique o desempate e por que material com zero uso não entra.

<a id="fn-painel-listar_materiais_mais_citados"></a>

#### 08. `listar_materiais_mais_citados(atividades, materiais)`

**Onde está:** [painel/painel.py, linha 102](painel.py#L102).

**Entradas:** `atividades`: lista de provas usadas na agregação; `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Conta referências nos registros de provas, uma vez por material em cada prova; devolve ranking de tuplas. Referência sem material recebe rótulo de removido.

**Como apresentar:** Compare duas referências repetidas na mesma prova com referências em duas provas diferentes.

<a id="fn-painel-listar_materiais_pendentes"></a>

#### 09. `listar_materiais_pendentes(materiais)`

**Onde está:** [painel/painel.py, linha 131](painel.py#L131).

**Entradas:** `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Devolve materiais pendentes ordenados por ID; registros legados sem status são tratados como pendentes.

**Como apresentar:** Explique que listar a fila não aprova nenhum item; a aprovação pertence a materiais.

<a id="fn-painel-titulo_secao"></a>

#### 10. `titulo_secao(texto)`

**Onde está:** [painel/painel.py, linha 149](painel.py#L149).

**Entradas:** `texto`: string que será gravada/impressa.

**O que faz / resultado:** Imprime separadores e um título, sem retorno útil e sem acesso a arquivos.

**Como apresentar:** Mostre como centraliza a aparência das seções sem repetir os prints em todas as telas.

<a id="fn-painel-percentual"></a>

#### 11. `percentual(parte, total)`

**Onde está:** [painel/painel.py, linha 155](painel.py#L155).

**Entradas:** `parte`: quantidade de um grupo; `total`: quantidade total usada na divisão.

**O que faz / resultado:** Devolve uma string de porcentagem arredondada, ou 0% se o total é zero.

**Como apresentar:** Use o exemplo percentual(1, 4) → 25% e explique o tratamento de divisão por zero.

<a id="fn-painel-mostrar_atividades_por_professor"></a>

#### 12. `mostrar_atividades_por_professor(atividades)`

**Onde está:** [painel/painel.py, linha 161](painel.py#L161).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Combina contagens e cadastro, inclui professores ativos com zero provas, mantém autores inativos e imprime números/percentuais.

**Como apresentar:** Aponte que desativar um professor não apaga a autoria nem remove suas provas da contagem.

<a id="fn-painel-mostrar_atividades_por_disciplina"></a>

#### 13. `mostrar_atividades_por_disciplina(atividades)`

**Onde está:** [painel/painel.py, linha 192](painel.py#L192).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Calcula a contagem por disciplina e encaminha para mostrar_distribuicao; seu efeito é imprimir.

**Como apresentar:** Relacione a função de cálculo puro à função que formata a tabela no terminal.

<a id="fn-painel-mostrar_atividades_por_serie"></a>

#### 14. `mostrar_atividades_por_serie(atividades)`

**Onde está:** [painel/painel.py, linha 197](painel.py#L197).

**Entradas:** `atividades`: lista de provas usadas na agregação.

**O que faz / resultado:** Calcula a contagem por série e usa a mesma tela de distribuição, sem persistência.

**Como apresentar:** Mostre que a reaplicação do mesmo exibidor evita duplicar a regra de porcentagem.

<a id="fn-painel-mostrar_distribuicao"></a>

#### 15. `mostrar_distribuicao(titulo, contagem, total_atividades)`

**Onde está:** [painel/painel.py, linha 202](painel.py#L202).

**Entradas:** `titulo`: título da tela ou do material; `contagem`: dicionário grupo → quantidade; `total_atividades`: número de provas do conjunto apresentado.

**O que faz / resultado:** Ordena os grupos pela quantidade e nome, imprime total e porcentagens usando total_atividades como denominador.

**Como apresentar:** Explique que o percentual se refere ao conjunto de provas recebido, não ao número de professores.

<a id="fn-painel-mostrar_materiais_mais_citados"></a>

#### 16. `mostrar_materiais_mais_citados(atividades, materiais=None)`

**Onde está:** [painel/painel.py, linha 217](painel.py#L217).

**Entradas:** `atividades`: lista de provas usadas na agregação; `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Calcula e imprime ranking de citações; se materiais=None usa a lista compartilhada da biblioteca.

**Como apresentar:** Mostre a opção 3 e diferencie suas citações do contador cumulativo de usos.

<a id="fn-painel-mostrar_materiais_mais_usados"></a>

#### 17. `mostrar_materiais_mais_usados(materiais)`

**Onde está:** [painel/painel.py, linha 233](painel.py#L233).

**Entradas:** `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Imprime o ranking de até três materiais obtido por listar_materiais_mais_usados; lista vazia gera aviso.

**Como apresentar:** Mostre a opção 8 depois de uma consulta e uma prova salva na mesma fonte.

<a id="fn-painel-mostrar_fila_pendentes"></a>

#### 18. `mostrar_fila_pendentes(materiais=None)`

**Onde está:** [painel/painel.py, linha 242](painel.py#L242).

**Entradas:** `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Imprime a fila, contexto e autor quando encontrado no mapa de usuários. Não aprova e não salva.

**Como apresentar:** Abra a fila antes da aprovação e indique quem sugeriu o material de teste.

<a id="fn-painel-mostrar_resumo"></a>

#### 19. `mostrar_resumo(materiais=None)`

**Onde está:** [painel/painel.py, linha 264](painel.py#L264).

**Entradas:** `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Imprime totais de materiais, aprovados/pendentes e distribuições de materiais por disciplina/série; usa lista recebida ou compartilhada.

**Como apresentar:** Diferencie este resumo de materiais das funções contar_atividades, que agregam provas.

<a id="fn-painel-mostrar_painel_completo"></a>

#### 20. `mostrar_painel_completo(atividades, materiais=None)`

**Onde está:** [painel/painel.py, linha 293](painel.py#L293).

**Entradas:** `atividades`: lista de provas usadas na agregação; `materiais`: lista de materiais usada em cálculo/exibição.

**O que faz / resultado:** Combina total de provas/professores ativos, resumo da biblioteca, distribuições, rankings e fila. Sem retorno útil e sem gravação.

**Como apresentar:** Use a opção 5 como fechamento da apresentação, mostrando o resultado do trabalho dos outros módulos.

<a id="fn-painel-menu_painel"></a>

#### 21. `menu_painel(usuario=None)`

**Onde está:** [painel/painel.py, linha 313](painel.py#L313).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Recebe a sessão da coordenação ou ID na execução isolada, verifica permissão e relê as fontes a cada escolha; trata erro e volta com 0.

**Como apresentar:** No fluxo principal entre com e-mail/senha. Reconheça que a entrada isolada por ID é compatibilidade de diagnóstico, não autenticação forte.

### Arquivo `main.py`

[Abrir fonte](../main.py)

<a id="fn-main-menu_coordenacao"></a>

#### 22. `menu_coordenacao(usuario)`

**Onde está:** [main.py, linha 11](../main.py#L11).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Revalida a sessão a cada ciclo e encaminha às operações de usuários, biblioteca/aprovação, regras, painel e histórico. Retorna sair com 0 ou None com troca/recusa.

**Como apresentar:** Mostre a opção 9 para trocar de usuário; a senha não é passada para cada operação, e sim o dicionário da sessão.

<a id="fn-main-menu_professor"></a>

#### 23. `menu_professor(usuario)`

**Onde está:** [main.py, linha 47](../main.py#L47).

**Entradas:** `usuario`: dicionário da sessão atual; None não autoriza operação protegida.

**O que faz / resultado:** Revalida sessão e encaminha pesquisa, sugestão, consulta, geração, histórico/exportação e edição da própria biblioteca. Retorna sair com 0 ou None para login.

**Como apresentar:** Mostre que o professor não recebe gestão de usuários/aprovação e que os módulos ainda verificam acesso por conta própria.

<a id="fn-main-menu_principal"></a>

#### 24. `menu_principal()`

**Onde está:** [main.py, linha 83](../main.py#L83).

**Entradas:** Não recebe argumentos; pode ler teclado, arquivo ou constantes, conforme descrito abaixo..

**O que faz / resultado:** Carrega materiais, repete login, direciona por perfil e encerra quando login retorna None ou menu devolve sair. Não implementa os CRUDs dentro dele.

**Como apresentar:** Trace o caminho main → fazer_login → menu do perfil → módulo. O bloco __main__ abaixo trata erros gerais e interrupção do teclado.

## 5. Perguntas técnicas e respostas para ensaiar

### Isso é realmente um CRUD separado?

O painel é um módulo de leitura e agregação, não uma quarta coleção com operações de inserir e excluir. A divisão de quatro CRUDs é uma divisão funcional do projeto.

### Qual a arquitetura?

Um único programa procedural modular, executado no terminal. Funções importam outras funções; dados são listas/dicionários persistidos em JSON. Não são microsserviços.

### O que significa agregação?

Agrupar registros por uma chave e calcular uma medida. Duas provas do mesmo professor incrementam a mesma entrada do dicionário de contagem.

### Usos e citações são iguais?

Não. usos soma consultas com evidência e provas salvas. Citações são referências presentes no histórico atual de provas, sem repetir material dentro da mesma prova.

### Como o painel fica atualizado?

O menu relê as fontes antes da opção selecionada. Não há agendamento, socket ou atualização automática da tela sem interação.

### Por que separar calcular e imprimir?

As funções de contagem retornam dados que podem ser testados sem teclado/tela. As mostrar_* formatam esses dados para o usuário.

### O painel isolado usa senha?

O caminho principal passa a sessão autenticada. A entrada isolada de diagnóstico menu_painel(None) ainda aceita ID; não é uma proteção equivalente ao login por senha. Isso é um limite atual a reconhecer.

### 77 testes provam que não há bugs?

Não. Eles verificam os cenários programados, incluindo o fluxo real e falhas importantes. Não são prova matemática nem substituem revisão e novos testes para novos cenários.

## 6. Limites que precisam ser apresentados com honestidade

Não possui interface web, atualização em tempo real, gráfico ou armazenamento próprio de métricas. A entrada isolada do painel por ID é um caminho de compatibilidade, não login seguro. A integridade dos arquivos e a proteção do computador não são garantidas por uma tela de menu.

## 7. Testes para mostrar ao professor

Na pasta `prototipo-terminal-python`, execute:

```powershell
py -B -m unittest discover -s tests -p test_painel.py -v
py -B -m unittest discover -s tests -p test_integracao.py -v
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
