from django.contrib import admin
from .models import Corso, Sala, Prenota,Messaggio, ListaAttesa, Inserito


admin.site.register(Corso)
admin.site.register(Sala)
admin.site.register(Prenota)
admin.site.register(Messaggio)
admin.site.register(ListaAttesa)
admin.site.register(Inserito)