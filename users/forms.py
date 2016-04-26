from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': 'Enter Password'}))


class MemberRegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': "Your Password"}))
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': "Your Password Again"}))

    class Meta:
        model = User
        fields = ["name", "email"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': "Your Name"}),
            'email': forms.TextInput(attrs={'class': 'form-control input-lg',
                                            'placeholder': 'Your Email'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
