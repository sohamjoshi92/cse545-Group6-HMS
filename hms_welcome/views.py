from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def login(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username = name, password = password)
        try:
            if user is not None:
                #login(request, user)
                print('Logged in successfully !!')
            else :
                print('Invalid login credentials')
        except Exception as e:
            print(e)
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['re-password']
        try :
            if password == repeatpassword:
                print('Done')
                user = User.objects.create_user(name, email, password)
                user.save()
                return redirect(login)
        except Exception as e :
            print('Exception occured') #Add the error view redirection here
    return render(request, 'register.html')