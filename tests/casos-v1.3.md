# Casos de regressao da versao 1.3

1. Um evento contem inicial e procuracao: gerar dois documentos, cada qual com seus limites.
2. A peca comeca em pagina conhecida e termina sem marcador: usar fim `?`, criterio `INCERTA` e nao estimar.
3. O rotulo cadastrado diz `OUTROS`, mas o conteudo e CNIS: preservar o rotulo em observacao e normalizar como `PROVA_LABORAL_PREVIDENCIARIA` / `CNIS`.
4. Fragmento sem titulo nem assinatura: registrar confianca `BAIXA` e incluir em confirmar.
5. Norma nao citada nos autos, mas conhecida pelo modelo: nao incluir em `normas_invocadas`.
6. Dois anexos com nomes semelhantes e titulares distintos: nao fundir.
7. Documento `NAO LIDO`: pode constar no indice, mas nao sustenta fato comprovado.
8. Migracao de schema 1.2: preservar IDs, preencher campos novos com `?` e registrar historico.
9. `documents`: listar todos os documentos na ordem do processo com inicio, fim e confianca.
10. `screening`: devolver somente marcadores presentes no JSON, sem enriquecimento externo.
