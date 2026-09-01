# OrgMap Lab

**Repo:** `ludwa6/orgmap-lab` — **private for now.** The renderer is destined to be open source;
the repo also carries `data/vdl/*.csv`, which names real staff. Those names are already public at
<https://valedalama.github.io/vdl-orgdev/> by a deliberate transparency decision, so going public
breaks nothing — but publishing is one click and un-publishing is not, so the default is closed until
that is a decision rather than a side effect.

A local sandbox for prototyping org-map **views** and **controlled vocabularies** over two real
datasets, without touching either project repo. Nothing here deploys anywhere.

```sh
./run.sh              # local, on whichever machine you are editing on
./deploy-to-mini.sh   # push to the always-on Mini and restart it there
```

| Where | URL | When to use it |
|---|---|---|
| This machine | `http://localhost:8090/` | editing |
| The Mini, over Tailscale | `http://mudvalleyinstitutes-mac-mini.tailb0b9f5.ts.net:8090/` | **demoing, from any device on the tailnet** |

The Mini copy is held up by a `KeepAlive` LaunchAgent (`com.waltz.orgmap-lab`), so it survives a
crash and comes back at login. It does **not** come back on an unattended reboot — FileVault, same
as the WordPress sandbox. Editing happens here and is pushed there; the Mini copy is a deployment,
not a second working tree.

## The two products

The same file runs in two modes. `manifest.json` sets the default; `?mode=view` and
`?mode=workbench` override it.

| | The Map | The Workbench |
|---|---|---|
| For | everyone in the organisation | whoever does the modelling |
| Editor | **removed from the DOM** | present |
| Writes to the browser | **nothing at all** | edits and layout |

A per-organisation deployment sets `"mode": "view"` and declares only its own dataset. This repo is
the workbench: `mode: workbench`, three datasets.

**Live example:** <https://valedalama.github.io/vdl-orgdev/> runs this renderer in view mode.

## Adding an organisation

Touches no code &mdash; tested, not asserted. A manifest entry, a schema, and two CSVs:

```
manifest.json          one entry under "datasets"
schemas/<yours>.json   node kinds, predicates, and what may join what
data/<yours>/nodes.csv id, name, nodeType, + anything else you keep
data/<yours>/edges.csv subject, predicate, object
```

Copy `schemas/example.json` and `data/example/` &mdash; they exist to be forked.

A dataset may instead declare `"source": {"format": "graph", "path": "graph.json"}` to read a single
`{nodes, edges}` JSON, which is how the Vale da Lama deployment consumes what its Notion job emits.

A plain `file://` open will not work — the page fetches its schemas and CSVs.

---

**End-user documentation:** [`docs/field-guide.html`](docs/field-guide.html) &mdash; rewritten
2026-09-01 for the current app: two products, roles as nodes, channels and beads, modes and
manifest; purpose, the two reader paths (new at Vale da Lama, new to the Barlavento community),
the two administrator roles, the full data models, and what is still provisional. It is served
from this repo's Pages at <https://ludwa6.github.io/orgmap-lab/docs/field-guide.html>, which is
where every deployment's `manifest.guideUrl` points. This README is the builder's view; the guide
is the user's.

## The premise it corrects

The VdL and barlavento maps are **not** the same code with different data. They are forked
siblings off a common ancestor (`~/claude-workspace/projects/vdl-orgmap`) that have since diverged:

| | `~/dev/vdl-orgdev/index.html` | `~/dev/ercb-orgmap/index.html` |
|---|---|---|
| D3 | CDN (`cdnjs`, 7.9.0) | vendored (`vendor/d3.min.js`) |
| Data | `fetch('graph.json')` from Notion | `const DATA={…}` inlined at line 137 |
| Nodes | `nodeType`: circle, person | `NODE_STYLES`: Project, Initiative, Convener, Network |
| Edges | subcircle, represents, leads, energizes | convener, region, network, person |

Same bones (`graphContainer`, `activeFilters`, `forceSimulation`, an `EDGE_STYLES` table), diverged
flesh. So this lab is not a third fork. It is **one renderer that knows nothing about either
organisation**, driven entirely by an external schema file.

## Layout

```
index.html              the renderer + editor + validator (single file, d3 vendored)
schemas/*.json          four controlled vocabularies — two per dataset
data/<ds>/nodes.csv     seeded from the real sources; the only data in the repo
data/<ds>/edges.csv
scripts/seed.py         regenerates the CSVs from ercb-orgmap and vdl-orgdev
run.sh                  static server
```

## The design move: the schema pair is the argument, made executable

