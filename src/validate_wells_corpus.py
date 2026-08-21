#!/usr/bin/env python3
"""Replicate orientation-sensitive Mahadevan findings in the Wells corpus.

The PLOS supporting CSV is a bare sequence file in physical left-to-right
order.  The script reverses each row for the majority right-to-left reading,
then uses mayig's explicitly versioned sign crosswalk.  Crosswalk ambiguity is
reported rather than silently collapsed.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


TARGETS = [342, 267, 391, 293, 99, 59, 176, 211, 336, 89, 123, 150]


def load_sequences(path: Path) -> list[tuple[int, ...]]:
    sequences: list[tuple[int, ...]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.reader(handle):
            visual = tuple(int(value) for value in row if value.strip())
            if visual:
                sequences.append(tuple(reversed(visual)))
    return sequences


def load_crosswalk(feature_dir: Path) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    m_to_w: dict[int, set[int]] = defaultdict(set)
    w_to_m: dict[int, set[int]] = defaultdict(set)
    for path in sorted(feature_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        mahadevan = [int(value.removeprefix("M")) for value in data["mahadevan_graphemes"]]
        wells = [int(value.removeprefix("W")) for value in data["wells_graphemes"]]
        for m_sign in mahadevan:
            m_to_w[m_sign].update(wells)
        for w_sign in wells:
            w_to_m[w_sign].update(mahadevan)
    return m_to_w, w_to_m


def load_mahadevan_profiles(path: Path) -> dict[int, dict[str, float]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return {
            int(row["sign"]): {
                "lines": int(row["lines"]),
                "initial_rate": float(row["initial_rate"]),
                "terminal_rate": float(row["terminal_rate"]),
            }
            for row in csv.DictReader(handle)
        }


def aggregate_profile(sequences: list[tuple[int, ...]], wells: set[int]) -> dict[str, float | int]:
    occurrences = sum(sign in wells for seq in sequences for sign in seq)
    lines = sum(any(sign in wells for sign in seq) for seq in sequences)
    initial = sum(seq[0] in wells for seq in sequences)
    terminal = sum(seq[-1] in wells for seq in sequences)
    return {
        "tokens": occurrences,
        "lines": lines,
        "initial_count": initial,
        "terminal_count": terminal,
        "initial_rate": initial / lines if lines else 0.0,
        "terminal_rate": terminal / lines if lines else 0.0,
    }


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    x_bar = sum(xs) / len(xs)
    y_bar = sum(ys) / len(ys)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
    x_den = math.sqrt(sum((x - x_bar) ** 2 for x in xs))
    y_den = math.sqrt(sum((y - y_bar) ** 2 for y in ys))
    return numerator / (x_den * y_den) if x_den and y_den else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wells-csv", type=Path, required=True)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--mahadevan-profiles", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()

    sequences = load_sequences(args.wells_csv)
    m_to_w, w_to_m = load_crosswalk(args.features)
    m_profiles = load_mahadevan_profiles(args.mahadevan_profiles)

    rows: list[dict] = []
    for m_sign in sorted(m_profiles):
        wells = m_to_w.get(m_sign, set())
        if not wells:
            continue
        profile = aggregate_profile(sequences, wells)
        ambiguous_wells = {
            sign: sorted(w_to_m[sign]) for sign in wells if len(w_to_m[sign]) > 1
        }
        rows.append(
            {
                "mahadevan": m_sign,
                "wells": sorted(wells),
                "ambiguous_wells": ambiguous_wells,
                "mahadevan_lines": m_profiles[m_sign]["lines"],
                "wells_lines": profile["lines"],
                "mahadevan_initial_rate": m_profiles[m_sign]["initial_rate"],
                "wells_initial_rate": profile["initial_rate"],
                "mahadevan_terminal_rate": m_profiles[m_sign]["terminal_rate"],
                "wells_terminal_rate": profile["terminal_rate"],
            }
        )

    # Correlation is restricted to adequately represented signs and exact
    # one-Wells-to-one-Mahadevan mappings.  This avoids manufacturing agreement
    # by merging broad allograph families.
    exact = [
        row
        for row in rows
        if row["mahadevan_lines"] >= 10
        and row["wells_lines"] >= 10
        and len(row["wells"]) == 1
        and not row["ambiguous_wells"]
    ]
    result = {
        "wells_lines": len(sequences),
        "wells_tokens": sum(len(seq) for seq in sequences),
        "wells_distinct_signs": len({sign for seq in sequences for sign in seq}),
        "orientation": "CSV physical LTR reversed to majority RTL reading order",
        "crosswalk_source": "mayig features/*.json",
        "exact_mapping_signs_in_correlation": len(exact),
        "initial_rate_pearson": pearson(
            [row["mahadevan_initial_rate"] for row in exact],
            [row["wells_initial_rate"] for row in exact],
        ),
        "terminal_rate_pearson": pearson(
            [row["mahadevan_terminal_rate"] for row in exact],
            [row["wells_terminal_rate"] for row in exact],
        ),
        "targets": [row for row in rows if row["mahadevan"] in TARGETS],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "mahadevan", "wells", "ambiguous_wells", "mahadevan_lines", "wells_lines",
            "mahadevan_initial_rate", "wells_initial_rate",
            "mahadevan_terminal_rate", "wells_terminal_rate",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["wells"] = " ".join(f"W{sign:03d}" for sign in row["wells"])
            output["ambiguous_wells"] = json.dumps(row["ambiguous_wells"], sort_keys=True)
            writer.writerow(output)


if __name__ == "__main__":
    main()
