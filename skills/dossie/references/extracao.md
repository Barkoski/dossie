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

**PARTE/ATOR** — pessoa ou orgao com papel no caso: requerente, requerido, conjuge, dependente, instituidor, terceiro, perito ou orgao julgador. Perito e juizo sao atores processuais, nao polos da demanda.
`id | nome ou iniciais | natureza | papel | origem_conversa | observacao`

**DOCUMENTO** — peca fisica ou digital dos autos. Quando o texto dos autos estiver disponivel, aplicar [identificacao-documental.md](identificacao-documental.md).
`id | familia | tipo normalizado | titular | inicio/fim | resumo | confianca da identificacao | qualidade da leitura | lido? | origem_conversa`

**FATO** — acontecimento ou circunstancia afirmada.
`id | enunciado | data ou periodo | grau | documento(s) que sustentam | origem_conversa`

**REQUISITO** — condicao legal que o caso precisa satisfazer.
`id | enunciado | situacao | fatos que o sustentam | lacuna | origem_conversa`

**TESE** — argumento juridico, proprio ou da parte contraria.
`id | enunciado | polo | fatos e requisitos que invoca | forca | origem_conversa`

`origem_conversa` descreve de onde o item foi extraido: mensagem do usuario, resposta anterior, arquivo e pagina citados ou outro marcador disponivel. Nao inventar numero de turno. Se a interface nao expuser marcador confiavel, usar descricao curta como `relato do usuario na conversa`.

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
- PARTE/ATOR **titulariza** DOCUMENTO
- FATO **contradiz** FATO
- TESE **opoe-se a** TESE

Toda aresta carrega a origem: de onde na conversa saiu essa ligacao. Relacao nao afirmada pode aparecer apenas quando for util expor uma inferencia ja feita na conversa; nesse caso, marcar `inferida: true`, explicar a base e nunca usa-la sozinha para promover grau de comprovacao.

Nao criar aresta por semelhanca de tema, proximidade no texto ou coincidencia de data. Relacao nao afirmada nao e relacao.

## Estrutura interna

```json
{
  "caso": {
    "identificacao": "", "materia": "", "fase": "",
    "decisao_enfrentada": "", "data_referencia": ""
  },
  "triagem": {
    "tipo_procedimento":"", "assunto_principal":"", "questao_central":"",
    "pontos_controvertidos":[], "palavras_chave":[], "normas_invocadas":[],
    "origem_conversa":""
  },
  "partes":     [{"id":"P1","nome":"","natureza":"parte|ator_processual",
                  "papel":"","origem_conversa":"","obs":""}],
  "documentos": [{"id":"D1","familia":"","tipo":"","titular":"",
                  "evento_inicio":"?","pagina_inicio":"?","evento_fim":"?","pagina_fim":"?",
                  "localizacao":"","resumo":"","criterio_delimitacao":"",
                  "confianca_identificacao":"","qualidade":"","lido":true,
                  "conteudo":"","origem_conversa":""}],
  "fatos":      [{"id":"F1","enunciado":"","data":"","grau":"",
                  "documentos":["D1"],"origem_conversa":"","conferir":true}],
  "requisitos": [{"id":"R1","enunciado":"","situacao":"",
                  "fatos":["F1"],"lacuna":"","origem_conversa":""}],
  "teses":      [{"id":"T1","enunciado":"","polo":"",
                  "apoia_se":["R1"],"forca":"","origem_conversa":""}],
  "arestas":    [{"de":"D1","para":"F1","tipo":"comprova",
                  "origem_conversa":"","inferida":false,"base_inferencia":""}],
  "pendencias": {"sem_fonte":[],"nao_lidos":[],"conferir":[]}
}
```

Campo `conteudo` do documento: o que ele diz de concreto, com o dado que o individualiza — `venda de 320 litros de leite`, `compra de 10 parafusos`. Descricao generica como `comprovante de atividade` nao serve: nao permite conferencia nem sustenta argumento.

## Conflito na conversa

Quando a conversa contiver duas versoes do mesmo dado, preservar ambas como conflito. Substituir a anterior somente quando houver correcao explicita do usuario ou fonte mais qualificada identificada na conversa; registrar a versao substituida e o motivo. Ordem temporal da mensagem, sozinha, nao define veracidade.

Quando dois documentos se contradizerem, isso nao e erro de extracao: gerar aresta `contradiz` entre os fatos e destacar. Contradicao entre documentos e frequentemente o achado mais valioso da analise.

## Integridade referencial

- Usar identificadores unicos e estaveis dentro do dossie.
- Nao apontar documento, fato, requisito, tese ou parte inexistente.
- Nao duplicar entidade apenas por variacao de grafia; registrar alias em observacao.
- Nao fundir homonimos ou documentos semelhantes sem base expressa.
- Manter o mesmo enunciado e o mesmo grau em tabela, grafo, cronologia e relatorio.
