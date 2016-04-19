from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.testpage,name="Test Page"),
    url(r'^login$',views.login,name='Faculty Login'),
    url(r'^faculty_portal$',views.faculty_portal,name='Faculty Portal'),
    url(r'^logout$',views.logout,name='Logout'),
    url(r'^createCodeTest$',views.createCodeTest,name='Create Code Test'),
    url(r'^createCodeTestv2',views.createCodeTestv2,name='Create Code Test version 2'),
    url(r'^finish_code_test',views.finishCodeTest,name='Finish Creating a code test'),
    url(r'^discard_code_test',views.discardCodeTest,name='Discard a partially created code test'),
    url(r'^debugCodeTest$',views.debugCodeTest,name='Debug Code Tests'), # Debug, Remove in final
]