# Generated by Django 4.2.8 on 2024-01-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0012_alter_contract_vat_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='vat_rate',
            field=models.CharField(choices=[('5%', '5%'), ('20%', '20%'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=30, verbose_name='VAT Rate'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='vat_rate',
            field=models.CharField(choices=[('5%', '5%'), ('20%', '20%'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=30, verbose_name='VAT Rate'),
        ),
    ]
