import email
from django.db import models

# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.first_name


class Prescription(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    doctor_first_name = models.CharField(max_length=50)
    doctor_last_name = models.CharField(max_length=50)
    doctor_email_id = models.EmailField(unique=False)
    patient_email_id = models.EmailField(unique=True)
    doctor_phone_number = models.CharField(max_length=15)
    doctor_address = models.CharField(max_length=200)
    medicine = models.CharField(max_length=500)
    dosage = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)

    def __str__(self):
        return self.patient_first_name


class Appointment(models.Model):
    patient_email = models.EmailField()
    doctor_name = models.CharField(max_length=50)
    app_date = models.DateField()
    app_time = models.TimeField()
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.patient_first_name


class Diagnosis(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    doctor_first_name = models.CharField(max_length=50)
    doctor_last_name = models.CharField(max_length=50)
    doctor_email_id = models.EmailField(unique=False)
    patient_email_id = models.EmailField(unique=True)
    doctor_phone_number = models.CharField(max_length=10)
    diagnosis_comments = models.CharField(max_length=200)
    recommended_tests = models.CharField(max_length=200, default="None")

    def __str__(self):
        return self.patient_first_name


class Report(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    test_date = models.DateField()
    test_time = models.TimeField()
    birthdate = models.DateField()
    patient_email_id = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    test_name = models.CharField(max_length=200)
    test_result = models.CharField(max_length=1000)
    comments = models.CharField(max_length=500)
    reference_doctor = models.CharField(max_length=30)

    def __str__(self):
        return self.patient_first_name


class Test(models.Model):
    test_name = models.CharField(max_length=200, unique=True)
    comments = models.CharField(max_length=500)
    cost = models.IntegerField()

    def __str__(self):
        return self.test_name


class Test_Request(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    test_date = models.DateField()
    test_time = models.TimeField()
    birthdate = models.DateField()
    patient_email_id = models.EmailField()
    gender = models.CharField(max_length=10)
    test_name = models.CharField(max_length=200)
    test_status = models.CharField(max_length=1000)

    def __str__(self):
        return self.patient_first_name


class Insurance_Policy(models.Model):
    policy_name = models.CharField(max_length=200)
    discount = models.DecimalField(decimal_places=2, max_digits=4)


class Insurance_Statement(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    patient_email = models.EmailField(unique=False)
    patient_visible = models.BooleanField()
    policy_name = models.CharField(max_length=200)
    policy_discount = models.DecimalField(decimal_places=2, max_digits=4)
    approved = models.BooleanField(default=False)
    requested = models.BooleanField(default=False)
    date = models.DateField()


class Transaction(models.Model):
    patient_first_name = models.CharField(max_length=50)
    patient_last_name = models.CharField(max_length=50)
    patient_email = models.EmailField(unique=False)
    case_number = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)


class Malicious_Login(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(default='riya.2398@gmail.com')
    failed_login_attempts = models.IntegerField()


class Employee(models.Model):
    employee_first_name = models.CharField(max_length=50)
    employee_last_name = models.CharField(max_length=50)
    employee_email = models.EmailField(unique=False)
    employee_phone = models.CharField(max_length=10)
    employee_group = models.CharField(max_length=20)
