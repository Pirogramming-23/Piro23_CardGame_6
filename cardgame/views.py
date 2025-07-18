import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required # login_required 데코레이터를 임포트합니다.

# --- 중요: 아래 라인에서 'User' 임포트 제거 ---
from .models import Game # Game 모델만 임포트합니다.
# ---------------------------------------------

# 사용자 모델은 항상 get_user_model()을 통해 가져와야 합니다.
User = get_user_model()


@login_required
def main_view(request):
    """
    메인 페이지를 렌더링하는 뷰 함수입니다.
    로그인한 사용자만 접근할 수 있습니다.
    """
    context = {}
    return render(request, 'cardgame/main.html', context)


@login_required
def game_start(request):
    """
    새로운 게임을 시작하는 뷰 함수입니다.
    GET 요청 시 카드 선택 및 상대방 선택 화면을 보여주고,
    POST 요청 시 게임을 생성하여 저장합니다.
    """
    if request.method == "POST":
        attacker_card = int(request.POST.get("attacker_card"))
        defender_id = int(request.POST.get("defender_id"))
        win_rule = random.choice(["min", "max"])

        # 방어자 User 객체를 가져옵니다. 없으면 404 에러 발생.
        defender = get_object_or_404(User, pk=defender_id)

        new_game = Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=attacker_card,
            win_rule=win_rule,
            status="pending"
        )
        messages.success(request, "게임이 성공적으로 시작되었습니다. 상대방의 반격을 기다리세요!")
        return redirect("main")

    else: # GET 요청 시
        # 1부터 10까지의 숫자 중 5개를 무작위로 선택 (카드)
        card_choices = random.sample(range(1, 11), 5)
        # 현재 로그인한 사용자를 제외한 모든 사용자 목록을 가져와 상대방 선택지로 제공
        defender_choices = User.objects.exclude(pk=request.user.pk)
        context = {
            'card_choices': card_choices,
            'defender_choices': defender_choices,
        }
        # cardgame/gamestart.html 템플릿을 렌더링하고 컨텍스트를 전달합니다.
        return render(request, 'cardgame/gamestart.html', context)


@login_required
def game_list(request):
    """
    현재 로그인한 사용자가 참여하고 있는 모든 게임 목록을 보여주는 뷰 함수입니다.
    """
    games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
    context = {
        "games": games,
        "current_user": request.user, # 현재 로그인한 사용자 정보
    }
    return render(request, "cardgame/gamelist.html", context)


@login_required
def game_detail(request, pk):
    """
    특정 게임의 상세 정보를 보여주는 뷰 함수입니다.
    """
    # pk에 해당하는 Game 객체를 가져옵니다. 없으면 404 에러.
    game = get_object_or_404(Game, pk=pk)
    context = {
        "game": game,
        "user": request.user,
    }
    return render(request, 'cardgame/gamedetail.html', context)


@login_required
def game_counterattack(request, pk):
    """
    방어자가 공격에 반격하는 뷰 함수입니다.
    """
    game = get_object_or_404(Game, pk=pk)
    print(f"Counterattack view accessed by user: {request.user}, game defender: {game.defender}, game defender_card: {game.defender_card}")

    if request.method == "POST":
        if game.defender != request.user:
            print("Redirecting because user is not defender.")  # For the first condition
            messages.error(request, "해당 게임의 방어자만 반격할 수 있습니다.")
            return redirect('game_detail', pk=game.id)

        if game.defender_card:
            print("Redirecting because defender_card already exists.")  # For the second condition
            messages.warning(request, "이미 반격이 완료된 게임입니다.")
            return redirect('game_detail', pk=game.id)

        selected_card = int(request.POST.get("defender_card"))
        game.defender_card = selected_card
        game.status = "completed"

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
        messages.success(request, "반격이 성공적으로 완료되었습니다. 결과를 확인하세요!")
        return redirect('game_detail', pk=game.id)

    else:  # GET 요청
        if game.defender != request.user:
            print("Redirecting because user is not defender.")  # For the first condition
            messages.error(request, "해당 게임의 방어자만 반격할 수 있습니다.")
            return redirect('game_detail', pk=game.id)

        if game.defender_card:
            print("Redirecting because defender_card already exists.")  # For the second condition
            messages.warning(request, "이미 반격이 완료된 게임입니다.")
            return redirect('game_detail', pk=game.id)

        card_choices = random.sample(range(1, 11), 5)
        context = {
            'game': game,
            'card_choices': card_choices,
        }
        return render(request, 'cardgame/gamecounterattack.html', context)


@login_required
def cancel_game(request, pk):
    """
    게임 취소 뷰 함수입니다. (POST 요청만 처리)
    """
    game = get_object_or_404(Game, pk=pk) # pk에 해당하는 Game 객체 가져오기

    if request.method == "POST":
        # 현재 로그인한 사용자가 게임의 공격자이고, 게임 상태가 '대기 중'일 때만 취소 가능
        if game.attacker == request.user and game.status == "pending":
            game.delete()
            messages.success(request, "게임이 성공적으로 취소되었습니다.")
        else:
            messages.error(request, "게임을 취소할 권한이 없거나 이미 진행 중인 게임입니다.")
        return redirect("game_list") # 게임 취소 후 게임 목록 페이지로 리다이렉트

    else: # POST 요청이 아닌 경우 (예: URL 직접 입력 등 GET 요청)
        messages.warning(request, "잘못된 접근입니다. 게임 취소는 POST 요청으로만 가능합니다.")
        return redirect("game_list") # 게임 목록 페이지로 리다이렉트
