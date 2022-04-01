from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
# Create your views here.

#정원
def join(request):
    return render(request,"App/join.html")

def test(request):
    return render(request,"App/test.html")


#건호
def home(request):
    return render(request, "App/home.html")

def Practice(request):
    return render(request, "App/Practice.html")

def Exam(request):
    return render(request, "App/Exam.html")
    
def QuizReg(request):
    return render(request, "App/QuizReg.html")

def Grade(request):
    return render(request, "App/Grade.html")


#준엽
def signup(request):
    if request.method == "GET":
        return render(request, 'App/signup.html')


    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(request.POST)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("인증 성공")
            return HttpResponseRedirect(reverse('posts:index'))
        else:
            print("인증 실패")
            return render(request, 'App/signup.html')
    return render(request, 'App/signup.html')

#부건
