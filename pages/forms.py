from django import forms

from .models import Page

from domains.models import Domain

import re


class PageRegistrationForm(forms.ModelForm):
    error_messages = {
        'invalid_pageID': "Please use alphabets and numbers only.",
        'invalid_domainID': "The Domain ID cannot be found.",
    }

    referenceID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                                'placeholder': "Your Parent Domain's ID"}))

    class Meta:
        model = Page
        fields = ["name", "pageID", "description"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': "Your Page's Name"}),
            'pageID': forms.TextInput(attrs={'class': 'form-control input-lg',
                                             'placeholder': 'An Unique Identifier for Your Page'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control input-lg', 'placeholder': 'A Brief Description of Your Page'})
        }

    def clean_pageID(self):
        pageId = self.cleaned_data.get("pageID")
        if re.match('^[a-zA-Z0-9]+$', pageId) is not None:
            return pageId
        else:
            raise forms.ValidationError(
                self.error_messages['invalid_pageID'],
                code='invalid_pageID',
            )

    def clean_referenceID(self):
        domainID = self.cleaned_data.get("referenceID")
        try:
            domain = Domain.objects.get(domainID=domainID)
        except Exception:
            raise forms.ValidationError(
                self.error_messages['invalid_domainID'],
                code='invalid_domainID',
            )
        return domain
