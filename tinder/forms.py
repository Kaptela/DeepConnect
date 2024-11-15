from django.forms import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import forms, ModelForm, EmailField
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    
class SignUpForm(UserCreationForm):
    email = EmailField(max_length=200, required=False)
    usable_password = None
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'lastname', 'phone', 'date_of_birth', 'sex', 'social_orientation', 'agreeableness', 'emotional_stablility']