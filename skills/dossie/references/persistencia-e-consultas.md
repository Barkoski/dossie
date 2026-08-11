# Persistencia, atualizacao e consultas

Usar este modulo somente quando houver pedido de salvar, atualizar ou consultar um dossie em arquivo.

## Arquivo canonico

Salvar o estado em `dossie.json`, UTF-8, com `schema_version: "1.3"`. O JSON e a fonte das saidas Markdown e HTML; nao reconstruir o estado a partir do HTML.

Acrescentar ao esquema de [extracao.md](extracao.md):

```json
{
  "schema_version": "1.3",
  "gerado_em": "AAAA-MM-DDTHH:MM:SSZ",
  "atualizado_em": "AAAA-MM-DDTHH:MM:SSZ",
  "historico": [
    {"data":"","tipo":"criacao|atualizacao|correcao","resumo":"","origem_conversa":""}
  ]
}
```

## Salvamento

- Pedir ou usar pasta autorizada pelo usuario.
- Usar nome `dossie-<identificacao-neutra>.json`, sem nome, CPF, NB ou numero processual.
- Nao sobrescrever arquivo existente sem pedido expresso.
- Gerar Markdown e HTML a partir do JSON salvo para evitar divergencia.

## Atualizacao incremental

1. Ler e validar o JSON existente antes de alterar.
2. Extrair apenas informacao nova da conversa ou arquivo indicado.
3. Comparar por identidade e conteudo, nao apenas por texto identico.
4. Preservar IDs existentes; criar ID novo somente para entidade realmente nova.
5. Nao apagar versao conflitante. Marcar substituicao apenas com correcao explicita e registrar motivo.
6. Recalcular arestas, pendencias e contagens derivadas.
7. Acrescentar entrada em `historico` com resumo e origem.
8. Validar novamente e mostrar ao usuario: adicionados, alterados, conflitos e itens inalterados.

## Migracao da versao 1.2

Ao abrir `schema_version: "1.2"`, nao descartar dados. Criar `triagem` com `?` e listas vazias, acrescentar aos documentos os campos de identificacao descritos em [identificacao-documental.md](identificacao-documental.md), usando `?` e `INCERTA` quando o material nao permitir recuperar limites. Registrar a migracao no historico e somente entao alterar para `1.3`.

## Consultas

- `explicar <ID>`: mostrar entidade, grau/situacao, origem, fonte probatoria e arestas de entrada/saida.
- `caminho <ID1> <ID2>`: encontrar menor caminho no grafo; mostrar cada aresta, tipo, origem e se e inferida.
- `contradicoes`: listar arestas `contradiz`, as duas versoes e suas fontes.
- `lacunas`: listar requisitos nao comprovados/controvertidos, documentos nao lidos e itens sem fonte.

Responder somente com dados presentes no JSON. Ausencia de caminho e resultado valido: `NAO HA CAMINHO REGISTRADO NO DOSSIE`.

Quando Python estiver disponivel, preferir as consultas deterministicas de `scripts/dossie_tool.py`. Sem Python, aplicar as mesmas regras diretamente ao JSON.
