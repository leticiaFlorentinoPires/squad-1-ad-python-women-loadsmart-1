from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)

class AgentAPIViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer

class EventAPIViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

