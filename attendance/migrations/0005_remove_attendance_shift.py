# Generated by Django 5.0.6 on 2024-06-11 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_remove_attendance_employeeintimeshift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='shift',
        ),
    ]
