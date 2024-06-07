from django import forms
from .models import Contract


class ContractNotesForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ["notes"]
