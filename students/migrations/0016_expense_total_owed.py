# Generated by Django 4.1.3 on 2023-06-04 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_alter_classroom_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='total_owed',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]