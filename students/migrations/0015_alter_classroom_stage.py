# Generated by Django 4.1.3 on 2023-05-28 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_classroom_fee_per_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='stage',
            field=models.CharField(choices=[('', 'Choose Classroom'), ('BC', 'Baby Class'), ('KG1', 'Kindergarten 1'), ('KG2', 'Kindergarten 2'), ('Prim1', 'Grade 1'), ('Prim2', 'Grade 2'), ('Prim3', 'Grade 3'), ('Prim4', 'Grade 4'), ('Prim5', 'Grade 5'), ('Prim6', 'Grade 6'), ('Prep7', 'Grade 7'), ('Prep8', 'Grade 8'), ('Prep9', 'Grade 9'), ('Sec1', 'Secondary School 1'), ('Sec2', 'Secondary School 2'), ('Sec3', 'Secondary School 3')], default='default_value', max_length=50, null=True),
        ),
    ]