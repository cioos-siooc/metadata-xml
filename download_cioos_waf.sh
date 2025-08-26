#!/usr/bin/env bash

# Download all metadata files from the CIOOS WAF into a local folder.
# Usage:
#   ./download_unpublished.sh [WAF_URL] [DEST_DIR]
# Defaults:
#   WAF_URL  = https://waf.forms.cioos.ca/metadata/unpublished/
#   DEST_DIR = metadata

set -euo pipefail

WAF_URL="${1:-https://waf.forms.cioos.ca/metadata/}"
DEST_DIR="${2:-metadata}"

if ! command -v wget >/dev/null 2>&1; then
  echo "Error: wget is required. Install it (e.g., sudo apt-get install wget) and retry." >&2
  exit 1
fi

mkdir -p "${DEST_DIR}"

# Recursively fetch YAML/YML files only, do not ascend to parent, and avoid index pages.
# -nH drops the host directory; --cut-dirs=1 strips the leading 'metadata' segment so
# files land under DEST_DIR/unpublished/...
wget \
  --recursive \
  --no-parent \
  --no-host-directories \
  --cut-dirs=1 \
  --accept '*.yaml,*.yml' \
  --reject 'index.html*' \
  --timestamping \
  --directory-prefix="${DEST_DIR}" \
  "${WAF_URL}"

echo "Downloaded files under: ${DEST_DIR}"
