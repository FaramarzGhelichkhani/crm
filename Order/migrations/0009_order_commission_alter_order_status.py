# Generated by Django 4.2.1 on 2023-06-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0008_alter_followup_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commission',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='کمیسیون'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('در حال انجام', 'در حال انجام'), ('انجام شد', 'انجام شد'), ('در آستانه کنسلی', 'در آستانه کنسلی'), ('کنسلی قطعی', 'کنسلی قطعی')], default='در حال انجام', max_length=15, verbose_name='وضعیت سفارش'),
        ),
    ]