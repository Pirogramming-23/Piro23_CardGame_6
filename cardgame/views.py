from django.shortcuts import render

def main_page(request):
    return render(request, 'cardgame/main.html')

def start_game(request):
    # 게임 시작 로직
    return render(request, 'cardgame/start.html')

def list_game(request):
    # 게임 목록 로직
    return render(request, 'cardgame/list.html')
