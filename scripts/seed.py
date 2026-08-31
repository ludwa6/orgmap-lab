#!/usr/bin/env python3
"""Seed the lab's CSV datasets from the two real orgmap sources.

  barlavento  <-  ~/dev/ercb-orgmap/index.html      (the inlined `const DATA={...}` block)
  vdl         <-  ~/dev/vdl-orgdev/graph.json       (generated from Notion by build-graph.mjs)

Deliberate omissions, both recorded in the vault note:
  * the spreadsheet's `contact` column (14 named individuals) is NOT carried over
  * nothing is invented: the 27 VdL Roles live only in Notion and graph.json holds none,
    so the seeded vdl dataset has no role nodes and will fail the vdl-target schema.

Usage:  python3 scripts/seed.py
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERCB = os.path.expanduser("~/dev/ercb-orgmap/index.html")
VDL  = os.path.expanduser("~/dev/vdl-orgdev/graph.json")

NODE_COLS = ["id", "name", "nodeType", "region", "membership", "roleType",
             "ratifiedOn", "reviewDate", "fullName", "status", "website", "themes", "purpose"]
EDGE_COLS = ["subject", "predicate", "object", "via", "confirmed", "source", "note"]

AFFILIATION = "https://schema.org/affiliation"
SHARED_PERS = "https://barlavento-eco.github.io/predicates/shared-personnel/"
MEMBER_OF   = "https://schema.org/memberOf"
COLOCATED   = "urn:barlavento:colocated"   # local pseudo-predicate; an attribute, never an edge

ETYPE_TO_PREDICATE = {
    "person":   SHARED_PERS,
    "network":  AFFILIATION,
    "convener": MEMBER_OF,
    "region":   COLOCATED,
}


def js_object_to_json(src):
    """The ercb DATA block is a JS literal: unquoted keys, otherwise JSON-compatible."""
    return re.sub(r'([{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', src)


def load_ercb():
    html = open(ERCB, encoding="utf-8").read()
    start = html.index("const DATA={")
    i = html.index("{", start)
    depth, j = 0, i
    while True:                       # brace-match rather than regex across 40 lines
        if html[j] == "{":
            depth += 1
        elif html[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    return json.loads(js_object_to_json(html[i:j + 1]))


def write_csv(path, cols, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"  {os.path.relpath(path, HERE)}  ({len(rows)} rows)")


def seed_barlavento():
    data = load_ercb()
    nodes = []
    for n in data["nodes"]:
        nodes.append({
            "id": n["id"], "name": n["name"], "nodeType": n.get("type", "Project"),
            "region": n.get("region", ""),
            # every organisation in this dataset is a community member; see the vault note on
            # why that makes membership carry zero distinguishing information today.
            "membership": "barlavento-eco",
            "website": n.get("website", ""),
            "themes": "; ".join(n.get("themes", [])),
            "purpose": n.get("purpose", ""),
            # n["contact"] deliberately dropped
        })
    edges = []
    for e in data["edges"]:
        pred = ETYPE_TO_PREDICATE[e["etype"]]
        label, via = e.get("label", ""), ""
        # The person is who the relationship runs THROUGH. It is recorded locally, in its own
        # column, and never travels into the published predicate -- see the note on `via` in
        # docs/GUIDE.md. Keeping it structured beats burying a name in free text.
        if pred == SHARED_PERS:
            via, label = label, ""
        edges.append({
            "subject": e["source"], "predicate": pred, "object": e["target"], "via": via,
            "confirmed": "false" if e.get("candidate") else "true",
            "source": "curated", "note": label,
        })
    print("barlavento:")
    write_csv(os.path.join(HERE, "data/barlavento/nodes.csv"), NODE_COLS, nodes)
    write_csv(os.path.join(HERE, "data/barlavento/edges.csv"), EDGE_COLS, edges)


def seed_vdl():
    g = json.load(open(VDL, encoding="utf-8"))
    nodes = [{
        "id": n["id"], "name": n.get("name", n["id"]), "nodeType": n.get("nodeType", ""),
        "fullName": n.get("fullName", ""),
        "status": n.get("status", ""), "purpose": n.get("purpose", ""),
        "roleType": n.get("roleType", ""),
        "ratifiedOn": n.get("ratifiedOn", ""), "reviewDate": n.get("reviewDate", ""),
    } for n in g["nodes"]]
    edges = [{
        "subject": e["source"], "predicate": e["type"], "object": e["target"], "via": "",
        "confirmed": "true", "source": "notion", "note": e.get("label", ""),
    } for e in g["edges"]]
    print("vdl:")
    write_csv(os.path.join(HERE, "data/vdl/nodes.csv"), NODE_COLS, nodes)
    write_csv(os.path.join(HERE, "data/vdl/edges.csv"), EDGE_COLS, edges)


if __name__ == "__main__":
    for p in (ERCB, VDL):
        if not os.path.exists(p):
            sys.exit(f"missing source: {p}")
    seed_barlavento()
    seed_vdl()
