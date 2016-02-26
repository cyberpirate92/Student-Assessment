from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm
from Faculty.models import StudentLogin
# Create your views here.


def testpage(request):
    return HttpResponse("<h2> Student Test Page <h2>")


def login(request):
    #  If already logged in, redirect user to his/her portal
    if request.session.__contains__('username'):
        return HttpResponseRedirect('student_portal')
    # else, login or serve the login form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student = StudentLogin()
            student.username = form.cleaned_data['username']
            student.password = form.cleaned_data['password']
            if StudentLogin.objects.filter(username=student.username,password=student.password).exists():
                request.session.create()
                request.session['username'] = student.username
                return HttpResponseRedirect('student_portal')
            else:
                form = LoginForm(request.POST)
    else:
        form = LoginForm()
    template_data = {"title":"Student Login","form_action":"login","form":form}
    return render(request,'login_generic.html',template_data)


def student_portal(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('login')
    else:
        username = request.session['username']
        template_data = {'data':'Welcome to your portal!','username':username}
        return render(request,'student_portal.html',template_data)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')