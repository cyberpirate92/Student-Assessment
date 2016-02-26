from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Student.forms import LoginForm
from .models import FacultyLogin

# Create your views here.


def testpage(request):
    return HttpResponse("<h2> Faculty Test Page <h2>")


def login(request):
    #  If already logged in, redirect user to his/her portal
    if request.session.__contains__('username'):
        return HttpResponseRedirect('faculty_portal')
    # else, login or serve the login form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            faculty = FacultyLogin()
            faculty.username = form.cleaned_data['username']
            faculty.password = form.cleaned_data['password']
            if FacultyLogin.objects.filter(username=faculty.username,password=faculty.password).exists():
                request.session.create()
                request.session['username'] = faculty.username
                return HttpResponseRedirect('faculty_portal')
            else:
                form = LoginForm(request.POST)
    else:
        form = LoginForm()
    template_data = {"title":"Faculty Login","form_action":"login","form":form}
    return render(request,'login_generic.html',template_data)


def faculty_portal(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('login')
    else:
        username = request.session['username']
        template_data = {'data':'Welcome to your portal!','username':username}
        return render(request,'faculty_portal.html',template_data)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')