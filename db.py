# db.py
from __future__ import annotations
import csv
from pathlib import Path
from typing import List
from objects import Player


DEFAULT_FILE = "lineup.csv"


def load_players(csv_path: str = DEFAULT_FILE) -> List[Player]:
    path = Path(csv_path)
    if not path.exists():
        return []

    players: List[Player] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # expected headers: name,position,at_bats,hits
        for row in reader:
            try:
                name = (row.get("name") or "").strip()
                position = (row.get("position") or "").strip().upper()
                at_bats = int(row.get("at_bats", 0))
                hits = int(row.get("hits", 0))

                if not name:
                    continue

                p = Player(name=name, position=position, at_bats=at_bats, hits=hits)
                players.append(p)
            except Exception:
                continue

    return players


def save_players(players: List[Player], csv_path: str = DEFAULT_FILE) -> None:
    path = Path(csv_path)
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "position", "at_bats", "hits"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in players:
            writer.writerow(
                {
                    "name": p.name,
                    "position": p.position,
                    "at_bats": p.at_bats,
                    "hits": p.hits,
                }
            )