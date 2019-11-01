from rest_framework import serializers
from events.models import Event, Agent
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["name", "status", "env", "version", "address"]


class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "level", "data", "archived", "date", "agent"]


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all'


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all'