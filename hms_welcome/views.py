from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.

def login(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username = name, password = password)
        try:
            if user is not None:
                auth_login(request, user)
                print('Logged in successfully !!')
                return render(request, 'patient_home.html')
            else :
                print('Invalid login credentials')
        except Exception as e:
            print(e)
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect(login)

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['re-password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        dob = request.POST['dob']
        bg = request.POST['bg']
        #print(fname,lname,gender,phone,address,dob,bg)
        try :
            if password == repeatpassword:
                Patient.objects.create(first_name=fname,last_name=lname,email_id=email,gender=gender,phone_number=phone,address=address, birth_date=dob,blood_group = bg)
                print('Done')
                user = User.objects.create_user(name, email, password)
                patient_group = Group.objects.get(name='Patient')
                patient_group.user_set.add(user)
                user.save()
                return redirect(login)
        except Exception as e :
            print('Exception occured') #Add the error view redirection here
    return render(request, 'register.html')

def patient_profile(request):
    print(request.user.email)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Patient.objects.all().filter(email_id = request.user.email)
        data = { 'patients' : patients}
        return render(request, 'patient_profile.html', data)

def patient_prescription(request):
    print(request.user.email)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Prescription.objects.filter(patient_email_id = request.user.email)
        data = { 'patients' : patients}
        return render(request, 'patient_prescription.html', data)
        
def patient_make_appointment(request):
    if request.method == 'POST':
        doctor = request.POST['doctor']
        doa = request.POST['doa']
        toa = request.POST['toa']
        reason = request.POST['reason']
        try:
            Appointment.objects.create(patient_email=request.user.email,doctor_name=doctor,app_date=doa,app_time=toa,reason=reason,status='Pending')
        except Exception as e:
            print('Exception occured')
        return render(request, 'patient_make_appointment.html')
    elif request.method == 'GET':
        return render(request, 'patient_make_appointment.html')

def patient_view_appointments(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        appointments = Appointment.objects.filter(patient_email=request.user.email)
        d = {'appointments' : appointments}
        return render(request, 'patient_view_appointments.html',d)

def patient_view_diagnosis(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        diagnosis = Diagnosis.objects.filter(patient_email_id=request.user.email)
        d = {'diagnosis' : diagnosis}
        return render(request, 'patient_diagnosis.html',d)

def patient_view_testreport(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        reports = Report.objects.filter(patient_email_id=request.user.email)
        d = {'reports' : reports}
        return render(request, 'patient_testreport.html',d)
