import os
import django
from django.test import TestCase
from django.contrib.auth.models import User, Group

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "central_erros.settings")
django.setup()

from events.models import Event, Agent

from events.views import (
    list_events
)


# Create your tests here.
class TestViews(TestCase):
    def setUp(self) -> None:
        admin = Group.objects.create(name="admin")

        ada = User.objects.create(
            name="__USER__", email="mail@mail.com", password="__PASSWORD__"
        )
        joan = User.objects.create(
            name="__USER__", email="mail@mail.com", password="__PASSWORD__"
        )

        leticia.group.set([admin])

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

    def list_all_errors(self):
        events = list_events()
        assert isinstance(users[0], Event)
        self.assertEqual(admins.count(), 2)

