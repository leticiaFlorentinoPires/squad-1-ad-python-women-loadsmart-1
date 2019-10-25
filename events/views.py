from django.db.models import QuerySet, Count
from django.shortcuts import render
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from events.models import Event, Agent
from .serializers import (
    EventModelSerializer,
    AgentModelSerializer
)


class EventsListView(ListView):
    
    paginate_by = 10
    model = Event


class EventFilter(ListView):
    model = Event
    template_name = '../templates/events/event_list.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        print("oioioioi")
        context = super(EventFilter, self).get_context_data(**kwargs)
        teste= Event.objects.values('agent__env').distinct()
        # lista_env=list()
        # for env in teste:
        #     lista_env.append(env['agent__env'])
        context['dropdown_list'] =  teste
        print(Event.objects.values('agent__env').distinct())
        return context

    def get(self, request, *args, **kwargs):
        # print(Event.objects.values('agent__env').distinct())
        return super(EventFilter, self).get(request, *args, **kwargs)

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