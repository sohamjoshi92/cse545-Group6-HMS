from urllib.robotparser import RequestRate
from django.forms import GenericIPAddressField
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
import pyotp
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
# Create your views here.
logger = logging.getLogger(__name__)



def login(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username=name, password=password)
        # grp = request.user.groups.all()[0].name
        try:
            if user is not None:
                auth_login(request, user)
                logger.info("User with user name {} succesfully logged in".format(user.username))
                grp = request.user.groups.all()[0].name
                if grp == 'Patient':
                    return render(request, 'patient_home.html')
                elif grp == 'lab_staff':
                    return render(request, 'labstaff_home.html')
                elif grp == 'hospital_staff':
                    return render(request, 'hospitalstaff_home.html')
                elif grp == 'insurance_staff':
                    return render(request, 'insurance_staff_home.html')
                elif grp == 'Doctor':
                    return render(request, 'doc_home.html')
                elif grp == 'admin':
                    return render(request, 'admin_home.html')
            else:
                if Malicious_Login.objects.filter(username=name).exists():
                    un = Malicious_Login.objects.get(username=name)
                    fla = un.failed_login_attempts
                    #print(fla)
                    un.failed_login_attempts = fla + 1
                    if fla == 2:
                        un.failed_login_attempts = 0
                        un.save()
                        return redirect(malicious_login_otp)
                    un.save()
                else:
                    Malicious_Login.objects.create(
                        username=name, failed_login_attempts=1)
        except Exception as e:
            logger.error(e)
    return render(request, 'login.html')


def logout(request):
    logger.info("{} succesfully logged out".format(request.user.username))
    auth_logout(request)
    return redirect(login)

