"""Extrai dados de HTML legado sem executar JavaScript ou modificar o original."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata


class ScriptReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.current = {'attrs': dict(attrs), 'text': ''}

    def handle_data(self, text):
        if self.current is not None:
            self.current['text'] += text

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.scripts.append(self.current)
            self.current = None


def extract_data(html):
    reader = ScriptReader()
    reader.feed(html)
    for script in reader.scripts:
        if script['attrs'].get('id') == 'dossie-data':
            data = json.loads(script['text'])
            if not isinstance(data, dict):
                raise ValueError('O objeto do dossiê deve ser um dicionário.')
            return data
    for script in reader.scripts:
        found = re.search(r'\b(?:const|let|var)\s+DATA\s*=\s*', script['text'])
        if not found:
            continue
        data, data_end = json.JSONDecoder().raw_decode(script['text'][found.end():])
        if not isinstance(data, dict):
            raise ValueError('O objeto DATA deve ser um dicionário.')
        # Somente texto literal já escrito no relatório; não executar funções do HTML.
        script_after_data = script['text'][found.end() + data_end:]
        literals = re.findall(r"lines\.push\('((?:\\.|[^'\\])*)'\)", script_after_data)
        for position, text in enumerate(literals):
            normalized = ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c))
            if normalized.strip().upper() != 'CONCLUSAO DOCUMENTAL':
                continue
            conclusion = next((x for x in literals[position + 1:] if x.strip()), None)
            if conclusion and len(conclusion) > 80 and 'resumo_documental' not in data:
                escapes = {'n': '\n', 'r': '\r', 't': '\t', "'": "'", '"': '"', '\\': '\\'}
                conclusion = re.sub(r'\\([nrt\'"\\])', lambda m: escapes[m.group(1)], conclusion)
                data['resumo_documental'] = conclusion
                data['origem_resumo_documental'] = 'Conclusão textual do relatório no HTML legado; preservada sem nova validação de mérito.'
            break
        return data
    raise ValueError('Não foi encontrado JSON canônico reconhecível. Nenhum script foi executado.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output-json', required=True, type=Path)
    args = parser.parse_args()
    data = extract_data(args.input.read_text(encoding='utf-8-sig'))
    with args.output_json.open('x', encoding='utf-8') as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
    print('Dados extraídos localmente. Revise as fontes e os identificadores antes de apresentar.')
