# Generated by Django 4.2.1 on 2023-05-19 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_alter_followup_total_price_cusotmer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='followups', to='Order.order'),
        ),
    ]