Both datasets ship with **two** schemas — the model the map uses today, and the model its open
issue is arguing for. Switching between them changes nothing in the data file, only the reading of
it, which is the "one dataset, many views" claim tested rather than asserted.

| Dataset | Switch from | to | What you see |
|---|---|---|---|
| Barlavento | as recorded today | `vocabulary.md` (PR #19) | **23 rows in, 5 edges out.** Membership and co-location are absorbed onto the nodes; the convener stops being the centre |
| VdL | as `build-graph.mjs` emits | `org:Post` model (#2) | the 18 collapsed `leads` / `represents` / `energizes` edges **fail validation**, each naming the rule it breaks |

## Vocabulary enforcement, two layers

1. **By construction.** Every schema-controlled field in the editor is a `<select>` populated from
   the schema. The relationship editor only offers predicates whose `kind` is `edge` — you cannot
   record co-location as a line, because the option does not exist. A value already in the data that
   the schema does not allow is kept, marked red, and labelled *not in vocabulary* rather than
   silently dropped.
2. **By validation.** The Validate tab runs every rule over the whole dataset:
   `node.type-in-vocabulary` · `node.attribute-in-vocabulary` · `edge.predicate-in-vocabulary` ·
   `edge.subject-type` · `edge.object-type` · `edge.endpoint-exists` · `edge.no-self-loop` ·
   `edge.duplicate` · `edge.predicate-deprecated` · `edge.absorbed-as-attribute`.

Endpoint typing is the load-bearing rule for VdL: `energizes` must run person → **role**, so a
person → circle edge is refused rather than quietly drawn. That refusal is exactly the loss
`valedalama/vdl-orgdev#2` describes.

## Writing a schema

```jsonc
{
  "nodeTypes":  [ { "id": "role", "label": "Role (org:Post)", "color": "#f5a623", "r": 18 } ],
  "attributes": [ { "key": "roleType", "control": "enum",       // enum | enum-open | text
                    "values": ["", "Secretary", "Circle Lead"],
                    "render": "badge" } ],                      // color | badge | (omit)
  "predicates": [
    { "id": "energizes", "kind": "edge",                        // edge | attribute
      "subjectTypes": ["person"], "objectTypes": ["role"],      // "*" allows any
      "directed": true, "style": { "color": "#2dd4bf", "width": 1.8, "dash": null } },

    { "id": "https://schema.org/memberOf", "kind": "attribute", // never drawn as a line
      "absorbInto": { "key": "membership", "value": "barlavento-eco" },
      "rationale": "Belonging is a fact about one organisation." }
  ]
}
```

`kind: "attribute"` is the whole point of the exercise: the row stays in the data file, and the
renderer moves it onto the nodes instead of drawing it. Set `absorbInto.value` to `null` when the
nodes already carry the fact themselves (co-location does — every node has its own `region`).

## Framing the map

The docked view is for editing; the map wants the whole screen when you are reading the effect of a
tweak. Four ways to get it, all remembered between sessions:

| | |
|---|---|
| `m` | **map only** — hides both the panels and the controls |
| `p` | panels on/off (the tab strip stays; clicking a tab brings them back to it) |
| `c` | controls on/off |
| `f` | browser fullscreen |
| `esc` | bring it all back |

The same four are buttons in the header, and the bar above the tab strip drags to any height.

The layout responds to the space it is given: a small change nudges the centring force so the graph
you were reading stays put, while a big one (going map-only or fullscreen) re-derives the layout and
widens the link distances so the graph actually fills the canvas instead of sitting in a clump.
**Re-derive layout** forces a fresh one at any time.

## Editing and export

Edits persist to `localStorage` per dataset, so a reload keeps them. **Reset to seed** discards them
and re-reads the CSVs. **Export nodes.csv / edges.csv** hands back a file in the same shape it was
loaded in, so a session's work can go into a repo as a real data file.

The lab is not a source of truth. It is where you decide what the schema should say before writing
it into `barlavento-eco/barlavento-eco.github.io` or `valedalama/vdl-orgdev`.

## Honest limits

- **The 27 VdL Roles are not here.** `graph.json` holds none of them; they live in Notion, and this
  lab does not invent data. So the `vdl-target` schema describes a model the seeded data cannot yet
  satisfy — the validation failures are the finding, not a defect.
- **The `contact` column is dropped on seed** (14 named individuals). Nothing in the render used it.
- The one edge recorded as `candidate: TRUE` is carried through as `confirmed: false` and drawn
  dotted, rather than silently promoted to fact.
