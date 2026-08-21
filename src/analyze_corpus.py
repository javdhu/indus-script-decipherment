#!/usr/bin/env python3
"""Reproducible structural audit of a Mahadevan-numbered Indus corpus.

The code intentionally uses only Python's standard library. It makes no
phonetic assignments. Its job is to establish which claims a later semantic or
phonetic decipherment has to explain and to expose easy orientation/coverage
errors in candidate models.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


START = "<START>"
END = "<END>"
UNK = "<UNK>"


@dataclass(frozen=True)
class Inscription:
    artifact: str
    object_type: str
    location: str
    field_symbol: str
    side: str
    line: int
    declared_length: int | None
    visual: tuple[int, ...]

    @property
    def face(self) -> tuple[str, str]:
        return self.artifact, self.side

    @property
    def reading(self) -> tuple[int, ...]:
        # The source strings are in visual left-to-right order. Most texts are
        # read right-to-left; keeping this assumption explicit makes it easy to
        # rerun orientation-sensitive tests.
        return tuple(reversed(self.visual))


def normalize_category(value: str) -> str:
    value = value.strip()
    if not value or value in {"0", "0.0", "nan", "None"}:
        return "UNKNOWN"
    try:
        number = float(value)
        if number.is_integer():
            return str(int(number))
    except ValueError:
        pass
    return value


def load_corpus(path: Path) -> list[Inscription]:
    rows: list[Inscription] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for raw in csv.DictReader(handle):
            signs = tuple(
                int(token)
                for token in raw["SIGNS"].strip().split("-")
                if token.strip()
            )
            try:
                declared = int(raw["LENGTH"])
            except (ValueError, TypeError):
                declared = None
            rows.append(
                Inscription(
                    artifact=raw["ID"].strip(),
                    object_type=normalize_category(raw["OBJTYPE"]),
                    location=normalize_category(raw["LOCATION"]),
                    field_symbol=normalize_category(raw["FIELDSYM"]),
                    side=normalize_category(raw["SIDE"]),
                    line=int(raw["LINE"]),
                    declared_length=declared,
                    visual=signs,
                )
            )
    return rows


def clean_corpus(rows: Sequence[Inscription]) -> tuple[list[Inscription], dict]:
    lines_by_face: dict[tuple[str, str], set[int]] = defaultdict(set)
    for row in rows:
        lines_by_face[row.face].add(row.line)
    multiline_faces = {face for face, lines in lines_by_face.items() if len(lines) > 1}

    unknown_rows = [row for row in rows if 0 in row.visual]
    length_mismatches = [
        row
        for row in rows
        if row.declared_length is not None and row.declared_length != len(row.visual)
    ]
    invalid_sign_rows = [
        row for row in rows if any(sign < 0 or sign > 417 for sign in row.visual)
    ]
    eligible = [
        row
        for row in rows
        if row.visual
        and 0 not in row.visual
        and row.face not in multiline_faces
        and not any(sign < 1 or sign > 417 for sign in row.visual)
    ]

    # EBUDS keeps one occurrence of an exact sequence. Deduplication happens
    # before train/test splitting to prevent duplicate leakage.
    dedup: dict[tuple[int, ...], Inscription] = {}
    duplicate_occurrences = 0
    for row in eligible:
        if row.reading in dedup:
            duplicate_occurrences += 1
        else:
            dedup[row.reading] = row
    unique = list(dedup.values())

    audit = {
        "raw_lines": len(rows),
        "raw_nonempty_lines": sum(bool(row.visual) for row in rows),
        "empty_catalogue_rows": sum(not row.visual for row in rows),
        "artifacts": len({row.artifact for row in rows}),
        "faces": len({row.face for row in rows}),
        "raw_tokens": sum(len(row.visual) for row in rows),
        "rows_with_unknown_000": len(unknown_rows),
        "multiline_faces": len(multiline_faces),
        "rows_on_multiline_faces": sum(row.face in multiline_faces for row in rows),
        "declared_length_mismatches": len(length_mismatches),
        "invalid_sign_rows": len(invalid_sign_rows),
        "eligible_clean_lines_before_dedup": len(eligible),
        "exact_duplicate_occurrences_removed": duplicate_occurrences,
        "ebuds_like_unique_lines": len(unique),
        "ebuds_like_tokens": sum(len(row.reading) for row in unique),
        "ebuds_like_distinct_signs": len({s for row in unique for s in row.reading}),
        "locations_raw": Counter(row.location for row in rows),
        "object_types_raw": Counter(row.object_type for row in rows),
        "field_symbols_known_raw": sum(row.field_symbol != "UNKNOWN" for row in rows),
        "orientation_assumption": "source visual LTR; canonical reading reverses to RTL",
    }
    return unique, audit


def relative_bin(index: int, length: int, bins: int = 5) -> int:
    if length <= 1:
        return bins // 2
    return min(bins - 1, int(index * bins / length))


def sign_profiles(rows: Sequence[Inscription]) -> dict[int, dict]:
    positions: dict[int, Counter] = defaultdict(Counter)
    line_counts: Counter = Counter()
    initial: Counter = Counter()
    terminal: Counter = Counter()
    left_neighbors: dict[int, set[int]] = defaultdict(set)
    right_neighbors: dict[int, set[int]] = defaultdict(set)
    sites: dict[int, set[str]] = defaultdict(set)
    objects: dict[int, set[str]] = defaultdict(set)
    fields: dict[int, set[str]] = defaultdict(set)

    for row in rows:
        seq = row.reading
        seen = set(seq)
        line_counts.update(seen)
        if seq:
            initial[seq[0]] += 1
            terminal[seq[-1]] += 1
        for i, sign in enumerate(seq):
            positions[sign][relative_bin(i, len(seq))] += 1
            sites[sign].add(row.location)
            objects[sign].add(row.object_type)
            if row.field_symbol != "UNKNOWN":
                fields[sign].add(row.field_symbol)
            if i:
                left_neighbors[sign].add(seq[i - 1])
            if i + 1 < len(seq):
                right_neighbors[sign].add(seq[i + 1])

    token_counts = Counter(s for row in rows for s in row.reading)
    result: dict[int, dict] = {}
    for sign, count in token_counts.items():
        bins = [positions[sign][i] for i in range(5)]
        probs = [value / count for value in bins if value]
        entropy = -sum(p * math.log2(p) for p in probs)
        result[sign] = {
            "sign": sign,
            "tokens": count,
            "lines": line_counts[sign],
            "initial_count": initial[sign],
            "terminal_count": terminal[sign],
            "initial_rate": initial[sign] / line_counts[sign],
            "terminal_rate": terminal[sign] / line_counts[sign],
            "position_bins": bins,
            "position_concentration": 1.0 - entropy / math.log2(5),
            "left_context_types": len(left_neighbors[sign]),
            "right_context_types": len(right_neighbors[sign]),
            "site_types": len(sites[sign]),
            "object_types": len(objects[sign]),
            "field_symbol_types": len(fields[sign]),
        }
    return result


def positional_concentration(sequences: Sequence[Sequence[int]]) -> float:
    bins: dict[int, Counter] = defaultdict(Counter)
    counts: Counter = Counter()
    for seq in sequences:
        for i, sign in enumerate(seq):
            bins[sign][relative_bin(i, len(seq))] += 1
            counts[sign] += 1
    weighted = 0.0
    total = 0
    for sign, count in counts.items():
        if count < 5:
            continue
        probs = [value / count for value in bins[sign].values()]
        entropy = -sum(p * math.log2(p) for p in probs)
        concentration = 1.0 - entropy / math.log2(5)
        weighted += concentration * count
        total += count
    return weighted / total if total else 0.0


def positional_permutation_test(
    rows: Sequence[Inscription], permutations: int = 300, seed: int = 731943
) -> dict:
    sequences = [row.reading for row in rows]
    lengths = [len(seq) for seq in sequences]
    tokens = [sign for seq in sequences for sign in seq]
    observed = positional_concentration(sequences)
    rng = random.Random(seed)
    null: list[float] = []
    for _ in range(permutations):
        shuffled = tokens[:]
        rng.shuffle(shuffled)
        cursor = 0
        generated = []
        for length in lengths:
            generated.append(shuffled[cursor : cursor + length])
            cursor += length
        null.append(positional_concentration(generated))
    mean = statistics.fmean(null)
    stdev = statistics.pstdev(null)
    return {
        "metric": "token-weighted five-bin positional concentration",
        "observed": observed,
        "null_mean": mean,
        "null_stdev": stdev,
        "z_score": (observed - mean) / stdev if stdev else None,
        "empirical_p_ge": (1 + sum(value >= observed for value in null))
        / (permutations + 1),
        "permutations": permutations,
        "null_preserves": "sequence lengths and global sign frequencies",
    }


def stable_fold(artifact: str, folds: int = 5) -> int:
    digest = hashlib.sha256(artifact.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % folds


def evaluate_ngram(rows: Sequence[Inscription], folds: int = 5, alpha: float = 0.1) -> dict:
    fold_results = []
    for fold in range(folds):
        train = [row.reading for row in rows if stable_fold(row.artifact, folds) != fold]
        test = [row.reading for row in rows if stable_fold(row.artifact, folds) == fold]
        unigram = Counter()
        bigram: dict[str | int, Counter] = defaultdict(Counter)
        vocabulary: set[int] = set()
        for seq in train:
            vocabulary.update(seq)
            mapped: list[str | int] = list(seq) + [END]
            unigram.update(mapped)
            previous: str | int = START
            for token in mapped:
                bigram[previous][token] += 1
                previous = token

        outcomes: list[str | int] = list(vocabulary) + [END, UNK]
        unigram_total = sum(unigram.values())
        unigram_log2 = 0.0
        bigram_log2 = 0.0
        token_total = 0
        for seq in test:
            mapped = [token if token in vocabulary else UNK for token in seq] + [END]
            previous: str | int = START
            for token in mapped:
                unigram_prob = (unigram[token] + alpha) / (
                    unigram_total + alpha * len(outcomes)
                )
                context_total = sum(bigram[previous].values())
                bigram_prob = (bigram[previous][token] + alpha) / (
                    context_total + alpha * len(outcomes)
                )
                unigram_log2 -= math.log2(unigram_prob)
                bigram_log2 -= math.log2(bigram_prob)
                token_total += 1
                previous = token
        fold_results.append(
            {
                "fold": fold,
                "test_lines": len(test),
                "tokens_including_end": token_total,
                "unigram_bits_per_token": unigram_log2 / token_total,
                "bigram_bits_per_token": bigram_log2 / token_total,
            }
        )
    uni = statistics.fmean(item["unigram_bits_per_token"] for item in fold_results)
    bi = statistics.fmean(item["bigram_bits_per_token"] for item in fold_results)
    return {
        "split": "five-fold deterministic artifact split after exact-sequence deduplication",
        "alpha": alpha,
        "folds": fold_results,
        "mean_unigram_bits_per_token": uni,
        "mean_bigram_bits_per_token": bi,
        "bigram_information_gain_bits": uni - bi,
        "unigram_perplexity": 2**uni,
        "bigram_perplexity": 2**bi,
    }


def binary_association(rows: Sequence[Inscription], attribute: str) -> dict[int, dict]:
    category_counts = Counter(getattr(row, attribute) for row in rows)
    valid_categories = {
        key for key, count in category_counts.items() if key != "UNKNOWN" and count >= 10
    }
    valid_rows = [row for row in rows if getattr(row, attribute) in valid_categories]
    total = len(valid_rows)
    if not total:
        return {}
    sign_line_counts = Counter(s for row in valid_rows for s in set(row.reading))
    category_sign_counts: dict[str, Counter] = defaultdict(Counter)
    for row in valid_rows:
        category_sign_counts[getattr(row, attribute)].update(set(row.reading))

    result: dict[int, dict] = {}
    for sign, present in sign_line_counts.items():
        if present < 5:
            continue
        best = None
        for category in valid_categories:
            n_category = category_counts[category]
            a = category_sign_counts[category][sign]
            b = n_category - a
            c = present - a
            d = total - n_category - c
            lift = (a / n_category) / (present / total) if a else 0.0
            log_odds = math.log((a + 0.5) / (b + 0.5)) - math.log(
                (c + 0.5) / (d + 0.5)
            )
            score = abs(log_odds) * math.sqrt(max(a, 1))
            candidate = {
                "category": category,
                "category_lines": n_category,
                "sign_lines_in_category": a,
                "sign_lines_total": present,
                "lift": lift,
                "log_odds": log_odds,
                "ranking_score": score,
            }
            if best is None or candidate["ranking_score"] > best["ranking_score"]:
                best = candidate
        if best:
            result[sign] = best
    return result


def collect_formulas(rows: Sequence[Inscription]) -> list[dict]:
    counts: dict[tuple[str, tuple[int, ...]], list[Inscription]] = defaultdict(list)
    for row in rows:
        seq = row.reading
        for width in range(1, min(4, len(seq)) + 1):
            counts[("initial", seq[:width])].append(row)
            counts[("terminal", seq[-width:])].append(row)
        counts[("whole", seq)].append(row)
    output = []
    for (kind, sequence), matches in counts.items():
        if len(matches) < (2 if kind == "whole" else 3):
            continue
        output.append(
            {
                "kind": kind,
                "sequence": "-".join(f"M{s:03d}" for s in sequence),
                "width": len(sequence),
                "count": len(matches),
                "sites": len({row.location for row in matches}),
                "object_types": len({row.object_type for row in matches}),
                "known_field_symbols": len(
                    {row.field_symbol for row in matches if row.field_symbol != "UNKNOWN"}
                ),
            }
        )
    return sorted(output, key=lambda item: (-item["count"], item["kind"], item["sequence"]))


def substitution_frames(rows: Sequence[Inscription]) -> list[dict]:
    frames: dict[tuple[int, tuple[int | None, ...]], Counter] = defaultdict(Counter)
    contexts: dict[tuple[int, tuple[int | None, ...]], set[tuple[str, str]]] = defaultdict(set)
    for row in rows:
        seq = row.reading
        if len(seq) < 2 or len(seq) > 10:
            continue
        for index, sign in enumerate(seq):
            frame = tuple(None if i == index else value for i, value in enumerate(seq))
            key = index, frame
            frames[key][sign] += 1
            contexts[key].add((row.location, row.object_type))
    output = []
    for (index, frame), alternatives in frames.items():
        occurrences = sum(alternatives.values())
        if len(alternatives) < 3 or occurrences < 4:
            continue
        output.append(
            {
                "length": len(frame),
                "reading_position": index,
                "frame": "-".join("*" if s is None else f"M{s:03d}" for s in frame),
                "occurrences": occurrences,
                "alternative_count": len(alternatives),
                "alternatives": " ".join(
                    f"M{sign:03d}:{count}" for sign, count in alternatives.most_common()
                ),
                "site_object_contexts": len(contexts[(index, frame)]),
            }
        )
    return sorted(
        output,
        key=lambda item: (-item["alternative_count"], -item["occurrences"], item["frame"]),
    )


def audit_candidate_anchors(
    path: Path | None, profiles: dict[int, dict], rows: Sequence[Inscription]
) -> dict | None:
    if path is None or not path.exists():
        return None
    anchors = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for raw in csv.DictReader(handle):
            value = raw.get("Sign", "").strip().upper().removeprefix("M")
            if not value.isdigit():
                continue
            item = dict(raw)
            item["sign_number"] = int(value)
            anchors.append(item)

    token_counts = Counter(s for row in rows for s in row.reading)
    total_tokens = sum(token_counts.values())
    accepted = [a for a in anchors if a.get("Confidence") in {"HIGH", "MEDIUM"}]
    covered = sum(token_counts[a["sign_number"]] for a in accepted)
    positional_conflicts = []
    terminal_terms = ("terminal", "suffix", "case marker", "genitive", "locative")
    initial_terms = ("initial", "prefix", "title")
    for anchor in anchors:
        sign = anchor["sign_number"]
        profile = profiles.get(sign)
        if not profile or profile["lines"] < 10:
            continue
        claim = " ".join(
            str(anchor.get(field, "")) for field in ("Reading", "Basis", "Source")
        ).lower()
        expects_terminal = any(term in claim for term in terminal_terms)
        expects_initial = any(term in claim for term in initial_terms)
        conflict = None
        if expects_terminal and profile["initial_rate"] > profile["terminal_rate"] + 0.25:
            conflict = "claims terminal/suffixal behavior but is substantially more reading-initial"
        elif expects_initial and profile["terminal_rate"] > profile["initial_rate"] + 0.25:
            conflict = "claims initial/prefixal behavior but is substantially more reading-terminal"
        if conflict:
            positional_conflicts.append(
                {
                    "sign": f"M{sign:03d}",
                    "reading": anchor.get("Reading", ""),
                    "confidence": anchor.get("Confidence", ""),
                    "conflict": conflict,
                    "lines": profile["lines"],
                    "initial_rate": profile["initial_rate"],
                    "terminal_rate": profile["terminal_rate"],
                    "basis": anchor.get("Basis", ""),
                }
            )
    return {
        "model": str(path),
        "anchors": len(anchors),
        "high_or_medium_anchors": len(accepted),
        "clean_corpus_token_coverage": covered / total_tokens if total_tokens else 0.0,
        "coverage_is_not_validation": True,
        "positional_conflicts": sorted(
            positional_conflicts,
            key=lambda item: (-item["lines"], item["sign"]),
        ),
    }


def write_csv(path: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--object-types", type=Path)
    parser.add_argument("--candidate-anchors", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    raw = load_corpus(args.corpus)
    clean, audit = clean_corpus(raw)
    profiles = sign_profiles(clean)
    permutation = positional_permutation_test(clean)
    prediction = evaluate_ngram(clean)
    formulas = collect_formulas(clean)
    frames = substitution_frames(clean)
    associations = {
        "field_symbol": binary_association(clean, "field_symbol"),
        "location": binary_association(clean, "location"),
        "object_type": binary_association(clean, "object_type"),
    }
    candidate = audit_candidate_anchors(args.candidate_anchors, profiles, clean)

    summary = {
        "corpus_audit": audit,
        "positional_permutation_test": permutation,
        "held_out_prediction": prediction,
        "candidate_model_audit": candidate,
    }
    (args.output / "analysis.json").write_text(
        json.dumps(summary, indent=2, default=dict) + "\n", encoding="utf-8"
    )
    (args.output / "associations.json").write_text(
        json.dumps(associations, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(
        args.output / "sign_profiles.csv",
        [profiles[sign] for sign in sorted(profiles)],
    )
    write_csv(args.output / "formulas.csv", formulas)
    write_csv(args.output / "substitution_frames.csv", frames)

    most_initial = sorted(
        (p for p in profiles.values() if p["lines"] >= 10),
        key=lambda p: (-p["initial_rate"], -p["lines"]),
    )[:12]
    most_terminal = sorted(
        (p for p in profiles.values() if p["lines"] >= 10),
        key=lambda p: (-p["terminal_rate"], -p["lines"]),
    )[:12]
    top_tokens = sorted(profiles.values(), key=lambda p: -p["tokens"])[:15]
    report = [
        "# Structural analysis — generated result",
        "",
        "## Corpus",
        "",
        f"- Raw: {audit['raw_lines']:,} lines on {audit['artifacts']:,} artifacts; "
        f"{audit['raw_tokens']:,} sign positions.",
        f"- EBUDS-like clean unique subset: {audit['ebuds_like_unique_lines']:,} lines, "
        f"{audit['ebuds_like_tokens']:,} tokens, {audit['ebuds_like_distinct_signs']} signs.",
        f"- Removed/flagged: {audit['rows_with_unknown_000']:,} lines with M000, "
        f"{audit['rows_on_multiline_faces']:,} rows on multi-line faces, and "
        f"{audit['exact_duplicate_occurrences_removed']:,} exact duplicate occurrences.",
        "",
        "## Tests that do not assume a language",
        "",
        f"- Positional concentration: {permutation['observed']:.3f} observed vs "
        f"{permutation['null_mean']:.3f} shuffled (z={permutation['z_score']:.1f}, "
        f"empirical p={permutation['empirical_p_ge']:.4g}).",
        f"- Held-out artifact split: unigram {prediction['mean_unigram_bits_per_token']:.3f} "
        f"bits/token vs bigram {prediction['mean_bigram_bits_per_token']:.3f}; "
        f"gain {prediction['bigram_information_gain_bits']:.3f} bits/token.",
        "- These results establish ordered structure; they do not select Dravidian, Sanskrit, "
        "a non-linguistic code, or any particular translation.",
        "",
        "## Highest-frequency signs",
        "",
        "| Sign | Tokens | Lines | Initial rate | Terminal rate | Position concentration |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for p in top_tokens:
        report.append(
            f"| M{p['sign']:03d} | {p['tokens']} | {p['lines']} | "
            f"{p['initial_rate']:.2f} | {p['terminal_rate']:.2f} | "
            f"{p['position_concentration']:.2f} |"
        )
    report += ["", "## Strong reading-initial candidates", ""]
    report.append(
        ", ".join(
            f"M{p['sign']:03d} ({p['initial_rate']:.0%}, n={p['lines']})"
            for p in most_initial
        )
    )
    report += ["", "## Strong reading-terminal candidates", ""]
    report.append(
        ", ".join(
            f"M{p['sign']:03d} ({p['terminal_rate']:.0%}, n={p['lines']})"
            for p in most_terminal
        )
    )
    report += ["", "## Most productive substitution frames", ""]
    for item in frames[:12]:
        report.append(
            f"- `{item['frame']}`: {item['alternative_count']} alternatives across "
            f"{item['occurrences']} clean inscriptions ({item['alternatives']})."
        )
    if candidate:
        report += ["", "## Candidate-model positional audit", ""]
        report.append(
            f"The supplied model assigns {candidate['high_or_medium_anchors']} HIGH/MEDIUM "
            f"readings and thereby covers {candidate['clean_corpus_token_coverage']:.1%} of "
            "tokens. Coverage is descriptive, not validation."
        )
        for conflict in candidate["positional_conflicts"][:12]:
            report.append(
                f"- {conflict['sign']} `{conflict['reading']}`: {conflict['conflict']} "
                f"(initial {conflict['initial_rate']:.0%}, terminal "
                f"{conflict['terminal_rate']:.0%}, n={conflict['lines']})."
            )
    report += [
        "",
        "## Epistemic status",
        "",
        "This report supports a structured formula system and identifies testable sign roles. "
        "It does not by itself recover sound values or sentence-level meanings.",
        "",
    ]
    (args.output / "structural_report.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
