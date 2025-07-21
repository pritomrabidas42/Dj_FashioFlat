from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    fullname = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fullname', 'phone_number', 'password1', 'password2')

    