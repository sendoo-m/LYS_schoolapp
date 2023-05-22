from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_tuition_classroom_stage_alter_academicyear_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='academic_year',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='name',
        ),
        migrations.AddField(
            model_name='student',
            name='academic_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='students.academicyear'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classroom',
            name='stage',
            field=models.CharField(choices=[('', 'Choose Educational Stage'), ('BC', 'Preparatory Stage'), ('KG1', 'Kindergarten 1'), ('KG2', 'Kindergarten 2'), ('Prim1', 'Grade 1'), ('Prim2', 'Grade 2'), ('Prim3', 'Grade 3'), ('Prim4', 'Grade 4'), ('Prim5', 'Grade 5'), ('Prim6', 'Grade 6'), ('Prep7', 'Grade 7'), ('Prep8', 'Grade 8'), ('Prep9', 'Grade 9'), ('Sec1', 'Secondary School 1'), ('Sec2', 'Secondary School 2'), ('Sec3', 'Secondary School 3')], default='default_value', max_length=50, null=True),
        ),
    ]
