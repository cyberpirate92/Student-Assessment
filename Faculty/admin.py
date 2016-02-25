from django.contrib import admin
from .models import FacultyLogin,StudentLogin

# Register your models here.

admin.site.register(FacultyLogin)
admin.site.register(StudentLogin)