# objects.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Iterator

POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")


@dataclass
class Player:
    name: str
    position: str
    at_bats: int = 0
    hits: int = 0

    @property
    def average(self) -> float:
        if self.at_bats <= 0:
            return 0.0
        return self.hits / self.at_bats

    def set_position(self, new_position: str) -> None:
        new_position = new_position.strip().upper()
        if new_position not in POSITIONS:
            raise ValueError(f"Invalid position. Choose from: {', '.join(POSITIONS)}")
        self.position = new_position

    def set_stats(self, at_bats: int, hits: int) -> None:
        if at_bats < 0 or hits < 0:
            raise ValueError("At-bats and hits cannot be negative.")
        if hits > at_bats:
            raise ValueError("Hits cannot be greater than at-bats.")
        self.at_bats = at_bats
        self.hits = hits


class Lineup:
    def __init__(self, players: List[Player] | None = None) -> None:
        self._players: List[Player] = list(players) if players else []

    def __iter__(self) -> Iterator[Player]:
        return iter(self._players)

    def __len__(self) -> int:
        return len(self._players)

    def get_players(self) -> List[Player]:
        return list(self._players)

    def add_player(self, player: Player) -> None:
        self._players.append(player)

    def remove_player(self, index_1based: int) -> Player:
        idx = self._to_index(index_1based)
        return self._players.pop(idx)

    def move_player(self, from_1based: int, to_1based: int) -> None:
        from_idx = self._to_index(from_1based)
        to_idx = self._to_index(to_1based)
        player = self._players.pop(from_idx)
        self._players.insert(to_idx, player)

    def edit_position(self, index_1based: int, new_position: str) -> None:
        idx = self._to_index(index_1based)
        self._players[idx].set_position(new_position)

    def edit_stats(self, index_1based: int, at_bats: int, hits: int) -> None:
        idx = self._to_index(index_1based)
        self._players[idx].set_stats(at_bats, hits)

    def _to_index(self, index_1based: int) -> int:
        if index_1based < 1 or index_1based > len(self._players):
            raise IndexError(f"Choose a number from 1 to {len(self._players)}.")
        return index_1based - 1