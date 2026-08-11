# /dossie

Transforma a anÃ¡lise de um caso jurÃ­dico feita na conversa com uma IA em **dossiÃª estruturado e auditÃ¡vel**: tabela de provas rastreÃ¡vel, quadro de requisitos, cronologia, grafo do caso e relatÃ³rio.

**Sem dependÃªncias de execuÃ§Ã£o.** NÃ£o exige `pip`, servidor, CDN ou biblioteca externa. Funciona no Codex, Claude Code, Claude Desktop, Cowork e ChatGPT.

ConstruÃ­do por [Lucas Barkoski](https://github.com/Barkoski), advogado previdenciarista.

## VersÃ£o 1.2

- estado persistente e versionado em `dossie.json`;
- atualizaÃ§Ã£o incremental com IDs estÃ¡veis e histÃ³rico de alteraÃ§Ãµes;
- consultas de entidade, caminho, contradiÃ§Ãµes e lacunas;
- validador determinÃ­stico opcional, sem bibliotecas externas;
- exemplos fictÃ­cios completos em Markdown, JSON e HTML offline;
- testes de regressÃ£o para persistÃªncia, consultas e seguranÃ§a.

### Melhorias herdadas da versÃ£o 1.1

- origem da conversa separada da fonte probatÃ³ria em todas as entidades;
- conflitos preservados, sem escolher automaticamente a Ãºltima versÃ£o;
- validaÃ§Ã£o de integridade entre tabelas, grafo, cronologia e relatÃ³rio;
- proteÃ§Ã£o do HTML contra conteÃºdo executÃ¡vel vindo da conversa ou dos autos;
- controles de acessibilidade e navegaÃ§Ã£o por teclado;
- barras de requisitos sem transformar quantidade de documentos em chance de Ãªxito;
- metadados e instruÃ§Ãµes de instalaÃ§Ã£o para o Codex.

## O problema

VocÃª passa uma hora analisando um processo com uma IA. Ao final tem uma conversa longa, cheia de achados bons â€” e nada que dÃª para levar para os autos, arquivar ou revisar depois.

Pior: no meio dessa conversa hÃ¡ afirmaÃ§Ãµes sÃ³lidas, com pÃ¡gina citada, misturadas com afirmaÃ§Ãµes que a IA soltou sem fonte nenhuma. Do jeito que ficam na tela, **as duas parecem iguais**.

## O que ele faz

LÃª a conversa e devolve a anÃ¡lise estruturada, separando o que tem lastro do que nÃ£o tem.

| SaÃ­da | ConteÃºdo |
|---|---|
| Tabela de provas | Documento, conteÃºdo concreto, data, **titular**, localizaÃ§Ã£o, qualidade da leitura, o que prova, marcaÃ§Ã£o de conferÃªncia |
| Quadro de requisitos | SituaÃ§Ã£o de cada requisito, fatos que o sustentam, lacuna e risco |
| Cronologia | Evento, grau de comprovaÃ§Ã£o, fonte e localizaÃ§Ã£o |
| Grafo do caso | Partes, documentos, fatos, requisitos e teses, com as relaÃ§Ãµes **afirmadas** na conversa |
| RelatÃ³rio | Texto corrido gerado a partir do que foi estruturado, pronto para copiar ou imprimir |
| PendÃªncias | TrÃªs blocos: sem fonte, pendente de leitura, confirmar antes de usar |

## O princÃ­pio

**O dossiÃª nÃ£o produz conhecimento novo. Ele estrutura o que jÃ¡ existe na conversa.**

Nada de inferir data, valor, pÃ¡gina ou documento que nÃ£o foi dito. Quando algo essencial falta, o dossiÃª **mostra a falta** â€” e essa Ã© a sua funÃ§Ã£o mais Ãºtil.

Todo fato entra com um de quatro graus:

```
FATO COMPROVADO         sustentado por documento identificado, com localizaÃ§Ã£o
ALEGACAO                afirmado por alguÃ©m, sem documento que sustente
INFERENCIA              deduzido do conjunto, com registro de onde
SEM FONTE NA CONVERSA   apareceu na anÃ¡lise e nada diz de onde veio
```

O quarto grau Ã© o produto. Em teste com um processo real, quatro afirmaÃ§Ãµes caÃ­ram nele â€” todas citaÃ§Ãµes legais que a IA tinha marcado "de memÃ³ria" e nunca confirmou. A anÃ¡lise parecia sÃ³lida nos fatos, e estava; mas as **regras jurÃ­dicas** que sustentavam o quadro de requisitos inteiro estavam penduradas no vazio. O dossiÃª expÃ´s isso em quatro linhas.

A mesma disciplina vale no grafo: aresta sÃ³ existe se a relaÃ§Ã£o foi **afirmada**. Nada de ligar nÃ³s por semelhanÃ§a de tema ou coincidÃªncia de data. E clicar num nÃ³ abre o painel com a origem â€” sem isso, grafo Ã© enfeite.

## Comandos

```
/dossie                # dossiÃª completo
/dossie provas         # sÃ³ a tabela de provas
/dossie requisitos     # sÃ³ o quadro requisito-prova-lacuna
/dossie linha          # sÃ³ a cronologia
/dossie grafo          # sÃ³ o grafo do caso
/dossie relatorio      # relatÃ³rio em prosa
/dossie --md           # forÃ§ar saÃ­da sÃ³ em markdown
/dossie --html         # forÃ§ar o dossiÃª visual
/dossie salvar         # persistir em dossie.json
/dossie atualizar      # incorporar apenas mudanÃ§as novas
/dossie explicar R1    # explicar entidade e conexÃµes
/dossie caminho D1 T1  # mostrar caminho entre entidades
/dossie contradicoes   # listar conflitos registrados
/dossie lacunas        # listar requisitos e leituras pendentes
```

NÃ£o Ã© preciso preparar nada. Analise o caso normalmente e depois chame o comando ou peÃ§a em linguagem natural para organizar a anÃ¡lise como dossiÃª.

## Administrativo e judicial

Serve aos dois. As cinco entidades â€” parte, documento, fato, requisito, tese â€” sÃ£o de litÃ­gio em geral.

| | Administrativo | Judicial |
|---|---|---|
| LocalizaÃ§Ã£o | pÃ¡gina do PDF, ID do anexo | evento, ID do documento, folha |
| Requisito | requisito legal do benefÃ­cio | requisito legal + pressuposto processual |
| Tese | tese do requerente, motivo do indeferimento | tese de cada polo, fundamento da decisÃ£o |

Em processo judicial, juÃ­zo e perito entram como partes quando produzem ato relevante, e a decisÃ£o judicial entra como documento â€” Ã© fonte de fato como qualquer peÃ§a.

## O dossiÃª visual

Um **Ãºnico arquivo HTML**, sem nenhuma dependÃªncia externa. Abre com duplo clique, funciona offline, renderiza como artifact.

O grafo Ã© desenhado Ã  mÃ£o em SVG e JavaScript puro â€” biblioteca de CDN Ã© bloqueada em artifact e quebra offline. Layout dirigido por forÃ§as, calculado na carga.

Seis abas: grafo, provas com busca e filtro, requisitos em barras, cronologia, pendÃªncias e relatÃ³rio com copiar e imprimir.

Tema claro e escuro. Paleta em tons mÃ©dios, e cor nunca Ã© o Ãºnico portador de significado â€” todo estado vem acompanhado de rÃ³tulo em texto.

## Exemplo completo

O diretÃ³rio [`examples/`](examples/) contÃ©m o mesmo caso inteiramente fictÃ­cio em trÃªs formatos:

- `caso-ficticio.md` â€” entrega legÃ­vel e copiÃ¡vel;
- `caso-ficticio.json` â€” estado canÃ´nico persistente;
- `caso-ficticio.html` â€” visual interativo e offline.

Para validar e consultar o exemplo, usando somente a biblioteca padrÃ£o do Python:

```bash
python skills/dossie/scripts/dossie_tool.py validate examples/caso-ficticio.json --html examples/caso-ficticio.html
python skills/dossie/scripts/dossie_tool.py explain examples/caso-ficticio.json R1
python skills/dossie/scripts/dossie_tool.py path examples/caso-ficticio.json D1 T1
python skills/dossie/scripts/dossie_tool.py contradictions examples/caso-ficticio.json
python skills/dossie/scripts/dossie_tool.py gaps examples/caso-ficticio.json
```

## InstalaÃ§Ã£o

### Claude Code

Baixe o repositÃ³rio e copie a pasta `skills/dossie` para `~/.claude/skills/` (no Windows, `C:\Users\SEU_USUARIO\.claude\skills\`). Reinicie a sessÃ£o.

O resultado final deve ser `.claude/skills/dossie/SKILL.md`.

### Codex

Baixe o repositÃ³rio e copie a pasta `skills/dossie` para `~/.codex/skills/` (no Windows, `C:\Users\SEU_USUARIO\.codex\skills\`). Reinicie o Codex ou inicie uma nova tarefa.

O resultado final deve ser `.codex/skills/dossie/SKILL.md`. A skill tambÃ©m inclui `agents/openai.yaml` para nome, descriÃ§Ã£o e prompt sugerido na interface.

### Claude Cowork

Baixe o arquivo `dossie.plugin`, arraste para uma conversa do Cowork e confirme.

Para gerar o `.plugin` a partir do repositÃ³rio: selecione o **conteÃºdo** da pasta (`.claude-plugin`, `skills`, `README.md`) â€” nÃ£o a pasta que os contÃ©m â€”, compacte e renomeie de `.zip` para `.plugin`. O `plugin.json` precisa ficar na raiz do arquivo compactado.

### ChatGPT

Cole o conteÃºdo de `SKILL.md` e dos cinco arquivos de `references/` nas instruÃ§Ãµes de um GPT personalizado. Depois Ã© sÃ³ analisar o caso e pedir o dossiÃª.

## Limites

- **SÃ³ estrutura o que estÃ¡ na conversa.** NÃ£o abre processo, nÃ£o lÃª PDF, nÃ£o pesquisa. Para isso existem outras ferramentas; esta entra depois delas.
- **NÃ£o confere nada.** Toda linha sai marcada para conferÃªncia humana. A tabela Ã© roteiro de conferÃªncia, nÃ£o certificado de veracidade.
- **NÃ£o decide.** Organiza a anÃ¡lise; a conclusÃ£o Ã© do advogado.
- **NÃ£o busca fora.** Nenhum dado do caso sai para serviÃ§o externo. O dossiÃª gerado contÃ©m dados sigilosos e deve ser tratado como tal.

## LicenÃ§a

MIT â€” ver [LICENSE](LICENSE).

## InspiraÃ§Ã£o

A ideia geral de representar conhecimento como grafo auditÃ¡vel foi inspirada pelo projeto [Graphify](https://github.com/Graphify-Labs/graphify). O DossiÃª nÃ£o copia cÃ³digo, templates ou implementaÃ§Ã£o do Graphify: sua ontologia, regras de prova, rastreabilidade jurÃ­dica, persistÃªncia e visualizaÃ§Ã£o foram desenvolvidas especificamente para anÃ¡lise de casos jurÃ­dicos.

