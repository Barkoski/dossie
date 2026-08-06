# /dossie

Transforma a análise de um caso jurídico feita na conversa com uma IA em **dossiê estruturado e auditável**: tabela de provas rastreável, quadro de requisitos, cronologia, grafo do caso e relatório.

**Não instala nada.** Sem `pip`, sem servidor, sem shell. Funciona no Claude Code, no Claude Desktop, no Cowork e no ChatGPT.

Construído por [Lucas Barkoski](https://github.com/Barkoski), advogado previdenciarista.

## O problema

Você passa uma hora analisando um processo com uma IA. Ao final tem uma conversa longa, cheia de achados bons — e nada que dê para levar para os autos, arquivar ou revisar depois.

Pior: no meio dessa conversa há afirmações sólidas, com página citada, misturadas com afirmações que a IA soltou sem fonte nenhuma. Do jeito que ficam na tela, **as duas parecem iguais**.

## O que ele faz

Lê a conversa e devolve a análise estruturada, separando o que tem lastro do que não tem.

| Saída | Conteúdo |
|---|---|
| Tabela de provas | Documento, conteúdo concreto, data, **titular**, localização, qualidade da leitura, o que prova, marcação de conferência |
| Quadro de requisitos | Situação de cada requisito, fatos que o sustentam, lacuna e risco |
| Cronologia | Evento, grau de comprovação, fonte e localização |
| Grafo do caso | Partes, documentos, fatos, requisitos e teses, com as relações **afirmadas** na conversa |
| Relatório | Texto corrido gerado a partir do que foi estruturado, pronto para copiar ou imprimir |
| Pendências | Três blocos: sem fonte, pendente de leitura, confirmar antes de usar |

## O princípio

**O dossiê não produz conhecimento novo. Ele estrutura o que já existe na conversa.**

Nada de inferir data, valor, página ou documento que não foi dito. Quando algo essencial falta, o dossiê **mostra a falta** — e essa é a sua função mais útil.

Todo fato entra com um de quatro graus:

```
FATO COMPROVADO         sustentado por documento identificado, com localização
ALEGACAO                afirmado por alguém, sem documento que sustente
INFERENCIA              deduzido do conjunto, com registro de onde
SEM FONTE NA CONVERSA   apareceu na análise e nada diz de onde veio
```

O quarto grau é o produto. Em teste com um processo real, quatro afirmações caíram nele — todas citações legais que a IA tinha marcado "de memória" e nunca confirmou. A análise parecia sólida nos fatos, e estava; mas as **regras jurídicas** que sustentavam o quadro de requisitos inteiro estavam penduradas no vazio. O dossiê expôs isso em quatro linhas.

A mesma disciplina vale no grafo: aresta só existe se a relação foi **afirmada**. Nada de ligar nós por semelhança de tema ou coincidência de data. E clicar num nó abre o painel com a origem — sem isso, grafo é enfeite.

## Comandos

```
/dossie                # dossiê completo
/dossie provas         # só a tabela de provas
/dossie requisitos     # só o quadro requisito-prova-lacuna
/dossie linha          # só a cronologia
/dossie grafo          # só o grafo do caso
/dossie relatorio      # relatório em prosa
/dossie --md           # forçar saída só em markdown
/dossie --html         # forçar o dossiê visual
```

Não é preciso preparar nada. Analise o caso normalmente e depois chame o comando: ele lê a própria conversa.

## Administrativo e judicial

Serve aos dois. As cinco entidades — parte, documento, fato, requisito, tese — são de litígio em geral.

| | Administrativo | Judicial |
|---|---|---|
| Localização | página do PDF, ID do anexo | evento, ID do documento, folha |
| Requisito | requisito legal do benefício | requisito legal + pressuposto processual |
| Tese | tese do requerente, motivo do indeferimento | tese de cada polo, fundamento da decisão |

Em processo judicial, juízo e perito entram como partes quando produzem ato relevante, e a decisão judicial entra como documento — é fonte de fato como qualquer peça.

## O dossiê visual

Um **único arquivo HTML**, sem nenhuma dependência externa. Abre com duplo clique, funciona offline, renderiza como artifact.

O grafo é desenhado à mão em SVG e JavaScript puro — biblioteca de CDN é bloqueada em artifact e quebra offline. Layout dirigido por forças, calculado na carga.

Seis abas: grafo, provas com busca e filtro, requisitos em barras, cronologia, pendências e relatório com copiar e imprimir.

Tema claro e escuro. Paleta em tons médios, e cor nunca é o único portador de significado — todo estado vem acompanhado de rótulo em texto.

## Instalação

### Claude Code

Baixe o repositório e copie a pasta `skills/dossie` para `~/.claude/skills/` (no Windows, `C:\Users\SEU_USUARIO\.claude\skills\`). Reinicie a sessão.

O resultado final deve ser `.claude/skills/dossie/SKILL.md`.

### Claude Cowork

Baixe o arquivo `dossie.plugin`, arraste para uma conversa do Cowork e confirme.

Para gerar o `.plugin` a partir do repositório: selecione o **conteúdo** da pasta (`.claude-plugin`, `skills`, `README.md`) — não a pasta que os contém —, compacte e renomeie de `.zip` para `.plugin`. O `plugin.json` precisa ficar na raiz do arquivo compactado.

### ChatGPT

Cole o conteúdo de `SKILL.md` e dos três arquivos de `references/` nas instruções de um GPT personalizado. Depois é só analisar o caso e pedir o dossiê.

## Limites

- **Só estrutura o que está na conversa.** Não abre processo, não lê PDF, não pesquisa. Para isso existem outras ferramentas; esta entra depois delas.
- **Não confere nada.** Toda linha sai marcada para conferência humana. A tabela é roteiro de conferência, não certificado de veracidade.
- **Não decide.** Organiza a análise; a conclusão é do advogado.
- **Não busca fora.** Nenhum dado do caso sai para serviço externo. O dossiê gerado contém dados sigilosos e deve ser tratado como tal.

## Licença

MIT — ver [LICENSE](LICENSE).
