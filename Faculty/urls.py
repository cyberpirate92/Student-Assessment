from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.testpage,name="Test Page"),
    url(r'^login$',views.login,name='Faculty Login'),
    url(r'^faculty_portal$',views.faculty_portal,name='Faculty Portal'),
    url(r'^logout$',views.logout,name='Logout'),
]