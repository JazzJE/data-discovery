"""Summarize FlowER reaction files without loading a model."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from config import Config

FLOWER_DATASET_DIR = Config.FolderPaths.ROOT / "models" / "FlowER" / "data" / "flower_new_dataset"


ATOM_MAP_PATTERN = re.compile(r"\[[^\]]*:\d+\]")


def analyze_file(path: Path, sample_size: int) -> dict:
    line_count = 0
    blank_lines = 0
    malformed_lines = 0
    mapped_lines = 0
    reaction_lines = 0
    sequence_index_lines = 0
    product_count = Counter()
    reactant_component_count = Counter()
    samples = []

    with path.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line_count += 1
            line = raw_line.strip()

            if not line:
                blank_lines += 1
                continue

            if len(samples) < sample_size:
                samples.append(line)

            if ">>" not in line:
                malformed_lines += 1
                continue

            reaction_lines += 1
            reactants, products = line.split(">>", 1)
            product_text, separator, sequence_index = products.rpartition("|")

            if separator and sequence_index.isdigit():
                sequence_index_lines += 1
                products = product_text

            if ATOM_MAP_PATTERN.search(line):
                mapped_lines += 1

            reactant_component_count[len([part for part in reactants.split(".") if part])] += 1
            product_count[len([part for part in products.split(".") if part])] += 1

    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "lines": line_count,
        "blank_lines": blank_lines,
        "reaction_lines": reaction_lines,
        "malformed_lines": malformed_lines,
        "mapped_lines": mapped_lines,
        "unmapped_lines": reaction_lines - mapped_lines,
        "sequence_index_lines": sequence_index_lines,
        "reactant_components": dict(sorted(reactant_component_count.items())),
        "product_components": dict(sorted(product_count.items())),
        "samples": samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=FLOWER_DATASET_DIR,
        help="Directory containing FlowER .txt files.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=2,
        help="Number of example lines to show per file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON.",
    )
    args = parser.parse_args()

    if not args.dataset_dir.is_dir():
        parser.error(f"Dataset directory does not exist: {args.dataset_dir}")
    if args.sample_size < 0:
        parser.error("--sample-size must be non-negative")

    reports = [
        analyze_file(path, args.sample_size)
        for path in sorted(args.dataset_dir.glob("*.txt"))
    ]

    if args.json:
        print(json.dumps(reports, indent=2))
        return

    print(f"Dataset: {args.dataset_dir.resolve()}")
    for report in reports:
        print(f"\n{Path(report['path']).name} ({report['bytes']:,} bytes)")
        print(f"  lines: {report['lines']:,}")
        print(f"  reaction lines: {report['reaction_lines']:,}")
        print(f"  malformed lines: {report['malformed_lines']:,}")
        print(f"  mapped/unmapped: {report['mapped_lines']:,}/{report['unmapped_lines']:,}")
        print(f"  sequence-index lines: {report['sequence_index_lines']:,}")
        print(f"  reactant component counts: {report['reactant_components']}")
        print(f"  product component counts: {report['product_components']}")
        for index, sample in enumerate(report["samples"], start=1):
            print(f"  sample {index}: {sample[:200]}")


if __name__ == "__main__":
    main()
