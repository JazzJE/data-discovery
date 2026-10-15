#!/usr/bin/env python3
"""Convert the Isha reaction CSV into FlowER text format.

Run this script from the repository root:

    python src/FlowER/convert_reactions.py
"""

import csv
import re
from pathlib import Path


INPUT_PATH = Path("data/original/isha_data_ord_100_reactions.csv")
OUTPUT_PATH = Path("data/flower_filtered/isha.txt")
ANNOTATION_PATTERN = re.compile(r"\s+\|[^|]*\|\s*$")


def convert_reaction(reaction: str, row_number: int) -> str:
    """Convert reactants>reagents>products to reactants>>products."""
    parts = reaction.strip().split(">")
    if len(parts) != 3:
        raise ValueError(
            f"row {row_number}: expected reactants>reagents>products, "
            f"found {len(parts) - 1} separator(s)"
        )

    reactants, reagents, products = (part.strip() for part in parts)
    products = ANNOTATION_PATTERN.sub("", products).strip()
    reactant_side = ".".join(
        molecule
        for field in (reactants, reagents)
        for molecule in field.split(".")
        if molecule.strip()
    )

    if not reactant_side or not products:
        raise ValueError(f"row {row_number}: reactants and products must be non-empty")

    return f"{reactant_side}>>{products}"


def convert_dataset(input_path: Path, output_path: Path) -> None:
    """Write each CSV reaction as one FlowER reaction per output line."""
    rows_written = 0

    with input_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None or "reaction_smiles" not in reader.fieldnames:
            raise ValueError(
                f"{input_path} must have a 'reaction_smiles' column in its header."
            )

        # Create the output directory if OUTPUT_PATH points to a new directory.
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8", newline="\n") as txt_file:
            for row_number, row in enumerate(reader, start=2):
                reaction = row.get("reaction_smiles")

                if reaction is None or not reaction.strip():
                    print(f"Skipping row {row_number}: missing reaction_smiles.")
                    continue

                txt_file.write(f"{convert_reaction(reaction, row_number)}\n")
                rows_written += 1

    print(f"Wrote {rows_written:,} reactions to: {output_path}")


if __name__ == "__main__":
    convert_dataset(INPUT_PATH, OUTPUT_PATH)
