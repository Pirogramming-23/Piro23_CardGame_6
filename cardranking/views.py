from django.shortcuts import render

# Create your views here.
def ranking_view(request):
    rankings = [
        {'username': 'user2', 'score': 11},
        {'username': 'user1', 'score': -1},
        {'username': 'user4', 'score': -6},
    ]
    return render(request, 'cardranking/ranking.html', {'rankings': rankings})


from django.contrib.auth import get_user_model

User = get_user_model()

def ranking_view(request):
    rankings = User.objects.order_by('-score')[:10]  # 상위 10명
    context = {'rankings': rankings}
    return render(request, 'cardranking/ranking.html', context)
