# Generated by Django 4.1.3 on 2023-06-22 08:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_delete_archivestudent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID', default=1)),
                ('name', models.CharField(max_length=50)),
                ('national_number', models.IntegerField(unique=True)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('', '---------'), ('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('total_payments', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('total_owed', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('academic_year', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='students.academicyear')),
                ('classroom', models.ManyToManyField(to='students.classroom')),
            ],
        ),
    ]
