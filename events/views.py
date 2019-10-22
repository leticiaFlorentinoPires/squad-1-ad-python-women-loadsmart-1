from django.db.models import QuerySet, Count
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import viewsets

from events.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)

def list_events(request):
    """Return all events."""
    #gerar frequencia
    events = Event.objects.all()

    result_group_by = list(Event.objects.values('agent_id','level').annotate(acount=Count('agent_id')))

    print("resultado do group by \n")
    # print(result_group_by)

    event_count = list()
    # print(result_group_by)
    for group in result_group_by:
        # print(group)
        for event in events:
            # print(dados)
            if group['agent_id'] == event.agent.id and group['level']==event.level:
                event_count.append({'event': event,
                                    'agentId': group['agent_id'],
                                    'count': group['acount'] })


    # para passar para o "dropdown" de enviroments
    enviroments = Agent.objects.values('env').distinct()
    envReturn = list()
    for env in enviroments:
        envReturn.append(env['env'])
    # print(event_count)
    context = {
        'events': event_count,
        'env': envReturn,
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

