from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")
