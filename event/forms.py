from django import forms

from .models import Event


class CreateEventForm(forms.ModelForm):
    error_messages = {
        'invalid_id': "Please use alphabets and numbers only.",
    }

    class Meta:
        model = Event
        fields = ["name", "date_event", "location", "function", "description"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event name"}),
            'date_event': forms.DateTimeField(attrs={'class': 'form-control',
                                               'placeholder': 'Date of event'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'location'}),
            'function': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of function'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }
