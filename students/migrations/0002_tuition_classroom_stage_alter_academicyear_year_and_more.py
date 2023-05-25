# Generated by Django 4.1.3 on 2023-05-21 09:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tuition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('paid', models.BooleanField(default=False)),
                ('receipt_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='stage',
            field=models.CharField(choices=[('', 'اختار المرحلة التعليمية'), ('BC', 'مرحلة تمهيدي'), ('KG1', 'رياض أطفال 1'), ('KG2', 'رياض أطفال 2'), ('Prim1', 'الصف الأول الابتدائي- Grade 1'), ('Prim2', 'الصف الثاني الابتدائي- Grade 2'), ('Prim3', 'الصف الثالث الابتدائي- Grade 3'), ('Prim4', 'الصف الرابع الابتدائي- Grade 4'), ('Prim5', 'الصف الخامس الابتدائي- Grade 5'), ('Prim6', 'الصف السادس الابتدائي- Grade 6'), ('Prep7', 'الصف الأول الإعدادي- Grade 7'), ('Prep8', 'الصف الثاني الإعدادي- Grade 8'), ('Prep9', 'الصف الثالث الإعدادي- Grade 9'), ('Sec1', 'الصف الأول الثانويSecondary School 1'), ('Sec2', 'الصف الثاني الثانويSecondary School 2'), ('Sec3', 'الصف الثالث الثانويSecondary School 3')], default='default_value', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='year',
            field=models.CharField(choices=[('1', '2021-2022'), ('2', '2022-2023'), ('3', '2023-2024')], default='default_value', max_length=50, null=True, verbose_name='Academic Year'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Class room'),
        ),
        migrations.AlterField(
            model_name='educationalstage',
            name='name',
            field=models.CharField(choices=[('1', 'Primary Stage'), ('2', 'Prep Stage'), ('3', 'Secondary Stage')], default='default_value', max_length=50, null=True, verbose_name='Educational Stage'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_Expense', to='students.student'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.DeleteModel(
            name='Installment',
        ),
        migrations.AddField(
            model_name='tuition',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='students.student'),
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ManyToManyField(to='students.classroom'),
        ),
    ]