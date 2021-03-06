# Generated by Django 4.0.3 on 2022-04-02 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms_welcome', '0014_malicious_login_diagnosis_recommended_tests_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_first_name', models.CharField(max_length=50)),
                ('employee_last_name', models.CharField(max_length=50)),
                ('employee_email', models.EmailField(max_length=254)),
                ('employee_phone', models.CharField(max_length=10)),
                ('employee_group', models.CharField(max_length=20)),
            ],
        ),
    ]
