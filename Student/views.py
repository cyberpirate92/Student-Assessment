from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def testpage(request):
    return HttpResponse("<h2> Faculty Test Page <h2>")