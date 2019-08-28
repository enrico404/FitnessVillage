from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime
from django.shortcuts import get_object_or_404

class Sala(models.Model):
    cap_max = models.IntegerField()
    num = models.IntegerField()
    cancellato = models.BooleanField(default=False)


class Corso(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateField()
    operatore = models.ForeignKey(User, on_delete=models.CASCADE)
    cap = models.IntegerField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    ora_inizio = models.TimeField(default=datetime.time(00, 00))
    ora_fine = models.TimeField(default=datetime.time(00, 00))
    posti_prenotati = models.IntegerField()
    cancellato = models.BooleanField(default=False)

    def scaduto(self):
        if self.data <= datetime.date.today():
            if self.ora_fine < datetime.datetime.now().time():
                return True
        return False

class Prenota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)
    cancellato = models.BooleanField(default=False)


class Messaggio(models.Model):
    userMittente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userMittente')
    userDestinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userDestinatario')
    data_ora = models.DateTimeField()
    text = models.CharField(max_length=500)
    letto = models.BooleanField(default=False)


class ListaAttesa(models.Model):
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)


class Inserito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listaAttesa = models.ForeignKey(ListaAttesa, on_delete=models.CASCADE)
    cancellato = models.BooleanField(default=False)

