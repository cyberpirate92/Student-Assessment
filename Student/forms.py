from django import forms
from django.forms import Form


languages = [(1,"python")]


class LoginForm(Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=255,widget=forms.PasswordInput)


class CodeSubmissionForm(Form):
    language = forms.ChoiceField(choices=languages,label='Language')
    code = forms.CharField(widget=forms.Textarea,label='Code')