# Extracao: da conversa para a estrutura

Converter a analise feita na conversa em cinco entidades. Extrair somente o que foi dito. O que nao foi dito nao existe para o dossie.

As cinco entidades servem tanto a processo administrativo quanto a processo judicial. O que muda entre eles:

| | Administrativo | Judicial |
|---|---|---|
| Localizacao | pagina do PDF, ID do anexo | evento, ID do documento, folha |
| Requisito | requisito legal do beneficio | requisito legal + pressuposto processual |
| Tese | tese do requerente e motivo do indeferimento | tese de cada polo, fundamento da decisao |
| Fase | requerimento, exigencia, recurso | inicial, contestacao, saneamento, sentenca, recurso |

Em caso judicial, incluir tambem como entidade `PARTE` o juizo e o perito quando tiverem produzido ato relevante, e registrar decisao judicial como `DOCUMENTO` — ela e fonte de fato como qualquer outra peca.

## As cinco entidades

**PARTE** — pessoa ou orgao com papel no caso: requerente, requerido, conjuge, dependente, instituidor, terceiro, perito, orgao julgador.
`id | nome ou iniciais | papel | observacao`

**DOCUMENTO** — peca fisica ou digital dos autos.
`id | tipo | titular | localizacao | qualidade da leitura | lido?`

**FATO** — acontecimento ou circunstancia afirmada.
`id | enunciado | data ou periodo | grau | documento(s) que sustentam`

**REQUISITO** — condicao legal que o caso precisa satisfazer.
`id | enunciado | situacao | fatos que o sustentam | lacuna`

**TESE** — argumento juridico, proprio ou da parte contraria.
`id | enunciado | polo | fatos e requisitos que invoca | forca`

## Grau de comprovacao do fato

- `FATO COMPROVADO` — sustentado por documento identificado na conversa, com localizacao.
- `ALEGACAO` — afirmado por alguem (parte, INSS, testemunha) sem documento que o sustente.
- `INFERENCIA` — deduzido do conjunto, sem afirmacao direta. Registrar de que fatos foi deduzido.
- `SEM FONTE NA CONVERSA` — apareceu na analise, mas nada na conversa diz de onde veio.

O quarto grau e o mais importante do dossie. Ele nao e um erro a esconder: e o produto. Uma analise que gera muitas linhas assim esta mal ancorada, e o advogado precisa saber disso antes de levar o material adiante.

Nunca promover grau: documento mencionado sem localizacao nao transforma alegacao em fato comprovado.

## Situacao do requisito

`COMPROVADO`, `PARCIALMENTE COMPROVADO`, `CONTROVERTIDO`, `NAO COMPROVADO`, `NAO APLICAVEL`.

Requisito que a conversa nao discutiu entra com situacao `?` e lacuna "nao analisado na conversa". Nao presumir que esteja satisfeito por nao ter sido mencionado.

## Localizacao do documento

Copiar exatamente como apareceu na conversa: `p. 47`, `pp. 63-65`, `evento 12`, `fl. 117`, `ID 916401037`. Preservar a forma usada — ela e o que permite a conferencia.

Quando houver duas numeracoes (PDF e autos), registrar as duas.

Sem localizacao na conversa: `PAGINA NAO IDENTIFICADA`. **Nunca estimar, nunca arredondar, nunca deduzir por proximidade.**

## Qualidade da leitura

`TEXTO NITIDO`, `OCR DUVIDOSO`, `LEITURA PARCIAL`, `ILEGIVEL`, `NAO LIDO`.

Documento que a conversa citou mas ninguem abriu entra como `NAO LIDO` e vai para o bloco de pendencias. Ele **nao** sustenta fato nenhum, por mais sugestivo que seja o nome do arquivo.

## Titular do documento

Em nome de quem o documento foi emitido. Campo obrigatorio, e decisivo: documento em nome de terceiro sustenta prova por extensao, nao prova direta — e e frequentemente o ponto onde a parte contraria ataca.

Desconhecido: `?`. Nunca presumir que seja do requerente.

## Arestas do grafo

Gerar aresta apenas quando a relacao foi afirmada na conversa:

- DOCUMENTO **comprova** FATO
- FATO **sustenta** REQUISITO
- REQUISITO **compoe** TESE
- PARTE **titulariza** DOCUMENTO
- FATO **contradiz** FATO
- TESE **opoe-se a** TESE
- DOCUMENTO **pertence a** PARTE

Toda aresta carrega a origem: de onde na conversa saiu essa ligacao. Aresta sem origem e marcada `INFERIDA` e recebe tracejado no grafo.

Nao criar aresta por semelhanca de tema, proximidade no texto ou coincidencia de data. Relacao nao afirmada nao e relacao.

## Estrutura interna

```json
{
  "caso": {
    "identificacao": "", "materia": "", "fase": "",
    "decisao_enfrentada": "", "data_referencia": ""
  },
  "partes":     [{"id":"P1","nome":"","papel":"","obs":""}],
  "documentos": [{"id":"D1","tipo":"","titular":"","localizacao":"",
                  "qualidade":"","lido":true,"conteudo":""}],
  "fatos":      [{"id":"F1","enunciado":"","data":"","grau":"",
                  "documentos":["D1"],"conferir":true}],
  "requisitos": [{"id":"R1","enunciado":"","situacao":"",
                  "fatos":["F1"],"lacuna":""}],
  "teses":      [{"id":"T1","enunciado":"","polo":"",
                  "apoia_se":["R1"],"forca":""}],
  "arestas":    [{"de":"D1","para":"F1","tipo":"comprova","origem":"","inferida":false}],
  "pendencias": {"sem_fonte":[],"nao_lidos":[],"conferir":[]}
}
```

Campo `conteudo` do documento: o que ele diz de concreto, com o dado que o individualiza — `venda de 320 litros de leite`, `compra de 10 parafusos`. Descricao generica como `comprovante de atividade` nao serve: nao permite conferencia nem sustenta argumento.

## Conflito na conversa

Quando a conversa contiver duas versoes do mesmo dado — uma data corrigida depois, um numero que mudou —, registrar a **ultima** e anotar a anterior no campo de observacao. Nao escolher em silencio.

Quando dois documentos se contradizerem, isso nao e erro de extracao: gerar aresta `contradiz` entre os fatos e destacar. Contradicao entre documentos e frequentemente o achado mais valioso da analise.
