import re
from this import d
from urllib import request
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
                print(user.groups.all()[0].name)
                if(user.groups.all()[0].name == 'Patient'):
                    return render(request, 'patient_home.html')
                elif user.groups.all()[0].name == 'Doctor':
                    return render(request,'doc_Home.html')
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
                patient_group, created = Group.objects.get_or_create(name='Patient')
                user.groups.add(patient_group)
                user.save()
                return redirect(login)
        except Exception as e :
            print(e) #Add the error view redirection here
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


def doctor_update_patient_records(request):
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
    if request.method == 'POST':
        pfname = request.POST['fname']
        plname = request.POST['lname']
        pId = request.POST['pid']
        dob = request.POST['dob']
        age = request.POST['age']
        gender = request.POST['gender']
        dfname = request.POST['dfname']
        dlname = request.POST['dlname']
        dId = request.user.email
        dPh = request.POST['dph']
        daddr = request.POST['daddr']
        med = request.POST['med']
        dos = request.POST['dos']
        comm = request.POST['comm']

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
            return render(request,'docPtPrescription.html',{'res':'Created Prescription for the patient ' + pfname + ' ' + plname})

        except Exception as e:
            print(e)
            
    return render(request,'docPtPrescription.html',{'err':'Weird Error'})

def update_prescription(request):
    if request.method == 'POST':
        pId = request.POST['pid']
        dId = request.user.email
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
            prescription = Prescription.objects.filter(patient_email_id=pId)
            if len(prescription) == 0:
                print('Prescription for this patient does not exist.')
                return render(request,'updatePtPrescription.html')
            Prescription.objects.filter(patient_email_id=pId).update(patient_first_name=pfname,
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
            return render(request,'updatePtPrescription.html')
        except Exception as e:
            print(e)
            
    return render(request,'updatePtPrescription.html',{'err':'Weird Error'})

def doc_patient_prescription(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor':
        patients = Prescription.objects.filter(doctor_email_id = request.user.email)
        data = { 'patients' : patients}
        return render(request, 'viewPtPrescription.html', data)

def doc_reg(request):
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
    if request.method == 'POST':
        p_email = request.POST['pid']
        d_email = request.user.email
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
        try:
            if len(Diagnosis.objects.filter(patient_email_id=p_email)) > 0:
                return render(request,'createDiagnosis.html',{'err':'Diagnosis already exists, please select Update Diagnosis to update it'})
            Diagnosis.objects.create(patient_first_name=pfname,
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
            return render(request,'createDiagnosis.html')

        except Exception as e:
            print(e)
    return render(request,'createDiagnosis.html')

def updateDiagnosis(request):
    if request.method == 'POST':
        p_email = request.POST['pid']
        d_email = request.user.email
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
        try:
            if len(Diagnosis.objects.filter(patient_email_id=p_email)) == 0:
                return render(request,'updateDiagnosis.html')
            Diagnosis.objects.filter(patient_email_id=p_email).update(patient_first_name=pfname,
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
            return render(request,'updateDiagnosis.html')
        except Exception as e:
            print(e)
    return render(request,'updateDiagnosis.html')


def deleteDiagnosis(request):
    if request.method == 'POST':
        pemail = request.POST['pid']
        try:
            diagnosis = Diagnosis.objects.filter(patient_email_id=pemail)
            if len(diagnosis) == 0:
                return render(request,'deleteDiagnosis.html')
            Diagnosis.objects.filter(patient_email_id=pemail).delete()
            return render(request,'deleteDiagnosis.html')
        except Exception as e:
            print(e)
    return render(request,'deleteDiagnosis.html')

def viewDiagnosis(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor':
        diagnosis = Diagnosis.objects.filter(doctor_email_id=request.user.email)
        d = {'diagnosis' : diagnosis}
        return render(request, 'viewDiagnosis.html',d)

def doctor_view_testreport(request):
    grp = request.user.groups.all()[0].name
    if grp == 'Doctor':
        reports = Report.objects.filter(reference_doctor_email=request.user.email)
        d = {'reports' : reports}
        return render(request, 'viewLabReports.html',d)
