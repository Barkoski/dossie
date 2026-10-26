import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'dossie' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from migrate_legacy_html import extract_data
from render_dashboard import render


class LegacyMigrationTests(unittest.TestCase):
    def test_extracts_json_without_executing_the_rest_of_the_script(self):
        data = {'caso': {'identificacao': 'Exemplo fictício'}, 'marcos': [{'evento': 'Marco fictício'}], 'contradicoes': [{'id': 'C1', 'enunciado': 'Divergência fictícia'}]}
        html = '<script>const DATA = ' + json.dumps(data) + '; throw new Error("nunca executar");</script>'
        self.assertEqual(extract_data(html), data)

    def test_preserves_unknown_fields_and_original_classifications(self):
        data = {'fatos': [{'id': 'F1', 'grau': 'ALEGACAO'}], 'campo_adicional': {'origem': 'exemplo fictício'}}
        html = '<script>let DATA=' + json.dumps(data) + ';</script>'
        self.assertEqual(extract_data(html), data)

    def test_imports_only_the_literal_legacy_conclusion(self):
        conclusion = 'Conclusão documental fictícia explicitamente escrita no relatório antigo, preservada como texto de origem sem nova avaliação de mérito.'
        html = '<script>const DATA = {}; function reportText(){lines.push(\'CONCLUSÃO DOCUMENTAL\');lines.push(\'\');lines.push(\'' + conclusion + '\');}</script>'
        result = extract_data(html)
        self.assertEqual(result['resumo_documental'], conclusion)
        self.assertIn('sem nova validação', result['origem_resumo_documental'])

    def test_rejects_javascript_object_that_is_not_json(self):
        with self.assertRaises(ValueError):
            extract_data('<script>const DATA = {caso: dangerousFunction()};</script>')

    def test_rejects_html_without_recognizable_case_data(self):
        with self.assertRaises(ValueError):
            extract_data('<html><body>Texto sem JSON</body></html>')

    def test_text_inside_case_data_is_not_treated_as_report_code(self):
        data = {'conteudo': "lines.push('CONCLUSAO DOCUMENTAL');lines.push('" + 'x' * 100 + "');"}
        result = extract_data('<script>const DATA=' + json.dumps(data) + ';</script>')
        self.assertEqual(result, data)

    def test_new_renderer_preserves_all_optional_case_collections(self):
        data = {'caso': {'identificacao': 'Exemplo fictício'}, 'marcos': [{'data': '2001', 'evento': 'Marco de teste', 'fonte': 'D1', 'localizacao': 'p. 1'}], 'contradicoes': [{'id': 'C1', 'enunciado': 'Tensão de teste', 'fontes': 'D1 / D2'}], 'resumo_documental': 'Síntese fictícia já registrada.', 'triagem': {'questao_central': 'Questão de teste'}}
        self.assertEqual(extract_data(render(data)), data)


if __name__ == '__main__':
    unittest.main()
