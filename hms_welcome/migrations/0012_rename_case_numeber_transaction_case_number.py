# Generated by Django 4.0.3 on 2022-03-30 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hms_welcome', '0011_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='case_numeber',
            new_name='case_number',
        ),
    ]