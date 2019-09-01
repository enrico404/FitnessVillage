from django import forms
from django.utils import timezone
import datetime

class ContactForm(forms.Form):
    """
    form relativo all'assistenza clienti
    """
    date = forms.DateTimeField(initial=datetime.datetime.today(), disabled=True)
    messaggio = forms.CharField(widget=forms.Textarea)
