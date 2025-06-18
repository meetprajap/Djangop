from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta: #meta class define the model to be used in the form
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']
