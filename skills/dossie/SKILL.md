---
name: dossie
description: Organiza analise juridica da conversa ou documentos expressamente indicados em dossie estruturado, persistente e auditavel, com indice e delimitacao de documentos, triagem, tabela de provas, requisitos, cronologia, grafo, relatorio, pendencias e consultas. Use quando o usuario pedir dossie, identificacao ou indice documental, classificacao de pecas, triagem processual, tabela ou quadro de provas, mapa ou grafo do caso, linha do tempo, relatorio, exportacao Markdown/JSON/HTML, atualizacao de dossie existente, caminho entre entidades, contradicoes, lacunas ou explicacao de item. Nao pesquisar nem acrescentar conhecimento externo ao caso.
---

# Dossiê jurídico — revisão 1.4 (JSON 1.3 compatível)

Transforma o que foi analisado na conversa em dossie estruturado: tabela de provas rastreavel, quadro de requisitos, cronologia, grafo do caso e relatorio.

Nao requer biblioteca, servidor ou recurso externo. Pode gerar Markdown no chat ou HTML autocontido quando o ambiente permitir criar arquivo.

## Uso

```
/dossie                      # dossie completo do caso analisado na conversa
/dossie provas               # apenas a tabela de provas
/dossie documentos           # indice, delimitacao e classificacao documental
/dossie triagem              # classe do caso, questao central e marcadores
/dossie requisitos           # apenas o quadro requisito-prova-lacuna
/dossie linha                # apenas a cronologia
/dossie grafo                # apenas o grafo do caso
/dossie relatorio            # relatorio em prosa a partir do que foi confirmado
/dossie --md                 # forcar saida so em markdown, sem HTML
/dossie --html               # forcar o dossie visual autocontido
/dossie salvar               # salvar estado persistente em dossie.json
/dossie atualizar <arquivo>  # incorporar apenas fatos novos ou corrigidos
/dossie explicar <ID>        # explicar entidade e suas conexoes
/dossie caminho <ID1> <ID2>  # mostrar caminho rastreavel entre entidades
/dossie contradicoes         # listar conflitos e suas fontes
/dossie lacunas              # listar requisitos e leituras pendentes
```

Aceitar tambem pedidos em linguagem natural. Sem argumento, entregar o dossie completo em Markdown; gerar HTML junto apenas quando o usuario pedir arquivo, visual ou exportacao.

## Principio inegociavel

**O dossiê não inventa nem pesquisa conhecimento externo. Estrutura o material disponível no modo pedido: conversa ou documentos indicados.**

Nao inferir fato, data, valor, pagina, parte ou documento que nao tenha sido dito. Nao completar lacuna com o que seria plausivel. Quando algo essencial faltar, o dossie mostra a falta — e essa e a sua funcao mais util.

Todo item carrega duas trilhas distintas: `origem_conversa` indica onde apareceu na conversa; `fonte_probatoria` indica qual documento ou ato o sustenta. Origem na conversa nao transforma afirmacao em prova. Item sem origem identificavel e marcado `SEM FONTE NA CONVERSA` e aparece destacado, nunca omitido nem silenciosamente aceito.

## O que fazer quando invocado

### Passo 1 — Delimitar o caso

Examinar o material disponivel e fixar: parte ou partes, materia, fase, decisao ou peca em discussao, e quais documentos foram efetivamente lidos. Se houver varios casos, usar o claramente indicado; perguntar apenas se persistir ambiguidade relevante. Nao misturar casos.

Se nao houver analise previa, mas o pedido indicar documentos para montar o dossie, ler os arquivos indicados localmente e registrar esse modo de origem e cobertura. Se nao houver nenhum material, informar o que falta; nao inventar caso. Se houver mais de um caso e nao for possivel separa-los com seguranca, pedir ao usuario que escolha um.

### Passo 2 — Extrair

