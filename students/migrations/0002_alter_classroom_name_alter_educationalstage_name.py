# Generated by Django 4.1.3 on 2023-05-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Class room'),
        ),
        migrations.AlterField(
            model_name='educationalstage',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Educational Stage'),
        ),
    ]
