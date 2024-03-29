# Generated by Django 4.2.6 on 2023-11-08 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0007_alter_contract_contract_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='future_standing_charge',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='Future Standing Charge'),
        ),
        migrations.AddField(
            model_name='historicalcontract',
            name='future_standing_charge',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True, verbose_name='Future Standing Charge'),
        ),
    ]
