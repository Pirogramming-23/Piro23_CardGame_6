from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from .models import Game, User  # 실제 모델 import 필요

#
# 각 view 함수에 주석, 변수 정의, context 구조 추가
#
def main_view(request):
    # 메인 페이지 context 준비 (필요시)
    context = {}
    return render(request, 'cardgame/main.html', context)

def game_start(request):
    if request.method == "POST":
        attacker_card = int(request.POST.get("attacker_card"))
        defender_id = int(request.POST.get("defender_id"))
        win_rule = random.choice(["min", "max"])

        defender = User.objects.get(pk=defender_id)

        new_game = Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=attacker_card,
            win_rule=win_rule,
            status="pending"
        )
        return redirect("main")
    else:
        card_choices = random.sample(range(1, 11), 5)
        defender_choices = User.objects.exclude(pk=request.user.pk)
        context = {
            'card_choices': card_choices,
            'defender_choices': defender_choices,
        }
        return render(request, 'cardgame/gamestart.html', context)

def game_list(request):
    # 로그인한 유저 기준 게임 목록 불러오기
    games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
    context = {
        'games': games,
        'current_user': request.user,
    }
    return render(request, 'cardgame/gamelist.html', context)

def game_detail(request, pk):
    # 특정 게임 정보 조회
    game = Game.objects.get(pk=pk)
    context = {
        'game': game,
        'user': request.user,
    }
    return render(request, 'cardgame/gamedetail.html', context)

def game_counterattack(request, pk):
    game = Game.objects.get(pk=pk)

    if request.method == "POST":
        if game.defender_card:
            return redirect('game_detail', pk=game.id)

        selected_card = int(request.POST.get("defender_card"))
        game.defender_card = selected_card
        game.status = "completed"

        # 승패 판정
        if (game.win_rule == "min" and game.attacker_card < game.defender_card) or \
           (game.win_rule == "max" and game.attacker_card > game.defender_card):
            game.winner = game.attacker
            game.loser = game.defender
            game.result = "attacker_win"
        elif game.attacker_card == game.defender_card:
            game.result = "draw"
        else:
            game.winner = game.defender
            game.loser = game.attacker
            game.result = "defender_win"

        game.save()
        return redirect('game_detail', pk=game.id)

    else:
        if game.defender_card:
            return redirect('game_detail', pk=game.id)

        card_choices = random.sample(range(1, 11), 5)
        context = {
            'game': game,
            'card_choices': card_choices,
        }
        return render(request, 'cardgame/gamecounterattack.html', context)

# 게임 취소함수
def cancel_game(request, pk):
    if request.method == "POST":
        game = Game.objects.get(pk=pk)
        if game.attacker == request.user and game.status == "pending":
            game.delete()
        return redirect("main")
    return HttpResponse("Cancel game logic here")   