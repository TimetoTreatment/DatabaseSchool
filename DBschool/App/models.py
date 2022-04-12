from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#TABLE : 사용자목로(Users)
#PROBLEM
#참여수업목록은 여기있으면 안될것 같음. ID로 참여수업을 조회하는게 나음
#완료

#TABLE : 수업목록
#PROBLEM
#학생 목록, 퀴즈 목록은 제외
class Class(models.Model):
    ID = models.BigAutoField(auto_created=True, primary_key=True) 
    Name = models.CharField(max_length = 30)
    Teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class RegClass(models.Model):
    UserID=models.ForeignKey(User, on_delete=models.CASCADE)
    ClassID=models.ForeignKey(Class, on_delete=models.CASCADE)

#TBALE : 퀴즈 목록
#점수는 따로 함수형식으로 만들어야 될듯함
class Quiz(models.Model):
    ID= models.BigAutoField(auto_created=True, primary_key=True)
    Name=models.CharField(max_length=30)
    StartDateTime=models.DateTimeField()
    EndDateTime=models.DateTimeField()
    ClassID=models.ForeignKey(Class, on_delete=models.CASCADE) 


class Query(models.Model):
    ID=models.BigAutoField(auto_created=True, primary_key=True)
    Difficulty=models.FloatField(default=0.0)
    Query=models.TextField()

class Problem(models.Model):
    ID=models.BigAutoField(auto_created=True, primary_key=True)
    Query=models.ForeignKey(Query, on_delete=models.CASCADE)
    Statement=models.TextField()
    

class Submit(models.Model):
    ID=models.BigAutoField(auto_created=True, primary_key=True)
    UserName=models.ForeignKey(User, on_delete=models.CASCADE)
    ProblemID=models.ForeignKey(Problem, on_delete=models.CASCADE)
    AcceptRate=models.FloatField(default=0.0, null=False)

#TABLE : 점수
#PRIMAY KEY는 필요없음
class Score(models.Model):
    StudentID=models.ForeignKey(User, on_delete=models.CASCADE)
    ProblemID=models.ForeignKey(Problem, on_delete=models.CASCADE)
    Score=models.IntegerField(null=False, default=0)