Seguir [references/extracao.md](references/extracao.md). Ele define as cinco entidades (parte, documento, fato, requisito, tese), como classificar cada afirmacao pelo grau de comprovacao, e o que fazer com afirmacao sem fonte. Quando houver texto de autos, eventos, anexos ou paginas, ler tambem [references/identificacao-documental.md](references/identificacao-documental.md) para montar o indice documental e a triagem antes de relacionar provas e fatos.

O resultado interno e um JSON com a estrutura descrita la. Nao mostrar esse JSON ao usuario, salvo pedido expresso. Preservar conflitos e correcoes: nunca escolher silenciosamente uma versao apenas porque apareceu por ultimo.

Quando o usuario pedir salvar, atualizar ou consultar dossie persistente, ler [references/persistencia-e-consultas.md](references/persistencia-e-consultas.md). Manter IDs estaveis e historico de alteracoes. Nao sobrescrever arquivo existente sem pedido expresso.

### Passo 3 — Montar as saidas

Conforme o argumento recebido. As saidas em Markdown seguem [references/tabelas.md](references/tabelas.md). O dossie visual segue [references/html.md](references/html.md).

### Passo 4 — Fechar com o que falta

Toda entrega termina com tres blocos curtos:

- **Sem fonte na conversa**: afirmacoes que entraram sem origem identificavel.
- **Pendente de leitura**: documento citado na conversa que nao chegou a ser aberto.
- **Confirmar antes de usar**: tudo que depende de conferencia humana.

Se os tres estiverem vazios, dizer isso explicitamente — e uma informacao boa, nao uma secao a se omitir.

### Passo 5 — Validar antes de entregar

Aplicar [references/validacao.md](references/validacao.md). Conferir integridade dos identificadores, correspondencia entre tabelas, grafo e relatorio, neutralizacao de conteudo no HTML, ausencia de conhecimento novo e completude dos blocos de pendencia. Quando Python estiver disponivel e houver `dossie.json`, executar `scripts/dossie_tool.py validate <arquivo>`, acrescentando `--html <arquivo>` quando houver HTML. Se uma verificacao falhar, corrigir antes de apresentar o dossie como completo.

## Regras de forma

- Rotulo tecnico em caixa alta e sem acento: `FATO COMPROVADO`, `ALEGACAO`, `INFERENCIA`, `SEM FONTE NA CONVERSA`, `PENDENTE DE LEITURA`.
- Todo o restante em portugues correto, com acentuacao.
- Tabela com celula vazia e erro: usar `—` para nao aplicavel e `?` para desconhecido, nunca deixar em branco.
- Nao prometer resultado, exito ou prazo. O dossie organiza; quem decide e o advogado.
- Nao transformar quantidade de documentos em probabilidade de exito ou forca juridica.
- Nao afirmar que uma linha foi conferida na fonte quando a conversa nao registra essa conferencia.

## Sigilo

O dossie usa a conversa ou arquivos indicados para leitura local. Nao buscar dado externo, nao consultar web, nao abrir conectores e nao enviar conteudo para fora para enriquecer o resultado.

Ao gerar arquivo, usar nome sem identificador pessoal e lembrar em uma linha que ele contem dados do caso e deve ser tratado como material sigiloso. Nao publicar, compartilhar ou enviar o arquivo sem pedido expresso.

## Integração e modos

Modo conversa apenas reorganiza o histórico disponível; modo documentos lê os arquivos expressamente indicados para produzir o dossiê, sem pesquisa jurídica externa. Registre `modo_origem` no caso. Não procure outras conversas por rotina. Para análise de mérito nova, use a skill jurídica pertinente quando disponível, sem bloquear a organização se ela faltar. No Codex, aceite `$dossie` e linguagem natural; a notação `/dossie` não pressupõe comando instalado.

Mantenha separados original conferido, transcrição lida, fonte relatada e revisão humana. Dossiê parcial entrega o recorte solicitado e pendências pertinentes. Validar JSON não valida os fatos. Dados salvos localmente não tornam o modelo da conversa uma IA local. Para transpor JSON previdenciário, preserve IDs e fontes; as famílias documentais dos dois formatos são diferentes.