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
    doctor_email_id = models.EmailField(unique=True)
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
    doctor_email_id = models.EmailField(unique=True)
    patient_email_id = models.EmailField(unique=True)
    doctor_phone_number = models.CharField(max_length=10)
    diagnosis_comments = models.CharField(max_length=200)

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
