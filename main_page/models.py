from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

class Sala(models.Model):
    cap_max = models.IntegerField()

class Corso(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateTimeField()
    operatore  = models.ForeignKey(User, on_delete=models.CASCADE)
    cap = models.IntegerField()
    sala_id = models.ForeignKey(Sala, on_delete=models.CASCADE)



class Prenota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corso_id = models.ForeignKey(Corso, on_delete=models.CASCADE)

