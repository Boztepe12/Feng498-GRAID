from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def start_communation(request):
    return HttpResponse("Hello, from Django server!")
