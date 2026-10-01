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
VALID_FACT_GRADES = {"FATO COMPROVADO", "ALEGACAO", "INFERENCIA", "SEM FONTE NA CONVERSA", "CONCLUSAO JURIDICA"}
VALID_REQUIREMENT_STATES = {
    "COMPROVADO", "PARCIALMENTE COMPROVADO", "CONTROVERTIDO",
    "NAO COMPROVADO", "NAO APLICAVEL", "?",
}
VALID_DOCUMENT_FAMILIES = {
    "PECA_PROCESSUAL", "DECISAO", "ATO_PROCESSUAL", "PROVA_PESSOAL",
    "PROVA_MEDICA", "PROVA_LABORAL_PREVIDENCIARIA", "PROVA_CIVIL",
    "PROVA_ECONOMICA", "PROVA_RURAL", "PARECER_OU_LAUDO", "MIDIA", "OUTRO",
}
VALID_IDENTIFICATION_CONFIDENCE = {"ALTA", "MEDIA", "BAIXA"}



def _shape_errors(data):
    """Reject malformed JSON fields before semantic checks or queries use them."""
    if not isinstance(data, dict):
        return ["a raiz do JSON deve ser um objeto"]
    errors = []
    object_keys = ("caso", "triagem", "pendencias")
    for key in object_keys:
        if key in data and not isinstance(data[key], dict):
            errors.append(key + ": deve ser um objeto")
    collections = (*COLLECTIONS, "arestas", "historico", "normas", "marcos", "prazos")
    scalar_fields = {
        "id", "grau", "situacao", "familia", "confianca_identificacao", "qualidade",
        "qualidade_da_leitura", "estado", "documento", "requisito", "de", "para",
        "tipo", "localizacao", "estado_conferencia", "enunciado", "origem",
        "origem_conversa", "base_inferencia",
    }
    for key in collections:
        if key not in data:
            continue
        if not isinstance(data[key], list):
            errors.append(key + ": deve ser uma lista")
            continue
        for pos, item in enumerate(data[key]):
            label = f"{key}[{pos}]"
            if not isinstance(item, dict):
                errors.append(label + ": deve ser um objeto")
                continue
            for field in scalar_fields:
                if field in item and not isinstance(item[field], str):
                    errors.append(label + ": " + field + " deve ser texto")
            for field in ("lido", "inferida", "documento_estranho"):
                if field in item and not isinstance(item[field], bool):
                    errors.append(label + ": " + field + " deve ser booleano")
            for field in ("documentos", "fatos", "apoia_se"):
                if field in item and (not isinstance(item[field], list) or any(not isinstance(x, str) or not x.strip() for x in item[field])):
                    errors.append(label + ": " + field + " deve ser lista de IDs textuais")
            if "suportes" in item and (not isinstance(item["suportes"], list) or any(not isinstance(x, dict) for x in item["suportes"])):
                errors.append(label + ": suportes deve ser lista de objetos")
    for key in ("decisao_operacional", "decisao_paralela"):
        if key in data and data[key] is not None and not isinstance(data[key], str):
            errors.append(key + ": deve ser texto")
    return errors

def _missing(value):
    return value is None or (isinstance(value, str) and value.strip().upper() in
        ("", "?", "PAGINA NAO IDENTIFICADA", "NAO INFORMADO", "NÃO INFORMADO"))

def _pending_cites(items, entity_id):
    for item in items:
        value = str(item).strip()
        if value == entity_id or (value.startswith(entity_id) and value[len(entity_id):len(entity_id)+1] in (":", " ", "-", ".", ",", ")", "—")):
            return True
    return False

