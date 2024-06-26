# Generated by Django 4.2.11 on 2024-03-25 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0026_alter_contract_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contract",
            options={
                "ordering": ["contract_end_date"],
                "permissions": [
                    ("can_export_commissions", "Can export commissions"),
                    ("can_access_bulk_upload_template", "Can access bulk upload template"),
                ],
                "verbose_name": "Client Contract",
                "verbose_name_plural": "Client Contracts",
            },
        ),
    ]
