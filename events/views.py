from django.db.models import QuerySet, Count
from django.shortcuts import render, redirect
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from requests import Response
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from events.models import Event, Agent
from rest_framework_extensions.mixins import NestedViewSetMixin

from .serializers import (
    EventModelSerializer,
    AgentModelSerializer,
    GroupModelSerializer, UserModelSerializer)


class EventsListView(ListView):
    """
    List all events, related to :model: `events.Event`
    """
    paginate_by = 10
    model = Event


class EventFilter(ListView):
    """
    Apply filters to select particular event, 
    related to :model:`events.Event`
    """
    
    model = Event
    template_name = '../templates/events/event_list.html'
    env = None
    orderBy = None
    search_for = None
    pesquisa_text = None
    retorno_query = None
    ordering = ["level"]

    def calcula_frequencia(self):
        """
        Search events based on frequency, 
            related to :model:`events.Event`
        
        **Context**
        
        ``mymodel``
            An instance of :model:`events.Event`
            
        **Template:**
            :template:`events/events_list.html`
        
        """
        
        event_group_by = self.retorno_query.values('agent__id', 'level').annotate(freq=Count('agent_id'))
        dict_frequencia = dict()
        for grupo in event_group_by:
            for event in Event.objects.all():
                if grupo['agent__id'] == event.agent_id and grupo['level'] == event.level:
                      dict_frequencia[event.id] = (event,grupo['freq'],grupo['level'])
        return dict_frequencia

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Search events from particular environment, 
            related to :model:`events.Event`
            
        **Context**
        
        ``mymodel``
            An instance of :model:`events.Event`
            
        **Template:**
            :template:`events/events_list.html`
        """
        
        context = super(EventFilter, self).get_context_data(**kwargs)
        context['dropdown_list'] = ["dev","producao","homologacao"]
        context['query_set_result'] = self.get_queryset()
        return context

    def get_queryset(self):
        """
        Search a particular event :model:`events.Event`
        
        **Context**
        
        ``mymodel``
            An instance of :model:`events.Event`
            
        **Template:**
            :template:`events/events_list.html`
        """
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
        """
        Display events based on filters :model:`events.Event`.
        
        **Context**
        
        ``mymodel``
            An instance of :model:`events.Event`
            
        **Template:**
            :template:`events/events_list.html`
        """  
        
        if request.method == "GET":
            self.env = request.GET.get('envName')
            self.orderBy = request.GET.get('orderBy')
            self.search_for = request.GET.get('buscarPor')
            self.pesquisa_text = request.GET.get('pesquisaText')

        return super(EventFilter, self).get(request, *args, **kwargs)

class ShelveEvent(DetailView):
    """
    Change event from shelver = False to shelved = True,
        related to :model:`events.Event`
    """

    def get(self, request, pk):
        """
        Display updated events, related to :model:`events.Event`
        
        **Context**
        ``mymodel``
            An instance of :model:`events.Event`
        
        **Template:**
            :template:`events/events_list.html`
        """
        
        event = Event.objects.get(pk=pk)
        event.archived = True
        event.save()
        return redirect('events:events-list')

class UnshelveEvent(DetailView):
    """
    Change event from shelver = True to shelved = False,
        related to :model:`events.Event`
    """

    def get(self, request, pk):
        """
        Display updated events, related to :model:`events.Event`
        
        **Context**
        ``mymodel``
            An instance of :model:`events.Event`
        
        **Template:**
            :template:`events/events_list.html`
        """
        
        event = Event.objects.get(pk=pk)
        event.archived = False
        event.save()
        return redirect('events:events-list')

class DeleteEvent(DetailView):
    """
    Delete a particular event, related to :model:`events.Event`
    """

    def get(self, request, pk):
        """
        Display updated events, related to :model:`events.Event`
        
        **Context**
        ``mymodel``
            An instance of :model:`events.Event`
        
        **Template:**
            :template:`events/events_list.html`
        """
        event = Event.objects.get(pk=pk)
        event.delete()
        return redirect('events:events-list')

class EventDetail(DetailView):
    """
    Display a particual Event entry, related to :model:`events.Event`
    """

    def get(self, request, event_id):
        """
        Display an individual event :model:`events.Event`
        
        **Context**
        ``mymodel``
            An instance of :model:`events.Event`
            
        **Template:**
            :template:`events/detail.html`
        """
        
        event = Event.objects.get(pk=event_id)
        context = {
            'event': event,
            }
        return render(request, 'events/detail.html', context=context)


class AgentAPIViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Agents.
    """
    
    queryset = Agent.objects.all()
    serializer_class = AgentModelSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Users.
    """
    
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class GroupAPIViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Groups.
    """
    
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer


class EventAPIViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Events.
    """
    
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer



