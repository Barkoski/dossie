import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
