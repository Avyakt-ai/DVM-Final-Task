# Generated by Django 4.2.7 on 2024-01-07 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('railway_staff', '0023_rename_email_passengerinformation_passenger_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='fare',
        ),
    ]
