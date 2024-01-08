# Generated by Django 4.2.7 on 2024-01-06 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway_staff', '0020_remove_train_first_ac_fare_remove_train_general_fare_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='first_ac_fare',
            field=models.DecimalField(decimal_places=2, default=300, max_digits=8),
        ),
        migrations.AddField(
            model_name='train',
            name='general_fare',
            field=models.DecimalField(decimal_places=2, default=80, max_digits=8),
        ),
        migrations.AddField(
            model_name='train',
            name='second_ac_fare',
            field=models.DecimalField(decimal_places=2, default=250, max_digits=8),
        ),
        migrations.AddField(
            model_name='train',
            name='sleeper_fare',
            field=models.DecimalField(decimal_places=2, default=120, max_digits=8),
        ),
        migrations.AddField(
            model_name='train',
            name='third_ac_fare',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=8),
        ),
    ]