def changepassword(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        confirmpassword = request.POST['cpsw']
        if password != confirmpassword:
            e = {'page': 'changepassword'}
            return render(request, 'errors.html', e)
        else:
            user = User.objects.get(username=name)
            user.set_password(confirmpassword)
            user.save()
            logger.info("{} changed the password".format(user.username))
            return redirect(login)
    return render(request, 'changepassword.html')

#---------------------Patient Views ---------------------------------------

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
                
                user = User.objects.create_user(name, email, password)
                patient_group = Group.objects.get(name='Patient')
                patient_group.user_set.add(user)
                user.save()
                logger.info("{} successfully registered".format(user.username))
                if request.user.is_anonymous:
                    return redirect(login)
                grp = request.user.groups.all()[0].name
                if grp == 'hospital_staff':
                    return redirect(hospitalstaff_view_patients)
                else:
                    redirect(login)
                return redirect(login)
            else:
                'handle not same passwords'
        except Exception as e:
            logging.error(e)
    return render(request, 'register.html')


def patient_profile(request):
    if request.user.is_anonymous:
        return redirect(login)
    print(request.user.email)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Patient.objects.filter(email_id=request.user.email)
        print(len(patients))
        data = {'patients': patients}
        return render(request, 'patient_profile.html', data)
    else:
        ensure_groups(request, grp)
    


def patient_prescription(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        patients = Prescription.objects.filter(
            patient_email_id=request.user.email)
        data = {'patients': patients}
        return render(request, 'patient_prescription.html', data)
    else:
        ensure_groups(request, grp)


def patient_make_appointment(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient' or grp =="admin":
        if request.method == 'POST':
            doctor = request.POST['doctor']
            doa = request.POST['doa']
            toa = request.POST['toa']
            reason = request.POST['reason']

            email = request.user.email
            if grp == "admin":
                email = request.POST['email']
            try:
                Appointment.objects.create(patient_email=email, doctor_name=doctor,
                                        app_date=doa, app_time=toa, reason=reason, status='Pending')
            except Exception as e:
                print('Exception occured')
            appointments = Appointment.objects.all()
            d = {'appointments': appointments}
            return render(request, 'hospitalstaff_view_appointments.html', d)
        elif request.method == 'GET':
            return render(request, 'patient_make_appointment.html')
    else:
        ensure_groups(request, grp)

def patient_view_appointments(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        appointments = Appointment.objects.filter(
            patient_email=request.user.email)
        d = {'appointments': appointments}
        return render(request, 'patient_view_appointments.html', d)
    elif grp == 'hospital_staff' or grp == 'admin':
        appointments = Appointment.objects.all()
        d = {'appointments': appointments}
        return render(request, 'hospitalstaff_view_appointments.html',d)
    else:
        ensure_groups(request, grp)

def patient_view_diagnosis(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        diagnosis = Diagnosis.objects.filter(
            patient_email_id=request.user.email)
        d = {'diagnosis': diagnosis}
        return render(request, 'patient_diagnosis.html', d)
    else:
        ensure_groups(request, grp)

def patient_view_tests(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient' or grp == 'admin':
        tests = Test.objects.all()
        d = {'tests':tests}
        return render(request, 'patient_view_tests.html',d)
    else:
        ensure_groups(request, grp)

def patient_request_test(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient' or grp == 'admin':
        patient = Patient.objects.filter(email_id=request.user.email)
        test = Test.objects.filter(id=id)
        d = {'patient':patient, 'test':test}
        if request.method == 'POST':
            date = request.POST['doa']
            time = request.POST['toa']
            if grp == 'Patient':
                last_name = patient[0].last_name
                first_name = patient[0].first_name
                email = request.user.email
                dob = patient[0].birth_date
                gender = patient[0].gender
            elif grp == 'admin':
                last_name = request.POST['lname']
                first_name = request.POST['fname']
                email = request.POST['pid']
                dob = request.POST['dob']
                gender = request.POST['gender']
            Test_Request.objects.create(
                patient_first_name= first_name,
                patient_last_name= last_name,
                test_date = date, 
                test_time = time,
                birthdate= dob,
                patient_email_id= email,
                gender= gender,
                test_name= test[0].test_name,
                test_status='Requested')
            return redirect(patient_view_tests)
        return render(request, 'patient_make_test_request.html', d)
    else:
        ensure_groups(request, grp)


def patient_view_testreport(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        reports = Report.objects.filter(patient_email_id=request.user.email).filter(patient_visible=True)
        d = {'reports': reports}
        return render(request, 'patient_testreport.html', d)
    else:
        ensure_groups(request, grp)

def patient_request_reports(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        Report.objects.filter(patient_email_id=request.user.email).update(
            patient_visible = True
        )
        reports = Report.objects.filter(patient_email_id=request.user.email).filter(patient_visible=True)
        d = {'reports': reports}
        return render(request, 'patient_testreport.html', d)
    else:
        ensure_groups(request, grp)



def view_insurance_statements(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        statements = Insurance_Statement.objects.filter(patient_email=request.user.email, patient_first_name=request.user.first_name, patient_last_name=request.user.last_name, patient_visible=True)
        d = {'policy_statements': statements}
        return render(request, 'patient_view_statements.html', d)
    else:
        ensure_groups(request, grp)

def request_insurance_statements(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        if request.method == 'POST':
            if (request.POST['first_name'] == request.user.first_name) and (request.POST['last_name'] == request.user.last_name) and (request.POST['email'] == request.user.email):
                try:
                    Insurance_Statement.objects.filter(patient_email=request.user.email, patient_first_name=request.user.first_name, patient_last_name=request.user.last_name, patient_visible=False).update(
                        requested=True
                    )
                except Exception as e:
                    print('Exception occured', e)
            else:
                print('invalid request')
            return redirect(view_insurance_statements)
        elif request.method == 'GET':
            return render(request, 'patient_request_statement.html')
            ###################added this check later
        else:
            return redirect(view_insurance_statements)
    else:
        ensure_groups(request, grp)


#Replace the below view's name with "otp"

# echo "export SENDGRID_API_KEY='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'" > sendgrid.env
# echo "sendgrid.env" >> .gitignore
# source ./sendgrid.env
def otp(request):
    if request.user.is_anonymous:
        return redirect(login)
    totp = pyotp.TOTP("base32topsecret7", digits=6, interval=120)
    grp = request.user.groups.all()[0].name
    if grp == 'Patient':
        #totp = pyotp.TOTP(SECRET_KEY, digest=hashlib.sha256, digits=6, interval=30)
        if request.method == 'POST':
            otp = request.POST['otp']
            if otp == str(totp.now()) :
                return redirect(view_insurance_statements)
            else :
                # print(totp.now())
                d = {'error': 'OTP is wrong or might have expired.'}
                return render(request, 'otp.html', d)
        elif request.method == 'GET':
            message = Mail(
                from_email='sohamjoshi92@gmail.com',
                to_emails=request.user.email,
                subject='CSE-545-HMS-Group6 OTP',
                html_content='<strong>This otp will expire in 120 seconds : ' + str(totp.now()) + '</strong>')
            try:
                sg = SendGridAPIClient('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')
                response = sg.client.mail.send.post(request_body=message.get())
                # print(response.status_code)
                # print(response.body)
                # print(response.headers)
            except Exception as e:
                print(e)
            return render(request, 'otp.html')

 def malicious_login_otp(request):
    totp = pyotp.TOTP("base32topsecret7", digits=6, interval=120)
    # totp = pyotp.TOTP(SECRET_KEY, digest=hashlib.sha256, digits=6, interval=30)
    if request.method == 'POST':
        otp = request.POST['otp']
        if otp == str(totp.now()):
            return redirect(changepassword)
        else:
            # print(totp.now())
            d = {'error': 'OTP is wrong or might have expired.'}
            return render(request, 'otp.html', d)
    elif request.method == 'GET':
        message = Mail(
            from_email='sohamjoshi92@gmail.com',
            to_emails='riya.2398@gmail.com',
            subject='CSE-545-HMS-Group6 OTP',
            html_content='<strong>This otp will expire in 120 seconds : ' + str(totp.now()) + '</strong>')
        try:
            sg = SendGridAPIClient(
                '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')
            response = sg.client.mail.send.post(request_body=message.get())
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)
        except Exception as e:
            print(e)
        return render(request, 'otp.html')

#-----------------------Lab Staff Views start here ---------------------------------
def labstaff_create_report(request):  
    if request.user.is_anonymous:
        return redirect(login)
    print(request.user.groups.all())
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff' or grp =='admin':
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
            return redirect(labstaff_view_reports)
        elif request.method == 'GET':
            return render(request, 'labstaff_report.html')
    else:
        ensure_groups(request, grp)


def labstaff_view_reports(request):
    if request.user.is_anonymous:
        return redirect(login)
    print(request.user.groups.all())
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff' or grp == 'admin':
        reports = Report.objects.all()
        d = {'reports': reports}
        return render(request, 'labstaff_reportsgrid.html', d)
    else:
        ensure_groups(request, grp)
    


def labstaff_delete_report(request, rid):
    if request.user.is_anonymous:
        return redirect(login)
    print(request.user.groups.all())
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff' or grp =='admin':
        if not request.user.is_active:
            return redirect('loginpage')
        report = Report.objects.get(id=rid)
        report.delete()
        return redirect(labstaff_view_reports)
    else:
        ensure_groups(request, grp)


def labstaff_update_report(request, rid):
    if request.user.is_anonymous:
        return redirect(login)
    print(request.user.groups.all())
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff' or grp =='admin':
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
            return redirect(labstaff_view_reports)

        return render(request, 'labstaff_report.html', data)
    else:
        ensure_groups(request, grp)


def labstaff_view_patient_diagnosis(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff':
        diagnosis = Diagnosis.objects.all()
        d = {'diagnosis': diagnosis}
        return render(request, 'labstaff_diagnosisgrid.html', d)
    else:
        ensure_groups(request, grp)

def test_request(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'lab_staff' or grp == 'admin':
        requests = Test_Request.objects.all()
        d = {'requests' : requests}
        return render(request, 'labstaff_view_test_request.html', d)
    elif grp == 'Patient':
        requests = Test_Request.objects.filter(patient_email_id=request.user.email)
        d = {'requests' : requests}
        return render(request, 'patient_view_test_request.html', d)
    else:
        ensure_groups(request, grp)

def labstaff_update_request(request, id, action):
    if request.user.is_anonymous:
        return redirect(login)
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
    else:
        ensure_groups(request, grp)


#-----------------------Hospital Staff Views start here ---------------------------------
def hospitalstaff_view_patients(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        patients = Patient.objects.all()
        d = {'patients': patients}
        return render(request, 'hospitalstaff_view_patients.html', d)
    else:
        ensure_groups(request, grp)

def hospitalstaff_view_patientdata(request, email):
    if request.user.is_anonymous:
        return redirect(login)
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
    else:
        ensure_groups(request, grp)

def hospitalstaff_update_appointment(request, id, action):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        if action == 'approve':
            Appointment.objects.filter(id=id).update(status='Approved')
        elif action == 'deny':
            Appointment.objects.filter(id=id).update(status='Denied')
        return redirect(patient_view_appointments)
    else:
        ensure_groups(request, grp)

def create_transaction(request, email):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
        patient = Patient.objects.filter(email_id=email)[0]
        Transaction.objects.create(patient_first_name=patient.first_name, patient_last_name=patient.last_name, patient_email=email, case_number='0786', amount='20', status='Created')
        return redirect(patient_view_appointments)
    else:
        ensure_groups(request, grp)


def hospitalstaff_view_transactions(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'hospital_staff':
       transactions = Transaction.objects.all()
       d = {'transactions':transactions}
       return render(request, 'hospitalstaff_view_transactions.html',d)
    else:
        ensure_groups(request, grp)

#----------------------Insurance Staff Views start here --------------------------------


def insurance_staff_view_policies(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'insurance_staff' or grp == 'admin':
        policies = Insurance_Policy.objects.all()
        d = {'policies': policies}
        return render(request, 'insurance_staff_view_policies.html', d)
    else:
        ensure_groups(request, grp)

def insurance_staff_new_policy(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'insurance_staff' or grp == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            discount = request.POST['discount']
            try:
                Insurance_Policy.objects.create(policy_name=name,
                                    discount=discount,)
            except Exception as e:
                print('Exception occured', e)
            return redirect(insurance_staff_view_policies)
        elif request.method == 'GET':
            return render(request, 'insurance_staff_new_policy.html')
    else:
        ensure_groups(request, grp)

def insurance_staff_view_statements(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'insurance_staff':
        if request.method == 'GET':
            statements = Insurance_Statement.objects.filter(requested=True)
            d = {'policy_statements': statements}
            return render(request, 'insurance_staff_view_statements.html', d)
    if grp == 'admin':
        if request.method == 'GET':
            statements = Insurance_Statement.objects.all()
            d = {'policy_statements': statements}
            return render(request, 'insurance_staff_view_statements.html', d)
    else:
        ensure_groups(request, grp)

def insurance_staff_approve_deny_statement(request, id, action):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'insurance_staff' or grp == 'admin':
        if action == 'approve':
            Insurance_Statement.objects.filter(id=id).update(approved=True, requested=False, patient_visible=True)
        elif action == 'deny':
            Insurance_Statement.objects.filter(id=id).update(approved=False, requested=False, patient_visible=True)
        return redirect(insurance_staff_view_statements)
    else:
        ensure_groups(request, grp)

def insurance_staff_create_statement(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp == 'insurance_staff':
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            patient_email = request.POST['email']
            policy_name = request.POST['policy']
            policy_discount = request.POST['discount']
            date = request.POST['date']
            try:
                Insurance_Statement.objects.create(
                    patient_first_name=fname,
                    patient_last_name = lname,
                    patient_email = patient_email,
                    patient_visible = False,
                    policy_name = policy_name,
                    policy_discount = policy_discount,
                    approved = False,
                    requested = True,
                    date = date
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(insurance_staff_create_statement)
        elif request.method == 'GET':
            return render(request, 'insurance_staff_create_statement.html')
    else:
        ensure_groups(request, grp)

#----------------------Doctor Staff Views start here --------------------------------

def doctor_update_patient_records(request):
    if request.user.is_anonymous:
        return redirect(login)
    if request.method == 'POST':
        patient_email_id = request.POST['p_email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        dob = request.POST['dob']
        bg = request.POST['bg']

        Patient.objects.filter(email_id=patient_email_id).update(first_name=fname,last_name=lname,gender=gender,phone_number=phone,address=address, birth_date=dob,blood_group = bg)
    
    return render(request,'docPtRecords.html')
        
def create_prescription(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp == 'Doctor':
        if request.method == 'POST':
            pfname = request.POST['fname']
            plname = request.POST['lname']
            pId = request.POST['pid']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            dfname = request.POST['dfname']
            dlname = request.POST['dlname']
            dPh = request.POST['dph']
            daddr = request.POST['daddr']
            med = request.POST['med']
            dos = request.POST['dos']
            comm = request.POST['comm']
            dId = request.POST['email']

            try:
                prescription = Prescription.objects.filter(patient_email_id=pId)
                if len(prescription) > 0:
                    print('Prescription for this patient already exists.')
                    return render(request,'updatePtPrescription.html',{'err':'Prescription for this patient already exists.'})
                Prescription.objects.create(patient_first_name=pfname,
                                            patient_last_name=plname,
                                            birthdate = dob,
                                            age = age,
                                            gender = gender,
                                            doctor_first_name = dfname,
                                            doctor_last_name = dlname,
                                            doctor_email_id = dId,
                                            patient_email_id = pId,
                                            doctor_phone_number = dPh,
                                            doctor_address = daddr,
                                            medicine = med,
                                            dosage = dos,
                                            comments = comm)
                patient = Prescription.objects.all()
                patients = { 'patients' : patient}
                return render(request, 'viewPtPrescription.html', patients)
            

            except Exception as e:
                print(e)
        elif request.method == 'GET':
            return render(request,'docPtPrescription.html')
                
    else:
        ensure_groups(request, grp)

def update_prescription(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp == 'Doctor':
        if request.method == 'POST':
            pId = request.POST['pid']
            dId = request.POST['email']
            pfname = request.POST['fname']
            plname = request.POST['lname']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            dfname = request.POST['dfname']
            dlname = request.POST['dlname']
            dPh = request.POST['dph']
            daddr = request.POST['daddr']
            med = request.POST['med']
            dos = request.POST['dos']
            comm = request.POST['comm']
            
            try:
                Prescription.objects.filter(id=id).update(patient_first_name=pfname,
                                            patient_last_name=plname,
                                            birthdate=dob,
                                            age=age,
                                            gender=gender,
                                            doctor_first_name=dfname,
                                            doctor_last_name=dlname,
                                            doctor_email_id=dId,
                                            patient_email_id=pId,
                                            doctor_phone_number=dPh,
                                            doctor_address=daddr,
                                            medicine=med,
                                            dosage=dos,
                                            comments=comm)
                patient = Prescription.objects.all()
                patients = { 'patients' : patient}
                return render(request, 'viewPtPrescription.html', patients)
            except Exception as e:
                print(e)
        return render(request,'updatePtPrescription.html',{'err':'Weird Error'})
    else:
        ensure_groups(request, grp)
            
    

def doc_patient_prescription(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor' or grp =='admin':
        patients = Prescription.objects.all()
        data = { 'patients' : patients}
        return render(request, 'viewPtPrescription.html', data)
    else:
        ensure_groups(request, grp)
    

def doc_reg(request):
    if request.user.is_anonymous:
        return redirect(login)
    return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        retypepassword = request.POST['re-password']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        dob = request.POST['dob']
        bg = request.POST['bg']
        dept = request.POST['dept']
        rank = request.POST['rank']

        #print(fname,lname,gender,phone,address,dob,bg)
        try :
            if password == retypepassword:
                Doctor.objects.create(first_name=fname,last_name=lname,email_id=email,gender=gender,phone_number=phone,address=address, birth_date=dob,blood_group = bg,department=dept,rank=rank)
                print('Done')
                user = User.objects.create_user(name, email, password)
                patient_group, created = Group.objects.get_or_create(name='Doctor')
                #print(patient_group)
                user.groups.add(patient_group)
                user.save()
                return redirect(login)
        except Exception as e :
            print(e) #Add the error view redirection here
    return render(request, 'doc_register.html')

def createDiagnosis(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp =='Doctor':
        if request.method == 'POST':
            p_email = request.POST['pid']
            pfname = request.POST['fname']
            plname = request.POST['lname']
            dfname = request.POST['dfname']
            dlname = request.POST['dlname']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            dph = request.POST['dph']
            rec_test = request.POST['test']
            comm = request.POST['comm']
            if grp == 'admin':
                d_email = request.POST['email']
            elif grp == 'Doctor':
                d_email = request.user.email
            try:
                if len(Diagnosis.objects.filter(patient_email_id=p_email)) > 0:
                    return render(request,'createDiagnosis.html',{'err':'Diagnosis already exists, please select Update Diagnosis to update it'})
                Diagnosis.objects.create(
                    patient_first_name=pfname,
                    patient_last_name=plname,
                    birthdate=dob,
                    age=age,
                    gender=gender,
                    doctor_first_name=dfname,
                    doctor_last_name=dlname,
                    doctor_email_id=d_email,
                    patient_email_id=p_email,
                    doctor_phone_number=dph,
                    recommended_tests=rec_test,
                    diagnosis_comments=comm)
                diagnosis = Diagnosis.objects.all()
                data = { 'diagnosis' : diagnosis}
                return render(request, 'viewDiagnosis.html', data)
            except Exception as e:
                print(e)
        elif request.method == 'GET':
            return render(request,'createDiagnosis.html')
    else:
        ensure_groups(request, grp)


def updateDiagnosis(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp =='Doctor':
        if request.method == 'POST':
            p_email = request.POST['pid']
            pfname = request.POST['fname']
            plname = request.POST['lname']
            dfname = request.POST['dfname']
            dlname = request.POST['dlname']
            dob = request.POST['dob']
            age = request.POST['age']
            gender = request.POST['gender']
            dph = request.POST['dph']
            rec_test = request.POST['test']
            comm = request.POST['comm']
            if grp == 'admin':
                d_email = request.POST['email']
            elif grp == 'Doctor':
                d_email = request.user.email
            try:
                Diagnosis.objects.filter(id=id).update(
                    patient_first_name=pfname,
                    patient_last_name=plname,
                    birthdate=dob,
                    age=age,
                    gender=gender,
                    doctor_first_name=dfname,
                    doctor_last_name=dlname,
                    doctor_email_id=d_email,
                    patient_email_id=p_email,
                    doctor_phone_number=dph,
                    recommended_tests=rec_test,
                    diagnosis_comments=comm)
                diagnosis = Diagnosis.objects.all()
                data = { 'diagnosis' : diagnosis}
                return render(request, 'viewDiagnosis.html', data)
            except Exception as e:
                print(e)
        return render(request,'updateDiagnosis.html')
    else:
        ensure_groups(request, grp)

def deleteDiagnosis(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp =='Doctor':
        try:
            Diagnosis.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        diagnosis = Diagnosis.objects.all()
        data = { 'diagnosis' : diagnosis}
        return render(request, 'viewDiagnosis.html', data)
    else:
        ensure_groups(request, grp)

def viewDiagnosis(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor':
        diagnosis = Diagnosis.objects.all()
        d = {'diagnosis' : diagnosis}
        return render(request, 'viewDiagnosis.html',d)
    elif grp == "admin":
        diagnosis = Diagnosis.objects.all()
        d = {'diagnosis' : diagnosis}
        return render(request, 'viewDiagnosis.html',d)
    else:
        ensure_groups(request, grp)

def doctor_view_testreport(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor':
        reports = Report.objects.all()
        d = {'reports' : reports}
        return render(request, 'viewLabReports.html',d)
    else:
        ensure_groups(request, grp)



# ----------------------- admin views ---------------------------------
def admin_transactions(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
       transactions = Transaction.objects.all()
       d = {'transactions':transactions}
       return render(request, 'admin_transactions.html',d)
    elif grp =='insurance_staff':
        transactions = Transaction.objects.filter(status="Approved")
        d = {'transactions':transactions}
        return render(request, 'admin_transactions.html',d)
    elif grp =='hospital_staff':
        transactions = Transaction.objects.filter(Q(status="Approved") | Q(status="Dispersed")).filter(completed=False)
        d = {'transactions':transactions}
        return render(request, 'admin_transactions.html',d)
    elif grp =='Patient':
        transactions = Transaction.objects.filter(patient_email=request.user.email).filter(status="Dispersed").filter(completed=True)
        d = {'transactions':transactions}
        return render(request, 'admin_transactions.html',d)
    else:
        ensure_groups(request, grp)

def admin_approve_deny_transaction(request, id, action):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin' or grp =='insurance_staff' or grp == 'hospital_staff':
        if action == 'approve':
            Transaction.objects.filter(id=id).update(status="Approved")
        elif action == 'deny':
            Transaction.objects.filter(id=id).update(status="Denied")
        elif action == 'delete':
            Transaction.objects.filter(id=id).delete()
        elif action == 'disperse':
            Transaction.objects.filter(id=id).update(status="Dispersed")
        elif action == 'complete':
            Transaction.objects.filter(id=id).update(completed=True)
        return redirect(admin_transactions)
    else:
        ensure_groups(request, grp)

def admin_update_insurance_policies(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            pol_name = request.POST['pol_name']
            name = request.POST['name']
            discount = request.POST['discount']
            try:
                Insurance_Policy.objects.filter(policy_name=pol_name).update(policy_name=name,
                                    discount=discount)
            except Exception as e:
                print('Exception occured', e)
            return redirect(insurance_staff_view_policies)
        elif request.method == 'GET':
            return render(request, 'admin_update_insurance_policies.html')
    else:
        ensure_groups(request, grp)

def admin_delete_insurance_policy(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        try:
            Insurance_Policy.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        return redirect(insurance_staff_view_policies)
    else:
        ensure_groups(request, grp)

def admin_create_transaction(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            pid = request.POST['pid']
            amount = request.POST['amount']
            case = request.POST['case']
            try:
                Transaction.objects.create(
                    patient_first_name=fname,
                    patient_last_name = lname,
                    patient_email = pid,
                    case_number = case,
                    amount = amount,
                    status = 'Created'
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(admin_transactions)
        elif request.method == 'GET':
            return render(request, 'admin_create_transaction.html')
    else:
        ensure_groups(request, grp)

def update_transaction(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            pid = request.POST['pid']
            amount = request.POST['amount']
            case = request.POST['case']
            status = request.POST['status']
            completed = request.POST['complete']
            id = id
            try:
                Transaction.objects.filter(id=id).update(
                    patient_first_name=fname,
                    patient_last_name = lname,
                    patient_email = pid,
                    case_number = case,
                    amount = amount,
                    status = status,
                    completed = completed
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(admin_transactions)

        d = {'id' : id}
        return render(request, 'admin_update_transaction.html', d)
    else:
        ensure_groups(request, grp)

def admin_delete_insurance_statement(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        try:
            Insurance_Statement.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        return redirect(insurance_staff_view_statements)
    else:
        ensure_groups(request, grp)


def admin_update_insurance_statement(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            patient_email = request.POST['email']
            policy_name = request.POST['policy']
            policy_discount = request.POST['discount']
            date = request.POST['date']
            id = id
            try:
                Insurance_Statement.objects.filter(id=id).update(
                    patient_first_name=fname,
                    patient_last_name = lname,
                    patient_email = patient_email,
                    patient_visible = False,
                    policy_name = policy_name,
                    policy_discount = policy_discount,
                    approved = False,
                    requested = True,
                    date = date
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(insurance_staff_view_statements)

        d = {'id' : id}
        return render(request, 'admin_update_insurance_statement.html', d)
    else:
        ensure_groups(request, grp)

def admin_delete_prescription(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        try:
            Prescription.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        prescriptions = Prescription.objects.all()
        patients = {'patients': prescriptions}
        return render(request, 'viewPtPrescription.html', patients)
    else:
        ensure_groups(request, grp)


def admin_create_test(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            cost = request.POST['cost']
            comments = request.POST['comments']
            try:
                Test.objects.create(
                    test_name=name,
                    cost = cost,
                    comments = comments,
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(admin_create_test)
        elif request.method == 'GET':
            return render(request, 'admin_create_test.html')
    else:
        ensure_groups(request, grp)

def admin_update_test(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            cost = request.POST['cost']
            comments = request.POST['comments']
            curr_name = request.POST['curr_name']
            try:
                Test.objects.filter(test_name=curr_name).update(
                    test_name=name,
                    cost = cost,
                    comments = comments,
                                  )
            except Exception as e:
                print('Exception occured', e)
            return redirect(admin_update_test)
        elif request.method == 'GET':
            return render(request, 'admin_update_test.html')
    else:
        ensure_groups(request, grp)

def admin_delete_test(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            try:
                tests = Test.objects.filter(test_name=name)
                if len(tests) == 0:
                    return redirect(admin_delete_test)
                Test.objects.filter(test_name=name).delete()
                return redirect(admin_delete_test)
            except Exception as e:
                print(e)
            return redirect(admin_delete_test)
        elif request.method == 'GET':
            return render(request, 'admin_delete_test.html')
    else:
        ensure_groups(request, grp)

def admin_delete_appointment(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        try:
            Appointment.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        appointments = Appointment.objects.all()
        d = {'appointments': appointments}
        return render(request, 'hospitalstaff_view_appointments.html',d)
    else:
        ensure_groups(request, grp)

def admin_update_appointment(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        
        if request.method == 'POST':
            patient_email = request.POST['email']
            doctor_name = request.POST['doctor']
            app_date = request.POST['doa']
            app_time = request.POST['toa']
            reason = request.POST['reason']
            status = request.POST['status']
            id = id
            try:
                Appointment.objects.filter(id=id).update(
                    patient_email = patient_email,
                    doctor_name = doctor_name,
                    app_date = app_date,
                    app_time = app_time,
                    reason = reason,
                    status = status
                                  )
            except Exception as e:
                print('Exception occured', e)
            appointments = Appointment.objects.all()
            d = {'appointments': appointments}
            return render(request, 'hospitalstaff_view_appointments.html', d)

        d = {'id' : id}
        return render(request, 'admin_update_appointment.html', d)
    else:
        ensure_groups(request, grp)


def admin_delete_test_request(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        try:
            Test_Request.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
        requests = Test_Request.objects.all()
        d = {'appointments': requests}
        return redirect(test_request)
    else:
        ensure_groups(request, grp)


def admin_update_test_request(request, id):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            last_name = request.POST['lname']
            first_name = request.POST['fname']
            email = request.POST['pid']
            dob = request.POST['dob']
            gender = request.POST['gender']
            date = request.POST['doa']
            time = request.POST['toa']
            test = request.POST['test']
            status = request.POST['status']
            id = id
            try:
                Test_Request.objects.filter(id=id).update(
                    patient_first_name= first_name,
                    patient_last_name= last_name,
                    test_date = date, 
                    test_time = time,
                    birthdate= dob,
                    patient_email_id= email,
                    gender= gender,
                    test_name= test,
                    test_status=status
                                  )
            except Exception as e:
                print('Exception occured', e)
            
            return redirect(test_request)

        d = {'id' : id}
        return render(request, 'admin_update_test_request.html', d)
    else:
        ensure_groups(request, grp)

def admin_view_employees(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        employees = Employee.objects.all()
        d = {'employees':employees}
        return render(request, 'admin_view_employees.html',d)

def admin_add_employee(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            lname = request.POST['lname']
            uname = request.POST['uname']
            psw = request.POST['psw']
            rpsw = request.POST['rpsw']
            email = request.POST['email']
            phone = request.POST['phone']
            group = request.POST['group']
            if psw == rpsw:
                Employee.objects.create(employee_first_name=name, employee_last_name=lname, employee_email=email, employee_phone=phone, employee_group=group)
                user = User.objects.create_user(uname, email, psw)
                user_group = Group.objects.get(name=group)
                user_group.user_set.add(user)
                logger.info("Admin added {} successfully".format(user.username))
                user.save()
                return redirect(admin_view_employees)
            else:
                print('Passwords Do not match')
        elif request.method == 'GET':
            return render(request,'admin_add_employee.html')

def admin_update_employee(request, id, action):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        if action == 'delete':
            employee = Employee.objects.filter(id=id)
            User.objects.filter(email = employee[0].employee_email).delete()
            employee.delete()
            return redirect(admin_view_employees)
        elif action == 'update':
            if request.method == 'POST':
                name = request.POST['name']
                lname = request.POST['lname']
                phone = request.POST['phone']
                Employee.objects.filter(id=id).update(employee_first_name=name,employee_last_name=lname,employee_phone=phone)
                return redirect(admin_view_employees)
            elif request.method == 'GET':
                employee = Employee.objects.filter(id=id)
                d={'employee':employee}
                return render(request, 'admin_update_employee.html',d)

def admin_view_logs(request):
    if request.user.is_anonymous:
        return redirect(login)
    grp = request.user.groups.all()[0].name
    if grp == 'admin':
        f = open(os.path.join(os.path.dirname( __file__ ), '..', 'SHSLogging.log'))
        d = {'logs':f.readlines()}
        return render(request, 'admin_view_logs.html', d)






#---------------------- supporting functions -----------------------
def ensure_groups(request, grp):
    if grp == 'admin':
        return render(request, 'admin_home.html')
    elif grp == 'Patient':
        return render(request, 'patient_home.html')
    elif grp == 'lab_staff':
        return render(request, 'labstaff_home.html')
    elif grp == 'hospital_staff':
        return render(request, 'hospitalstaff_home.html')
    elif grp == 'insurance_staff':
        return render(request, 'insurance_staff_home.html')
    elif grp == 'Doctor':
        return render(request, 'doc_home.html')
    else:
        return render(request, login)
