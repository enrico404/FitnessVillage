from django import forms
from django.utils import timezone
import datetime

class ContactForm(forms.Form):
    date = forms.DateTimeField(initial=datetime.datetime.today(), disabled=True)
    messaggio = forms.CharField(widget=forms.Textarea)


class registrationForm(forms.Form):
    email = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    ripeti_password = forms.CharField(max_length=200)