from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import validate_ipv4_address


class AgentManager(models.Manager):
    def get_agent_level(self, envName):
        queryset = self.get_queryset().filter(env=envName)
        return queryset


class Agent(models.Model):
    ENV_CHOICES =[
        ("producao","producao"),
        ("homologacao","homologacao"),
        ("dev","dev")
    ]

    objects = AgentManager()
    name = models.CharField("name", max_length=50)
    status = models.BooleanField(default=False)
    env = models.CharField("env", max_length=20,choices=ENV_CHOICES)
    version = models.CharField("version", max_length=5)
    address = models.GenericIPAddressField(
        validators=[validate_ipv4_address], null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="user"
    )

    def __str__(self):
        return f'{self.name}, {self.status}, {self.env},{self.version}, {self.address}'


class Event(models.Model):
    LEVEL_CHOICES = [
        (5,"critical"),
        ( 4,"debug"),
        (3,"error"),
        (2,"warning"),
        (1,"information"),
    ]

    @property
    def frequencia(self):
        freq=0
        for e in Event.objects.all():
            if self.level == e.level and self.agent_id == e.agent_id:
                freq += 1

        return freq

    title = models.CharField("title", max_length=100)
    level = models.IntegerField("level", choices=LEVEL_CHOICES)
    data = models.TextField("data")
    archived = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    agent = models.ForeignKey(
        Agent, on_delete=models.PROTECT, null=True, related_name="agent"
    )

    def __str__(self):
        return f'{self.title}, {self.level}, {self.data}, {self.archived}, {self.agent}'

