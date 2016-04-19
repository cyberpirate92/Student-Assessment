from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Student.forms import LoginForm
from Faculty.forms import CodeQuestionForm, CodeQuestionFormV2
from .models import FacultyLogin, TestInfo, CodeQuestion, CodeQuestionV2
from . import utils
import random

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
            if FacultyLogin.objects.filter(username=faculty.username, password=faculty.password).exists():
                request.session.create()
                request.session['username'] = faculty.username
                return HttpResponseRedirect('faculty_portal')
            else:
                form = LoginForm(request.POST)
    else:
        form = LoginForm()
    template_data = {"title" : "Faculty Login","form_action" : "login","form" : form}
    return render(request,'login_generic.html', template_data)


def faculty_portal(request):
    if not request.session.__contains__('username'):
        return HttpResponseRedirect('login')
    else:
        username = request.session['username']
        code_tests = displayAllCodeTests(username)
        template_data = {'data':'Welcome to your portal!','username':username,'code_tests':code_tests}
        return render(request,'faculty_portal.html',template_data)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')


def createCodeTest(request):
    request.session['error'] = request.method
    if request.method == 'POST':
        if request.session.__contains__("username") and request.session.__contains__("TEST_ID") and request.session.__contains__("CURRENT_QUESTION"):
            form = CodeQuestionForm(request.POST)
            if form.is_valid():
                codeQuestion = CodeQuestion()
                codeQuestion.question = form.cleaned_data['question']
                codeQuestion.testcase1_input = form.cleaned_data['t1_input']
                codeQuestion.testcase1_output = form.cleaned_data['t1_output']
                codeQuestion.testcase2_input = form.cleaned_data['t2_input']
                codeQuestion.testcase2_output = form.cleaned_data['t2_output']
                codeQuestion.testcase3_input = form.cleaned_data['t3_input']
                codeQuestion.testcase3_output = form.cleaned_data['t3_output']
                codeQuestion.test_id_id = request.session["TEST_ID"]
                codeQuestion.question_number = request.session['CURRENT_QUESTION']
                codeQuestion.save()
                request.session['CURRENT_QUESTION'] = int(request.session['CURRENT_QUESTION']) + 1
            else:
                return createCodeQuestion_GET(request,"Invalid form data submitted")
            return createCodeQuestion_GET(request)

    else:
        if request.session.__contains__("username"):
            if not ( request.session.__contains__("TEST_ID") and request.session.__contains__("CURRENT_QUESTION") ):
                test_name = "Unnamed Test"
                test_id = 0
                while True:
                    test_id = random.randint(1000,99999)
                    if len(TestInfo.objects.filter(test_id=test_id)) == 0:
                        break
                new_test = TestInfo(test_name=test_name,test_id=test_id,faculty_id_id=request.session['username'])
                new_test.save()
                request.session["TEST_ID"] = test_id
                request.session["CURRENT_QUESTION"] = 1
                request.session["TEST_NAME"] = test_name
            return createCodeQuestion_GET(request)

        else:
            return HttpResponseRedirect("login")


# The below function is not an actual view, but more of a proxy ( a helper method, created for reuse)


def createCodeQuestion_GET(request,errors=None):
    form = CodeQuestionForm()
    question_number = request.session["CURRENT_QUESTION"]
    test_id = request.session["TEST_ID"]
    question_nav = getQuestionNavTable(question_number,test_id)
    template_data = dict()
    template_data['username'] = request.session['username']
    template_data['test_name'] = request.session["TEST_NAME"]
    template_data['test_id'] = request.session["TEST_ID"]
    template_data['question_nav_table'] = question_nav
    template_data['form'] = form
    if errors is None:
        template_data['error'] = ""
    else:
        template_data["error"] = errors
    return render(request,'faculty_create_code_test.html',template_data)


# The below function is NOT a View, it's a utility function that returns the HTML for question navigation table
# This function might be shifted to a file util.py later as the need arises
# The urls for each question follow the following format/pattern : viewCodeQuestion/<test-id>/<question-number>

def getQuestionNavTable(number,test_id):
    base_url = 'viewCodeQuestion/'+str(test_id)+'/'
    html = '<tr>'
    for i in range(number):
        current_url = base_url + str(i)
        html += "<td><a href='"+current_url+"'>"+str(i+1)+"</a></td>"
        if i != 0 and (i+1)%5 == 0:
            html += "</tr><tr>"
    html+="</tr>"
    return html


