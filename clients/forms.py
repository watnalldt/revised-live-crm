import datetime

from django import forms


class MeterForm(forms.Form):
    from_email = forms.EmailField(required=True)
    client_name = forms.CharField(required=True)
    site_address = forms.CharField(required=True, label="Site Name:")
    mpan_mpr = forms.CharField(required=True, label="MPAN or MPR:")
    meter_serial_number = forms.CharField(required=True, label="Meter Serial Number")
    utility_type = forms.CharField(required=True, label="Utility Type")
    supplier = forms.CharField(required=True, label="Supplier")
    meter_reading = forms.CharField(required=True, label="Meter Reading")
    meter_reading_date = forms.CharField(
        widget=forms.widgets.DateTimeInput(format="%d/%m/%Y"),
        initial=datetime.date.today,
    )
    attachment = forms.FileField(
        required=False, label="Optionally upload a photo of your meter reading"
    )


class MultipleMeterForm(forms.Form):
    from_email = forms.EmailField(required=True)
    client_name = forms.CharField(required=True)
    site_address = forms.CharField(required=True, label="Site Name:")
    mpan_mpr = forms.CharField(required=True, label="MPAN or MPR:")
    meter_serial_number = forms.CharField(required=True, label="Meter Serial Number")
    utility_type = forms.CharField(required=True, label="Utility Type")
    supplier = forms.CharField(required=True, label="Supplier")
    day_normal_meter_reading = forms.CharField(required=True, label="Day/Normal Meter Reading")
    night_low_meter_reading = forms.CharField(required=False, label="Night/Low Meter Reading")
    weekend_other_meter_reading = forms.CharField(
        required=False, label="Weekend/Other Meter Reading"
    )
    meter_reading_date = forms.CharField(
        widget=forms.widgets.DateTimeInput(format="%d/%m/%Y"),
        initial=datetime.date.today,
    )
    attachment = forms.FileField(
        required=False, label="Optionally upload a photo of your meter reading"
    )
