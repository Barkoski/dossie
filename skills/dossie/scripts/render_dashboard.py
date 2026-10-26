"""Renderiza um dossiê JSON em painel HTML autocontido, sem rede."""
import argparse
import json
from pathlib import Path
from dossie_tool import load_json


def render(data):
    payload = json.dumps(data, ensure_ascii=False)
    for char, escaped in [('&', '\\u0026'), ('<', '\\u003c'), ('>', '\\u003e'), ('\u2028', '\\u2028'), ('\u2029', '\\u2029')]:
        payload = payload.replace(char, escaped)
    template = Path(__file__).resolve().parents[1] / 'assets' / 'dashboard.html'
    html = template.read_text(encoding='utf-8').replace('__DOSSIE_DATA__', payload)
    # Assets são incorporados: o arquivo final funciona sem rede ou arquivos auxiliares.
    assets = template.parent
    css = (assets / 'mapa.css').read_text(encoding='utf-8')
    js = (assets / 'mapa.js').read_text(encoding='utf-8')
    css += '\n' + (assets / 'mapa-light.css').read_text(encoding='utf-8')
    js += '\n' + (assets / 'mapa-flow.js').read_text(encoding='utf-8')
    css += '\n' + (assets / 'lawyer.css').read_text(encoding='utf-8')
    js += '\n' + (assets / 'lawyer.js').read_text(encoding='utf-8')
    css += '\n' + (assets / 'evidence.css').read_text(encoding='utf-8')
    js += '\n' + (assets / 'evidence.js').read_text(encoding='utf-8')
    css += '\n' + (assets / 'document.css').read_text(encoding='utf-8')
    js += '\n' + (assets / 'document.js').read_text(encoding='utf-8')
    return html.replace('</style>', '</style><style>' + css + '</style>', 1).replace('</body>', '<script>' + js + '</script></body>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('json', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    data = load_json(args.json)
    with args.output.open('w' if args.overwrite else 'x', encoding='utf-8') as handle:
        handle.write(render(data))
    print(args.output.resolve())
