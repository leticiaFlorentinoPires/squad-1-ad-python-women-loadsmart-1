from rest_framework import serializers
from .models import User, Event, Log


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_login', 'email', 'password']


class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'codigo', 'descricao', 'env', 'arquivado', 'date']

class LogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'descricao', 'level', 'detalhes', 'origem', 'date', 'user', 'event']