from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .models import problem
from . import views

app_name = 'app'


urlpatterns =[
    path('', views.main, name='main'),
    path('practice/', views.main, name='practice'),

    path('manage/', views.manage, name='manage'),
    path('manage/<int:classid>/', views.manage, name='manage_quiz'),
    path('manage/<int:classid>/<int:quizid>', views.manage, name='manage_student'),
    path('manage/delete/<int:classid>', views.delete_class, name='delete_class'),
    path('manage/delete/<int:classid>/<int:quizdeleteid>', views.delete_quiz, name='delete_quiz'),
    
    #quizreg
    path('quizreg/', views.quizreg_view, name='quizreg_view_class'),
    path('quizreg/<int:classid>', views.quizreg_view, name='quizreg_view_quiz'),
    
    #addclass
    path('manage/addclass', views.addclass, name='addclass'),
    
    #addstudent
    path('manage/addstudent', views.addstudent, name='addstudent'),
    
    
    path('quizreg/reg/<int:classid>', views.quizreg_2, name='quizreg_2'),
    path('quizreg/reg/en', views.quizreg_3, name='quizreg_3'),
    
    #test
    path('test/', views.test_view, name='test_view_class'),
    path('test/<int:classid>', views.test_view, name='test_view_quiz'),
    path('test/<int:classid>/<int:quizid>', views.test_view, name='test_view_student'),
    path('test/<int:classid>/<int:quizid>/<int:problemid>', views.test_exam, name='test_exam'),
    path('test/submit/<int:classid>/<int:quizid>/<int:problemid>', views.test_submit, name='test_submit')
    

]


#모든가능성