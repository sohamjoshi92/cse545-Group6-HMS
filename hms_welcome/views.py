from operator import delitem
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    return render(request, 'login.html',{'name': 'Neeraj'})

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['email']
        repeatpassword = request.POST['re-password']
        try :
            if password == repeatpassword:
                user = User.objects.create_user(name, email, password)
                user.save()
        except Exception as e :
            print(e)
        return redirect(login)
    return render(request, 'register.html')