# Generated by Django 4.2.10 on 2024-02-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0014_contract_vat_declaration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='future_unit_rate_1',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 1'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='future_unit_rate_2',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 2'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='future_unit_rate_3',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 3'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='unit_rate_1',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 1'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='unit_rate_2',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 2'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='unit_rate_3',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 3'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='future_unit_rate_1',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 1'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='future_unit_rate_2',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 2'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='future_unit_rate_3',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Future Unit Rate 3'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='unit_rate_1',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 1'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='unit_rate_2',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 2'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='unit_rate_3',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Unit Rate 3'),
        ),
    ]
