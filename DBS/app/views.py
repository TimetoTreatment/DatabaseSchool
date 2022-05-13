from dataclasses import dataclass
from logging import exception
from .models import *
from .QueryBuilder import *
from datetime import datetime
from this import d
from django.shortcuts import get_object_or_404, render, redirect
from pytz import timezone
from .models import Class, Quiz, RegClass, Score, problem, submit
from .forms import addClassForm, addQuiz, addRegClass
from django.db.models import Max, Min, Avg, Count
import datetime as dt
from account.models import CustomUser as User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import pandas as pd
from django.db import connection
# Create your views here.
def main(request):
    return render(request, 'app/main.html')

#수업삭제
def delete_class(request, classid):
    model = Class.objects.get(pk=classid)
    model.delete()

    return redirect('app:manage')

#퀴즈삭제
def delete_quiz(request, classid, quizdeleteid):
    model= Quiz.objects.filter(classid = classid, id = quizdeleteid)
    model.delete()
    return redirect('app:manage_quiz', classid = classid)

def manage(request, **kwargs):
    context ={}
    context ={'class' : Class.objects.filter(profid = request.user),}
    if("classid" in kwargs):
        context['quiz'] = Quiz.objects.filter(classid = kwargs['classid'])
    
    if('quizid' in kwargs):
        context['quiz'] = Quiz.objects.filter(classid = kwargs['classid'])
        student = RegClass.objects.filter(classid = kwargs['classid'])

        for row in student:
            row.student_name = User.objects.filter(id = row.userid.id).first().first_name
            grade = Score.objects.filter(classid = kwargs['classid'], quizid= kwargs['quizid'], studentid=row.userid).values('studentid').annotate(max_score=Max('Score')).first()
            if (grade):
                row.grade = grade['max_score']
            else:
                row.grade = '미제출'
    
        context['grade'] = student
    return render(request, 'app/mypage_manage.html', context)


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
    context['quiz'] = Q=  Quiz.objects.get(id=quizid)
    context['quizid'] = quizid
    context['classid'] = classid
    
    Q1 = OurQuery(table_school, Q.tablename, Q.problemnum)
    if(Q.sqlkeyword =="select"):
        query = Q1.select_query()
    elif(Q.sqlkeyword =="update"):
        query = Q1.update_query()
    elif(Q.sqlkeyword =="delete"):
        query = Q1.delete_query()
    elif(Q.sqlkeyword =="insert"):
        query = Q1.insert_query()        
    
    context['makequery'] = query
    context['prob'] = "+".join(query)

    raw_queryset1 =  table_school.objects.raw('SELECT address, tel, id, classnum, name FROM app_table_school WHERE classnum = 6')
    raw_queryset2 = table_school.objects.raw('SELECT address, tel, id, classnum, name FROM app_table_school WHERE classnum = 6')

    return render(request, 'app/quizreg_2.html', context)

def quizreg_4(request, classid, quizid, prob):
    prob = prob.split('+')
    for i in prob:
        _class = Class.objects.get(id = classid)
        _quiz = Quiz.objects.get(id = quizid)
        pro = problem(classid=_class, quizid=_quiz, profid=request.user, contents="", sql=i)
        print(pro)
        pro.save()
        
    return redirect('app:quizreg_view_class')

def quizreg_view(request, **kwargs):
    context ={}
    _class = Class.objects.filter(profid = request.user.id)
    _quiz=None
    _classid=None
    
    if( "classid" in kwargs.keys()):
        _quiz =  Quiz.objects.filter(classid= kwargs['classid'], profid = request.user.id)
        _classid = kwargs['classid']
    context ={
        "class" : _class,
        "quiz" : _quiz,
        "classid" : _classid
              }
    
    return render(request, 'app/quizreg_0.html', context)

