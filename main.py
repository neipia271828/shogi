import random
import json
import time
import os
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.console import Console

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from pathlib import Path

console = Console()
session = PromptSession(history=InMemoryHistory()) #type:ignore

BASE_DIR = Path(__file__).parent

turn = random.randint(0, 1)
game_continue = True

with open(BASE_DIR / "constants.json", "r", encoding="utf-8") as f:
    constants = json.load(f)

board = constants["initial_board"]
symbol = constants["symbol"]

print("initial_board type : ", type(board[0][0]))
print("symbol type : ", type(symbol["1"]))

# def print_board(board):
#     for i in range(8):
#         print()
#         for j in range(8):
#             print(f"{board[j][i]} ", end = "")

def main():
    print("Let's play shogi")
    print("Your are", "first hand" if turn == 1 else "second hand")

    print_board(board, symbol)

    with Live(make_board_table(board, move_count), console=console, auto_refresh=False) as live:
        while True:
            live.stop()
            try:
                cmd = session.prompt("指し手 > ")
            except (KeyboardInterrupt, EOFError):
                break
            live.start()

            if cmd.strip() == "quit":
                break

            live.update(make_board_table(board, move_count, last_move))
            live.refresh()

def make_board_table(board, move_count, last_move=None):
    table = Table(
        title=f"手番: {move_count}",
        show_header=True,
        header_style="bold",
        show_lines=True,
    )

    #列ヘッダー (9 ~ 1)
    table.add_column("", justify="center", width=2)
    for col in "9 8 7 6 5 4 3 2 1":
        table.add_column(col, justify="center", width=2)

    # 行ラベル
    row_labels = "一二三四五六七八九"

    for i, row in enumerate(board):
        table.add_row(row_labels[i], *row)
    
    return Table


if __name__ == "__main__":
    main()
