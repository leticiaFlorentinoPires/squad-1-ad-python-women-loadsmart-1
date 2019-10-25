from django.db.models import QuerySet, Count
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import viewsets

from events.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)


class EventsListView(ListView):
    
    paginate_by = 100
    model = Event


class EventFilter(DetailView):
    
    def get(self, request, envName):
        
        event =  Event.objects.get_queryset().filter(agent__env=envName)
        context = {
            'object_list': event,
            }
        return render(request, 'events/event_list.html', context=context)

class EventDetail(DetailView):

    def get(self, request, event_id):

        event = Event.objects.get(pk=event_id)
        context = {
            'event': event,
            }
        return render(request, 'events/detail.html', context=context)


class AgentAPIViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer


class EventAPIViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer