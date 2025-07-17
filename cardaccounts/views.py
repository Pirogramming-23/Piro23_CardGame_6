from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import login

# Create your views here.
def social_login(request):
    social_type = 'kakao'  # 예시
    social_id = request.POST.get('social_id')
    email = request.POST.get('email')
    nickname = request.POST.get('nickname')

    user, created = CustomUser.objects.get_or_create(
        social_type=social_type,
        social_id=social_id,
        defaults={'username': nickname, 'email': email}
    )
    login(request, user)
