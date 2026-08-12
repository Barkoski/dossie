# Política de segurança

## O que conta como vulnerabilidade aqui

Este projeto é uma skill jurídica com um utilitário de validação. Não há servidor, autenticação nem armazenamento remoto. O risco está em **fazer um advogado confiar no que não se sustenta**, em **vazar dado de caso** e no **HTML gerado**, que carrega o caso inteiro dentro de um arquivo.

Trate como vulnerabilidade e reporte em privado:

- **Execução de conteúdo no HTML gerado.** O dossiê embute texto vindo da conversa e dos autos num arquivo HTML. Se algum caminho permitir que esse conteúdo execute script, dispare evento inline, carregue recurso externo ou quebre o objeto de dados, é vulnerabilidade — e das graves, porque o texto dos autos é escrito por terceiros. Payloads de teste estão em `references/validacao.md`.
- **Requisição externa a partir do arquivo gerado.** Qualquer `fetch`, CDN, fonte remota, imagem externa ou telemetria no HTML. O dossiê tem de abrir offline. Um recurso externo transforma um documento sigiloso em requisição para fora.
- **Vazamento de sigilo.** Instrução, exemplo ou caminho de código que leve a buscar dado externo, consultar web, abrir conector ou enviar conteúdo do caso para fora. O dossiê se monta só com o que já está na conversa.
- **Nome de arquivo com dado pessoal.** O arquivo gerado não pode conter nome, CPF, NB ou número de processo no próprio nome.
- **Falso verde do validador.** Caso que viola uma regra e mesmo assim passa em `validate`. É o pior defeito possível: o validador existe para recusar, e um falso verde induz confiança em conteúdo não conferido.
- **Conhecimento novo introduzido pelo dossiê.** Caminho que faça o dossiê inferir fato, data, valor, página ou parte que não foi dito, ou promover grau de comprovação silenciosamente. É defeito de integridade, e aqui vale como vulnerabilidade.
- **Dado real no repositório.** Se encontrar dado de caso real em qualquer arquivo ou no histórico, reporte em privado, não abra issue pública.

Bug comum — mensagem de erro confusa, caso não coberto, incompatibilidade de versão — é issue normal.

## Como reportar

Use o **relato privado de vulnerabilidade do GitHub**, na aba *Security* deste repositório, em *Report a vulnerability*. Fica visível apenas para o mantenedor.

Não abra issue pública para os itens acima.

**Não inclua dados de caso real no relato, nem anexe um dossiê gerado a partir de caso real.** Para demonstrar execução de conteúdo, use os payloads fictícios de `references/validacao.md`.

## O que esperar

Projeto mantido por uma pessoa, ao lado da advocacia. Não há acordo de nível de serviço. O compromisso realista: confirmação de recebimento assim que possível; resposta dizendo se foi reproduzido e o que será feito; crédito no commit da correção, se você quiser.

## Versões

Correções entram na versão corrente publicada no catálogo `barkoski-skills`. Não há manutenção de versões anteriores.

```bash
/plugin marketplace update barkoski-skills
```

## O que o validador não protege

Limite de projeto, não defeito a corrigir: o script verifica estrutura, referências, integridade dos identificadores e restrições técnicas do HTML. Ele **não** confere a fonte probatória, não abre documento e não avalia a veracidade do caso. Resultado sem erro significa dossiê internamente coerente, não caso verdadeiro. A conferência na fonte continua sendo humana.
