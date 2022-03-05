from operator import delitem
from django.shortcuts import render
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
        return render(request, 'login.html',{'name': 'Neeraj'})
    return render(request, 'register.html')

# def login_user(request):
#     uname = request.POST['uname']
#     passw = request.POST['pass']
#     with open('data.csv','r') as f:
#         flag = -1
#         reader = csv.reader(f,delimiter = ',')
#         for i, line in enumerate(reader):
#             if len(line) == 0:
#                 continue
#             if line[2] == uname:
#                 flag = 0
#                 break
        
#         if flag == -1:
#             return render(request,'login.html',{'err': "Wrong username or password."})
#         else:
#             if line[3] == passw:
#                 return render(request,'result.html',{'result': 'login successful'})
#             else:
#                 return render(request,'login.html',{'err': "Wrong username or password"})