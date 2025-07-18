from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.
def social_login(request):
    if request.method == 'POST':
        social_type = 'kakao'
        social_id = request.POST.get('social_id')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

        user, created = CustomUser.objects.get_or_create(
            social_type=social_type,
            social_id=social_id,
            defaults={'username': nickname, 'email': email}
        )
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('home')
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup/signup.html', {'form': form})

def home(request):
    return render(request, 'base/base.html')