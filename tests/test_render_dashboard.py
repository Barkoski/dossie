import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'dossie' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location('render_dashboard', SCRIPTS / 'render_dashboard.py')
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)
import dossie_tool


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.example = json.loads((ROOT / 'examples' / 'caso-ficticio.json').read_text(encoding='utf-8'))

    def test_case_data_round_trips_without_executable_markup(self):
        attack = '</script><img src=x onerror=alert(1)> & \u2028 \u2029'
        self.example['caso']['identificacao'] = attack
        html = RENDERER.render(self.example)
        embedded = re.search(r'<script id="dossie-data" type="application/json">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(embedded)['caso']['identificacao'], attack)
        self.assertNotIn('</script><img', html)
        self.assertNotIn('\u2028', embedded)
        self.assertNotIn('\u2029', embedded)

    def test_renderer_does_not_mutate_the_canonical_case(self):
        before = json.dumps(self.example, ensure_ascii=False)
        RENDERER.render(self.example)
        self.assertEqual(json.dumps(self.example, ensure_ascii=False), before)

    def test_full_document_preserves_long_text_and_inert_markup(self):
        full = 'Página 1\n' + ('texto do documento\n' * 1000) + '</script><img src=x onerror=alert(1)>\nFIM DA ÍNTEGRA'
        self.example['documentos'][0].update(texto_integral=full, texto_integral_status='COMPLETO', texto_integral_origem='documento fictício, pp. 1-2')
        rendered = RENDERER.render(self.example)
        payload = re.search(r'<script id="dossie-data" type="application/json">(.*?)</script>', rendered, re.S).group(1)
        self.assertEqual(json.loads(payload)['documentos'][0]['texto_integral'], full)
        self.assertNotIn('</script><img', rendered)

    def test_legacy_document_does_not_gain_an_invented_transcript(self):
        self.example['documentos'][0].pop('texto_integral', None)
        rendered = RENDERER.render(self.example)
        payload = re.search(r'<script id="dossie-data" type="application/json">(.*?)</script>', rendered, re.S).group(1)
        self.assertNotIn('texto_integral', json.loads(payload)['documentos'][0])

    def test_self_contained_html_passes_existing_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'dossie.html'
            output.write_text(RENDERER.render(self.example), encoding='utf-8')
            errors, warnings = dossie_tool.validate(self.example, output)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)

    def test_cli_preserves_existing_output_by_default(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'existing.html'
            output.write_text('preservar', encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPTS / 'render_dashboard.py'), str(ROOT / 'examples' / 'caso-ficticio.json'), '--output', str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding='utf-8'), 'preservar')

    def test_actual_inline_event_attribute_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'unsafe.html'
            output.write_text(RENDERER.render(self.example).replace('<body>', '<body onload="alert(1)">', 1), encoding='utf-8')
            errors, _ = dossie_tool.validate(self.example, output)
        self.assertIn('HTML contem evento inline', errors)


if __name__ == '__main__':
    unittest.main()
