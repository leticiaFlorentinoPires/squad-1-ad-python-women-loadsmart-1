from django.db import models
from datetime import date
from django.contrib.auth.models import User

     
class Agent(models.Model):
    name = models.CharField('name', max_length=20)
    status = models.BooleanField(default=False)
    env = models.CharField('env', max_length=20)
    version = models.CharField('env', max_length=5)
    address = models.CharField('name', max_length=39)
    date = models.DateTimeField(auto_now=True)

class Event(models.Model):
    title = models.CharField('title', max_length=100)
    level = models.CharField('level', max_length=20)
    data = models.TextField('data')
    arquivado = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    agent = models.ForeignKey(Agent, on_delete = models.PROTECT, null = True, related_name='agent')
