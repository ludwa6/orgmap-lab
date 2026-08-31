#!/bin/sh
# Serve the lab locally. A plain file:// open will NOT work — the page fetches
# its schemas and CSVs, and browsers block that on the file: scheme.
PORT=${1:-8090}
echo "OrgMap Lab -> http://localhost:$PORT/"
exec python3 -m http.server "$PORT" --directory "$(dirname "$0")"
