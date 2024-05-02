# Generated by Django 4.2.11 on 2024-04-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0028_alter_contract_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="contract_status",
            field=models.CharField(
                choices=[
                    ("LIVE", "Live"),
                    ("REMOVED", "Removed"),
                    ("LOCKED", "Locked"),
                    ("PRICING", "Pricing"),
                    ("OBJECTION", "Objection"),
                    ("NEW", "New"),
                    ("LOST", "Lost"),
                    ("EXPIRED", "Expired"),
                    ("FUTURE", "Future"),
                    ("CONTRACT_REQUESTED", "Contract Requested"),
                    ("AWAITING_DA", "Awaiting DA"),
                    ("DUPLICATE", "Duplicate"),
                ],
                default="LIVE",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="historicalcontract",
            name="contract_status",
            field=models.CharField(
                choices=[
                    ("LIVE", "Live"),
                    ("REMOVED", "Removed"),
                    ("LOCKED", "Locked"),
                    ("PRICING", "Pricing"),
                    ("OBJECTION", "Objection"),
                    ("NEW", "New"),
                    ("LOST", "Lost"),
                    ("EXPIRED", "Expired"),
                    ("FUTURE", "Future"),
                    ("CONTRACT_REQUESTED", "Contract Requested"),
                    ("AWAITING_DA", "Awaiting DA"),
                    ("DUPLICATE", "Duplicate"),
                ],
                default="LIVE",
                max_length=20,
            ),
        ),
    ]
