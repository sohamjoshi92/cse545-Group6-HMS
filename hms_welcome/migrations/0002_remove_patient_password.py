# Generated by Django 4.0.3 on 2022-03-11 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hms_welcome', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='password',
        ),
    ]
