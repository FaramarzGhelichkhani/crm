# Generated by Django 4.2.1 on 2023-06-03 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmdadUser', '0005_alter_customuser_phone'),
        ('Emdad', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motor',
            name='technecians',
            field=models.ManyToManyField(blank=True, null=True, to='EmdadUser.technecian'),
        ),
        migrations.AlterField(
            model_name='region',
            name='technecians',
            field=models.ManyToManyField(blank=True, null=True, to='EmdadUser.technecian'),
        ),
        migrations.AlterField(
            model_name='service',
            name='technecians',
            field=models.ManyToManyField(blank=True, null=True, to='EmdadUser.technecian'),
        ),
    ]
