from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def say_hello(request):
    return HttpResponse("Welcome to the Hospital Management System.\n Done by Group 6. We are just getting started.")