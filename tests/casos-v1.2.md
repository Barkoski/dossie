# Casos de regressao da versao 1.2

1. Salvar um caso novo: gerar `schema_version: 1.2`, IDs unicos e historico de criacao.
2. Atualizar fato existente sem correcao explicita: preservar as duas versoes como conflito.
3. Atualizar com correcao explicita: manter ID, registrar versao substituida e historico.
4. Consultar caminho existente D1-T1: listar todas as arestas e origens.
5. Consultar caminho inexistente: responder `NAO HA CAMINHO REGISTRADO NO DOSSIE`.
6. Explicar ID inexistente: falhar sem inventar entidade.
7. Validar fato comprovado apoiado por documento nao lido: retornar erro.
8. Validar aresta inferida sem base: retornar erro.
9. Validar HTML com recurso externo, evento inline ou `fetch`: retornar erro.
10. Gerar Markdown e HTML do JSON: graus, enunciados e contagens devem coincidir.
