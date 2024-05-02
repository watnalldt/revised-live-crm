from django.db import models
from clients.models import Client


class JobTitle(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        help_text="Please enter a valid phone number", max_length=16, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.email}"
