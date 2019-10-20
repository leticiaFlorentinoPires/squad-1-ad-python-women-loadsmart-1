from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)

def list_events(request):
    events = Event.objects.all()

    context = {
        'events': events,
        'events_empty': []
    }

    return render(request, 'events/list.html', context=context)

class AgentAPIViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer

class EventAPIViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

