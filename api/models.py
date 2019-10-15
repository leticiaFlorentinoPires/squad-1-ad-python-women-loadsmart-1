from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import validate_ipv4_address

     
class Agent(models.Model):
    name = models.CharField('name', max_length=50)
    status = models.BooleanField(default=False)
    env = models.CharField('env', max_length=20)
    version = models.CharField('version', max_length=5)
    address = models.GenericIPAddressField(validators=[validate_ipv4_address], null=True)
    user = models.ForeignKey(User, on_delete = models.PROTECT, null = True, related_name='user')

class Event(models.Model):
    
    LEVEL_CHOICES = [
        ('critical', 'critical'),
        ('debug', 'debug'),
        ('error', 'error'),
        ('warning', 'warning'),
        ('information', 'information')
        ]

    title = models.CharField('title', max_length=100)
    level = models.CharField('level', max_length=20, choices=LEVEL_CHOICES)
    data = models.TextField('data')
    archived = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    agent = models.ForeignKey(Agent, on_delete = models.PROTECT, null = True, related_name='agent')
