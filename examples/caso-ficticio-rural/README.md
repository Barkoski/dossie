# Caso rural fictício completo

Exemplo **inteiramente fictício** de dossiê grande: 31 documentos, 24 fatos, 6 requisitos, 4 teses, 145 relações, cronologia e contradições.
Nomes, locais, datas, valores e quantidades são inventados; qualquer semelhança com pessoas ou processos reais é coincidência.

Arquivos:

- `dossie.json`: estado canônico persistente;
- `dossie.html`: painel interativo offline (gerado por `render_dashboard.py`);
- `relatorio.md`: relatório legível.

O caso mostra os pontos que costumam travar uma aposentadoria rural: prova em nome do companheiro, área total acima de quatro módulos, endereço urbano na escritura e data de ciência não localizada.

Para validar:

```bash
python skills/dossie/scripts/dossie_tool.py validate examples/caso-ficticio-rural/dossie.json --html examples/caso-ficticio-rural/dossie.html
```
