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
    env = None
    orderBy = None
    search_for = None
    pesquisa_text = None
    retorno_query = None
    ordering = ["level"]

    def calcula_frequencia(self):
        event_group_by = self.retorno_query.values('agent__id', 'level').annotate(freq=Count('agent_id'))
        dict_frequencia = dict()
        for grupo in event_group_by:
            for event in Event.objects.all():
                if grupo['agent__id'] == event.agent_id and grupo['level'] == event.level:
                      dict_frequencia[event.id] = (event,grupo['freq'],grupo['level'])
        return dict_frequencia

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventFilter, self).get_context_data(**kwargs)
        context['dropdown_list'] = ["dev","producao","homologacao"]
        print(Event.objects.values('agent__env').distinct())
        return context

    def get_queryset(self):
        print("resultado do get_queryset")
        self.retorno_query = Event.objects.all()
        if self.env is not None and self.env!="env":
           self.retorno_query= self.retorno_query.filter(agent__env=self.env)
        if self.search_for is not None and self.search_for!="buscaCampo":
            if self.pesquisa_text is not None and not self.pesquisa_text == "":
                if self.search_for == "level":
                    self.retorno_query = self.retorno_query.filter(level__icontains=self.pesquisa_text)
                elif self.search_for == "descricao":
                    self.retorno_query = self.retorno_query.filter(data__icontains=self.pesquisa_text)
                elif self.search_for == "origem":
                    print("origem")
                    print(self.pesquisa_text)
                    self.retorno_query = self.retorno_query.filter(agent__address__icontains=self.pesquisa_text)

        if self.orderBy is not None and self.orderBy!="ordenacao":
            if self.orderBy == "level":
                self.retorno_query = sorted(self.retorno_query, key=lambda m: m.level)
            else:
                self.retorno_query = sorted(self.retorno_query, key=lambda m: m.frequencia)
        return self.retorno_query

    def get(self, request, *args, **kwargs):
        print("estou no get")
        if request.method == "GET":
            print("estou no get")
            self.env = request.GET.get('envName')
            self.orderBy = request.GET.get('orderBy')
            self.search_for = request.GET.get('buscarPor')
            self.pesquisa_text = request.GET.get('pesquisaText')
            print("todos os parametros sao")
            print(self.env)
            print(self.orderBy)
            print(self.search_for)
            print(self.pesquisa_text)

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