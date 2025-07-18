from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('list/', views.game_list, name='game_list'),
    path('start/', views.game_start, name='game_start'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('<int:pk>/counterattack/', views.game_counterattack, name='game_counterattack'),
    path('<int:pk>/cancel/', views.cancel_game, name='cancel_game'),
]