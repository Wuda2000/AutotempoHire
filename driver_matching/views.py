from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Driver Matching App is working!")
