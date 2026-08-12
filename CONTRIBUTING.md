# Como contribuir

Obrigado pelo interesse. Este repositório é uma skill: texto e instruções, mais um utilitário em Python sem dependências. Não é aplicação, não tem servidor e não guarda dados.

## Regra nº 1 — nunca dados reais

**Não inclua dados de caso real em lugar nenhum: issue, pull request, exemplo, teste, captura de tela, HTML gerado ou mensagem de commit.**

Isso vale para nome de parte, CPF, NB, número de processo, endereço, data de nascimento, dado clínico, laudo e trecho de autos. Vale também para o que parece inofensivo isolado mas identifica alguém em conjunto.

Atenção especial ao **HTML gerado**: ele carrega o caso inteiro embutido. Nunca anexe um dossiê real a uma issue. Use [`examples/caso-ficticio.json`](examples/caso-ficticio.json), que é inteiramente fictício.

Contribuição que traga dado real será fechada sem merge, e o histórico terá de ser reescrito.

## O princípio que não se negocia

**O dossiê não produz conhecimento novo. Ele estrutura o que já existe na conversa.**

Toda proposta é medida por aí. Se uma mudança faz o dossiê inferir, completar lacuna com o plausível, promover grau de comprovação ou preencher campo por conveniência de layout, ela será recusada — por melhor que fique a saída.

O bloco de pendências é a função mais útil do projeto, não uma seção a esconder. Proposta que reduza a visibilidade do que falta parte com o ônus invertido.

## O que é uma boa contribuição

- **Regra nova precisa de motivo concreto**, de preferência um caso real que a expôs, descrito sem identificar ninguém.
- **Texto custa contexto** em toda invocação que carregar o módulo. Prefira precisão a volume.
- **Nada que prometa resultado.** O dossiê organiza; quem decide é o advogado. Não estime probabilidade de êxito nem transforme quantidade de documentos em força jurídica.

## Convenções de escrita

- Rótulo técnico em caixa alta e sem acento: `FATO COMPROVADO`, `ALEGACAO`, `INFERENCIA`, `SEM FONTE NA CONVERSA`, `PENDENTE DE LEITURA`.
- Todo o restante em português correto, com acentuação.
- Célula de tabela vazia é erro: `—` para não aplicável, `?` para desconhecido.

## Conjuntos fechados: mude em todos os lugares

Alguns valores são verificados por código. Se alterar um conjunto, atualize **todos** estes pontos, ou o validador passará a recusar entrada válida:

| Onde | O quê |
|---|---|
| `skills/dossie/scripts/dossie_tool.py` | as constantes `VALID_*` e `COLLECTIONS` |
| `skills/dossie/references/extracao.md` | entidades, graus, situações e estrutura interna |
| `skills/dossie/references/identificacao-documental.md` | famílias documentais e confiança |
| `skills/dossie/references/tabelas.md` | colunas das saídas em markdown |
| `skills/dossie/references/validacao.md` | o que o validador recusa |
| `skills/dossie/SKILL.md` | passos e comandos |
| `examples/` | os três exemplos precisam continuar válidos |

## Testes

Só biblioteca padrão. Antes de abrir o PR:

```bash
python -m unittest discover -s tests -v
```

```bash
python skills/dossie/scripts/dossie_tool.py validate examples/caso-ficticio.json --html examples/caso-ficticio.html
```

O CI roda em Python 3.9 e 3.13. **Regra nova precisa de teste que a proteja** — um teste que quebre a regra deliberadamente e exija recusa.

Mudança no HTML exige rodar a validação com `--html`: ela verifica ausência de recurso externo, `fetch`, script externo e evento inline, e a presença de renderização segura por `textContent`.

## Commits e PRs

- Uma mudança por PR.
- Mensagem de commit explica **por que**, não só o quê.
- Descreva o que testou e o que não testou.

## Licença

Ao contribuir, você concorda em licenciar sua contribuição sob a [licença MIT](LICENSE) do projeto.
