from django.forms import GenericIPAddressField
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.core import serializers

# Create your views here.


def login(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username=name, password=password)
        # grp = request.user.groups.all()[0].name
        try:
            if user is not None:
                auth_login(request, user)
                print('Logged in successfully !!')
                grp = request.user.groups.all()[0].name
                print(grp)
                if grp == 'Patient':
                    return render(request, 'patient_home.html')
                elif grp == 'lab_staff':
                    return render(request, 'labstaff_home.html')
            else:
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
        # print(fname,lname,gender,phone,address,dob,bg)
        try:
            if password == repeatpassword:
                Patient.objects.create(first_name=fname, last_name=lname, email_id=email, gender=gender,
                                       phone_number=phone, address=address, birth_date=dob, blood_group=bg)
                print('Done')
                user = User.objects.create_user(name, email, password)
                patient_group = Group.objects.get(name='Patient')
                patient_group.user_set.add(user)
                user.save()
                return redirect(login)
        except Exception as e:
            print('Exception occured')  # Add the error view redirection here
    return render(request, 'register.html')


def patient_profile(request):
    print(request.user.email)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Patient.objects.all().filter(email_id=request.user.email)
        data = {'patients': patients}
        return render(request, 'patient_profile.html', data)


def patient_prescription(request):
    print(request.user.email)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Prescription.objects.filter(
            patient_email_id=request.user.email)
        data = {'patients': patients}
        return render(request, 'patient_prescription.html', data)


def patient_make_appointment(request):
    if request.method == 'POST':
        doctor = request.POST['doctor']
        doa = request.POST['doa']
        toa = request.POST['toa']
        reason = request.POST['reason']
        try:
            Appointment.objects.create(patient_email=request.user.email, doctor_name=doctor,
                                       app_date=doa, app_time=toa, reason=reason, status='Pending')
        except Exception as e:
            print('Exception occured')
        return render(request, 'patient_make_appointment.html')
    elif request.method == 'GET':
        return render(request, 'patient_make_appointment.html')


def patient_view_appointments(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        appointments = Appointment.objects.filter(
            patient_email=request.user.email)
        d = {'appointments': appointments}
        return render(request, 'patient_view_appointments.html', d)


def patient_view_diagnosis(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        diagnosis = Diagnosis.objects.filter(
            patient_email_id=request.user.email)
        d = {'diagnosis': diagnosis}
        return render(request, 'patient_diagnosis.html', d)


def patient_view_testreport(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        reports = Report.objects.filter(patient_email_id=request.user.email)
        d = {'reports': reports}
        return render(request, 'patient_testreport.html', d)


def labstaff_create_report(request):    
    if request.method == 'POST':
        patient = request.POST['patient']
        testdate = request.POST['testdate']
        testtime = request.POST['testtime']
        dob = request.POST['dob']
        pemail = request.POST['pemail']
        age = request.POST['age']
        gender = request.POST['gender']
        testname = request.POST['testname']
        testresult = request.POST['testresult']
        comments = request.POST['comments']
        doctor = request.POST['doctor']

        try:
            Report.objects.create(patient_first_name=patient,
                                  test_date=testdate,
                                  test_time=testtime,
                                  birthdate=dob,
                                  patient_email_id=pemail,
                                  age=age,
                                  gender=gender,
                                  test_name=testname,
                                  test_result=testresult,
                                  comments=comments,
                                  reference_doctor=doctor)

        except Exception as e:
            print('Exception occured', e)
        return render(request, 'labstaff_report.html')
    elif request.method == 'GET':
        return render(request, 'labstaff_report.html')


def labstaff_view_reports(request):
    print(request.user.groups.all())
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff':
        reports = Report.objects.all()
        d = {'reports': reports}
        return render(request, 'labstaff_reportsgrid.html', d)


def labstaff_delete_report(request, rid):
    if not request.user.is_active:
        return redirect('loginpage')
    report = Report.objects.get(id=rid)
    report.delete()
    return redirect(labstaff_view_reports)


def labstaff_update_report(request, rid):
    p = Report.objects.all().filter(id=rid).values()
    data = [entry for entry in p]
    data={'data':data}
    if request.method == 'POST':
        patient = request.POST['patient']
        testdate = request.POST['testdate']
        testtime = request.POST['testtime']
        dob = request.POST['dob']
        pemail = request.POST['pemail']
        age = request.POST['age']
        gender = request.POST['gender']
        testname = request.POST['testname']
        testresult = request.POST['testresult']
        comments = request.POST['comments']
        doctor = request.POST['doctor']

        try:
            Report.objects.filter(id=rid).update(patient_first_name=patient,
                                                test_date=testdate,
                                                test_time=testtime,
                                                birthdate=dob,
                                                patient_email_id=pemail,
                                                age=age,
                                                gender=gender,
                                                test_name=testname,
                                                test_result=testresult,
                                                comments=comments,
                                                reference_doctor=doctor)
    
        except Exception as e:
            print('Exception occured', e)

    return render(request, 'labstaff_report.html', data)
