#!/usr/bin/env python3
"""Check what each deployment actually serves against SHARED.sha256.

SHARED.sha256 answers "do the repositories agree?". This answers the question
that stayed unanswered twice: "is what the sites serve the thing we published?"
A consumer that never re-copied, a Pages build that failed while the repo was
right, and a file edited by hand all look the same from here: the bytes a
visitor receives are not the bytes in the manifest.

Every file ends in one of three states, and they are kept apart on purpose:

  ok              served bytes hash to the manifest's value
  MISMATCH        served bytes hash to something else
  COULD NOT LOOK  no answer: a non-200, a timeout, or an EMPTY body

A failed fetch is never a pass and never a mismatch. An empty body is the trap
worth naming: it hashes to e3b0c442... and would otherwise compare as a real
answer.

    python3 scripts/deployment-check.py
    python3 scripts/deployment-check.py --report-dir /tmp/drift

Exit status: 0 all ok, 1 any mismatch, 2 could not look (and no mismatch),
3 configuration error. The Pages build API is deliberately never consulted:
on 2026-09-01 it reported "errored" for minutes after the fix was serving.
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "SHARED.sha256")
DEPLOYMENTS = os.path.join(ROOT, "deployments.json")

OK, MISMATCH, UNSEEN = "ok", "MISMATCH", "COULD NOT LOOK"
ATTEMPTS = 3
TIMEOUT = 30


def load_manifest(path):
    hashes = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            digest, sep, name = line.partition("  ")
            if not sep:
                digest, sep, name = line.partition(" *")
            if not sep or len(digest) != 64:
                raise ValueError("unreadable manifest line: %r" % line)
            hashes[name] = digest
    return hashes


def load_deployments(path):
    with open(path) as f:
        doc = json.load(f)
    deployments = doc.get("deployments")
    if not isinstance(deployments, list) or not deployments:
        raise ValueError("%s has no deployments list" % path)
    for d in deployments:
        for key in ("name", "url", "files"):
            if key not in d:
                raise ValueError("deployment %r is missing %r" % (d.get("name", "?"), key))
    return deployments


def fetch(url):
    """Return (body, None) or (None, reason). Never returns an empty body."""
    reason = "not attempted"
    for attempt in range(1, ATTEMPTS + 1):
        # Pages serves max-age=600 from a CDN; a fresh query string and no-cache
        # ask for what is being served now, not what was cached ten minutes ago.
        busted = "%s?deployment-check=%d" % (url, time.time_ns())
        req = urllib.request.Request(busted, headers={
            "Cache-Control": "no-cache",
            "User-Agent": "orgmap-lab deployment-check",
        })
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                status, body = r.status, r.read()
            if status != 200:
                reason = "HTTP %d" % status
            elif not body:
                reason = "empty body (would hash to %s...)" % hashlib.sha256(b"").hexdigest()[:8]
            else:
                return body, None
        except urllib.error.HTTPError as e:
            reason = "HTTP %d" % e.code
            if 400 <= e.code < 500:
                break                       # a 404 will not fix itself in four seconds
        except Exception as e:              # timeouts, DNS, TLS: all "could not look"
            reason = "%s: %s" % (type(e).__name__, e)
        if attempt < ATTEMPTS:
            time.sleep(2 * attempt)
    return None, reason


def check(manifest, deployments, fetcher=fetch):
    rows, config_errors = [], []
    for d in deployments:
        base = d["url"].rstrip("/")
        for name in d["files"]:
            want = manifest.get(name)
            if want is None:
                config_errors.append("%s lists %s, which SHARED.sha256 does not publish"
                                     % (d["name"], name))
                continue
            body, reason = fetcher(base + "/" + name)
            row = {"deployment": d["name"], "base": base, "file": name,
                   "want": want, "got": None, "reason": reason}
            if body is None:
                row["state"] = UNSEEN
            else:
                row["got"] = hashlib.sha256(body).hexdigest()
                row["state"] = OK if row["got"] == want else MISMATCH
            rows.append(row)
    return rows, config_errors


def exit_code(rows, config_errors):
    if config_errors:
        return 3
    if any(r["state"] == MISMATCH for r in rows):
        return 1
    if any(r["state"] == UNSEEN for r in rows):
        return 2
    return 0


def short(h):
    return h[:10] if h else "-"


def md(text):
    # Failure reasons carry things like "<urlopen error ...>", which GitHub would
    # swallow as an HTML tag, and a "|" would break the table row.
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def render_text(rows, config_errors):
    out, last = [], None
    for r in rows:
        if r["deployment"] != last:
            out.append("===== %s  (%s) =====" % (r["deployment"], r["base"]))
            last = r["deployment"]
        state = "** MISMATCH **" if r["state"] == MISMATCH else r["state"]
        line = "  %-32s %-14s got=%s want=%s" % (r["file"], state, short(r["got"]), short(r["want"]))
        if r["state"] == UNSEEN:
            line += "  (%s)" % r["reason"]
        out.append(line)
    out += ["CONFIG ERROR: " + e for e in config_errors]
    return "\n".join(out)


def counts(rows):
    return (sum(r["state"] == MISMATCH for r in rows),
            sum(r["state"] == UNSEEN for r in rows),
            len(rows))


def render_report(rows, config_errors):
    mism, unseen, total = counts(rows)
    deps = len({r["deployment"] for r in rows})
    lines = ["### Deployment check: %d mismatch, %d could not look, %d of %d files ok"
             % (mism, unseen, total - mism - unseen, total), ""]
    if config_errors:
        lines += ["**Configuration error**, so this run proves nothing about the sites:", ""]
        lines += ["- " + e for e in config_errors] + [""]
    lines += ["| deployment | file | result | served | expected |", "|---|---|---|---|---|"]
    for r in rows:
        result = {OK: "ok", MISMATCH: "**mismatch**", UNSEEN: "**could not look**: " + md(r["reason"])}[r["state"]]
        lines.append("| [%s](%s/) | `%s` | %s | `%s` | `%s` |"
                     % (r["deployment"], r["base"], r["file"], result, short(r["got"]), short(r["want"])))
    lines += ["",
              "*Mismatch* means the site serves a different file from the one `SHARED.sha256` "
              "publishes: the deployment has not re-copied it, its Pages build failed, or it was "
              "edited by hand. *Could not look* means the fetch failed; it is not a pass. "
              "%s listed in `deployments.json`." % plural(deps, "deployment")]
    return "\n".join(lines) + "\n"


def render_summary(rows, config_errors):
    mism, unseen, total = counts(rows)
    if exit_code(rows, config_errors) == 0:
        return ("**All deployments match.** %s across %s serve exactly what "
                "`SHARED.sha256` publishes.\n"
                % (plural(total, "file"), plural(len({r["deployment"] for r in rows}), "deployment")))
    lines = ["**%d mismatch, %d could not look%s.**" % (
        mism, unseen, ", configuration error" if config_errors else ""), ""]
    lines += ["- configuration: " + e for e in config_errors]
    for r in rows:
        if r["state"] == MISMATCH:
            lines.append("- `%s` serves `%s` as `%s`, expected `%s`"
                         % (r["deployment"], r["file"], short(r["got"]), short(r["want"])))
        elif r["state"] == UNSEEN:
            lines.append("- `%s` `%s`: could not look (%s)" % (r["deployment"], r["file"], md(r["reason"])))
    return "\n".join(lines) + "\n"


def fingerprint(rows, config_errors):
    # What is wrong, not when it was seen: the same stale file on consecutive
    # days fingerprints the same, so the issue is not re-announced daily. The
    # served hash is included, so a site moving to a different wrong file counts
    # as a change. Failure reasons are excluded, so a timeout that becomes a TLS
    # error is not news.
    problems = sorted("%s|%s|%s|%s" % (r["deployment"], r["file"], r["state"], r["got"] or "")
                      for r in rows if r["state"] != OK)
    problems += sorted("config|" + e for e in config_errors)
    if not problems:
        return "green"
    return hashlib.sha256("\n".join(problems).encode()).hexdigest()


def main(argv):
    manifest_path, deployments_path, report_dir = MANIFEST, DEPLOYMENTS, None
    args = list(argv)
    while args:
        flag = args.pop(0)
        if flag in ("--manifest", "--deployments", "--report-dir") and args:
            value = args.pop(0)
            if flag == "--manifest":
                manifest_path = value
            elif flag == "--deployments":
                deployments_path = value
            else:
                report_dir = value
        else:
            print(__doc__.strip(), file=sys.stderr)
            return 3
    try:
        manifest = load_manifest(manifest_path)
        deployments = load_deployments(deployments_path)
    except (OSError, ValueError) as e:
        print("CONFIG ERROR: %s" % e, file=sys.stderr)
        return 3

    rows, config_errors = check(manifest, deployments)
    print(render_text(rows, config_errors))
    code = exit_code(rows, config_errors)

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        for name, text in (("report.md", render_report(rows, config_errors)),
                           ("summary.md", render_summary(rows, config_errors)),
                           ("fingerprint.txt", fingerprint(rows, config_errors) + "\n")):
            with open(os.path.join(report_dir, name), "w") as f:
                f.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
