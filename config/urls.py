"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 게임, 랭킹
    path('game/', include('cardgame.urls')),
    path('ranking/', include('cardranking.urls')),

    # allauth (카카오, 소셜, 기본 로그인, 비번 찾기)
    path('accounts/', include('allauth.urls')),

    # 내 custom accounts (로그인, 회원가입, 마이페이지 등)
    path('user/', include('cardaccounts.urls')),

    # 메인 홈
    path('', include('cardaccounts.urls')),
]
