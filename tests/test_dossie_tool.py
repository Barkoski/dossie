import importlib.util
import io
import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "skills" / "dossie" / "scripts" / "dossie_tool.py"
SPEC = importlib.util.spec_from_file_location("dossie_tool", TOOL_PATH)
TOOL = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(TOOL)


class DossieToolTests(unittest.TestCase):
    def setUp(self):
        self.example = TOOL.load_json(ROOT / "examples" / "caso-ficticio.json")

    def test_example_is_valid(self):
        errors, warnings = TOOL.validate(
            self.example, ROOT / "examples" / "caso-ficticio.html"
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_duplicate_id_is_rejected(self):
        data = json.loads(json.dumps(self.example))
        data["fatos"].append(dict(data["fatos"][0]))
        errors, _ = TOOL.validate(data)
        self.assertTrue(any("id duplicado" in item for item in errors))

    def test_proven_fact_requires_read_document_with_location(self):
        data = json.loads(json.dumps(self.example))
        data["fatos"][0]["documentos"] = ["D3"]
        errors, _ = TOOL.validate(data)
        self.assertTrue(any("nao lido ou sem localizacao" in item for item in errors))

    def test_inferred_edge_requires_basis(self):
        data = json.loads(json.dumps(self.example))
        data["arestas"][0]["inferida"] = True
        data["arestas"][0]["base_inferencia"] = ""
        errors, _ = TOOL.validate(data)
        self.assertTrue(any("inferida sem base_inferencia" in item for item in errors))

    def test_external_html_resource_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            html = Path(folder) / "bad.html"
            html.write_text(
                '<script src="https://example.invalid/x.js"></script>'
                "Documento gerado a partir da analise em conversa textContent",
                encoding="utf-8",
            )
            errors, _ = TOOL.validate(self.example, html)
        self.assertTrue(any("recurso externo" in item for item in errors))

    def test_thesis_requires_existing_requirement(self):
        data = json.loads(json.dumps(self.example))
        data["teses"][0]["apoia_se"] = ["R404"]
        errors, _ = TOOL.validate(data)
        self.assertTrue(any("requisito inexistente" in item for item in errors))

    def capture(self, function, **kwargs):
        output = io.StringIO()
        with redirect_stdout(output):
            status = function(Namespace(**kwargs))
        return status, output.getvalue()

    def test_explain_returns_entity_and_connections(self):
        status, output = self.capture(
            TOOL.command_explain,
            json=ROOT / "examples" / "caso-ficticio.json",
            entity_id="R1",
        )
        self.assertEqual(status, 0)
        self.assertIn('"id": "R1"', output)
        self.assertIn("F1 --sustenta--> R1", output)

    def test_path_returns_registered_route(self):
        status, output = self.capture(
            TOOL.command_path,
            json=ROOT / "examples" / "caso-ficticio.json",
            start="D1",
            end="T1",
        )
        self.assertEqual(status, 0)
        self.assertIn("D1 --comprova [AFIRMADA]--> F1", output)
        self.assertIn("R2 --compoe [AFIRMADA]--> T1", output)

    def test_contradictions_reports_empty_case(self):
        status, output = self.capture(
            TOOL.command_contradictions,
            json=ROOT / "examples" / "caso-ficticio.json",
        )
        self.assertEqual(status, 0)
        self.assertIn("NENHUMA CONTRADICAO REGISTRADA", output)

    def test_gaps_reports_requirements_and_pending_items(self):
        status, output = self.capture(
            TOOL.command_gaps,
            json=ROOT / "examples" / "caso-ficticio.json",
        )
        self.assertEqual(status, 0)
        self.assertIn("R1: PARCIALMENTE COMPROVADO", output)
        self.assertIn("nao_lidos: D3: CNIS", output)

    def test_main_validate_command(self):
        argv = [
            "dossie_tool.py",
            "validate",
            str(ROOT / "examples" / "caso-ficticio.json"),
            "--html",
            str(ROOT / "examples" / "caso-ficticio.html"),
        ]
        output = io.StringIO()
        with patch.object(TOOL.sys, "argv", argv), redirect_stdout(output):
            status = TOOL.main()
        self.assertEqual(status, 0)
        self.assertIn("VALIDO: 0 aviso(s)", output.getvalue())

    def test_main_reports_missing_entity(self):
        argv = [
            "dossie_tool.py",
            "explain",
            str(ROOT / "examples" / "caso-ficticio.json"),
            "R404",
        ]
        output = io.StringIO()
        with patch.object(TOOL.sys, "argv", argv), redirect_stdout(output):
            status = TOOL.main()
        self.assertEqual(status, 1)
        self.assertIn("ENTIDADE NAO ENCONTRADA", output.getvalue())


if __name__ == "__main__":
    unittest.main()
