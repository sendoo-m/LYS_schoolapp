# Generated by Django 4.1.3 on 2023-06-14 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_alter_tuition_receipt_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tuition',
            old_name='amount',
            new_name='amount_tuition',
        ),
    ]
