# Generated by Django 4.2.8 on 2024-01-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0011_contract_client_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='vat_rate',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='VAT'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='vat_rate',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='VAT'),
        ),
    ]
