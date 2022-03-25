from django.forms import GenericIPAddressField
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.core import serializers
import pyotp
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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
                elif grp == 'hospital_staff':
                    return render(request, 'hospitalstaff_home.html')
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
                grp = request.user.groups.all()[0].name
                if grp == 'hospital_staff':
                    return redirect(hospitalstaff_view_patients)
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
    elif grp == 'hospital_staff':
        appointments = Appointment.objects.all()
        d = {'appointments': appointments}
        return render(request, 'hospitalstaff_view_appointments.html',d)

def patient_view_diagnosis(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        diagnosis = Diagnosis.objects.filter(
            patient_email_id=request.user.email)
        d = {'diagnosis': diagnosis}
        return render(request, 'patient_diagnosis.html', d)

def patient_view_tests(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        tests = Test.objects.all()
        d = {'tests':tests}
        return render(request, 'patient_view_tests.html',d)

def patient_request_test(request, id):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patient = Patient.objects.filter(email_id=request.user.email)
        test = Test.objects.filter(id=id)
        d = {'patient':patient, 'test':test}
        if request.method == 'POST':
            date = request.POST['doa']
            time = request.POST['toa']
            Test_Request.objects.create(patient_first_name=patient[0].first_name,
            patient_last_name=patient[0].last_name,
            test_date = date, test_time = time,
            birthdate=patient[0].birth_date,
            patient_email_id=request.user.email,
            gender=patient[0].gender,
            test_name=test[0].test_name,
            test_status='Requested')
            return redirect(patient_view_tests)
        return render(request, 'patient_make_test_request.html', d)


def patient_view_testreport(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        reports = Report.objects.filter(patient_email_id=request.user.email)
        d = {'reports': reports}
        return render(request, 'patient_testreport.html', d)


#Replace the below view's name with "otp"

# echo "export SENDGRID_API_KEY='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'" > sendgrid.env
# echo "sendgrid.env" >> .gitignore
# source ./sendgrid.env
def patient_view_transactions(request):
    totp = pyotp.TOTP("base32topsecret7", digits=6, interval=120)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        #totp = pyotp.TOTP(SECRET_KEY, digest=hashlib.sha256, digits=6, interval=30)
        if request.method == 'POST':
            otp = request.POST['otp']
            if otp == str(totp.now()) :
                return redirect(patient_view_transactions)
            else :
                # print(totp.now())
                print('Failure')
                return render(request, 'otp.html')
        elif request.method == 'GET':
            print(totp.now())
            message = Mail(
                from_email='sohamjoshi92@gmail.com',
                to_emails='sohamjoshi92@gmail.com',
                subject='CSE-545-HMS-Group6 OTP',
                html_content='<strong>This otp will expire in 120 seconds : ' + str(totp.now()) + '</strong>')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.client.mail.send.post(request_body=message.get())
                # print(response.status_code)
                # print(response.body)
                # print(response.headers)
            except Exception as e:
                print(e)
            return render(request, 'otp.html')


#-----------------------Lab Staff Views start here ---------------------------------
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

def test_request(request):
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff':
        requests = Test_Request.objects.all()
        d = {'requests' : requests}
        return render(request, 'labstaff_view_test_request.html', d)
    elif grp == 'Patient':
        requests = Test_Request.objects.filter(patient_email_id=request.user.email)
        d = {'requests' : requests}
        return render(request, 'patient_view_test_request.html', d)

def labstaff_update_request(request, id, action):
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff':
        if action == 'approve':
            Test_Request.objects.filter(id=id).update(test_status='Approved')
        elif action == 'deny':
            Test_Request.objects.filter(id=id).update(test_status='Denied')
        return redirect(test_request)
    elif grp == 'Patient':
        if action == 'request':
            Test_Request.objects.filter(id=id).update(test_status='Report Requested')
        return redirect(test_request)


#-----------------------Hospital Staff Views start here ---------------------------------
def hospitalstaff_view_patients(request):
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        patients = Patient.objects.all()
        d = {'patients': patients}
        return render(request, 'hospitalstaff_view_patients.html', d)

def hospitalstaff_view_patientdata(request, email):
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        diagnosis = Diagnosis.objects.filter(patient_email_id=email)
        prescriptions = Prescription.objects.filter(patient_email_id=email)
        reports = Report.objects.filter(patient_email_id=email)

        d = {'diagnosis':diagnosis, 'prescriptions':prescriptions, 'reports':reports}
        return render(request, 'hospitalstaff_patient_data.html', d)
    elif grp == 'lab_staff':
        diagnosis = Diagnosis.objects.filter(patient_email_id=email)
        d = {'diagnosis':diagnosis}
        return render(request, 'labstaff_patient_data.html', d)

def hospitalstaff_update_appointment(request, id, action):
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        if action == 'approve':
            Appointment.objects.filter(id=id).update(status='Approved')
        elif action == 'deny':
            Appointment.objects.filter(id=id).update(status='Denied')
        return redirect(patient_view_appointments)
