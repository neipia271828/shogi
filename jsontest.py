import json

with open("constants.json", "r", encoding="utf-8") as f:
    board = json.load(f)["initial_board"]
    symbol = json.load(f)["symbol"]

print(symbol[1])