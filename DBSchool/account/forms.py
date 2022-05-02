from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'Responsibility']
