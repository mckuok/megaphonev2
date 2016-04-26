from django import forms

from .models import Domain

import re


class DomainRegistrationForm(forms.ModelForm):
    error_messages = {
        'invalid_id': "Please use alphabets and numbers only.",
    }

    class Meta:
        model = Domain
        fields = ["name", "domainID", "description"]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control input-lg', 'placeholder': "Your Domain's Name"}),
            'domainID': forms.TextInput(attrs={'class': 'form-control input-lg',
                                               'placeholder': 'An Unique Identifier for Your Domain'}),
            'description': forms.Textarea(attrs={'class': 'form-control input-lg',
                                                 'placeholder': 'A Brief Description of Your Domain'})
        }

    def clean_domainID(self):
        domainId = self.cleaned_data.get("domainID")
        if re.match('^[a-zA-Z0-9]+$', domainId) is not None:
            return domainId
        else:
            raise forms.ValidationError(
                self.error_messages['invalid_id'],
                code='invalid_id',
            )
