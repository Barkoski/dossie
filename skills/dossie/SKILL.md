---
name: dossie
description: Transforma uma analise juridica ja feita na conversa em dossie estruturado e auditavel, com tabela de provas, requisitos, cronologia, grafo, relatorio e pendencias rastreaveis. Use quando o usuario pedir dossie, tabela ou quadro de provas, mapa ou grafo do caso, linha do tempo, relatorio de analise, exportacao em Markdown ou HTML, ou organizacao do que ja foi analisado. Nao pesquisar nem acrescentar conhecimento externo ao caso.
---

# Dossie juridico â€” v1.1

Transforma o que foi analisado na conversa em dossie estruturado: tabela de provas rastreavel, quadro de requisitos, cronologia, grafo do caso e relatorio.

Nao requer biblioteca, servidor ou recurso externo. Pode gerar Markdown no chat ou HTML autocontido quando o ambiente permitir criar arquivo.

## Uso

```
/dossie                      # dossie completo do caso analisado na conversa
/dossie provas               # apenas a tabela de provas
/dossie requisitos           # apenas o quadro requisito-prova-lacuna
/dossie linha                # apenas a cronologia
/dossie grafo                # apenas o grafo do caso
/dossie relatorio            # relatorio em prosa a partir do que foi confirmado
/dossie --md                 # forcar saida so em markdown, sem HTML
/dossie --html               # forcar o dossie visual autocontido
```

Aceitar tambem pedidos em linguagem natural. Sem argumento, entregar o dossie completo em Markdown; gerar HTML junto apenas quando o usuario pedir arquivo, visual ou exportacao.

## Principio inegociavel

**O dossie nao produz conhecimento novo. Ele estrutura o que ja existe na conversa.**

Nao inferir fato, data, valor, pagina, parte ou documento que nao tenha sido dito. Nao completar lacuna com o que seria plausivel. Quando algo essencial faltar, o dossie mostra a falta â€” e essa e a sua funcao mais util.

Todo item carrega duas trilhas distintas: `origem_conversa` indica onde apareceu na conversa; `fonte_probatoria` indica qual documento ou ato o sustenta. Origem na conversa nao transforma afirmacao em prova. Item sem origem identificavel e marcado `SEM FONTE NA CONVERSA` e aparece destacado, nunca omitido nem silenciosamente aceito.

## O que fazer quando invocado

### Passo 1 â€” Delimitar o caso

Varrer a conversa e fixar: parte ou partes, materia, fase, decisao ou peca em discussao, e quais documentos foram efetivamente lidos. Se a conversa tratar de mais de um caso, perguntar qual antes de seguir. Nao misturar casos.

Se a conversa nao contiver analise de caso nenhuma, dizer isso e parar. Nao inventar um caso para ter o que estruturar. Se houver mais de um caso e nao for possivel separa-los com seguranca, pedir ao usuario que escolha um.

### Passo 2 â€” Extrair

Seguir [references/extracao.md](references/extracao.md). Ele define as cinco entidades (parte, documento, fato, requisito, tese), como classificar cada afirmacao pelo grau de comprovacao, e o que fazer com afirmacao sem fonte.

O resultado interno e um JSON com a estrutura descrita la. Nao mostrar esse JSON ao usuario, salvo pedido expresso. Preservar conflitos e correcoes: nunca escolher silenciosamente uma versao apenas porque apareceu por ultimo.

### Passo 3 â€” Montar as saidas

Conforme o argumento recebido. As saidas em Markdown seguem [references/tabelas.md](references/tabelas.md). O dossie visual segue [references/html.md](references/html.md).

### Passo 4 â€” Fechar com o que falta

Toda entrega termina com tres blocos curtos:

- **Sem fonte na conversa**: afirmacoes que entraram sem origem identificavel.
- **Pendente de leitura**: documento citado na conversa que nao chegou a ser aberto.
- **Confirmar antes de usar**: tudo que depende de conferencia humana.

Se os tres estiverem vazios, dizer isso explicitamente â€” e uma informacao boa, nao uma secao a se omitir.

### Passo 5 â€” Validar antes de entregar

Aplicar [references/validacao.md](references/validacao.md). Conferir integridade dos identificadores, correspondencia entre tabelas, grafo e relatorio, neutralizacao de conteudo no HTML, ausencia de conhecimento novo e completude dos blocos de pendencia. Se uma verificacao falhar, corrigir antes de apresentar o dossie como completo.

## Regras de forma

- Rotulo tecnico em caixa alta e sem acento: `FATO COMPROVADO`, `ALEGACAO`, `INFERENCIA`, `SEM FONTE NA CONVERSA`, `PENDENTE DE LEITURA`.
- Todo o restante em portugues correto, com acentuacao.
- Tabela com celula vazia e erro: usar `â€”` para nao aplicavel e `?` para desconhecido, nunca deixar em branco.
- Nao prometer resultado, exito ou prazo. O dossie organiza; quem decide e o advogado.
- Nao transformar quantidade de documentos em probabilidade de exito ou forca juridica.
- Nao afirmar que uma linha foi conferida na fonte quando a conversa nao registra essa conferencia.

## Sigilo

O dossie e montado com o que ja esta na conversa. Nao buscar dado externo, nao consultar web, nao abrir conectores e nao enviar conteudo para fora para enriquecer o resultado.

Ao gerar arquivo, usar nome sem identificador pessoal e lembrar em uma linha que ele contem dados do caso e deve ser tratado como material sigiloso. Nao publicar, compartilhar ou enviar o arquivo sem pedido expresso.

