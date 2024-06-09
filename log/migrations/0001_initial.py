# Generated by Django 5.0.6 on 2024-06-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(choices=[('Anik', 'Anik'), ('Akash', 'Akash'), ('Rahat', 'Rahat'), ('Jibon', 'Jibon'), ('Milon', 'Milon')], max_length=10)),
                ('intime', models.DateField()),
                ('mintime', models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='log',
            constraint=models.UniqueConstraint(fields=('employee', 'intime'), name='employeeintime'),
        ),
    ]
