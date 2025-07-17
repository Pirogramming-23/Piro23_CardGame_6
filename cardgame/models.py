from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Game(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    attacker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attacker_games')
    defender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='defended_games')
    attacker_card = models.IntegerField()
    defender_card = models.IntegerField(null=True)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='lost_games')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
