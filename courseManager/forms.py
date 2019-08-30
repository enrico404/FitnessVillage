from django import forms
from django.utils import timezone
from main_page.models import Sala
import datetime

class CourseInsertForm(forms.Form):
    date = forms.DateField(initial=timezone.now())
    capienza = forms.IntegerField(initial=0, min_value=0)
    ora_inizio = forms.TimeField(initial=datetime.datetime.today())
    ora_fine = forms.TimeField(initial=(datetime.datetime.today()+datetime.timedelta(hours=1)))
    posti_prenotati = forms.IntegerField(initial=0, min_value=0)
    sala = forms.ModelChoiceField(queryset=Sala.objects.all())
