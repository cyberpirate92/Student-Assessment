from django import forms
from django.forms import Form


class LoginForm(Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=255,widget=forms.PasswordInput)