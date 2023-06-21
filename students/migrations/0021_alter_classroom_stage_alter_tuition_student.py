# Generated by Django 4.1.3 on 2023-06-18 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0020_alter_tuition_receipt_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='stage',
            field=models.CharField(choices=[('', 'اختار المرحلة التعليمية'), ('BC', 'مرحلة تمهيدي'), ('KG1', 'رياض أطفال 1'), ('KG2', 'رياض أطفال 2'), ('Prim1', 'الصف الأول الابتدائي- Grade 1'), ('Prim2', 'الصف الثاني الابتدائي- Grade 2'), ('Prim3', 'الصف الثالث الابتدائي- Grade 3'), ('Prim4', 'الصف الرابع الابتدائي- Grade 4'), ('Prim5', 'الصف الخامس الابتدائي- Grade 5'), ('Prim6', 'الصف السادس الابتدائي- Grade 6'), ('Prep7', 'الصف الأول الإعدادي- Grade 7'), ('Prep8', 'الصف الثاني الإعدادي- Grade 8'), ('Prep9', 'الصف الثالث الإعدادي- Grade 9'), ('Sec1', 'الصف الأول الثانويSecondary School 1'), ('Sec2', 'الصف الثاني الثانويSecondary School 2'), ('Sec3', 'الصف الثالث الثانويSecondary School 3')], default='default_value', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tuitions', to='students.student'),
        ),
    ]