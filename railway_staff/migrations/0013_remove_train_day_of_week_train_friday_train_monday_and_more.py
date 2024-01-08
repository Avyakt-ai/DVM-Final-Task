# Generated by Django 4.2.7 on 2024-01-02 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway_staff', '0012_alter_train_departure_station_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='day_of_week',
        ),
        migrations.AddField(
            model_name='train',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='train',
            name='wednesday',
            field=models.BooleanField(default=False),
        ),
    ]
