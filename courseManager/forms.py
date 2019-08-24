from django import forms
from django.utils import timezone
from main_page.models import Sala
import datetime

class CourseInsertForm(forms.Form):
    data = forms.DateField(initial=timezone.now())
    capienza = forms.IntegerField(initial=0)
    ora_inizio = forms.TimeField(initial=timezone.now())
    ora_fine = forms.TimeField(initial=timezone.now()+datetime.timedelta(hours=1))
    posti_prenotati = forms.IntegerField(initial=0)
    sala = forms.ModelChoiceField(queryset=Sala.objects.all())
