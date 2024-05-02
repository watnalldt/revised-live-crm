from django.contrib import admin
from .models import ElectricityCommission


class ElectricityCommissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(ElectricityCommission, ElectricityCommissionAdmin)
