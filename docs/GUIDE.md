# OrgMap Lab — Field Guide

*Insider preview, 29 August 2026. Everything here is up for revision; where a choice is still open,
this guide says so.*

A shareable rendering of this document lives alongside it as `docs/field-guide.html`. This file is
the version that travels with the code — correct it here first.

---

## 1. What this is

A tool for mapping the social system of an organisation, or of a community of organisations, from a
data file anyone can read.

Most org charts are drawings: somebody arranges boxes and the arrangement becomes the claim. When
the organisation changes the drawing is redrawn, and the reasoning behind the first version is lost.

OrgMap Lab works the other way round. A **data file** records what is true; a **schema** says what
kinds of thing may be recorded and how each is drawn. The picture is generated. Change the data and
the picture follows; change the schema and the same data is read differently, with nothing edited.

Two maps run in it today — a single farm's internal governance, and a bioregional network of
independent land projects. That they run on the same renderer is the point: a third context needs a
schema file, not a fork.

## 2. The one idea

**Attributes are not relationships.** Being in the same valley is a fact about *each* organisation,
not a line between them. Three organisations in Bensafrim should not produce a triangle. Belonging
to a community is the same kind of fact. Drawn as lines, these swamp the map — and they swamp it in
a way that looks like a finding rather than an artefact.

**A relationship is a claim, and it is typed.** Every line names its kind as a **predicate** — a
stable web address that explains what the line means. Not "a connection", but *this organisation
declares an affiliation with that one*, or *this role sits in that circle*. The type is data, not
styling, so the map can be filtered, checked and argued with.

**Views are filters over one dataset.** The public map, a regional view, a governance view: all the
same rows read through different rules. Never a second picture maintained by hand.

## 3. Reading a map

| Mark | Means |
|---|---|
| Circle | An entity — organisation, circle, role or person, depending on the map |
| Circle colour | Node kind by default; switchable to any attribute |
| Circle size | Node kind |
| Dotted halo | The badge attribute is present on this node |
| Line colour | **Which predicate.** Never decoration |
| Thick line | Mutual — both sides declared it |
| Dotted line | Recorded but unconfirmed |
| Red dashes | Flagged by the schema as a problem |
| Arrowhead | The predicate is directed |
| Number under a circle | Lines currently drawn to it — so it changes with the view |

- **Hover a circle** for everything recorded about it — its kind, how many lines are drawn to it in
  this view, and every attribute that has a value.
- **Hover a line** for both ends, the predicate spelled out in full, who declared it, whether it is
  confirmed, where the row came from, and any note. Lines are thin, so each carries a wide invisible
  catch area — you do not have to hit the stroke exactly.
- **Drag** a circle out of a tangle; scroll to zoom; drag the background to pan.
- **Field guide** in the header (or `g`) opens this document in a new tab.
- **Click** a circle or a line to open its full record in a panel on the right. Hovering is a
  glance; clicking is the record, and it stays open while you look elsewhere. Everything the
  selection is not about dims. Click the background or press `esc` to close.
- The panel **walks**: a node's record lists every connection, a line's record lists both ends —
  click any of them to move the panel there.

**What a line's record tells you.** Both ends, the predicate spelled out, who declared it, whether
both sides did, whether it is confirmed, where the row came from — plus two things worth naming:

- **Runs through** — where a relationship exists because of a particular person, the panel names
  them. The shared-personnel line between Mud Valley Foundation and Quinta Vale da Lama runs through
  Walt Ludwick, and the record says so.
- **What this publishes** — the exact two-field entry the subject would carry in its own Murmurations
  profile. Set beside the full record it shows the line that matters: *who the relationship runs
  through is recorded locally and is not part of the published claim.*
- A circle with no lines has none *of the kinds now being drawn*. It has not left the community.

## 4. If you are new at Vale da Lama

Vale da Lama runs on Holacracy: work is organised into **circles** rather than departments, and
people fill **roles** inside them. The map exists so you can see the shape of that without reading
the whole governance handbook first.

**Find yourself:**

1. Set **Dataset** to *Vale da Lama (Holacracy)*.
2. Leave **Schema** on *as build-graph.mjs emits today* — that is the live picture.
3. Find your name among the 14 people. Every line from you runs to a circle you are part of.
4. Hover any circle to read its **purpose** — the one sentence saying why it exists. Those sentences
   are the fastest orientation to the farm there is.

**What it can tell you today.** Nine circles: VdL Farm, Farm Ops, Casa Ops, Groups & Retreats,
Activities, B&B Accommodations, Restaurant, OMG (Organic Market Garden), HFC (Holistic Farm Care).
Eight lines show which circle sits inside which; the rest show which of the 14 people belong where.

> **Known gap — the map cannot yet tell you what anybody does.** A person connects straight to a
> circle, so three roles held in one circle look identical to one, and a role nobody fills shows as
> nothing at all. Switch the schema to *org:Post model* and the tool marks every such line: 7 errors
> and 11 warnings out of 26 rows.

**Why the vacancies matter.** The Roles database holds 27 roles and **8 have nobody in them**,
including every sub-circle Secretary. An unfilled role is exactly what a governance meeting needs to
see, and it is precisely what the current model hides.

