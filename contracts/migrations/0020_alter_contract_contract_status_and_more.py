# Generated by Django 4.2.11 on 2024-03-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0019_contract_meter_onboarded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_status',
            field=models.CharField(choices=[('LIVE', 'Live'), ('REMOVED', 'Removed'), ('LOCKED', 'Locked'), ('PRICING', 'Pricing'), ('OBJECTION', 'Objection'), ('NEW', 'New'), ('LOST', 'Lost'), ('EXPIRED', 'Expired'), ('FUTURE', 'Future'), ('CONTRACT_REQUESTED', 'Contract Requested')], default='LIVE', max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='contract_status',
            field=models.CharField(choices=[('LIVE', 'Live'), ('REMOVED', 'Removed'), ('LOCKED', 'Locked'), ('PRICING', 'Pricing'), ('OBJECTION', 'Objection'), ('NEW', 'New'), ('LOST', 'Lost'), ('EXPIRED', 'Expired'), ('FUTURE', 'Future'), ('CONTRACT_REQUESTED', 'Contract Requested')], default='LIVE', max_length=20),
        ),
    ]
