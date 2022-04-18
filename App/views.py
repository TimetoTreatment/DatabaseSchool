from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import *
from .QueryBuilder import OurQuery
# Create your views here.

#정원
def join(request):
    # print(User.objects.values_list())
    # Q = User.objects.values()
    # print(Q[0], type(User.objects.values()))
    # for key in Q[0]:
    #     print(type(key),key)
    c1 = OurQuery(User,"User")
    result = c1.select_query()
    for i in result:
        print(i)
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
    
    return render(request, 'App/signup.html')

#부건
