from dataclasses import dataclass
from logging import exception
from typing import final
from .models import *
from .QueryBuilder import *
from datetime import datetime
from this import d
from django.shortcuts import get_object_or_404, render, redirect,HttpResponseRedirect 
from django.urls import reverse_lazy
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
import json
import html
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
            grade1 = submit.objects.filter(classid = kwargs['classid'], quizid= kwargs['quizid'], studentid=row.userid, is_pass=True)
            grade2 = submit.objects.filter(classid = kwargs['classid'], quizid= kwargs['quizid'], studentid=row.userid, is_pass=False)
            quizcnt = problem.objects.filter(quizid = kwargs['quizid'])
            if(grade1 or grade2):
                grade= int(len(grade1)/len(quizcnt)*100)
            else :
                grade = 0
                
            if (grade):
                row.grade = grade
            else:
                row.grade = '미제출'
    
        context['grade'] = student
    return render(request, 'app/mypage_manage.html', context)


def quizreg_2(request, classid):
    context ={}
    context['classid'] = classid
    if request.method == 'POST':
        endtime = request.POST.get("starttime") + ":00"
        enddatetime= request.POST.get("date")+' ' + endtime
        enddatetime=datetime.strptime(enddatetime,'%Y-%m-%d %H:%M:%S')
        enddatetime = enddatetime + dt.timedelta(minutes=int(request.POST.get("timeout")))
        endtime = enddatetime.strftime('%H:%M:%S')
        context['quizlabel'] ={'quizname' :request.POST.get('quizname'),
                               'profid' : request.user.id,
                               'classid': classid,
                               'date' :request.POST.get('date'),
                               'endtime':endtime,
                               'problemnum':request.POST.get('problemnum'),
                               'sqlkeyword':request.POST.get('sqlkeyword'),
                               'tablename':request.POST.get('tablename'),
                               'starttime':request.POST.get('starttime'),
                               }
        tableObj = None
        tablename = request.POST.get('tablename')
        if( tablename== 'table_school'):
            tableObj = table_school
        elif tablename== 'parcel':
            tableObj = parcel
        elif tablename == 'restorant':
            tableObj = restorant
        elif tablename == 'book':
            tableObj = book
        
        Q1 = OurQuery(tableObj, request.POST.get('tablename'), int(request.POST.get('problemnum')))
        sqlkeyword = request.POST.get('sqlkeyword')
        if(sqlkeyword =="select"):
            query = Q1.select_query()
        elif(sqlkeyword =="update"):
            query = Q1.update_query()
        elif(sqlkeyword =="delete"):
            query = Q1.delete_query()
        elif(sqlkeyword =="insert"):
            query = Q1.insert_query()
        elif(sqlkeyword == "join"):
            query = Q1.join_query(parcel, 'parcel')        
            
        makequery = {}
        temp = []
        print(query)
        for k, v in query.items():
            makequery[k] = v[2]
            temp.append('|'.join(v[0:2]))
    
            
        context['contents']= temp
        context['makequery'] = makequery
        
        return render(request, 'app/quizreg_2.html', context)
            
    else:
        form = addClassForm()
        context['form'] = form
        
        return render(request, 'app/quizreg_1.html', context)
    return render(request, 'app/quizreg_1.html')


def quizreg_3(request):
    if request.method=="POST":
        quiz =addQuiz(request.POST)
        a =quiz.save()
        
        for i in range(1, int(request.POST.get('problemnum'))+1):
            print(1)
            _class = Class.objects.get(pk = request.POST.get('classid'))
            _proid = User.objects.get(pk = request.POST.get('profid'))
            pro = problem(classid = _class,
                          quizid = a,
                          profid = _proid,
                          sql = request.POST.get('query'+str(i)),
                          contents = request.POST.get('contents'+str(i)),
                          nan = request.POST.get('nan'+str(i))
                          )
            print(request.POST.get('nan'+str(1)))
            print(pro)
            pro.save()

    return redirect('app:quizreg_view_quiz', request.POST.get('classid'))


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
    
def sqlToDataFrame(sql, upper=False, table=None):
    sql = bigTosmal(sql)
    if(upper):
        sql = sql.upper()
    df = None
    with connection.cursor() as cursor:
        cursor.execute('begin transaction;')
        cursor.execute(sql)
        if('SELECT' not in sql.upper() and ('JOIN' not in sql.upper())):
            cursor.execute('SELECT * FROM {}'.format(table))
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame([
        dict(zip(columns, row)) for row in cursor.fetchall()
            ])
        cursor.execute('rollback;')
    return df


def test_exam(request, classid, quizid, problemid):
    context = {}
    
    context['class'] = Class.objects.get(pk=classid)
    context['quiz'] = Quiz.objects.get(pk=quizid)
    _problem = problem.objects.get(pk=problemid)
    context['problem'] = _problem
    context['contents'] = [html.unescape(i) for i in _problem.contents.split('|')]
    
    context['righttable'] = None
    context['origintable'] = sqlToDataFrame('select * from {}'.format(context['quiz'].tablename), upper=False, table=context['quiz'].tablename).to_html()
    if('JOIN' in _problem.sql.upper()):
        context['righttable'] = sqlToDataFrame('select * from {}'.format('parcel'), upper=False, table=context['quiz'].tablename).to_html()
    context['modifytable'] = sqlToDataFrame(context['problem'].sql, upper=False, table=context['quiz'].tablename).to_html()
    
    context['sql'] = ""
    context['print'] = None
    ans = None
    if request.method =="POST":
        context['sql'] = submit_sql = request.POST.get("code")
        auto_sql = problem.objects.get(pk=problemid).sql;
        auto_df = sqlToDataFrame(auto_sql, True, context['quiz'].tablename)
        
        submit_sql = textareaToStr(submit_sql)
        try:
            submit_df = sqlToDataFrame(submit_sql, True,context['quiz'].tablename)
            ans = compare_submit(submit_df, auto_df)
            context['table'] = sqlToDataFrame(submit_sql, False, context['quiz'].tablename).to_html()
        except:
            ans = "SQL에러"
        finally:
            if(ans ==True):
                context['answer'] ="정답입니다"
            elif(ans == False):
                context['answer'] ="실패입니다"
            else:
                context['answer'] =ans
        
    return render(request, 'app/test_1.html', context)


def test_submit(request, classid, quizid, problemid):
    context = {}
    context['class'] = Class.objects.get(pk=classid)
    context['quiz'] = Quiz.objects.get(pk=quizid)
    prob = problem.objects.get(pk=problemid)
    context['sql'] = ""
    context['print'] = None
    ans = None
    if request.method =="POST":
        context['sql'] = submit_sql = request.POST.get("code")
        auto_sql = problem.objects.get(pk=problemid).sql;
        auto_df = sqlToDataFrame(auto_sql, True, context['quiz'].tablename)
        
        submit_sql = textareaToStr(submit_sql)
        try:
            submit_df = sqlToDataFrame(submit_sql, True, context['quiz'].tablename)
            ans = compare_submit(submit_df, auto_df)
            context['table'] = sqlToDataFrame(submit_sql, False, context['quiz'].tablename).head(3).to_html()
        except:
            ans = False
        finally:
            if(ans ==True):
                form = submit.objects.create(is_pass=True, classid=context['class'], problemid = prob, quizid = context['quiz'], studentid= request.user)    
                form.save()
            else:
                form = submit.objects.create(is_pass=False, classid=context['class'], problemid = prob, quizid = context['quiz'], studentid= request.user)    
                print(form)
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