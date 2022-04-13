from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'Responsibility']
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields=['username',"password" ,'email']