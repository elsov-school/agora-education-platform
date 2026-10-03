# Ágora — Apresentação do Projeto

Apresentação HTML independente da aplicação web e do CRUD em Python.

O arquivo `index.html` é uma cópia do original `agora-apresentacao-completa-v6.html`, com o nome padrão para abrir na página inicial do site. O conteúdo foi preservado, incluindo as imagens incorporadas e os controles da apresentação.

## Abrir no computador

Abra `index.html` no navegador com um duplo clique. Não é necessário instalar Python, Flask ou pacotes.

## Publicar na Vercel

O projeto **agora-apresentacao** usa `agora-apresentacao` como **Root Directory**, o preset **Other** e a própria pasta como saída. Não há etapa de build.

Para publicar alterações pela CLI, abra o terminal na pasta principal do repositório:

```bash
vercel link --yes --project agora-apresentacao --scope lohans-projects-1668e663
vercel deploy --prod --scope lohans-projects-1668e663
```

A apresentação é publicada separadamente do site `agora-app`.
