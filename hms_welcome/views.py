from operator import delitem
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import csv
# Create your views here.
def say_hello(request):
    return render(request, 'home.html',{'name': 'Neeraj'})

def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    res = val1 + val2
    return render(request, "result.html", {'result':res})

def login(request):
    return render(request, 'login.html',{'name': 'Neeraj'})

def reg(request):
    return render(request, 'register.html')

def register(request):
    name = request.POST['name']
    email = request.POST['email']
    uname = request.POST['uname']
    passw = request.POST['pass']
    passag = request.POST['passag']

    if(passw != passag):
        return render(request, 'register.html',{'err': "Passwords do not match. Please enter again."})
    else:
        details = [name,email,uname,passw]
        with open("data.csv","a") as csv_file:
            writer = csv.writer(csv_file,delimiter=',')
            writer.writerow(details)
        return render(request, 'result.html', {'result': "User successfully registered."})

def login_user(request):
    uname = request.POST['uname']
    passw = request.POST['pass']
    u1 = "nsreedh3"
    p1 = "123456"
    res = ""
    if (uname == u1) and (passw == p1):
        res = "Login successful."
    else:
        res = "Login failed. Wrong username or password."
    
    return render(request, "result.html", {'result': res})