def finishCodeTest(request):
    if request.session.__contains__("username"):
        clearCodeTestSession(request)
        return HttpResponseRedirect('faculty_portal')
    else:
        return HttpResponseRedirect("login")

# The below method is called when a test needs to be discarded

def discardCodeTest(request):
    if request.session.__contains__("username"):
        if request.session.__contains__("TEST_ID"):
            test_id = request.session['TEST_ID']
            TestInfo.objects.filter(test_id=test_id).delete()
            clearCodeTestSession(request)
        return HttpResponseRedirect('faculty_portal')
    else:
        return HttpResponseRedirect("login")

# The below method is NOT a view and is used to clear the session variables after a code test has been created


def clearCodeTestSession(request):
    username = ""
    if request.session.__contains__("username"):
        username = request.session['username']
    request.session.clear()
    request.session['username'] = username


# NOT a view
def displayAllCodeTests(username):
    html = "<table class='tests_display'><tr><th> Test ID </th> <th> Test Name </th> <th> Date Created </th> </tr>"
    if FacultyLogin.objects.filter(username=username).exists():
        for test in TestInfo.objects.filter(faculty_id_id=username):
            date_string = utils.getDateTimeString(test.test_creation_date)
            html += "<tr><td>"+str(test.test_id)+"</td><td>"+test.test_name+"</td><td>"+date_string+"</td></tr>"
        html += "</table>"
        return html
    else:
        return

# This is a temporary view for debugging,


def debugCodeTest(request):
    html = getQuestionNavTable(6)
    template_data = dict()
    template_data['username'] = 'ram'
    template_data['test_name'] = 'Python Basics'
    template_data['test_id'] = '119982'
    template_data['question_nav_table'] = html
    return render(request,'faculty_create_code_test.html',template_data)


def createCodeTestv2(request):
    if request.method == 'POST':
        if request.session.__contains__("username") and request.session.__contains__("TEST_ID") and request.session.__contains__("CURRENT_QUESTION"):
            form = CodeQuestionFormV2(request.POST)
            if form.is_valid():
                codeQuestion = CodeQuestionV2()
                codeQuestion.question = form.cleaned_data['question']
                codeQuestion.visible_test_case_input = form.cleaned_data['visible_test_case_input']
                codeQuestion.visible_test_case_output = form.cleaned_data['visible_test_case_output']
                codeQuestion.hidden_test_case_input = form.cleaned_data['hidden_test_case_input']
                codeQuestion.hidden_test_case_output = form.cleaned_data['hidden_test_case_output']
                codeQuestion.test_id_id = request.session["TEST_ID"]
                codeQuestion.question_number = request.session['CURRENT_QUESTION']
                codeQuestion.max_exec_time = form.cleaned_data['max_exec_time']
                codeQuestion.save()
                request.session['CURRENT_QUESTION'] = int(request.session['CURRENT_QUESTION']) + 1
            else:
                return createCodeQuestionv2_GET(request,"Invalid form data submitted")
            return createCodeQuestionv2_GET(request)
    else:
        if request.session.__contains__("username"):
            if not ( request.session.__contains__("TEST_ID") and request.session.__contains__("CURRENT_QUESTION") ):
                test_name = "Unnamed Test"
                test_id = 0
                while True:
                    test_id = random.randint(1000,99999)
                    if len(TestInfo.objects.filter(test_id=test_id)) == 0:
                        break
                new_test = TestInfo(test_name=test_name,test_id=test_id,faculty_id_id=request.session['username'])
                new_test.save()
                request.session["TEST_ID"] = test_id
                request.session["CURRENT_QUESTION"] = 1
                request.session["TEST_NAME"] = test_name
            return createCodeQuestionv2_GET(request)

        else:
            return HttpResponseRedirect("login")
    pass


def createCodeQuestionv2_GET(request,errors=None):
    form = CodeQuestionFormV2()
    question_number = request.session["CURRENT_QUESTION"]
    test_id = request.session["TEST_ID"]
    question_nav = getQuestionNavTable(question_number,test_id)
    template_data = dict()
    template_data['username'] = request.session['username']
    template_data['test_name'] = request.session["TEST_NAME"]
    template_data['test_id'] = request.session["TEST_ID"]
    template_data['question_nav_table'] = question_nav
    template_data['form'] = form
    if errors is None:
        template_data['error'] = ""
    else:
        template_data["error"] = errors
    return render(request,'faculty_create_code_test_v2.html',template_data)

