# Consulta de conteúdos

## Entrega contrato v1

As funções de `consultas.consultas` recebem o usuário do login. A cada busca, o módulo carrega a biblioteca atual com `materiais.carregar_dados()` e aplica `usuarios.filtrar_materiais_do_professor(usuario, lista_materiais)`. O filtro de usuários verifica as atribuições do professor. A consulta exige `status_validacao` igual a `aprovado_coordenacao` para os dois perfis. Chamadas sem usuário ou com usuário inativo encerram a operação antes da leitura do termo.

| Função | Comportamento no terminal |
| --- | --- |
| `pesquisar_material(usuario=None)` | Busca em título, disciplina, série, conteúdo e habilidade BNCC. Lista ID, título, disciplina e série das fontes encontradas. A pesquisa preserva o contador de usos. |
| `consultar_com_evidencia(usuario)` | Procura o termo no conteúdo, ignorando maiúsculas e minúsculas. Para cada material encontrado, exibe a primeira linha que contém o termo exatamente como está na fonte, com ID, título, disciplina, série e habilidade BNCC. Chama `materiais.registrar_uso(id)` uma vez por material exibido. |
| `consultar_conteudo(usuario=None)` | Entrada compatível com o menu anterior. Encaminha o usuário para a consulta com evidência. |

O termo pode ser uma palavra ou expressão. Espaços externos são ignorados e uma entrada vazia é solicitada de novo. Quando falta um trecho correspondente, o terminal informa a ausência na base aprovada disponível para o usuário. Os campos de conteúdo e BNCC aceitam tanto os nomes atuais (`conteudo_texto`, `habilidade_bncc`) quanto os anteriores (`conteudo`, `bncc`).

### Testar

A partir de `prototipo-terminal-python`, execute:

```text
py -m unittest discover -s tests -p test_consultas.py -v
```

Os testes carregam materiais de um JSON temporário. Substituem o filtro de usuários e o registro de uso para conferir quais materiais a consulta exibe e quais IDs envia para contagem. A integração do menu exige os contratos v1 de usuários e materiais.
