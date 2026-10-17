#!/usr/bin/env bash
# Process the upstream dictionary dumps into the annotated form the builder
# reads: CEDict `CL:` / CC-Canto `M:` classifier info is pulled out of the
# definitions and into a trailing tab-separated column.
#
# Outputs are gitignored. Run this before `console build` or
# `console build test_set` from a fresh checkout; build_for_github_pages.ps1
# runs the `full/` half itself.
set -euo pipefail
cd "$(dirname "$0")/.."

python tools/process_cedict.py  full/cedict_ts.u8        full/cedict_ts.processed.u8
python tools/process_cccanto.py full/cccanto-webdist.txt full/cccanto-webdist.processed.txt
python tools/process_cedict.py  test/cedict_ts.u8        test/cedict_ts.processed.u8
python tools/process_cccanto.py test/cccanto-webdist.txt test/cccanto-webdist.processed.txt

echo "Processed dictionaries generated (gitignored)."
