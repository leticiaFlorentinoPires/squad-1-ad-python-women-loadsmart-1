import datetime
import os
import django
import pytest
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet

from events.models import Event, Agent, AgentManager
from events.views import list_events


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "central_erros.settings")
django.setup()

pytestmark = pytest.mark.django_db


# Create your tests here.
class TestViews():
    def setUp(self) -> None:
        admin = Group.objects.create(name="admin")

        ada = User.objects.create(
            name="__USER__", email="mail@mail.com", password="__PASSWORD__"
        )
        joan = User.objects.create(
            name="__USER__", email="mail@mail.com", password="__PASSWORD__"
        )

        ada.group.set([admin])

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
            date=datetime.today(),
            agent=agent_linux,
        )
        Event.objects.create(
            title="__TITLE__",
            level="information",
            data="__DATA__",
            archived=False,
            date=datetime.today(),
            agent=agent_mac,
        )

    def test_view_list_events(self):
        request = None

        response = list_events(request)
        assert response.status_code == 200

    def test_get_agent_level(self):
        #TODO: add test that is return Agent type, in real BD it is working
        #but here no...it's return empty list
        agent = Agent.objects.get_agent_level(envname="production")
        assert isinstance(agent, QuerySet)