from enum import unique
from django.db import models
from account.models import CustomUser as User
# Create your models here.
class Class(models.Model):
    classname = models.CharField(max_length = 30, null=True, unique=True, default='')
    profid = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.classname

class Quiz(models.Model):
    quizname=models.CharField(max_length=30)
    classid = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    profid=models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)
    tablename = models.CharField(max_length=40)
    sqlkeyword = models.CharField(max_length=40)
    problemnum = models.IntegerField()
    

class RegClass(models.Model):
    userid=models.ForeignKey(User, on_delete=models.CASCADE)
    classid = models.ForeignKey(Class, on_delete=models.CASCADE) 
    date = models.DateTimeField(null=True)

class Score(models.Model):
    studentid=models.ForeignKey(User, on_delete=models.CASCADE)
    classid=models.ForeignKey(Class, on_delete=models.CASCADE)
    quizid=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    Score=models.FloatField(null=False, default=0)

class table_school(models.Model):
    name = models.CharField(max_length=100)#학교이름
    studentnum = models.IntegerField() #학생수
    classnum = models.IntegerField() #학급수
    tel = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    
    