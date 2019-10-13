from django.db import models
from datetime import date


class User(models.Model):
    name = models.CharField('Nome', max_length=50)   
    last_login = models.DateField(default=date.today)
    email = models.CharField('email', max_length=254)   
    password = models.CharField('password', max_length=50)       


class Event(models.Model):
    codigo = models.IntegerField()
    descricao = models.TextField('descricao')
    env = models.CharField('env', max_length=20)
    arquivado = models.BooleanField(default=False)
    date = models.DateField(default=date.today)

class Log(models.Model):
    descricao = models.TextField('descricao')
    level = models.CharField('level', max_length=20)
    detalhes = models.TextField('descricao')
    origem = models.CharField('origem', max_length=254)
    date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete = models.PROTECT, null = True, related_name='user')
    event = models.ForeignKey(Event, on_delete = models.PROTECT, null = True, related_name='event')
