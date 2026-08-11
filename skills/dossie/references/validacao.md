# Validacao do dossie

Aplicar antes de cada entrega completa ou parcial.

## Fidelidade

1. Cada item possui `origem_conversa` ou esta marcado `SEM FONTE NA CONVERSA`.
2. Cada `FATO COMPROVADO` aponta documento lido e localizacao registrada.
3. Documento `NAO LIDO` nao sustenta fato nem requisito.
4. Inferencia informa a base e nao foi promovida silenciosamente a fato.
5. Conflitos permanecem visiveis; correcoes explicitas registram a versao substituida.
6. Nenhuma lei, tese, data, valor ou pagina foi acrescentada para completar lacuna.

## Integridade

1. Identificadores sao unicos e todas as referencias apontam para entidades existentes.
2. Tabela, cronologia, grafo e relatorio usam o mesmo grau e enunciado para cada item.
3. Toda aresta possui origem ou marcacao `inferida` com base declarada.
4. Contagens e razoes sao exatas e podem ser reproduzidas a partir das entidades.
5. Os tres blocos de pendencias existem, inclusive quando vazios.

## Seguranca do HTML

Testar como texto inerte pelo menos estes valores ficticios:

```text
</script><script>alert(1)</script>
<img src=x onerror=alert(1)>
" ' ` & < >
linhaâ€¨seguinteâ€©fim
```

O arquivo deve abrir offline sem executar conteudo, requisitar rede ou quebrar o objeto de dados. Usar `textContent` para renderizar dados e serializacao segura dentro de `<script>`.

## Sigilo e entrega

- Nome do arquivo sem nome, CPF, NB ou numero processual.
- Nenhum recurso externo, telemetria, `fetch`, CDN ou fonte remota.
- Rodape de sigilo visivel.
- Nao compartilhar, publicar ou enviar o arquivo sem pedido expresso.

Se qualquer verificacao falhar, corrigir e repetir a lista. Nao chamar a entrega de completa enquanto houver falha.

