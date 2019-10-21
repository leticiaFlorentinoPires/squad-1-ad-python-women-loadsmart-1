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
    """Return all events."""
    events = Event.objects.all()
    enviroments = Agent.objects.values('env').distinct()
    envReturn = list()
    for env in enviroments:
        envReturn.append(env['env'])

    context = {
        'events': events,
        'env': envReturn,
        'events_empty': []
    }

    return render(request, 'events/list.html', context=context)

def post_detail(request, envName):
    query = Event.objects.get_queryset().filter(agent__env=envName)
    context = {
        'events': query
    }

    return render(request, 'events/list.html', context=context)




class AgentAPIViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer

class EventAPIViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

