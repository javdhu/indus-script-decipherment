#!/usr/bin/env python3
"""Render corpus sign glyphs and frequent formulas for visual checking."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_glyph(sign_dir: Path, sign: int, size: int = 70) -> Image.Image:
    source = Image.open(sign_dir / f"{sign}.gif").convert("RGBA")
    bbox = source.getbbox()
    if bbox:
        source = source.crop(bbox)
    source.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), "white")
    canvas.alpha_composite(source, ((size - source.width) // 2, (size - source.height) // 2))
    return canvas.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sign-dir", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--formulas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=15)
    small = ImageFont.load_default(size=12)

    with args.profiles.open(newline="", encoding="utf-8") as handle:
        profiles = sorted(csv.DictReader(handle), key=lambda row: -int(row["tokens"]))[:48]
    cell_w, cell_h, columns = 132, 118, 8
    rows = (len(profiles) + columns - 1) // columns
    sheet = Image.new("RGB", (cell_w * columns, cell_h * rows), "white")
    draw = ImageDraw.Draw(sheet)
    for index, profile in enumerate(profiles):
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        sign = int(profile["sign"])
        sheet.paste(load_glyph(args.sign_dir, sign), (x + 30, y + 3))
        draw.text((x + 7, y + 76), f"M{sign:03d}  n={profile['tokens']}", fill="black", font=font)
        draw.text(
            (x + 7, y + 96),
            f"I {float(profile['initial_rate']):.0%}  T {float(profile['terminal_rate']):.0%}",
            fill="#333333",
            font=small,
        )
    sheet.save(args.output / "top_signs.png")

    with args.formulas.open(newline="", encoding="utf-8") as handle:
        raw_formulas = list(csv.DictReader(handle))
    selected = []
    seen = set()
    for row in raw_formulas:
        if row["kind"] == "initial" and 2 <= int(row["width"]) <= 4 and row["sequence"] not in seen:
            selected.append(row)
            seen.add(row["sequence"])
        elif row["kind"] == "terminal" and 2 <= int(row["width"]) <= 4 and row["sequence"] not in seen:
            selected.append(row)
            seen.add(row["sequence"])
        if len(selected) == 24:
            break

    row_h = 100
    formulas = Image.new("RGB", (1100, row_h * len(selected) + 40), "white")
    draw = ImageDraw.Draw(formulas)
    draw.text((20, 10), "Frequent formulas in canonical right-to-left reading order", fill="black", font=font)
    for row_index, row in enumerate(selected):
        y = 40 + row_index * row_h
        signs = [int(token.removeprefix("M")) for token in row["sequence"].split("-")]
        for sign_index, sign in enumerate(signs):
            formulas.paste(load_glyph(args.sign_dir, sign, 62), (20 + sign_index * 78, y + 4))
        label_x = 20 + max(4, len(signs)) * 78 + 20
        draw.text(
            (label_x, y + 15),
            f"{row['sequence']}  {row['kind']}  n={row['count']}",
            fill="black",
            font=font,
        )
        draw.text(
            (label_x, y + 43),
            f"sites={row['sites']}  object types={row['object_types']}",
            fill="#444444",
            font=small,
        )
        draw.line((15, y + row_h - 2, 1085, y + row_h - 2), fill="#dddddd", width=1)
    formulas.save(args.output / "frequent_formulas.png")


if __name__ == "__main__":
    main()
