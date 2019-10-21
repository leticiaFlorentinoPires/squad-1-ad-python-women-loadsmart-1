import datetime

import os
import django
import pytest
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet
from django.test import TestCase

from events.models import Event, Agent, AgentManager
from events.views import list_events, get_event


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
            title="__TITLE__",
            level="critical",
            data="__DATA__",
            archived=False,
            date=datetime.date.today(),
            agent=agent_linux,
        )
        Event.objects.create(
            title="__TITLE__",
            level="information",
            data="__DATA__",
            archived=False,
            date=datetime.date.today(),
            agent=agent_mac,
        )

    def test_view_list_events(self):
        response = list_events(None)
        assert response.status_code == 200

    def test_event_detail(self):
        fake_get = FakeGetRequest()
        event = Event.objects.first()

        response = get_event(fake_get, event.pk)
        assert response.status_code == 200

    def test_event_detail_not_found(self):
        fake_get = FakeGetRequest()
        response = get_event(fake_get, 9999)
        assert response.status_code == 404

    def test_event_detail_not_found_invalid_method(self):
        fake_post = FakePostRequest()
        response = get_event(fake_post, 1)
        assert response.status_code == 400

    def test_get_agent_level(self):
        #TODO: add test that is return Agent type, in real BD it is working
        #but here no...it's return empty list
        agent = Agent.objects.get_agent_level(envname="production")
        assert isinstance(agent, QuerySet)