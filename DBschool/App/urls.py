from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'App'

urlpatterns = [
    #정원
    path('join', views.join),
    path('test', views.test),
    
    #건호
    path('', views.home, name="Home"),
    path('Practice', views.Practice, name="Practice"),
    path('Exam', views.Exam, name="Exam"),
    path('QuizReg', views.QuizReg, name="QuizReg"),
    path('Grade', views.Grade, name="Grade"),



    #준엽
    path('login', views.signup),
    #부건


    #TEST
    path('myclass', views.myclass, name="myclass"),
    path('quiz', views.quiz, name="quiz"),
    path('datetime', views.datetime, name="datetime"),
    path('theme', views.theme, name="theme"),
    path('review', views.review, name="review"),
    path('onlineJudge', views.onlineJudge, name="onlineJudge"),
    path('classQuiz', views.classQuiz, name="classQuiz"),
    path('mypage', views.mypage, name="mypage"),
    path('test', views.test, name="test"),
]
