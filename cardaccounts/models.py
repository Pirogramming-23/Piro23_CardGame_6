from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    social_type = models.CharField(max_length=20, null=True, blank=True)  # 예: 'google', 'kakao'
    social_id = models.CharField(max_length=100, null=True, blank=True)   # 소셜 고유 id
    profile_image = models.URLField(null=True, blank=True)
    score = models.IntegerField(default=0)  # 게임 점수
