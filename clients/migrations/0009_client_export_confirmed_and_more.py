# Generated by Django 4.2.14 on 2024-07-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0008_client_client_lost_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="export_confirmed",
            field=models.BooleanField(default=False, verbose_name="Export Confirmed"),
        ),
        migrations.AddField(
            model_name="historicalclient",
            name="export_confirmed",
            field=models.BooleanField(default=False, verbose_name="Export Confirmed"),
        ),
    ]
