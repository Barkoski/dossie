# O que muda

<!-- Uma frase. O que o dossiê passa a fazer, ou deixa de fazer. -->

# Por quê

<!-- O motivo concreto. Se veio de um caso real, descreva sem identificar ninguém. -->

# Como testei

<!-- O que você rodou e o que verificou à mão. Diga também o que NÃO testou. -->

---

## Antes de pedir revisão

- [ ] **Nenhum dado de caso real** neste PR: código, exemplos, testes, capturas, HTML gerado ou mensagens de commit.
- [ ] A mudança não faz o dossiê produzir conhecimento novo — nada de inferir, completar lacuna com o plausível ou promover grau de comprovação.
- [ ] Os blocos de pendência continuam visíveis, inclusive quando vazios.
- [ ] Uma mudança por PR.
- [ ] Rótulo técnico em caixa alta e sem acento; o resto em português com acentuação.
- [ ] Nada aqui promete resultado, êxito ou probabilidade de ganho.

## Se mexi em conjunto fechado

Entidades, graus de comprovação, situação de requisito, famílias documentais ou confiança de identificação. Marque tudo que atualizou:

- [ ] `skills/dossie/scripts/dossie_tool.py` — `VALID_*` e `COLLECTIONS`
- [ ] `skills/dossie/references/extracao.md`
- [ ] `skills/dossie/references/identificacao-documental.md`
- [ ] `skills/dossie/references/tabelas.md`
- [ ] `skills/dossie/references/validacao.md`
- [ ] `skills/dossie/SKILL.md`
- [ ] `examples/` continuam válidos
- [ ] Não se aplica

> Mudar um sem os outros faz o validador recusar entrada válida.

## Se mexi no HTML

- [ ] Sem recurso externo, `fetch`, CDN, fonte remota ou telemetria — abre offline
- [ ] Dados renderizados por `textContent`, não por `innerHTML`
- [ ] Testei com os payloads de `references/validacao.md` e nada executou
- [ ] Rodapé de sigilo visível
- [ ] Não se aplica

## Testes

- [ ] `python -m unittest discover -s tests -v` passa
- [ ] `python skills/dossie/scripts/dossie_tool.py validate examples/caso-ficticio.json --html examples/caso-ficticio.html` passa
- [ ] Regra nova tem teste que a protege — quebra a regra de propósito e exige recusa
- [ ] Não se aplica: mudança só de texto, sem efeito no validador
