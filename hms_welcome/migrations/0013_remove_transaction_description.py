# Generated by Django 4.0.3 on 2022-03-31 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hms_welcome', '0012_rename_case_numeber_transaction_case_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
    ]
