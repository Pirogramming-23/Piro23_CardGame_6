from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cardaccounts'

urlpatterns = [
    path('social-login/', views.social_login, name='social_login'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])