def _conference_checks(index, errors):
    states = {"ORIGINAL CONFERIDO", "SOMENTE TRANSCRICAO", "RELATADO NA CONVERSA", "NAO LIDO"}
    for eid, item in index.items():
        if item.get("_colecao") != "documentos" or "estado_conferencia" not in item:
            continue
        state = item["estado_conferencia"]
        if state not in states:
            errors.append(eid + ": estado_conferencia invalido")
        if state == "ORIGINAL CONFERIDO" and (item.get("lido") is not True or _missing(item.get("registro_conferencia")) or _missing(item.get("localizacao"))):
            errors.append(eid + ": original conferido exige leitura, localizacao e registro_conferencia")
        if state == "NAO LIDO" and item.get("lido") is not False:
            errors.append(eid + ": estado_conferencia contradiz lido")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("a raiz do JSON deve ser um objeto")
    shape = _shape_errors(value)
    if shape:
        raise ValueError("; ".join(shape))
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
    shape = _shape_errors(data)
    if shape:
        return shape, []
    errors: list[str] = []
    warnings: list[str] = []
    if str(data.get("schema_version")) != "1.3":
        errors.append("schema_version deve ser 1.3")
    for key in ("caso", "triagem", *COLLECTIONS, "arestas", "pendencias", "historico"):
        if key not in data:
            errors.append(f"campo obrigatorio ausente: {key}")

    index, index_errors = index_entities(data)
    errors.extend(index_errors)
    _conference_checks(index, errors)
    documents = {k: v for k, v in index.items() if v.get("_colecao") == "documentos"}

    triage = data.get("triagem", {})
    if not isinstance(triage, dict):
        errors.append("triagem: deve ser um objeto")
    else:
        for key in ("tipo_procedimento", "assunto_principal", "questao_central", "origem_conversa"):
            if not triage.get(key):
                errors.append(f"triagem: campo ausente: {key}")
        for key in ("pontos_controvertidos", "palavras_chave", "normas_invocadas"):
            if not isinstance(triage.get(key), list):
                errors.append(f"triagem: {key} deve ser uma lista")

    for entity_id, item in index.items():
        if not item.get("origem_conversa"):
            warnings.append(f"{entity_id}: origem_conversa ausente")
        if item.get("_colecao") == "documentos":
            if item.get("familia") not in VALID_DOCUMENT_FAMILIES:
                errors.append(f"{entity_id}: familia documental invalida")
            if not item.get("tipo") or not item.get("resumo"):
                errors.append(f"{entity_id}: tipo ou resumo documental ausente")
            if item.get("confianca_identificacao") not in VALID_IDENTIFICATION_CONFIDENCE:
                errors.append(f"{entity_id}: confianca_identificacao invalida")
            for field in ("evento_inicio", "pagina_inicio", "evento_fim", "pagina_fim", "criterio_delimitacao"):
                if item.get(field) in (None, ""):
                    errors.append(f"{entity_id}: campo de delimitacao ausente: {field}")
            if item.get("confianca_identificacao") == "BAIXA" and item.get("lido"):
                warnings.append(f"{entity_id}: identificacao documental com confianca baixa")
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
                    if doc.get("lido") is not True or _missing(doc.get("localizacao")):
                        errors.append(f"{entity_id}: documento {doc_id} nao lido ou sem localizacao")
        if item.get("_colecao") == "requisitos":
            if item.get("situacao") not in VALID_REQUIREMENT_STATES:
                errors.append(f"{entity_id}: situacao invalida")
            if item.get("situacao") == "COMPROVADO" and not item.get("fatos"):
                errors.append(f"{entity_id}: requisito comprovado sem fatos de suporte")
            for fact_id in item.get("fatos", []):
                if fact_id not in index or index[fact_id].get("_colecao") != "fatos":
                    errors.append(f"{entity_id}: fato inexistente: {fact_id}")
        if item.get("_colecao") == "teses":
            for requirement_id in item.get("apoia_se", []):
                if requirement_id not in index or index[requirement_id].get("_colecao") != "requisitos":
                    errors.append(f"{entity_id}: requisito inexistente: {requirement_id}")

    case = data.get("caso", {})
    for field in ("identificacao", "materia", "fase", "data_referencia"):
        if field not in case or case[field] in (None, ""):
            errors.append("caso: campo ausente: " + field)
    pending = data.get("pendencias", {})
    for block in ("sem_fonte", "nao_lidos", "conferir"):
        if not isinstance(pending.get(block), list):
            errors.append("pendencias: bloco ausente ou invalido: " + block)
    valid_pending = all(isinstance(pending.get(k), list) for k in ("sem_fonte", "nao_lidos", "conferir"))
    for eid, item in index.items():
        collection = item["_colecao"]
        if _missing(item.get("origem_conversa")) and (not valid_pending or not _pending_cites(pending["sem_fonte"], eid)):
            errors.append(eid + ": sem origem e ausente de pendencias.sem_fonte")
        if collection == "documentos":
            if not isinstance(item.get("lido"), bool):
                errors.append(eid + ": lido deve ser booleano")
            if item.get("qualidade") not in {"TEXTO NITIDO", "OCR DUVIDOSO", "LEITURA PARCIAL", "ILEGIVEL", "NAO LIDO"}:
                errors.append(eid + ": qualidade invalida")
            if item.get("lido") == (item.get("qualidade") == "NAO LIDO"):
                errors.append(eid + ": leitura contradiz qualidade")
            if item.get("lido") is False and (not valid_pending or not _pending_cites(pending["nao_lidos"], eid)):
                errors.append(eid + ": nao lido ausente das pendencias")
        if collection == "fatos":
            if _missing(item.get("enunciado")):
                errors.append(eid + ": enunciado ausente")
            if item.get("grau") == "INFERENCIA" and _missing(item.get("base_inferencia")):
                errors.append(eid + ": inferencia sem base_inferencia")
            if item.get("grau") == "SEM FONTE NA CONVERSA" and (not valid_pending or not _pending_cites(pending["sem_fonte"], eid)):
                errors.append(eid + ": fato sem fonte ausente das pendencias")
            for doc_id in item.get("documentos", []):
                if doc_id in documents and documents[doc_id].get("lido") is not True:
                    errors.append(eid + ": documento nao lido nao sustenta fato: " + doc_id)

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
                errors.append(f"aresta {pos}: sem origem_conversa")
            if edge.get("inferida") and not edge.get("base_inferencia"):
                errors.append(f"aresta {pos}: inferida sem base_inferencia")
            if _missing(edge.get("tipo")):
                errors.append(f"aresta {pos}: tipo ausente")
            source = index.get(edge.get("de"), {})
            target = index.get(edge.get("para"), {})
            if edge.get("tipo") in ("comprova", "registra"):
                if source.get("_colecao") != "documentos" or target.get("_colecao") != "fatos":
                    errors.append(f"aresta {pos}: relacao documental deve ligar documento a fato")
                elif source.get("lido") is not True:
                    errors.append(f"aresta {pos}: documento nao lido nao sustenta fato")

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
        warnings.append("HTML: inspecao estatica parcial; testar offline, injecao, rede e interface no navegador. Nao e certificado de seguranca.")
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
    print(f"ESTRUTURA VALIDA: {len(warnings)} aviso(s). Fontes e merito nao conferidos pelo script.")
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


def command_documents(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    print("ID\tFAMILIA\tTIPO\tINICIO\tFIM\tCONFIANCA\tRESUMO")
    for doc in data.get("documentos", []):
        start = f"{doc.get('evento_inicio', '?')} / {doc.get('pagina_inicio', '?')}"
        end = f"{doc.get('evento_fim', '?')} / {doc.get('pagina_fim', '?')}"
        print(
            f"{doc.get('id')}\t{doc.get('familia')}\t{doc.get('tipo')}\t{start}\t{end}\t"
            f"{doc.get('confianca_identificacao')}\t{doc.get('resumo')}"
        )
    return 0


def command_screening(args: argparse.Namespace) -> int:
    data = load_json(args.json)
    triage = data.get("triagem")
    if not isinstance(triage, dict):
        print("TRIAGEM NAO ENCONTRADA")
        return 1
    print(json.dumps(triage, ensure_ascii=False, indent=2))
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
    documents = sub.add_parser("documents")
    documents.add_argument("json", type=Path)
    documents.set_defaults(func=command_documents)
    screening = sub.add_parser("screening")
    screening.add_argument("json", type=Path)
    screening.set_defaults(func=command_screening)
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