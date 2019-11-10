import datetime

import os
import django
import pytest
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from events.models import Event, Agent, AgentManager
from events.views import EventFilter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "central_erros.settings")
django.setup()

pytestmark = pytest.mark.django_db


class FakeGetRequest:
    method = 'GET'

class FakePostRequest:
    method = 'POST'


# Create your tests here.
class TestViews(TestCase):
    def setUp(self) -> None:
        admin = Group.objects.create(name="admin")

        ada = User.objects.create(
            username="__USER1__", email="mail@mail.com", password="__PASSWORD__"
        )
        joan = User.objects.create(
            username="__USER2__", email="mail@mail.com", password="__PASSWORD__"
        )

        admin.user_set.add(ada)
        admin.user_set.add(joan)

        agent_linux = Agent.objects.create(
            name="linux-server",
            status=True,
            env="production",
            version="1.1.1",
            address="10.0.34.15",
            user=ada,
        )
        agent_mac = Agent.objects.create(
            name="mac-server",
            status=True,
            env="production",
            version="1.1.2",
            address="10.0.34.123",
            user=joan,
        )

        Event.objects.create(
            title="title1",
            level=5,
            data="data1",
            archived=False,
            date=datetime.date.today(),
            agent=agent_linux,
        )
        Event.objects.create(
            title="title2",
            level=1,
            data="data2",
            archived=False,
            date=datetime.date.today(),
            agent=agent_mac,
        )

    def test_api_events(self):
        '''testing endpoint of events'''
        response = self.client.get('/events/api/events/')
        self.assertEqual(response.status_code, 200)

    def test_api_agents(self):
        '''testing endpoint of agents'''
        response = self.client.get('/events/api/agent/')
        self.assertEqual(response.status_code, 200)

    def test_api_users(self):
        '''testing endpoint of users'''
        response = self.client.get('/events/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_api_groups(self):
        '''testing endpoint of groups'''
        response = self.client.get('/events/api/groups/')
        self.assertEqual(response.status_code, 200)

    def test_context_of_view_event_list(self):
        '''testing context of event_list'''
        response = self.client.get(reverse('events:events-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['dropdown_list'], ["'dev'", "'producao'", "'homologacao'"])


    def test_context_of_view_detail(self):
        '''testing events detail view's context'''
        event = Event.objects.get(id=1)
        response = self.client.get(reverse('events:detail', kwargs={'event_id': 1}))
        self.assertEqual(response.context['event'].title, event.title)

    def test_context_of_view_order(self):
        '''testing events ordering'''
        event = Event.objects.get(id=2)
        response = self.client.get('/events/?envName=env&orderBy=level&buscarPor=buscaCampo&pesquisaText=&submit=search')
        self.assertEqual(response.context['query_set_result'][0].title, event.title)

    def test_context_of_view_busca_por(self):
        '''testing events search for'''
        event = Event.objects.get(id=1)
        response = self.client.get('/events/?envName=env&orderBy=ordenacao&buscarPor=descricao&pesquisaText=data1&submit=search')
        self.assertEqual(response.context['query_set_result'][0].data, event.data)

    def test_context_of_view_enviroment(self):
        '''testing events filter enviroment'''
        event = Event.objects.get(id=1)
        response = self.client.get('/events/?envName=production&orderBy=ordenacao&buscarPor=buscaCampo&pesquisaText=&submit=search')
        self.assertEqual(response.context['query_set_result'][0].title, event.title)

    def test_context_of_view_busca_por_level(self):
        '''testing events search for level'''
        event = Event.objects.get(id=1)
        response = self.client.get('/events/?envName=env&orderBy=ordenacao&buscarPor=level&pesquisaText=5&submit=search')
        self.assertEqual(response.context['query_set_result'][0].title, event.title)

    def test_context_of_view_busca_por_origem(self):
        '''testing events search for source IP'''
        event = Event.objects.get(id=1)
        response = self.client.get('/events/?envName=env&orderBy=ordenacao&buscarPor=origem&pesquisaText=10.0.34.15&submit=search')
        self.assertEqual(response.context['query_set_result'][0].title, event.title)

    def test_context_of_view_order_by_frequencia(self):
        '''testing events search for frequency'''
        event = Event.objects.get(id=1)
        response = self.client.get('http://127.0.0.1:8000/events/?envName=env&orderBy=frequencia&buscarPor=buscaCampo&pesquisaText=&submit=search')
        self.assertEqual(response.context['query_set_result'][0].title, event.title)



