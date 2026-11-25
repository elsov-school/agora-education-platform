# Ágora — protótipo de terminal Python

O protótipo reúne a biblioteca curricular, consultas com evidência, provas e métricas da escola. Use Python 3 e a biblioteca padrão. Na pasta `prototipo-terminal-python`, execute `py main.py` no Windows ou `python3 main.py` no Linux/macOS.

## Entrega contrato v1

O programa carrega a biblioteca e pede o e-mail e a senha de um usuário ativo. Não exibe a lista de contas nem aceita o ID como login. A senha fica oculta durante a digitação no terminal. No cadastro de demonstração, Paula Mendes representa a coordenação e Ana Souza é professora. O perfil e as atribuições vêm do cadastro. A opção **9** volta ao login e **0** encerra o programa nos menus de perfil.

| Perfil | Operações do menu |
| --- | --- |
| Coordenação | Gerenciar professores e atribuições, manter a biblioteca, aprovar pendências, configurar o padrão da escola, consultar métricas e acessar o histórico de provas |
| Professor | Abrir ou pesquisar a biblioteca permitida, sugerir e editar materiais próprios, consultar conteúdo com evidência, gerar e revisar provas, acessar o próprio histórico e exportar |

### Configurar e-mail e senha

Os cadastros antigos foram preservados e ainda não têm senha. Antes do primeiro login, execute nesta pasta:

```powershell
py configurar_acesso.py
```

O configurador identifica a conta de coordenação existente. Informe o e-mail que você quer usar para entrar (pode ser seu próprio e-mail) e escolha uma senha de pelo menos 8 caracteres, repetindo-a para confirmar. O e-mail anterior é atualizado, preservando ID, nome, perfil e demais dados; não é criada uma conta duplicada. Essa configuração local funciona uma única vez, enquanto nenhuma coordenação ativa tiver senha. Não existe senha padrão. Depois execute `py main.py` e entre com e-mail e senha.

Na coordenação, abra **1 — Gerenciar usuários → 6 — Definir ou redefinir senha** para dar acesso aos professores existentes. O cadastro de um novo professor já solicita senha e confirmação. Contas antigas sem senha e usuários inativos não conseguem entrar. A opção 0 no campo de e-mail encerra o programa.

O JSON guarda um hash PBKDF2-SHA256, um salt aleatório e o número de iterações, nunca a senha original. Esses recursos usam apenas a biblioteca padrão do Python. O arquivo JSON ainda exige proteção de acesso no computador; este é um protótipo local, sem recuperação de senha por e-mail. Não publique cadastros reais nem credenciais locais no repositório.

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

A partir da pasta do protótipo, execute `python -B -m unittest discover -s tests -v`.

O teste de ponta a ponta em `tests/test_integracao.py` executa o `main.py` em processos separados sobre uma cópia temporária. Cadastra dois professores, configura a escola, sugere e aprova material, consulta um trecho, revisa e salva uma prova, confere a autoria e os arquivos exportados e verifica as métricas após reiniciar. Nesse cenário, a consulta e a prova salva somam dois usos do material. O painel preserva o conteúdo dos JSONs.

O teste pode ser executado separadamente com `python -B -m unittest discover -s tests -p test_integracao.py -k TestEscolaTemporaria -v`.
