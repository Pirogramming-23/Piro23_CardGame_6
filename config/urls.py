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

    path('game/', include('cardgame.urls')),      # 게임 앱 (추후 활성화)
    
    path('accounts/', include('cardaccounts.urls')),  # account 앱 전용 URL  
    path('', include('cardaccounts.urls')),           # 루트 경로에서 cardaccounts로 연결
    path('user/', include('cardaccounts.urls')), # 내 custom 계정 앱

    path('ranking/', include('cardranking.urls')),  # 랭킹 앱 (추후 활성화) 

    path('auth/', include('allauth.urls')),          # allauth 카카오 로그인용
    path('accounts/', include('allauth.urls')),  # 소셜 + allauth 전용 로그인


]
