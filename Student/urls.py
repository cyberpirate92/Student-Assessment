from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.testpage, name='Test Page'),
    url(r'^login$', views.login, name="Student Login"),
    url(r'^student_portal$',views.student_portal,name='Student Portal'),
    url(r'^tests/([0-9]{4,5})/',views.initiate_test,name='Initiate Test'),
    url(r'^logout$',views.logout,name='Logout'),
]