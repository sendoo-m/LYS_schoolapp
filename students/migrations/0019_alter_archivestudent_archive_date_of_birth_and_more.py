# Generated by Django 4.1.3 on 2023-06-22 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_alter_archivestudent_archive_academic_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivestudent',
            name='archive_date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
