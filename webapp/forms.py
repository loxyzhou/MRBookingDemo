from django import forms
from django.forms import widgets
from django.forms import ValidationError
from webapp import models
import re


def mobile_validate(value):
    mobile_re = re.compile(r'\d{8}/g')
    if not mobile_re.match(value):
        raise ValidationError('Please enter valid contact no')


class RegForm(forms.Form):
    username = forms.CharField(
        label='UserName',
        max_length=16,
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        error_messages={
            'required': 'UserName is required',
        }
    )
    password = forms.CharField(
        label='Password',
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required':'Password is required',
            'invalid': 'Password is invalida',
            'min_length': 'The minimum length of password must be greater than 3 characters'
        }
    )
    r_password = forms.CharField(
        label='Confirm Password',
        min_length=3,
        widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required':'Password is required',
            'invalid': 'Password is invalida',
            'min_length': 'The minimum length of password must be greater than 3 characters'
        }
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        rel_password = self.cleaned_data.get("r_password")
        if rel_password and password != rel_password:
            self.add_error("r_password", ValidationError('The confirmed password is not matched'))
        else:
            return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        rep = models.UserInfo.objects.filter(username=username)
        if rep:
            self.add_error("username", ValidationError('The user already exists'))
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        rep = models.UserInfo.objects.filter(email=email)
        if rep:
            self.add_error("email", ValidationError('Email address already exists'))
        else:
            return email
