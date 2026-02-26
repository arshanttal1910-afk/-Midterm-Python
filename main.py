# main.py
from __future__ import annotations
from datetime import datetime, date
from typing import Optional

import db
import ui
from objects import Player, Lineup


CSV_FILE = "lineup.csv"


def get_game_date() -> Optional[date]:
    """Ask once at start; must be YYYY-MM-DD or Enter to skip."""
    while True:
        s = input("Enter next game date (YYYY-MM-DD) or press Enter to skip: ").strip()
        if s == "":
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def main() -> None:
    lineup = Lineup(db.load_players(CSV_FILE))
    game_date = get_game_date()

    while True:
        # ✅ DATES PRINT FIRST (your problem fixed here)
        ui.display_header_with_dates(game_date)
        ui.print_menu()

        choice = ui.get_menu_choice()

        if choice == "1":
            ui.display_lineup(lineup)

        elif choice == "2":
            try:
                name, pos, ab, hits = ui.prompt_add_player()
                p = Player(name=name, position=pos)
                p.set_stats(ab, hits)
                lineup.add_player(p)
                db.save_players(lineup.get_players(), CSV_FILE)
                ui.show_message("Player added.\n")
            except Exception as e:
                ui.show_error(str(e))

        elif choice == "3":
            if len(lineup) == 0:
                ui.show_message("Lineup is empty.\n")
                continue
            ui.display_lineup(lineup)
            try:
                num = ui.prompt_remove_player(len(lineup))
                removed = lineup.remove_player(num)
                db.save_players(lineup.get_players(), CSV_FILE)
                ui.show_message(f"Removed: {removed.name}\n")
            except Exception as e:
                ui.show_error(str(e))

        elif choice == "4":
            if len(lineup) < 2:
                ui.show_message("Need at least 2 players to move.\n")
                continue
            ui.display_lineup(lineup)
            try:
                from_num, to_num = ui.prompt_move_player(len(lineup))
                lineup.move_player(from_num, to_num)
                db.save_players(lineup.get_players(), CSV_FILE)
                ui.show_message("Player moved.\n")
            except Exception as e:
                ui.show_error(str(e))

        elif choice == "5":
            if len(lineup) == 0:
                ui.show_message("Lineup is empty.\n")
                continue
            ui.display_lineup(lineup)
            try:
                num, new_pos = ui.prompt_edit_position(len(lineup))
                lineup.edit_position(num, new_pos)
                db.save_players(lineup.get_players(), CSV_FILE)
                ui.show_message("Position updated.\n")
            except Exception as e:
                ui.show_error(str(e))

        elif choice == "6":
            if len(lineup) == 0:
                ui.show_message("Lineup is empty.\n")
                continue
            ui.display_lineup(lineup)
            try:
                num, ab, hits = ui.prompt_edit_stats(len(lineup))
                lineup.edit_stats(num, ab, hits)
                db.save_players(lineup.get_players(), CSV_FILE)
                ui.show_message("Stats updated.\n")
            except Exception as e:
                ui.show_error(str(e))

        elif choice == "7":
            db.save_players(lineup.get_players(), CSV_FILE)
            ui.show_message("Bye!")
            break

        else:
            ui.show_message("Invalid option. Choose 1-7.\n")


if __name__ == "__main__":
    main()