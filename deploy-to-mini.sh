#!/bin/sh
# Push this working copy to the always-on Mini and restart its server.
# The MacBook is where the lab is edited; the Mini is where it is demoed from.
set -e
HOST=${1:-macmini}
rsync -az --delete --exclude '.DS_Store' \
  "$(cd "$(dirname "$0")" && pwd)/" "$HOST:~/dev/orgmap-lab/"
ssh "$HOST" 'launchctl kickstart -k gui/$(id -u)/com.waltz.orgmap-lab 2>/dev/null || true'
echo "pushed -> http://mudvalleyinstitutes-mac-mini.tailb0b9f5.ts.net:8090/"

# The Mini copy is a deployment: files only, no history. If the working tree has
# commits the remote has not seen, say so — the Mini is not a backup.
if [ -n "$(git -C "$(dirname "$0")" log --branches --not --remotes --oneline 2>/dev/null)" ]; then
  echo "note: commits not yet pushed to origin — the Mini copy carries no history."
  echo "      git -C $(dirname "$0") push"
fi
