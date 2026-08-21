#!/usr/bin/env bash
# Fetch the third-party corpora the analysis reads, each at the commit the
# results in research/ were computed from (SOURCE_MANIFEST.md).
#
# None of these is redistributed here. toddcolsen/indus_script declares no
# licence; the mayig corpus's CISI-derived content is not covered by its MIT
# code licence; glossa-lab is read for one table. Each is cloned from its
# upstream into vendor/ (gitignored) and checked out at the pinned commit.
#
# Usage: scripts/fetch_inputs.sh   (needs git; run from anywhere)
set -euo pipefail
cd "$(dirname "$0")/.."

fetch() {
  local url=$1 dir=$2 commit=$3
  if [ -d "$dir/.git" ] && [ "$(git -C "$dir" rev-parse HEAD)" = "$commit" ]; then
    echo "$dir at $commit"
    return
  fi
  rm -rf "$dir"
  git init -q "$dir"
  git -C "$dir" remote add origin "$url"
  git -C "$dir" fetch -q --depth 1 origin "$commit"
  git -C "$dir" -c advice.detachedHead=false checkout -q FETCH_HEAD
  [ "$(git -C "$dir" rev-parse HEAD)" = "$commit" ] || { echo "$dir: expected $commit" >&2; exit 1; }
  echo "$dir at $commit"
}

fetch https://github.com/toddcolsen/indus_script.git \
  vendor/toddcolsen-indus-script 52a6fdb5fa235bca1b78ef8856a4ba54714d37fb
fetch https://github.com/BitConcepts/glossa-lab.git \
  vendor/glossa-lab 40812fc54470d5508b47af5fabcea7ccf044036c
fetch https://github.com/mayig/indus-valley-script-corpus.git \
  vendor/mayig-indus-valley-script-corpus ad2f1e218a34b8c33c57de0d6cb8d99272765bbb
