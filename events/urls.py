from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from events import views
from events.views import (
    EventsListView,
    EventFilter,
    EventDetail,
    ShelveEvent,
    UnshelveEvent,
    DeleteEvent
    )

router = routers.DefaultRouter()
router.register(r'events', views.EventAPIViewSet)
router.register(r'agents', views.AgentAPIViewSet)
router.register(r'users', views.UserAPIViewSet)
router.register(r'groups', views.GroupAPIViewSet)


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    '''#resource to get acess to get, post ,put , delete of /agent/id/event'''
    pass

#router for get acess to "get", "post", "put", "delete" of endpoint /agent/id/event
router_agent_events = NestedDefaultRouter()
agents_router = router_agent_events.register(r'agent', views.AgentAPIViewSet)
agents_router.register('events', views.EventAPIViewSet, basename='events-agents',
                       parents_query_lookups = ['agent'])

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(agents_router.router.urls)),
    path('', EventFilter.as_view(), name='events-list'),
    # re_path(r'agents/(?P<id_agent>\d+)/events/(?P<id_event>\d+)', agent_id_event_id , name='events_by_agents'),
    # path('<str:envName>', EventFilter.as_view(), name='filter_events'),
    path('<int:event_id>', EventDetail.as_view(), name='detail'),
    re_path(r'(?P<pk>\d+)?/shelved', ShelveEvent.as_view(), name = 'shelved'),
    re_path(r'(?P<pk>\d+)?/unshelved', UnshelveEvent.as_view(), name = 'unshelved'),
    re_path(r'(?P<pk>\d+)?/delete', DeleteEvent.as_view(), name = 'delete')
]