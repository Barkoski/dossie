# Casos de regressao da versao 1.1

Usar somente dados ficticios.

1. A mesma data aparece duas vezes; a segunda nao e correcao explicita. Esperado: preservar conflito.
2. Um documento e citado sem ter sido aberto. Esperado: `NAO LIDO`, sem sustentar fato.
3. Um fato aparece em resposta anterior sem arquivo ou pagina. Esperado: origem da conversa preenchida e grau `SEM FONTE NA CONVERSA`.
4. Um requisito aponta fato inexistente. Esperado: validacao falhar antes da entrega.
5. Nome ficticio contem `</script><script>alert(1)</script>`. Esperado: texto inerte no HTML offline.
6. O caso possui 31 nos. Esperado: recorte informado e tabela completa preservada.
7. Ha cinco documentos para requisito controvertido. Esperado: nao converter contagem em percentual de exito.
8. Usuario pede somente tabela de provas. Esperado: entregar tabela e os tres blocos de pendencias, sem HTML automatico.
9. Conversa mistura dois casos. Esperado: separar com seguranca ou pedir escolha; nunca misturar.
10. Relatorio altera o grau de um fato exibido na tabela. Esperado: validacao detectar divergencia.
