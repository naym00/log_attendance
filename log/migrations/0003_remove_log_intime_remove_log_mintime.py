# Generated by Django 5.0.6 on 2024-06-10 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_remove_log_employeeintime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='intime',
        ),
        migrations.RemoveField(
            model_name='log',
            name='mintime',
        ),
    ]
