#!/usr/bin/env python3
"""Valida e consulta dossies JSON sem dependencias externas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

COLLECTIONS = ("partes", "documentos", "fatos", "requisitos", "teses")
VALID_FACT_GRADES = {"FATO COMPROVADO", "ALEGACAO", "INFERENCIA", "SEM FONTE NA CONVERSA"}
VALID_REQUIREMENT_STATES = {
    "COMPROVADO", "PARCIALMENTE COMPROVADO", "CONTROVERTIDO",
    "NAO COMPROVADO", "NAO APLICAVEL", "?",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("a raiz do JSON deve ser um objeto")
    return value


def index_entities(data: dict) -> tuple[dict[str, dict], list[str]]:
    index: dict[str, dict] = {}
    errors: list[str] = []
    for collection in COLLECTIONS:
        items = data.get(collection, [])
        if not isinstance(items, list):
            errors.append(f"{collection}: deve ser uma lista")
            continue
        for item in items:
            if not isinstance(item, dict) or not item.get("id"):
                errors.append(f"{collection}: entidade sem id")
                continue
            entity_id = str(item["id"])
            if entity_id in index:
                errors.append(f"id duplicado: {entity_id}")
            index[entity_id] = item | {"_colecao": collection}
    return index, errors


def validate(data: dict, html_path: Path | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if str(data.get("schema_version")) != "1.2":
        errors.append("schema_version deve ser 1.2")
    for key in ("caso", *COLLECTIONS, "arestas", "pendencias", "historico"):
        if key not in data:
            errors.append(f"campo obrigatorio ausente: {key}")

    index, index_errors = index_entities(data)
    errors.extend(index_errors)
    documents = {k: v for k, v in index.items() if v.get("_colecao") == "documentos"}

    for entity_id, item in index.items():
        if not item.get("origem_conversa"):
            warnings.append(f"{entity_id}: origem_conversa ausente")
        if item.get("_colecao") == "fatos":
            grade = item.get("grau")
            if grade not in VALID_FACT_GRADES:
                errors.append(f"{entity_id}: grau invalido: {grade}")
            doc_ids = item.get("documentos", [])
            for doc_id in doc_ids:
                if doc_id not in documents:
                    errors.append(f"{entity_id}: documento inexistente: {doc_id}")
            if grade == "FATO COMPROVADO":
                if not doc_ids:
                    errors.append(f"{entity_id}: fato comprovado sem documento")
                for doc_id in doc_ids:
                    doc = documents.get(doc_id, {})
                    if not doc.get("lido") or doc.get("localizacao") in (None, "", "PAGINA NAO IDENTIFICADA"):
                        errors.append(f"{entity_id}: documento {doc_id} nao lido ou sem localizacao")
        if item.get("_colecao") == "requisitos":
            if item.get("situacao") not in VALID_REQUIREMENT_STATES:
                errors.append(f"{entity_id}: situacao invalida")
            for fact_id in item.get("fatos", []):
                if fact_id not in index or index[fact_id].get("_colecao") != "fatos":
                    errors.append(f"{entity_id}: fato inexistente: {fact_id}")
        if item.get("_colecao") == "teses":
            for requirement_id in item.get("apoia_se", []):
                if requirement_id not in index or index[requirement_id].get("_colecao") != "requisitos":
                    errors.append(f"{entity_id}: requisito inexistente: {requirement_id}")

    edges = data.get("arestas", [])
    if not isinstance(edges, list):
        errors.append("arestas: deve ser uma lista")
    else:
        for pos, edge in enumerate(edges, 1):
            if not isinstance(edge, dict):
                errors.append(f"aresta {pos}: formato invalido")
                continue
            for endpoint in ("de", "para"):
                if edge.get(endpoint) not in index:
                    errors.append(f"aresta {pos}: {endpoint} inexistente: {edge.get(endpoint)}")
            if not edge.get("origem_conversa") and not edge.get("inferida"):
                warnings.append(f"aresta {pos}: sem origem_conversa")
            if edge.get("inferida") and not edge.get("base_inferencia"):
                errors.append(f"aresta {pos}: inferida sem base_inferencia")

    if html_path:
        html = html_path.read_text(encoding="utf-8")
        for pattern, label in (
            (r"(?:src|href)\s*=\s*[\"']https?://|url\(\s*[\"']?https?://", "recurso externo"),
            (r"\bfetch\s*\(", "fetch"),
            (r"<script[^>]+src=", "script externo"),
            (r"onerror\s*=|onclick\s*=", "evento inline"),
        ):
            if re.search(pattern, html, flags=re.IGNORECASE):
                errors.append(f"HTML contem {label}")
        if "Documento gerado a partir da analise em conversa" not in html:
            errors.append("HTML sem rodape obrigatorio")
        if "textContent" not in html:
            errors.append("HTML nao demonstra renderizacao segura por textContent")
        if len(re.findall(r"<script(?:\s|>)", html, flags=re.IGNORECASE)) != 1:
            errors.append("HTML deve conter exatamente um script inline")
    return errors, warnings


def adjacency(data: dict) -> dict[str, list[tuple[str, dict]]]:
    graph: dict[str, list[tuple[str, dict]]] = {}
    for edge in data.get("arestas", []):
        a, b = edge.get("de"), edge.get("para")
        if a and b:
            graph.setdefault(a, []).append((b, edge))
            graph.setdefault(b, []).append((a, edge))
    return graph


def command_validate(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    errors, warnings = validate(data, args.html)
    for item in warnings:
        print(f"AVISO: {item}")
    for item in errors:
        print(f"ERRO: {item}")
    if errors:
        print(f"FALHOU: {len(errors)} erro(s), {len(warnings)} aviso(s)")
        return 1
    print(f"VALIDO: {len(warnings)} aviso(s)")
    return 0


def command_explain(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    index, errors = index_entities(data)
    if errors or args.entity_id not in index:
        print("ENTIDADE NAO ENCONTRADA")
        return 1
    item = index[args.entity_id]
    print(json.dumps(item, ensure_ascii=False, indent=2))
    for neighbor, edge in adjacency(data).get(args.entity_id, []):
        print(f"{edge.get('de')} --{edge.get('tipo', '?')}--> {edge.get('para')} | origem: {edge.get('origem_conversa', '?')}")
    return 0


def command_path(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    index, _ = index_entities(data)
    if args.start not in index or args.end not in index:
        print("ENTIDADE NAO ENCONTRADA")
        return 1
    graph = adjacency(data)
    queue = deque([(args.start, [])])
    seen = {args.start}
    while queue:
        node, path = queue.popleft()
        if node == args.end:
            if not path:
                print(node)
            for a, b, edge in path:
                marker = "INFERIDA" if edge.get("inferida") else "AFIRMADA"
                if edge.get("de") == a and edge.get("para") == b:
                    relation = f"{a} --{edge.get('tipo', '?')} [{marker}]--> {b}"
                else:
                    relation = f"{a} <--{edge.get('tipo', '?')} [{marker}]-- {b}"
                print(f"{relation} | origem: {edge.get('origem_conversa', '?')}")
            return 0
        for neighbor, edge in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [(node, neighbor, edge)]))
    print("NAO HA CAMINHO REGISTRADO NO DOSSIE")
    return 2


def command_contradictions(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    found = [e for e in data.get("arestas", []) if e.get("tipo") == "contradiz"]
    if not found:
        print("NENHUMA CONTRADICAO REGISTRADA")
        return 0
    for edge in found:
        print(f"{edge.get('de')} contradiz {edge.get('para')} | origem: {edge.get('origem_conversa', '?')}")
    return 0


def command_gaps(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    count = 0
    for req in data.get("requisitos", []):
        if req.get("situacao") not in ("COMPROVADO", "NAO APLICAVEL") or req.get("lacuna"):
            print(f"{req.get('id')}: {req.get('situacao')} | lacuna: {req.get('lacuna') or '?'}")
            count += 1
    pending = data.get("pendencias", {})
    for key in ("sem_fonte", "nao_lidos", "conferir"):
        for item in pending.get(key, []):
            print(f"{key}: {item}")
            count += 1
    if count == 0:
        print("NENHUMA LACUNA REGISTRADA")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("json", type=Path)
    check.add_argument("--html", type=Path)
    check.set_defaults(func=command_validate)
    explain = sub.add_parser("explain")
    explain.add_argument("json", type=Path)
    explain.add_argument("entity_id")
    explain.set_defaults(func=command_explain)
    path = sub.add_parser("path")
    path.add_argument("json", type=Path)
    path.add_argument("start")
    path.add_argument("end")
    path.set_defaults(func=command_path)
    contradictions = sub.add_parser("contradictions")
    contradictions.add_argument("json", type=Path)
    contradictions.set_defaults(func=command_contradictions)
    gaps = sub.add_parser("gaps")
    gaps.add_argument("json", type=Path)
    gaps.set_defaults(func=command_gaps)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
