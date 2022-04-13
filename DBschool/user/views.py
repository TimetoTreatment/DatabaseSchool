from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from user.forms import SignupForm
from user.forms import CustomUserChangeForm
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

def update(request, pk):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'user': form
    }
    return render(request, 'App/Grade_Mypage.html', context)