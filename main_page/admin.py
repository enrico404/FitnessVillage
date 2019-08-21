from django.contrib import admin
from .models import Corso, Sala, Prenota,Messaggio


admin.site.register(Corso)
admin.site.register(Sala)
admin.site.register(Prenota)
admin.site.register(Messaggio)