from rest_framework import serializers
from .models import Event, Agent


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'descricao', 'level', 'detalhes', 'origem', 'date', 'user', 'event']

class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'codigo', 'descricao', 'env', 'arquivado', 'date']

