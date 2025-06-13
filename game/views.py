from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Game, Player

OPERATORS = ['+', '-', '*', '/']

def create_game(request):
    if request.method == 'POST':
        name = request.POST.get('player_name')
        try:
            steps = int(request.POST.get('steps'))
        except ValueError:
            return render(request, 'game/create.html', {'error': 'Invalid number of steps.'})

        if steps not in [10, 20, 30, 40, 50]:
            return render(request, 'game/create.html', {'error': 'Rounds must be one of 10, 20, 30, 40, or 50.'})

        operand_limit = steps // 10
        max_number = steps + (steps // 2)
        number_pool = list(range(1, max_number + 1))

        game = Game.objects.create(steps=steps, parent_array=[])

        player = Player.objects.create(
            game=game,
            name=name,
            value=0,
            player_index=0,
            operands={op: operand_limit for op in OPERATORS},
            available_numbers=number_pool
        )
        return redirect('waiting_room', game_code=game.game_code)

    return render(request, 'game/create.html')

def winner(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game/winner.html', {'game': game, 'winner': game.winner})

def waiting_room(request, game_code):
    game = get_object_or_404(Game, game_code=game_code)
    if game.players.count() >= 2:
        player = game.players.filter(player_index=0).first()
        return redirect('play_game', player_id=player.id)
    return render(request, 'game/waiting.html', {'game': game})

def check_players(request, game_code):
    game = get_object_or_404(Game, game_code=game_code)
    if game.players.count() >= 2:
        player = game.players.filter(player_index=0).first()
        return JsonResponse({'ready': True, 'redirect_url': f'/play/{player.id}/'})
    return JsonResponse({'ready': False})

def join_game(request, game_code):
    game = get_object_or_404(Game, game_code=game_code)
    if game.players.count() >= 2:
        return render(request, 'game/full.html')

    if request.method == 'POST':
        name = request.POST.get('player_name')
        steps = game.steps
        operand_limit = steps // 10
        max_number = steps + (steps // 2)

        player = Player.objects.create(
            game=game,
            name=name,
            value=0,
            player_index=1,
            operands={op: operand_limit for op in OPERATORS},
            available_numbers=list(range(1, max_number + 1))
        )
        return redirect('play_game', player_id=player.id)

    return render(request, 'game/join.html', {'game': game})

def play_game(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    game = player.game
    opponent = game.players.exclude(id=player.id).first()
    players = game.players.all()

    both_done = all(len(p.available_numbers) == 0 for p in players)
    round_limit_reached = game.round >= game.steps

    # Game complete condition
    if both_done or round_limit_reached:
        game.is_complete = True
        if players[0].value > players[1].value:
            game.winner = players[0]
        elif players[1].value > players[0].value:
            game.winner = players[1]
        else:
            game.winner = None
        game.save()
        return redirect('winner', game_id=game.id)

    # Handle move submission
    if request.method == 'POST':
        if player.available_numbers:
            move = request.POST.get('move', '').replace(' ', '')
            process_move(game, player, opponent, move)

            player.has_moved = True
            player.save()

            # Round increment logic
            p1, p2 = game.players.all()
            if p1.has_moved and p2.has_moved:
                game.round += 1
                p1.has_moved = False
                p2.has_moved = False
                p1.save()
                p2.save()
                game.save()
            elif (not p1.available_numbers and p2.has_moved) or (not p2.available_numbers and p1.has_moved):
                game.round += 1
                p1.has_moved = False
                p2.has_moved = False
                p1.save()
                p2.save()
                game.save()

        return redirect('play_game', player_id=player.id)

    # Determine if this player can move
    is_turn = False
    if player.available_numbers:
        if game.current_turn == player.player_index:
            is_turn = True
        elif not opponent.available_numbers:
            is_turn = True

    message = None
    if not player.available_numbers:
        message = "You used all your numbers. Wait for the other player to make their move."

    return render(request, 'game/play.html', {
        'game': game,
        'player': player,
        'opponent': opponent,
        'is_turn': is_turn,
        'message': message
    })

def process_move(game, player, opponent, move):
    if not move:
        return

    # Parse operand and number
    if move[0] in '+-*/':
        operand = move[0]
        try:
            number = int(move[1:])
        except ValueError:
            return
    else:
        operand = ''
        try:
            number = int(move)
        except ValueError:
            return

    if number not in player.available_numbers:
        return

    # Apply operand effect with rule: min value = 1 (except for division)
    if operand:
        if player.operands.get(operand, 0) <= 0:
            return  # Operand already used

        result = opponent.value
        if operand == '+':
            result += number
            opponent.value = max(result, 1)
        elif operand == '-':
            result -= number
            opponent.value = max(result, 1)
        elif operand == '*':
            result *= number
            opponent.value = max(result, 1)
        elif operand == '/':
            if number != 0:
                opponent.value = opponent.value / number  # Allow decimal result
            else:
                return  # Invalid move: divide by zero

        player.operands[operand] -= 1
    else:
        opponent.value = max(number, 1)  # Direct value set – enforce min 1

    # Remove number and smaller ones
    player.available_numbers = [n for n in player.available_numbers if n > number]

    # Save updates
    player.save()
    opponent.save()

    # Turn logic
    if opponent.available_numbers:
        game.current_turn = opponent.player_index
    else:
        game.current_turn = player.player_index  # Let same player continue

    game.save()

def apply_op(a, b, op):
    if op == '+':
        return max(round(a + b, 2), 1)
    elif op == '-':
        return max(round(a - b, 2), 1)
    elif op == '*':
        return max(round(a * b, 2), 1)
    elif op == '/':
        return round(a / b, 2) if b != 0 else a
    return a

