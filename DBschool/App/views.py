from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

#로그인과 회원가입을 위한 import
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import auth

#정원
def join(request):
    if request.method == 'POST':
        user_email=request.POST["email"]
        user_password = request.POST["password"]
        username = request.POST["username"]
        userIT = request.POST["chk_info"]
        print(user_email)
        print(user_password)
        print(username)
        print(userIT)
        user = User.objects.create_user(user_email, user_password)
        auth.login(request, user)
        return redirect('/')
    return render(request,"App/join.html")


#건호
def home(request):
    return render(request, "App/home.html")



#준엽
def signup(request):
    if request.method == "GET":
        return render(request, 'App/signup.html')


    elif request.method == "POST":
        userid = request.POST['id']
        password = request.POST['password']
        user = authenticate(username = userid, password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
        else:
            print("인증실패")

    return render(request, 'App/signup.html')


#부건
