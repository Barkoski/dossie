---
name: dossie
description: Transforma a analise de um caso juridico feita na conversa em dossie estruturado e auditavel — tabela de provas com fonte e pagina, quadro de requisitos, cronologia, grafo do caso e relatorio. Use quando o usuario pedir dossie, tabela de provas, quadro de provas, mapa do caso, grafo do processo, linha do tempo do caso, relatorio de analise, ou quando disser para organizar, estruturar, visualizar ou exportar o que ja foi analisado na conversa. Funciona em qualquer ambiente, sem instalar nada.
---

# /dossie

Transforma o que foi analisado na conversa em dossie estruturado: tabela de provas rastreavel, quadro de requisitos, cronologia, grafo do caso e relatorio.

Nao instala nada e nao depende de shell. Funciona em Claude Code, Claude Desktop, claude.ai e ChatGPT.

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

Sem argumento: dossie completo, em markdown e HTML.

## Principio inegociavel

**O dossie nao produz conhecimento novo. Ele estrutura o que ja existe na conversa.**

Nao inferir fato, data, valor, pagina, parte ou documento que nao tenha sido dito. Nao completar lacuna com o que seria plausivel. Quando algo essencial faltar, o dossie mostra a falta — e essa e a sua funcao mais util.

Todo item carrega a origem. Item sem origem identificavel e marcado `SEM FONTE NA CONVERSA` e aparece destacado, nunca omitido nem silenciosamente aceito.

## O que fazer quando invocado

### Passo 1 — Delimitar o caso

Varrer a conversa e fixar: parte ou partes, materia, fase, decisao ou peca em discussao, e quais documentos foram efetivamente lidos. Se a conversa tratar de mais de um caso, perguntar qual antes de seguir. Nao misturar casos.

Se a conversa nao contiver analise de caso nenhuma, dizer isso e parar. Nao inventar um caso para ter o que estruturar.

### Passo 2 — Extrair

Seguir [references/extracao.md](references/extracao.md). Ele define as cinco entidades (parte, documento, fato, requisito, tese), como classificar cada afirmacao pelo grau de comprovacao, e o que fazer com afirmacao sem fonte.

O resultado interno e um JSON com a estrutura descrita la. Nao mostrar esse JSON ao usuario, salvo pedido expresso.

### Passo 3 — Montar as saidas

Conforme o argumento recebido. As saidas em markdown seguem [references/tabelas.md](references/tabelas.md). O dossie visual segue [references/html.md](references/html.md).

### Passo 4 — Fechar com o que falta

Toda entrega termina com tres blocos curtos:

- **Sem fonte na conversa**: afirmacoes que entraram sem origem identificavel.
- **Pendente de leitura**: documento citado na conversa que nao chegou a ser aberto.
- **Confirmar antes de usar**: tudo que depende de conferencia humana.

Se os tres estiverem vazios, dizer isso explicitamente — e uma informacao boa, nao uma secao a se omitir.

## Regras de forma

- Rotulo tecnico em caixa alta e sem acento: `FATO COMPROVADO`, `ALEGACAO`, `INFERENCIA`, `SEM FONTE NA CONVERSA`, `PENDENTE DE LEITURA`.
- Todo o restante em portugues correto, com acentuacao.
- Tabela com celula vazia e erro: usar `—` para nao aplicavel e `?` para desconhecido, nunca deixar em branco.
- Nao prometer resultado, exito ou prazo. O dossie organiza; quem decide e o advogado.

## Sigilo

O dossie e montado com o que ja esta na conversa. Nao buscar dado externo, nao consultar web e nao enviar conteudo para fora para enriquecer o resultado.

Ao gerar arquivo, lembrar em uma linha que ele contem dados do caso e deve ser tratado como material sigiloso.
