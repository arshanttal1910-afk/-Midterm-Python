# ui.py
from __future__ import annotations
from datetime import date
from typing import Optional
from objects import Lineup, POSITIONS


LINE = "=" * 64


def display_header_with_dates(game_date: Optional[date]) -> None:
    """Print header + dates FIRST (matches assignment look)."""
    today = date.today()

    print(LINE)
    print("Baseball Team Manager".center(64))
    print(LINE)

    print(f"CURRENT DATE : {today.strftime('%Y-%m-%d')}")

    if game_date is not None:
        print(f"GAME DATE    : {game_date.strftime('%Y-%m-%d')}")
        if game_date > today:
            days = (game_date - today).days
            print(f"DAYS UNTIL GAME : {days}")

    print(LINE)


def print_menu() -> None:
    print("\nMENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print()


def get_menu_choice() -> str:
    return input("Menu option: ").strip()


def display_positions() -> None:
    print("POSITIONS")
    print(", ".join(POSITIONS))
    print()


def display_lineup(lineup: Lineup) -> None:
    if len(lineup) == 0:
        print("\nLineup is empty.\n")
        return

    print("\nLineup")
    print("-" * 64)
    print(f"{'#':<3} {'Player':<22} {'POS':<4} {'AB':>6} {'H':>6} {'AVG':>10}")
    print("-" * 64)

    for i, p in enumerate(lineup, start=1):
        print(f"{i:<3} {p.name:<22} {p.position:<4} {p.at_bats:>6} {p.hits:>6} {p.average:>10.3f}")

    print()


# -------------------- input helpers --------------------

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")


def input_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Enter a valid whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Must be at most {max_value}.")
            continue
        return value


def input_position(prompt: str = "Position: ") -> str:
    while True:
        pos = input(prompt).strip().upper()
        if pos in POSITIONS:
            return pos
        print(f"Invalid position. Choose from: {', '.join(POSITIONS)}")


# -------------------- flows (just ask user, return values) --------------------

def prompt_add_player() -> tuple[str, str, int, int]:
    print("\nAdd Player")
    name = input_nonempty("Name: ")
    display_positions()
    position = input_position("Position: ")
    at_bats = input_int("At-bats: ", min_value=0)
    hits = input_int("Hits: ", min_value=0)
    return name, position, at_bats, hits


def prompt_remove_player(max_index: int) -> int:
    return input_int(f"Remove which player (1-{max_index}): ", min_value=1, max_value=max_index)


def prompt_move_player(max_index: int) -> tuple[int, int]:
    from_num = input_int(f"Move FROM (1-{max_index}): ", min_value=1, max_value=max_index)
    to_num = input_int(f"Move TO (1-{max_index}): ", min_value=1, max_value=max_index)
    return from_num, to_num


def prompt_edit_position(max_index: int) -> tuple[int, str]:
    num = input_int(f"Edit position for (1-{max_index}): ", min_value=1, max_value=max_index)
    display_positions()
    new_pos = input_position("New position: ")
    return num, new_pos


def prompt_edit_stats(max_index: int) -> tuple[int, int, int]:
    num = input_int(f"Edit stats for (1-{max_index}): ", min_value=1, max_value=max_index)
    at_bats = input_int("At-bats: ", min_value=0)
    hits = input_int("Hits: ", min_value=0)
    return num, at_bats, hits


def show_message(msg: str) -> None:
    print(msg)


def show_error(msg: str) -> None:
    print(f"Error: {msg}")