def test_view(request, **kwargs):
    context = {}
    context['class'] = RegClass.objects.filter(userid = request.user.id)
    
    if("classid" in kwargs.keys()):
        context['quiz'] = Quiz.objects.filter(classid=kwargs['classid'])
    
    if("quizid" in kwargs.keys()):
        prob = problem.objects.filter(classid=kwargs['classid'], quizid=kwargs['quizid']).order_by('id')
        print(prob)
        for row in prob:
            _submit=None
            _submit = submit.objects.filter(classid = kwargs['classid'], quizid= kwargs['quizid'], studentid=request.user.id, problemid=row.id).order_by('-is_pass').first()
            if (_submit):
                row.submit = _submit.is_pass
            else:
                row.submit = "미제출"
        context['prob'] = prob    
        context['classid'] = kwargs['classid']
        context['quizid'] = kwargs['quizid']

    return render(request, 'app/test_0.html', context)

def textareaToStr(text):
    return text.replace(chr(13),'').replace('\n', ' ')

def bigTosmal(text):
    return text.replace('"', "'")

def compare_submit(submit_df, auto_df):
    try:
        if(len(auto_df.compare(submit_df))):
            return False
    except:
        return False
    
    return True
    
def sqlToDataFrame(sql, upper=False):
    sql = bigTosmal(sql)
    if(upper):
        sql = sql.upper()
    df = None
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame([
        dict(zip(columns, row)) for row in cursor.fetchall()
            ])
    return df


def test_exam(request, classid, quizid, problemid):
    context = {}
    
    context['class'] = Class.objects.get(pk=classid)
    context['quiz'] = Quiz.objects.get(pk=quizid)
    context['problem'] = problem.objects.get(pk=problemid)
    context['sql'] = ""
    context['print'] = None
    ans = None
    if request.method =="POST":
        context['sql'] = submit_sql = request.POST.get("code")
        auto_sql = problem.objects.get(pk=problemid).sql;
        auto_df = sqlToDataFrame(auto_sql, True)
        
        submit_sql = textareaToStr(submit_sql)
        try:
            submit_df = sqlToDataFrame(submit_sql, True)
            ans = compare_submit(submit_df, auto_df)
            context['table'] = sqlToDataFrame(submit_sql, False).head(3).to_html()
        except:
            ans = "SQL에러"
        
        if(ans ==True):
            context['answer'] ="정답입니다"
        elif(ans == False):
            context['answer'] ="실패입니다"
        else:
            context['answer'] =ans
        

    return render(request, 'app/test_1.html', context)

def test_submit(request, classid, quizid, problemid):
    context = {}
    print('fqfwq')
    context['class'] = Class.objects.get(pk=classid)
    context['quiz'] = Quiz.objects.get(pk=quizid)
    prob = problem.objects.get(pk=problemid)
    context['sql'] = ""
    context['print'] = None
    ans = None
    if request.method =="POST":
        context['sql'] = submit_sql = request.POST.get("code")
        auto_sql = problem.objects.get(pk=problemid).sql;
        auto_df = sqlToDataFrame(auto_sql, True)
        
        submit_sql = textareaToStr(submit_sql)
        try:
            submit_df = sqlToDataFrame(submit_sql, True)
            ans = compare_submit(submit_df, auto_df)
            context['table'] = submit_df.head(3).to_html()
        except:
            ans = "SQL에러"
        
        if(ans ==True):
            form = submit.objects.create(is_pass=True, classid=context['class'], problemid = prob, quizid = context['quiz'], studentid= request.user)    
            form.save()
        else:
            form = submit.objects.create(is_pass=False, classid=context['class'], problemid = prob, quizid = context['quiz'], studentid= request.user)    
            form.save()
        
    return redirect('app:test_view_student', classid, quizid)
        

#addclass
def addclass(request):
    context = {}
    if request.method == 'POST':
        form = addClassForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.profid = request.user
            form.save()
            return redirect('app:manage')
    
    else:
        form = addClassForm()
    context['form'] = form
    return render(request, 'app/mypage_add_class.html', context)

#addclass
def addstudent(request):
    context = {}
    context['class'] = Class.objects.filter(profid = request.user)
    
    if request.POST:
        form = addRegClass(request.POST)
        if(form.is_valid()):
            reg=form.save(commit=False)
            userid = User.objects.get(username = request.POST.get('studentid'))
            if(userid):
                reg.userid = userid
                isvalue = RegClass.objects.filter(classid=request.POST.get('classid'), userid= reg.userid)
            
                if(not isvalue):
                    reg.save()
        
    return render(request, 'app/mypage_add_student.html', context)