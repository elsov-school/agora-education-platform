# Ágora — protótipo de terminal Python

O protótipo reúne a biblioteca curricular, consultas com evidência, provas e métricas da escola. Use Python 3 e a biblioteca padrão. Na pasta `prototipo-terminal-python`, execute `py main.py` no Windows ou `python3 main.py` no Linux/macOS.

## Entrega contrato v1

O programa carrega a biblioteca e abre o login. No cadastro de demonstração, Paula Mendes (ID 1) representa a coordenação e Ana Souza (ID 2) é professora. O perfil e as atribuições vêm do cadastro. A opção **9** volta ao login e **0** encerra o programa nos menus de perfil.

| Perfil | Operações do menu |
| --- | --- |
| Coordenação | Gerenciar professores e atribuições, manter a biblioteca, aprovar pendências, configurar o padrão da escola, consultar métricas e acessar o histórico de provas |
| Professor | Pesquisar a biblioteca permitida, sugerir um material, consultar conteúdo com evidência, gerar e revisar provas, acessar o próprio histórico e exportar |

### Roteiro para demonstração

1. Entre como coordenação e confira a atribuição de turma, série e disciplina do professor.
2. Entre como professor e sugira um material nessa atribuição. A sugestão entra na fila de aprovação.
3. Troque para a coordenação, abra **Aprovar materiais pendentes** e confira o ID antes de aprovar.
4. Volte como professor, pesquise o título e consulte uma palavra presente no conteúdo. A consulta exibe o trecho e a fonte.
5. Gere uma prova com o material, revise e salve. No histórico, exporte as versões do aluno e do professor.
6. No painel da coordenação, abra **Painel completo** para conferir a aprovação, os usos e a prova por professor, série e disciplina.

### Módulos e persistência

| Módulo | Dados e responsabilidade |
| --- | --- |
| [Usuários](usuarios/README.md) | `usuarios/usuarios.json` guarda perfis, situação e atribuições |
| [Materiais](materiais/README.md) | `materiais/materiais.json` guarda o conteúdo, o status de validação e o contador de usos |
| [Consultas](consultas/README.md) | Pesquisa e apresenta trechos dos materiais permitidos |
| [Provas](provas/README.md) | `provas/atividades.json` guarda autoria, questões e referências aos materiais |
| [Padrões e exportação](padroes/README.md) | `padroes/regras.json` guarda as regras da escola. Os textos exportados ficam em `exportacoes/` |
| [Painel e menus](painel/README.md) | Lê os cadastros e históricos para calcular métricas da coordenação |

Materiais antigos sem aprovação integram a fila de pendências. O conteúdo demonstrativo e os códigos BNCC são ilustrativos. As consultas recuperam texto cadastrado e as questões seguem regras locais.

### Verificação

Execute `python -m unittest discover -s tests -v` a partir da pasta do protótipo. Os testes do painel usam JSONs temporários. Os testes de navegação verificam a troca de perfil e o encaminhamento da sessão às funções dos módulos.

A execução do roteiro completo depende da integração das cinco branches com as APIs do contrato v1. Esta entrega inicial liga os menus a essas APIs.
