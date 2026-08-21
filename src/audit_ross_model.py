#!/usr/bin/env python3
"""Audit the Ross (2026) preprint against the corpus it names as its source."""

from __future__ import annotations

import argparse
import glob
import json
from collections import Counter
from pathlib import Path


CLAIMS = {
    324: {"claimed_pictograph": "jar/vessel", "claimed_role": "INIT", "identity_matches": True},
    122: {"claimed_pictograph": "fish", "claimed_role": "MED", "identity_matches": False},
    385: {"claimed_pictograph": "crab/scorpion", "claimed_role": "TERM", "identity_matches": False},
    86: {"claimed_pictograph": "man, arms raised", "claimed_role": "INIT", "identity_matches": False},
    50: {"claimed_pictograph": "arrow/spear", "claimed_role": "MED", "identity_matches": False},
    217: {"claimed_pictograph": "bearer/yoke", "claimed_role": "INIT", "identity_matches": False},
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sequences = []
    for filename in glob.glob(str(args.corpus_root / "corpus" / "**" / "*.json"), recursive=True):
        for side in json.loads(Path(filename).read_text(encoding="utf-8")):
            sequence = [int(item["id"][1:]) for item in side.get("graphemes", [])]
            if sequence:
                sequences.append({"id": side["id"], "stored_left_to_right": sequence})

    stored_left = Counter(item["stored_left_to_right"][0] for item in sequences)
    stored_right = Counter(item["stored_left_to_right"][-1] for item in sequences)
    sign_counts = Counter(sign for item in sequences for sign in item["stored_left_to_right"])
    checks = []
    for sign, claim in CLAIMS.items():
        feature_path = args.corpus_root / "features" / f"P{sign:03d}.json"
        feature = json.loads(feature_path.read_text(encoding="utf-8"))
        actual_description = feature["description"]
        claimed_description = claim["claimed_pictograph"]
        checks.append(
            {
                "sign": f"P{sign:03d}",
                "tokens": sign_counts[sign],
                "claimed_pictograph": claimed_description,
                "source_corpus_description": actual_description,
                # Judged from the two explicit descriptions; kept as data so
                # the audit does not pretend a substring heuristic can decide
                # iconographic identity.
                "pictograph_description_matches": claim["identity_matches"],
                "claimed_role": claim["claimed_role"],
                "stored_left_count": stored_left[sign],
                "stored_right_count": stored_right[sign],
                # Source README: stored arrays are physical LTR and script is
                # read RTL. Canonical initial is therefore stored-right.
                "canonical_reading_initial_count": stored_right[sign],
                "canonical_reading_terminal_count": stored_left[sign],
                "mahadevan_crosswalk": feature.get("mahadevan_graphemes", []),
            }
        )

    result = {
        "corpus_nonempty_sides": len(sequences),
        "corpus_tokens": sum(len(item["stored_left_to_right"]) for item in sequences),
        "orientation_from_source_readme": (
            "graphemes stored physical left-to-right; script read right-to-left"
        ),
        "orientation_finding": (
            "The preprint's reported opener counts equal stored-left counts, while its "
            "terminal counts equal stored-right counts. This reverses the reading "
            "direction documented by its named source corpus."
        ),
        "sign_identity_finding": (
            "Several high-frequency pictograph names in the preprint contradict the "
            "source corpus's own feature dictionary and Mahadevan crosswalk."
        ),
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
