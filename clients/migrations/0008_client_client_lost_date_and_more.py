# Generated by Django 4.2.13 on 2024-07-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0007_remove_client_client_term_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="client_lost_date",
            field=models.DateField(blank=True, null=True, verbose_name="Client Lost Date"),
        ),
        migrations.AddField(
            model_name="historicalclient",
            name="client_lost_date",
            field=models.DateField(blank=True, null=True, verbose_name="Client Lost Date"),
        ),
    ]
