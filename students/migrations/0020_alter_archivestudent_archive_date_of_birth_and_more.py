# Generated by Django 4.1.3 on 2023-06-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_alter_archivestudent_archive_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivestudent',
            name='archive_date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
