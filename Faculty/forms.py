from django import forms
from django.forms import Form


class CodeQuestionForm(Form):
    question = forms.CharField(widget=forms.Textarea, label='Question')
    t1_input = forms.CharField(widget=forms.Textarea, label='Input')
    t2_input = forms.CharField(widget=forms.Textarea, label='Input')
    t3_input = forms.CharField(widget=forms.Textarea, label='Input')
    t1_output = forms.CharField(widget=forms.Textarea, label='Output')
    t2_output = forms.CharField(widget=forms.Textarea, label='Output')
    t3_output = forms.CharField(widget=forms.Textarea, label='Output')


class CodeQuestionFormV2(Form):
    question = forms.CharField(widget=forms.Textarea, label='Question')
    visible_test_case_input = forms.CharField(widget=forms.Textarea, label='Input')
    visible_test_case_output = forms.CharField(widget=forms.Textarea, label='Ouput')
    hidden_test_case_input = forms.CharField(widget=forms.Textarea, label='Input')
    hidden_test_case_output = forms.CharField(widget=forms.Textarea, label='Output')
    max_exec_time = forms.IntegerField(label='Max Execution Time', initial=60)