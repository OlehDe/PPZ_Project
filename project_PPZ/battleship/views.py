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

# Ініціалізація гри
def init_game():
    global players, current_attacker_index
    from random import randint

    for player in players:
        board = [[0 for _ in range(10)] for _ in range(10)]  # 10x10 поле
        # Розставляємо 3 випадкові кораблі
        placed = 0
        while placed < 3:
            x, y = randint(0, 9), randint(0, 9)
            if board[y][x] == 0:
                board[y][x] = 1  # 1 = корабель
                placed += 1
        players[player]["board"] = board
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
