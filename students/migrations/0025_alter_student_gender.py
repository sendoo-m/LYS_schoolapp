# Generated by Django 4.1.3 on 2023-06-19 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0024_archivestudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('', ' اختار النوع'), ('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
