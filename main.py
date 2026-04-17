import random
import json
import os
from rich.live import Live
from rich.table import Table
from rich.console import Console
from pathlib import Path

console = Console()

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

    while(game_continue):
        console.clear()

        x_p = int(input("choose your peice x:"))
        y_p = int(input("choose your peice y:"))

        piece = (x_p, y_p)

        x_h = int(input("type your hand x:"))
        y_h = int(input("type your hand y:"))

        hand = (x_h, y_h)

        print(piece, hand)

        print_board(board, symbol)

def print_board(board, symbol):
    """盤面と持ち駒をテキストで描画"""
    print()
    # print("tegoma_g : ", end=" ")
    # for p in get_holdedpieces("second_hand"):  # 後手の持ち駒
    #     print(symbol[str(p)], end=" ")
    print("\n")

    print("1  2  3  4  5  6  7  8  9")
    for y in range(9):               # 0..8
        row = []
        for x in range(9):
            row.append(symbol[str(board[y][x])])
        print(" ".join(row), y+1)
    print()

    # print("tegoma_s : ", end="")
    # for p in get_holdedpieces("first_hand"):  # 先手の持ち駒
    #     print(symbol[str(p)], end=" ")
    print("\n")

def make_board_table(board, move_count):
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

    for i, row in enumerate(board)


if __name__ == "__main__":
    main()
