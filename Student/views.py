from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .forms import LoginForm,CodeSubmissionForm
from . import CompilerUtils
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
    else:
        if not test_id_exists(test_id):
            return Http404
        else:
            test_obj = TestInfo.objects.filter(test_id=test_id)
            num_questions = len(CodeQuestionV2.objects.filter(test_id_id=test_id))
            template_data = {"title": test_obj[0].test_name, "test": test_obj[0], "num_questions": num_questions}
            request.session['current_question'] = 1;
            return render(request,'test_initiate.html',template_data)


def user_is_logged_in(request):
    if request.session.__contains__('username'):
        return True
    return False


def test_id_exists(test_id):
    return len(TestInfo.objects.filter(test_id=test_id)) != 0


def question_number_exists(test_id,question_number):
    if test_id_exists(test_id):
        return len(CodeQuestionV2.objects.filter(test_id_id=test_id,question_number=question_number)) != 0
    else:
        return False


def question_view(request,test_id,question_number):
    if not test_id_exists(test_id):
        return Http404
    else:
        if not question_number_exists(test_id,question_number):
            return Http404
        else:
            template_data = dict()
            if request.method == 'POST':
                form = CodeSubmissionForm(request.POST)
                if form.is_valid():
                    language = CompilerUtils.Language(int(form.cleaned_data['language']))
                    code = form.cleaned_data['code']
                    compiler = CompilerUtils.Compiler()
                    compiler.set_code(code)
                    compiler.set_language(language)
                    question_obj = CodeQuestionV2.objects.filter(test_id_id=test_id,question_number=question_number)[0]
                    template_code = question_obj.template_code
                    if template_code is not None and len(template_code) != 0:
                        compiler.set_template(template_code)
                    visible_input = question_obj.visible_test_case_input
                    visible_output = question_obj.visible_test_case_output
                    hidden_input = question_obj.hidden_test_case_input
                    hidden_output = question_obj.hidden_test_case_output
                    test_cases = CompilerUtils.generate_test_cases(visible_input,visible_output)
                    hidden_test_cases = CompilerUtils.generate_test_cases(hidden_input,hidden_output)
                    for tc in hidden_test_cases:
                        tc.is_hidden_test_case = True
                    test_cases.extend(hidden_test_cases)
                    compiler.add_test_cases(test_cases)
                    compiler.execute()
                    compiler.delete_code_file()
                    status = compiler.exec_status
                    print("[*] Status : " + status.name)
                    template_data['status'] = status
                    template_data['percentage'] = compiler.get_overall_pass_percentage()
                    if status == CompilerUtils.ExecutionStatus.ACC:
                        request.session['current_question'] = int(request.session['current_question']) + 1
                else:
                    template_data['error'] = "Invalid submission!"

                # TODO: Update session such that it provides the next question when the answer is accepted

            form = CodeSubmissionForm()
            username = request.session['username']
            question_obj = CodeQuestionV2.objects.filter(test_id_id=test_id,question_number=question_number)[0]
            test_obj = TestInfo.objects.filter(test_id = test_id)[0]
            test_cases = CompilerUtils.generate_test_cases(question_obj.visible_test_case_input, question_obj.visible_test_case_output)
            template_data['username'] = username
            template_data['title'] = test_obj.test_name
            template_data['question'] = question_obj
            template_data['test_cases'] = test_cases
            template_data['form'] = form
            return render(request,'code_questions.html',template_data)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')