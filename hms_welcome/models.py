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