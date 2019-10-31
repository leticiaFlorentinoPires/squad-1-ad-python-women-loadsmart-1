from rest_framework import serializers
from events.models import Event, Agent


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["name", "status", "env", "version", "address"]


class EventModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["title", "level", "data", "archived", "date", "agent"]

    # def validate(self, data):
    #     print("to no validate")
    #     if 'agent' not in data:
    #         print("to no if")
    #         data['agent_id'] = Event.objects.get(subject=data['agent__id']).agent_id
    #     return data