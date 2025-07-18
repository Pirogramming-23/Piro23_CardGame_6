from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main_page, name='main_page'),
    path('start/', views.start_game, name='start_game'),
    path('list/', views.list_game, name='list_game'),
]