from django.db import models
import datetime
from django.utils import timezone

class FacultyLogin(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=255)


# In natural language, A test 'test_id' with an optional name 'test_name' has been created by faculty 'faculty_id'

class TestInfo(models.Model):
    test_name = models.CharField(max_length=30,null=True)
    test_id = models.IntegerField(primary_key=True)
    test_creation_date = models.DateTimeField(default=timezone.now())
    test_last_edited = models.DateTimeField(default=timezone.now())
    faculty_id = models.ForeignKey(FacultyLogin,on_delete=models.CASCADE)


class StudentLogin(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=255)


# django creates a id field which is auto incremented, that will be used for question_id


class MCQQuestion(models.Model):
    question = models.TextField()
    question_number = models.IntegerField(default=0)
    choice1 = models.CharField(max_length=300)
    choice2 = models.CharField(max_length=300)
    choice3 = models.CharField(max_length=300)
    choice4 = models.CharField(max_length=300)
    correctAnswer = models.IntegerField(default=0)
    test_id = models.ForeignKey(TestInfo,on_delete=models.CASCADE)

# django creates a id field which is auto incremented, that will be used for question_id


class CodeQuestion(models.Model):
    question = models.TextField()
    question_number = models.IntegerField(default=0)
    testcase1_input = models.TextField()
    testcase2_input = models.TextField()
    testcase3_input = models.TextField()
    testcase1_output = models.TextField()
    testcase2_output = models.TextField()
    testcase3_output = models.TextField()
    test_id = models.ForeignKey(TestInfo,on_delete=models.CASCADE)

class CodeQuestionV2(models.Model):
    question = models.TextField()
    question_number = models.IntegerField(default=0)
    visible_test_case_input = models.TextField()
    visible_test_case_output = models.TextField()
    hidden_test_case_input = models.TextField()
    hidden_test_case_output = models.TextField()
    max_exec_time = models.IntegerField()
    test_id = models.ForeignKey(TestInfo,on_delete=models.CASCADE)

# In the below model, the question id could also be declared to be a foreign key referencing the MCQQuestions Model,
# but test_id is declared as a foreign key and is enough, because when test_id is removed,
# so are all the question ids related to test_id
# It is also important to note that the more the number of foreign keys, more the time a DELETE query takes
#
# In natural language, A student 'username' has selected the answer 'selected_ans' for the question 'question_id' in the
# test 'test_id'

class MCQTestAnswers(models.Model):
    test_id = models.ForeignKey(TestInfo,on_delete=models.CASCADE)
    username = models.ForeignKey(StudentLogin,on_delete=models.CASCADE)
    selected_ans = models.IntegerField(default=1)
    question_id = models.IntegerField(default=0)

# The following model is used for identifying which which faculty is linked with what subjects
# The faculty username is a foreign key from the FacultyLogin table, while the subject is just a string
#
# In natural language, A faculty 'username' has subject 'subject' in slot 'slot'

class Faculty_Subjects(models.Model):
    subject = models.CharField(max_length=10)
    slot = models.CharField(max_length=15)
    username = models.ForeignKey(FacultyLogin,on_delete=models.CASCADE)


# The following model is used to assign students to subjects, please note that subject is just a string, not a
# foreign key reference
# .
# In natural language, a student 'student_username' has registered under faculty 'faculty_username'
# for subject 'subject'


class Student_Subject(models.Model):
    student_username = models.ForeignKey(StudentLogin,on_delete=models.CASCADE)
    faculty_username = models.ForeignKey(FacultyLogin,on_delete=models.CASCADE)
    subject = models.CharField(max_length=15)



