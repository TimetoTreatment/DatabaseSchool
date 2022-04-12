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
    path('Grade/Mypage', views.Mypage, name="Mypage"),



    #준엽
    path('login', views.signup),
    #부건

]
