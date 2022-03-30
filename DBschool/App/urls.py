from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #정원
    path('join', views.join),

    #건호
    path('', views.home),

    #준엽
    path('login', views.signup),

    #부건

]
