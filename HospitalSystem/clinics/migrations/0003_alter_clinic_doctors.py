# Generated by Django 5.0.7 on 2024-08-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0002_alter_clinic_doctors'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='doctors',
            field=models.ManyToManyField(to='doctors.doctor'),
        ),
    ]
