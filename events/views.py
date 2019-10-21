from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from events.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)

def list_events(request):
    """Return all events."""
    events = Event.objects.all()

    context = {
        'events': events,
        'events_empty': []
    }

    return render(request, 'events/list.html', context=context)

def get_event(request, event_id):
    """Return event by a given id."""
    if request.method == 'GET':
        try:
            event = Event.objects.get(pk=event_id)
            context = {
                'event': event,
            }
            return render(request, 'events/detail.html', context=context)
        except Event.DoesNotExist:
            return HttpResponseNotFound("event not found")
    return HttpResponseBadRequest("invalid action")
    

