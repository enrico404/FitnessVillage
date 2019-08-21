from django import forms
from django.utils import timezone

class ContactForm(forms.Form):
    data = forms.DateTimeField(initial=timezone.now(), disabled=True)
    messaggio = forms.CharField(widget=forms.Textarea)

