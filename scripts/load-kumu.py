#!/usr/bin/env python3
"""Turn a Kumu .xlsx export into a lab dataset.

    python3 scripts/load-kumu.py <export.xlsx> --dataset cofundeco

Kumu exports one flat sheet per side, with the union of every field any element
type has ever had — 140 columns here, most empty on any given row. Among them
are a members' survey: emails, LinkedIn URLs, postal codes, mailing-list
opt-ins.

⚠️ **This repository is public.** So the boundary rule is an ALLOWLIST, not a
denylist: a column reaches the CSVs only if it is named below. A new export
with a new personal field is therefore dropped by default rather than
published by default — the failure mode of a denylist is silent and permanent,
and no correction can un-publish it.

Names are kept. They are the node labels, a map without them says nothing, and
a Kumu map is already shared within its community. Contact details are not
kept: being in someone's map is not consent to be in someone's address book.
"""
import argparse
import csv
import pathlib
import re
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("needs openpyxl:  pip3 install openpyxl")

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (source column -> emitted column). Everything absent from these maps is dropped.
NODE_COLS = {
    "ID": "id",
    "Label": "name",
    "Type": "nodeType",
    "Description": "purpose",
    "city or town": "city",
    "country": "region",
    "project name": "project",
    "website(s)": "website",
    "segment": "segment",
}
EDGE_COLS = {
    "Type": "predicate",
    "Direction": "direction",
    "weight": "weight",
    "short description of this connection": "note",
    "status of my relationship with this project": "status",
}

# Named so the drop is a decision on the record rather than an oversight.
DROPPED_PERSONAL = [
    "email", "email for notifications", "project contact email", "first name", "last name",
    "linkedin", "postal code", "project postal code", "project street address",
    "node contact information", "other contact links", "other project contact info",
    "mailchimp opt-in", "email notification preference", "terms and conditions",
]

REF = re.compile(r"^(.*?)\s*<(\d+)>\s*$")   # Kumu writes endpoints as "Label <id>"


def sheet(wb, name):
    rows = list(wb[name].iter_rows(values_only=True))
    hdr = [str(c).strip() if c else "" for c in rows[0]]
    return hdr, rows[1:]


def cell(row, hdr, col):
    i = hdr.index(col) if col in hdr else -1
    if i < 0 or i >= len(row) or row[i] is None:
        return ""
    return str(row[i]).strip()


def endpoint(raw, by_label):
    """Resolve "Label <id>" — or a bare label — to a node id."""
    m = REF.match(raw or "")
    if m:
        return m.group(2)
    return by_label.get((raw or "").strip(), "")


def build(xlsx, dataset):
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    ehdr, erows = sheet(wb, "Elements")
    chdr, crows = sheet(wb, "Connections")

    present = [c for c in DROPPED_PERSONAL
               if c in ehdr and any(cell(r, ehdr, c) for r in erows)]

    nodes, by_label = [], {}
    for r in erows:
        n = {out: cell(r, ehdr, src) for src, out in NODE_COLS.items()}
        if not n["id"] or not n["name"]:
            continue
        nodes.append(n)
        by_label[n["name"]] = n["id"]

    ids = {n["id"] for n in nodes}
    edges, dropped = [], 0
    for r in crows:
        subj = endpoint(cell(r, chdr, "From"), by_label)
        obj = endpoint(cell(r, chdr, "To"), by_label)
        if subj not in ids or obj not in ids or subj == obj:
            dropped += 1          # an endpoint Kumu knows and this export does not
            continue
        e = {out: cell(r, chdr, src) for src, out in EDGE_COLS.items()}
        e.update(subject=subj, object=obj, confirmed="true", source="kumu")
        edges.append(e)

    out = ROOT / "data" / dataset
    out.mkdir(parents=True, exist_ok=True)
    ncols = list(NODE_COLS.values())
    ecols = ["subject", "predicate", "object"] + [c for c in EDGE_COLS.values() if c != "predicate"] \
            + ["confirmed", "source"]
    for path, cols, rows in ((out / "nodes.csv", ncols, nodes), (out / "edges.csv", ecols, edges)):
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    kinds = sorted({n["nodeType"] for n in nodes if n["nodeType"]})
    preds = sorted({e["predicate"] for e in edges if e["predicate"]})
    print(f"  {len(nodes)} nodes {kinds}")
    print(f"  {len(edges)} edges {preds}" + (f"  ({dropped} skipped: endpoint not in this export)" if dropped else ""))
    print(f"  dropped {len(present)} populated personal columns: {', '.join(present)}")
    print(f"  -> data/{dataset}/")

    # Say it out loud: a column nobody listed is a column nobody published.
    ignored = [c for c in ehdr
               if c and c not in NODE_COLS and c not in DROPPED_PERSONAL
               and any(cell(r, ehdr, c) for r in erows)]
    if ignored:
        print(f"\n  {len(ignored)} other populated columns were dropped because they are not on the")
        print("  allowlist. Add any that belong on the map to NODE_COLS:")
        for c in ignored:
            print(f"    - {c}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--dataset", required=True)
    a = ap.parse_args()
    build(a.xlsx, a.dataset)
