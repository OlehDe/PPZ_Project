from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Дані гри
players = {
    "A": {"board": [], "alive": True},
    "B": {"board": [], "alive": True},
    "C": {"board": [], "alive": True},
    "D": {"board": [], "alive": True},
}
player_order = ["A", "B", "C", "D"]
current_attacker_index = 0

import random

# Функція для перевірки чи можна поставити корабель
def can_place_ship(board, x, y, size, horizontal):
    for i in range(-1, size + 1):
        for j in [-1, 0, 1]:
            xi = x + (i if horizontal else 0)
            yi = y + (0 if horizontal else i)
            xi += j if not horizontal else 0
            yi += j if horizontal else 0
            if 0 <= xi < 10 and 0 <= yi < 10:
                if board[yi][xi] != 0:
                    return False
    return True

# Функція для розміщення корабля
def place_ship(board, x, y, size, horizontal):
    for i in range(size):
        xi = x + i if horizontal else x
        yi = y if horizontal else y + i
        board[yi][xi] = 1

# Генерація флоту
def generate_fleet():
    board = [[0 for _ in range(10)] for _ in range(10)]
    ships = [(4, 1), (3, 2), (2, 3), (1, 4)]  # (size, count)

    for size, count in ships:
        for _ in range(count):
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                x = random.randint(0, 10 - (size if horizontal else 1))
                y = random.randint(0, 10 - (1 if horizontal else size))
                if can_place_ship(board, x, y, size, horizontal):
                    place_ship(board, x, y, size, horizontal)
                    placed = True
    return board

# Ініціалізація гри
def init_game():
    global players, current_attacker_index
    for player in players:
        players[player]["board"] = generate_fleet()
        players[player]["alive"] = True
    current_attacker_index = 0


# Пошук наступного гравця
def next_target_index(start_index):
    idx = (start_index + 1) % len(player_order)
    while not players[player_order[idx]]["alive"]:
        idx = (idx + 1) % len(player_order)
    return idx

@csrf_exempt
def index(request):
    return render(request, "battleship/index.html")

@csrf_exempt
def attack(request):
    global current_attacker_index

    if not any(players[p]["board"] for p in players):
        init_game()

    if request.method == "POST":
        data = json.loads(request.body)
        try:
            x, y = int(data.get("x")), int(data.get("y"))
            target_name = data.get("target")
        except (TypeError, ValueError):
            return JsonResponse({"error": "Invalid data"}, status=400)

        target = players.get(target_name)
        if not target or not target["alive"]:
            return JsonResponse({"error": "Invalid target"}, status=400)

        # Якщо клітинка вже атакована
        if target["board"][y][x] in [2, 3]:
            return JsonResponse({"error": "Ця клітинка вже була атакована!"}, status=400)

        # 🟢 Перевірка діапазону
        if not (0 <= x < len(target["board"][0]) and 0 <= y < len(target["board"])):
            return JsonResponse({"error": "Invalid coordinates"}, status=400)

        attacker_name = player_order[current_attacker_index]
        hit = target["board"][y][x] == 1
        status = "hit" if hit else "miss"

        if target["board"][y][x] in [2, 3]:  # 2 = підбитий, 3 = промах
            return JsonResponse({"error": "Ця клітинка вже була атакована!"}, status=400)

        if hit:
            target["board"][y][x] = 2  # 2 = підбитий корабель
            result = f"{attacker_name} влучив у {target_name}!"
            if not any(1 in row for row in target["board"]):
                target["alive"] = False
                result += f" {target_name} знищений!"
        else:
            result = f"{attacker_name} промахнувся по {target_name}."
            current_attacker_index = next_target_index(current_attacker_index)

        # Перевірка переможця
        alive_players = [p for p in players if players[p]["alive"]]
        if len(alive_players) == 1:
            result += f" 🏆 {alive_players[0]} переміг!"

        next_target_idx = next_target_index(current_attacker_index)
        next_attacker = player_order[current_attacker_index]
        next_target = player_order[next_target_idx]

        return JsonResponse({
            "result": result,
            "status": status,
            "x": x,
            "y": y,
            "target": target_name,
            "next_attacker": next_attacker,
            "next_target": next_target
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def reset_game(request):
    init_game()
    return JsonResponse({"status": "ok"})
