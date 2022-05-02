from datetime import datetime
from this import d
from django.shortcuts import get_object_or_404, render, redirect
from pytz import timezone
from .models import Class, Quiz, RegClass, Score
from .forms import addClassForm, addQuiz
from django.db.models import Max, Min, Avg, Count
import datetime as dt
from account.models import CustomUser as User
# Create your views here.
def main(request):
    return render(request, 'app/main.html')

def manage(request):
    context ={}
    _class = Class.objects.filter(profid = request.user.id)
    context['class'] = _class
    if request.method == 'POST':
        form = addClassForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.profid = request.user
            question.save()
            return redirect('app:manage')
    else:
        form = addClassForm()
        context['form'] = form
        
        return render(request, 'app/manage.html', context)

def class_delete(request, deleteid):
    print(deleteid)
    model = Class.objects.filter(profid = request.user.id, id = deleteid)
    model.delete()
    return redirect('app:manage')

def quiz_student_print(request, class_id):
    context ={}
    _quiz = Quiz.objects.filter(profid = request.user.id, classid = class_id)
    _class = Class.objects.filter(profid = request.user.id)
    context['quiz'] = _quiz
    context['class'] = _class
    context['form'] = addClassForm()
    
    
    return render(request, 'app/manage.html', context)

def quiz_delete(request, classid, quizdeleteid):
    model= Quiz.objects.filter(classid = classid, id = quizdeleteid)
    model.delete()
    return redirect('app:main')

def enroll(request):
    return render(request, 'app/enroll.html')

def quizenroll_1(request):
    return render(request, 'app/quizenroll_1.html')

def student_print(request, classid, quizid):
    context ={}
    context['quiz'] =  Quiz.objects.filter(classid= classid, profid = request.user.id)
    context['class'] = Class.objects.filter(profid = request.user.id)
    grade = Score.objects.filter(classid = classid, quizid= quizid).values('studentid')\
    .annotate(max_score=Max('Score'))
    
    for row in grade:
        row['student_name']=\
            User.objects.filter(id = row['studentid']).first().username
    context['grade'] = grade
    a= Score.objects.filter(classid = classid, quizid= quizid)
    print(a)
    print(grade)
    return render(request, 'app/manage.html', context)

def quizreg_2(request, classid):
    context ={}
    context['classid'] = classid
    if request.method == 'POST':
        form = addQuiz(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.profid = request.user
            quiz.classid = Class.objects.get(id=classid)
            print(Class.objects.get(id=classid))
            endtime = request.POST.get("starttime") + ":00"
            enddatetime= request.POST.get("date")+' ' + endtime
            enddatetime=datetime.strptime(enddatetime,'%Y-%m-%d %H:%M:%S')
            enddatetime = enddatetime + dt.timedelta(minutes=int(request.POST.get("timeout")))
            quiz.endtime = enddatetime.strftime('%H:%M:%S')
            print(request.POST.get('sqlkeyword'))
            quiz.save()

            return redirect('app:quizreg_3', classid=classid,quizid= quiz.id)
    else:
        form = addClassForm()
        context['form'] = form
        
        return render(request, 'app/quizreg_1.html', context)
    return render(request, 'app/quizreg_1.html')

def quizreg_3(request, classid, quizid):
    context={}
    context['quiz'] = Quiz.objects.get(id=quizid)
    print(context['quiz'])
    return render(request, 'app/quizreg_2.html', context)
    


def quizreg_0(request):
    context ={}
    _class = Class.objects.filter(profid = request.user.id)
    context['class'] = _class
   
    return render(request, 'app/quizreg_0.html', context)

def quizreg_1(request, classid):
    context ={}
    context['class'] = Class.objects.filter(profid = request.user.id)
    context['quiz'] =  Quiz.objects.filter(classid= classid, profid = request.user.id)
    context['classid'] = classid
    return render(request, 'app/quizreg_0.html', context)

def exam_0(request):
    context = {}
    
    context['class'] = RegClass.objects.filter(userid = request.user.id)
    return render(request, 'app/test_0.html', context)

def exam_1(request, classid):
    context = {}
    
    context['class'] = RegClass.objects.filter(userid = request.user.id)
    context['quiz'] = Quiz.objects.filter(classid=classid)
    return render(request, 'app/test_0.html', context)

def exam_2(request, classid, quizid):
    
    return render(request, 'app/test_1.html')