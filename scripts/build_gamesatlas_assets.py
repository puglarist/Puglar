#!/usr/bin/env python3
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "gamesatlas_weapons" / "raw_scrape.json"
OUTDIR = ROOT / "assets" / "gamesatlas_weapons"


def main() -> None:
    data = json.loads(RAW.read_text())

    OUTDIR.mkdir(parents=True, exist_ok=True)

    # Stable sort for deterministic asset generation
    rows = sorted(data, key=lambda x: (x.get("game") or "", x.get("category") or "", x.get("title") or ""))

    (OUTDIR / "weapons.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")

    with (OUTDIR / "weapons.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["game", "title", "category", "season", "href", "image"])
        writer.writeheader()
        writer.writerows(rows)

    by_game = Counter(r.get("game") for r in rows)
    by_category = Counter(r.get("category") for r in rows)
    game_category = defaultdict(Counter)
    for r in rows:
        game_category[r.get("game")][r.get("category")] += 1

    summary = {
        "total_weapons": len(rows),
        "games": dict(by_game),
        "categories": dict(by_category),
        "game_category_breakdown": {g: dict(c) for g, c in game_category.items()},
    }
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
