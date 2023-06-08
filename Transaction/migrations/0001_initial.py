# Generated by Django 4.2.1 on 2023-05-16 11:14

import Transaction.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EmdadUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, null=True, verbose_name='زمان')),
                ('amount', models.PositiveIntegerField(verbose_name='مبلغ')),
                ('doc', models.FileField(blank=True, null=True, upload_to=Transaction.models.Transaction_handle_upload)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='EmdadUser.technecian')),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': 'تراکنش',
            },
        ),
    ]