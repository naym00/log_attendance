# Generated by Django 5.0.6 on 2024-06-11 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
