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
    path('selectClassQuiz', views.selectClassQuiz, name="selectClassQuiz"),
    path('datetime', views.datetime, name="datetime"),
    path('theme', views.theme, name="theme"),
    path('review', views.review, name="review"),
    path('onlineJudge', views.onlineJudge, name="onlineJudge"),
    path('classQuiz', views.classQuiz, name="classQuiz"),
    path('mypagePrivacy', views.mypagePrivacy, name="mypagePrivacy"),
    path('mypageClass', views.mypageClass, name="mypageClass"),
    path('mypageGrade', views.mypageGrade, name="mypageGrade"),
    path('mypageEnroll', views.mypageEnroll, name="mypageEnroll"),
    path('test', views.test, name="test"),
]