## 5. If you are new to the Barlavento community

Barlavento is not one organisation. It is a set of independent land projects, farms and initiatives
in the western Algarve, each owning its own story. The map shows how they connect *without* any one
of them narrating the others.

**See the community:**

1. Set **Dataset** to *Barlavento community*.
2. Start on *as recorded today*. One organisation sits in the middle, touching all 13 others.
3. Switch to *vocabulary.md*. Nothing in the data changed — but the map draws **5 lines instead of
   23**, and the centre is gone.

Of the 23 recorded connections, 12 were one organisation recording that it convenes everybody, and 6
were "these two are in the same place." Eighteen of twenty-three were facts about single
organisations drawn as relationships. Moved onto the circles where they belong, the honest size of
the recorded relationship graph is **five**.

**Nothing appears on the map that its subject did not choose to say.** That is the direction of
travel, and it is why every row records where it came from.

**Putting yourself on the map properly:**

1. Publish a **Murmurations profile** on your own website carrying the `barlavento-eco` tag. That is
   what puts you in the community's index.
2. Your location and address are ordinary profile fields — do not record them as connections.
3. To declare a relationship, add an entry to your profile's `relationships` array with a
   **predicate** (what kind) and the **other organisation's web address**.
4. Two predicates exist today: `https://schema.org/affiliation` for a genuine association, and the
   community's own `…/predicates/shared-personnel/` when a person is active in both organisations.

Both sides declaring the same link makes it **mutual** and the map draws it thicker. One side is
enough to draw it at all — you should not be invisible because somebody else has not published yet.

> **On naming people.** The shared-personnel claim deliberately **does not name the person**. "We
> share personnel with X" is your organisation's claim to make; naming an individual is that
> individual's.

## 6. Administering the Vale da Lama data

**The lab is not the source of truth. Notion is.**

Notion holds circles, people and roles → `scripts/build-graph.mjs` in the `vdl-orgdev` repository
produces `graph.json` → `scripts/seed.py` in the lab produces the two CSVs the lab reads.

- **To change what the map says:** change Notion, regenerate `graph.json`, re-run `seed.py`, press
  **Reset to seed**. Editing rows in the lab is for trying something out — those edits live in your
  browser only and the next reseed discards them.
- **To change what the map is *allowed* to say:** edit `schemas/vdl-current.json` or
  `schemas/vdl-target.json`. Adding a node kind, a predicate or an allowed value is a few lines of
  JSON. Adding one to `vdl-target` proposes a change to the model without touching any data.
- **Standing check:** after any reseed, open **Validate**. Baseline is **0 errors under the current
  schema**, **7 errors + 11 warnings under the target schema**. If the first moves, something
  upstream broke. If the second falls, somebody has done the role work.

> **Handle with care.** This map names real colleagues and shows where each sits. It is internal
> governance material, and there is no privacy layer in the lab yet — everyone who can open the map
> sees every name.

## 7. Administering the Barlavento data

Two sources, and one job: make the second disappear. Every row carries a `source`:

| Value | Means | What to do |
|---|---|---|
| `self-published` | Read from the member's own Murmurations profile | Nothing. It maintains itself |
| `curated` | Recorded *about* the member by somebody else | Help them publish it themselves, then delete the row |

**Today every row is curated.** Nobody in the original spreadsheet declared anything about
themselves. The `source` column is a ledger of unfinished business, and the map's honesty improves
as it empties. Hovering any line shows that row's provenance, so the ledger can be audited from the
map rather than the table.

- **Adding a member:** you don't. They publish a profile with the `barlavento-eco` tag and the index
  finds them. If you must record something ahead of that, mark it `curated`, and mark it
  **candidate** if you are not certain — an unverified guess about a real organisation must never
  render as fact. One such row is in the data today, waiting for confirmation since June.
- **Adding a new kind of relationship:** a predicate is a stable web address that explains itself.
  Open a pull request adding a page under `docs/predicates/` in the community repository with a
  fixed permalink. It must say what the claim means, what it does *not* claim, and the nearest
  standard term. A predicate address is a permanent commitment — it can be clarified, never
  repurposed or deleted.

> **Deliberately absent.** The original spreadsheet had a `contact` column naming an individual at
> each of the 14 organisations. It is not carried into this data: nothing in the map needs it, and
> those people did not opt in.

## 8. The data models

Two files per organisation, and a schema governing both.

**Node file** — `id` (unique; the key relationships point at) · `name` (what appears on the map) ·
`nodeType` (must be one the schema allows) · then every attribute the schema declares (region,
membership, role type, status, purpose).

**Relationship file** — `subject` (the id making the claim) · `predicate` (must be one the schema
allows) · `object` · `via` (who or what the relationship runs through — local record only, never
published) · `confirmed` (`false` marks a candidate; draws dotted) · `source` · `note`.

### Barlavento — the four kinds

Nodes are Project, Initiative, Network or Convener. The four recorded kinds of connection split two
and two, and that split is the entire difference between the two schemas:

