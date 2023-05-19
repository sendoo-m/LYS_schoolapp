from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'date_of_enrollment', 'national_id', 'department')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
