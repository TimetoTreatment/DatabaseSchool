from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'


urlpatterns =[
    path('', views.main, name='main'),
    path('practice/', views.main, name='practice'),

    
    path('manage/', views.manage, name='manage'),
    #path('manage/<int:userid>', views.Class, name='class'),
    
    path('manage/delete/<int:deleteid>', views.class_delete, name='class_delete'),
    path('manage/delete/<int:classid>/<int:quizdeleteid>', views.quiz_delete, name='quiz_delete'),
    
    path('manage/quiz/<int:class_id>', views.quiz_student_print, name='quiz_student_print'),
    path('manage/<int:classid>/<int:quizid>', views.student_print, name='student_print'),
    
    path('manage/enroll', views.enroll, name='enroll'),
    
    #quizreg
    path('quizreg/', views.quizreg_0, name='quizreg_0'),
    path('quizreg/<int:classid>', views.quizreg_1, name='quizreg_1'),
    path('quizreg/reg/<int:classid>', views.quizreg_2, name='quizreg_2'),
    path('quizreg/reg/<int:classid>/<int:quizid>', views.quizreg_3, name='quizreg_3'),
    
    #test
    path('exam/', views.exam_0, name='exam_0'),
    path('exam/<int:classid>', views.exam_1, name='exam_1'),
    path('exam/<int:classid>/<int:quizid>', views.exam_2, name='exam_2'),
]


#모든가능성