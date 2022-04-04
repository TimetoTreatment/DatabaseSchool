from django.db import models

# Create your models here.

class User(models.Model):
    user_email = models.CharField(max_length=32, unique=True, verbose_name='유저 이메일')
    user_pw = models.CharField(max_length=128, verbose_name='유저 비밀번호')
    user_name = models.CharField(max_length=16, verbose_name='유저 이름')
    user_identity = models.BooleanField(default=True, verbose_name='유저 신분확인')
    # user_register_time = models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')
    
    def __str__(self):
        return self.user_name
    
    
    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural ='유저'