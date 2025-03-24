from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("reviews App is working!")
from django.shortcuts import render

def review_list(request):
    return render(request, 'reviews/review_list.html')