| Kind | Rows | Under `vocabulary.md` | Drawn as |
|---|---:|---|---|
| Membership | 12 | attribute | a halo on the circle |
| Co-location | 6 | attribute | colour — already a field on every node |
| Affiliation | 3 | relationship | a line · `schema.org/affiliation` |
| Shared personnel | 2 | relationship | a line · the community's own predicate |

### Vale da Lama — the reified role

Nodes are Circle and Person today; the target model adds Role. Instead of a person connecting to a
circle, a person fills a *role*, and the role sits in the circle.

| Relationship | From → to | Standard term | Status |
|---|---|---|---|
| Sub-circle | circle → circle | `org:subOrganizationOf` | in use |
| Role in its circle | role → circle | `org:postIn` | target model |
| Fills the role | person → role | `org:holds` | target model |
| Leads | person → circle | — | collapsed; flagged |
| Represents | person → circle | — | collapsed; flagged |

A role that exists whether or not anybody holds it is a standard idea — the W3C Organization
Ontology calls it a `Post`, and the class exists for exactly this reason. Reifying the relationship
is what lets an empty position be *visible* instead of rendering as nothing.

### How the schema stops you

- **The editor only offers what is legal.** Every governed field is a dropdown built from the
  schema. Under `vocabulary.md` the relationship editor offers two predicates; co-location is listed
  but cannot be chosen, because it is not a relationship. You cannot type a typo into a controlled
  field.
- **Validate checks the whole file.** Ten rules, each naming itself: unknown predicate, wrong kind of
  thing at either end of a line, missing id, a line to nowhere, a line to itself, a duplicate claim,
  a value outside a controlled list, a deprecated predicate, and rows absorbed as attributes rather
  than drawn.

The rule carrying the most weight is the one about the ends of a line. *Fills the role* may only
point at a role — so a person connected straight to a circle is refused rather than quietly drawn.

## 9. Views and controls

| Dataset | Schema | Rows | Drawn | For |
|---|---|---:|---:|---|
| Barlavento | as recorded today | 23 | 23 | The live map, and the problem |
| Barlavento | vocabulary.md | 23 | 5 | The proposal, on the same rows |
| Vale da Lama | as generated today | 26 | 26 | The live governance map |
| Vale da Lama | org:Post model | 26 | 26 | The same rows, checked against where it is going |

- **Draw** — a switch per relationship kind. Turning them off one at a time is the fastest way to
  see what any single kind contributes.
- **Colour by** — node kind, or an attribute. Barlavento offers Region; Vale da Lama offers Status.
- **Badge by** — a halo where an attribute is present. Barlavento offers Membership; the Vale da
  Lama target model offers Role type.
- **Labels** — names on or off; whether mutual pairs draw thicker.
- **Re-derive layout** — throw the arrangement away and let it settle again.

**Giving the map the screen:** `esc` closes the record panel, or restores the chrome when none is
open · `g` field guide · `m` map only · `p` panels · `c` controls · `f` fullscreen. All five are header buttons too, the bar above the tabs drags to any height, and
the framing is remembered. A big size change re-derives the layout so the graph fills the space; a
small one leaves the arrangement you were reading alone.

## 10. What is provisional

**Open by design**

- **Every visual treatment.** How membership, region or a confirmed pair should *look* is a design
  decision and has not been made. What you see is a placeholder that reads clearly enough to argue
  about.
- **Whether four kinds are enough** for Barlavento. They are the four found in the recorded data,
  not a considered taxonomy. A real relationship with no home among them is the most useful thing
  you could report.
- **What a browsing member actually needs.** Most people will want to look something up and leave.
  There is no read-only view yet; everyone gets the full editor.

**Known noise**

- Membership is on all 14 Barlavento nodes, so as a badge it distinguishes nobody.
- Every Vale da Lama node has status `Active`, so colouring by status shows one colour.
- Themes and purpose are free text — useful on hover, uncontrolled, not worth filtering on.
- Both maps carry columns nothing renders (website, size, and similar) inherited from the source
  data. Stripping them is easy; knowing which ones somebody relies on is not — so say if you use one.

**What would help most**

1. Open the map that concerns you and try to answer a question you actually have. Report the
   question, not the bug.
2. Name a field you would delete, and one you wish existed.
3. If a line about your organisation is wrong, say so — that is data, and the fastest kind of fix.

## 11. Running it

Two places it runs. **For a demo, use the Mini** — it is the always-on machine, and the address
works from any device signed in to the tailnet, on or off the farm network:

<http://mudvalleyinstitutes-mac-mini.tailb0b9f5.ts.net:8090/>

To run a copy on your own machine instead:

```sh
./run.sh                  # http://localhost:8090/
python3 scripts/seed.py   # rebuild both datasets from their real sources
./deploy-to-mini.sh       # push your copy to the Mini and restart it there
```

Opening the file directly will not work — the page fetches its schemas and data, and browsers block
that for local files. Your edits are kept in your own browser; **Reset to seed** discards them, and
**Export** hands them back as files you can commit.

**Adding a third map** needs a schema file and two CSVs: node kinds, attributes with their allowed
values, and predicates with the kinds of thing each may connect. That is the whole contract. Nothing
in the renderer knows about farms, circles, or the Algarve.
