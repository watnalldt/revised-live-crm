from django import forms
from .models import Contract, Client


class ContractFilterForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    contract_status = forms.ChoiceField(choices=Contract.ContractStatus.choices, required=False)
