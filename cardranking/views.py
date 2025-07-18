from django.shortcuts import render

# Create your views here.
def ranking_view(request):
    rankings = [
        {'username': 'user2', 'score': 11},
        {'username': 'user1', 'score': -1},
        {'username': 'user4', 'score': -6},
    ]
    return render(request, 'cardranking/ranking.html', {'rankings': rankings})
