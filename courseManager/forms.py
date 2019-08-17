from django import forms
from django.utils import timezone
from main_page.models import Sala

class CourseInsertForm(forms.Form):
    nome = forms.CharField(max_length=100)
    data = forms.DateTimeField(initial=timezone.now)
    capienza = forms.IntegerField(initial=0)
    durata = forms.FloatField(initial=1)
    posti_prenotati = forms.IntegerField(initial=0)
    sala = forms.ModelChoiceField(queryset=Sala.objects.all())
