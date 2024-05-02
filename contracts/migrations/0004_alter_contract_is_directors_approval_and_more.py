# Generated by Django 4.2.5 on 2023-09-11 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_alter_contract_client_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='is_directors_approval',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Directors Approval'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='is_ooc',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Out Of Contract'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='is_directors_approval',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Directors Approval'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='is_ooc',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', verbose_name='Out Of Contract'),
        ),
    ]
