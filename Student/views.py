from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .forms import LoginForm
from Faculty.models import TestInfo,CodeQuestionV2
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
        tests = TestInfo.objects.all()
        template_data = {'username' : username,'tests':tests}
        return render(request,'student_portal.html',template_data)


# function initiate_test()
#   Check with db if the test id really exists
#   if exists,
#       check the test timings range and if the current time falls in the given range
#       if current time falls in the range,
#           Show the test meta data (number of questions, and a start button
#       else
#           Show the message that no such test exists [##]
#   else
#       Show the message that no such test exists [##]
def initiate_test(request,test_id):
    if test_id is None:
        return Http404
    if len(TestInfo.objects.filter(test_id=test_id)) == 0:
        return Http404
    else:
        test_obj = TestInfo.objects.filter(test_id=test_id)
        num_questions = len(CodeQuestionV2.objects.filter(test_id_id=test_id))
        template_data = {"title": test_obj[0].test_name, "test": test_obj[0], "num_questions": num_questions}
        return render(request,'test_initiate.html',template_data)
    pass

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')