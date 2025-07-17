from django.urls import path
from . import views

urlpatterns = [
    path('social-login/', views.social_login, name='social_login'),
]
